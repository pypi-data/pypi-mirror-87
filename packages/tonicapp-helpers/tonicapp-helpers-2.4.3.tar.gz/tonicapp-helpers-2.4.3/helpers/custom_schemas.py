import itertools

from rest_framework.schemas.openapi import AutoSchema
from rest_framework import serializers
from rest_framework.schemas.utils import is_list_view


class BaseSchema(AutoSchema):
    def __init__(self, **kwargs):
        self.customize_parameters = kwargs.pop("customize_parameters", None)

        self.request_serializer = kwargs.pop("request_serializer", None)

        self.required_authorization = kwargs.pop(
            "required_authorization", True
        )
        self.required_locale = kwargs.pop("required_locale", True)
        self.required_software_type = kwargs.pop(
            "required_software_type", True
        )
        self.filter_fields = kwargs.pop("filter_fields", [])
        self.sort_fields = kwargs.pop("sort_fields", [])
        self.responses = kwargs.pop("responses", None)

        # FIXME This two exceptions are specific for views with two routes. This should be deprecated!
        self.request_serializer_exception = kwargs.pop("request_serializer_exception", None)
        self.responses_exception = kwargs.pop("responses_exception", None)

        super().__init__(**kwargs)

    def get_filter_parameters(self, path, method):
        if not self.allows_filters(path, method):
            return []
        parameters = []
        for filter_backend in self.view.filter_backends:
            parameters += filter_backend().get_schema_operation_parameters(self.view)

        # # Custom filters
        if self.filter_fields:
            serializer, item_schema = self._custom_get_serializer(path, method)

            for field in serializer.fields.values():
                if field.field_name in self.filter_fields:
                    parameter = {}
                    schema = self.map_field(field)
                    name = f'{ field.field_name }[operator]'

                    available_operators = 'Available operators: gt, gte, lt, \
                        lte. Without operator the comparation is equal to.'

                    if schema['type'] == 'string':
                        available_operators = 'Available operators: contains, \
                            icontains, exact, iexact, in, startswith, \
                            istartswith, endswith, iendswith. Without \
                            operator the comparation is equal to.'
                    description = f'Filter by { field.field_name }. \
                        The available operators are: { available_operators }'

                    if schema['type'] == 'boolean':
                        name = f'{ field.field_name }'
                        description = f'Filter by { field.field_name }'

                    parameter['schema'] = schema
                    parameter['name'] = name
                    parameter['in'] = 'query'
                    parameter['required'] = False
                    parameter['description'] = description
                    parameters += [parameter]

        if self.sort_fields:
            description = f'Sort the queries, the available fields to \
                    sort are: { ", ".join(self.sort_fields) }. Example: \
                    sort_by=asc[{ self.sort_fields[0] }]'

            if len(self.sort_fields) > 1:
                description += f'or sort_by=asc[{ self.sort_fields[0] }],\
                        desc[{ self.sort_fields[1] }]'

            parameters += [{
                'name': 'sort_by',
                'in': 'query',
                'required': False,
                'description': description,
                'schema': {'type': 'string'}
            }]
        return parameters

    def get_components(self, path, method):
        """
        Return components with their properties from the serializer.
        """

        if method.lower() == 'delete':
            return {}

        if self.request_serializer:
            serializer = self.request_serializer()
            content = self.map_serializer(serializer)

        elif self.request_serializer_exception:
            for version in self.request_serializer_exception.keys():
                if version in path:
                    serializer = self.request_serializer_exception[version]()
                    break
            content = self.map_serializer(serializer)
        else:
            # Default from drf code
            serializer = self.get_serializer(path, method)
            if not isinstance(serializer, serializers.Serializer):
                return {}

            content = self.map_serializer(serializer)

        component_name = self.get_component_name(serializer)
        return {component_name: content}

    def get_operation(self, path, method):
        operation = {}
        operation['operationId'] = self.get_operation_id(path, method)
        operation['description'] = self.get_description(path, method)

        # FIXME Should be deprecated after route problem being solved
        if 'v0' in path:
            operation['operationId'] = f'{operation["operationId"]}_v0'

        parameters = []
        parameters += self.get_path_parameters(path, method)
        parameters += self.get_pagination_parameters(path, method)
        parameters += self.get_filter_parameters(path, method)

        if self.customize_parameters:
            parameters = self._update_parameters(parameters)

        parameters = self._default_parameters(parameters)

        operation['parameters'] = parameters

        request_body = self.get_request_body(path, method)
        if request_body:
            operation['requestBody'] = request_body
        operation['responses'] = self.get_responses(path, method)
        operation['tags'] = self.get_tags(path, method)
        return operation

    def get_responses(self, path, method):
        if method == 'DELETE':
            return {
                '204': {
                    'description': 'No response body'
                }
            }

        # FIXME responses exception it will be deprecated
        if self.responses_exception:
            responses = {}
            status_code = '201' if method == 'POST' else '200'
            for version in self.responses_exception.keys():
                if version in path:
                    serializer = self.request_serializer_exception[version]()
                    responses[status_code] = {
                        'content': {
                            'application/json' : {
                                'schema': {
                                    '$ref': '#/components/schemas/{}'.format(self.get_component_name(serializer))
                                }
                            }
                        },
                        'description': ""
                    }

            if self.responses:
                responses.update(self._custom_response(self.responses))
            return responses

        elif self.responses:
            responses = self._custom_response(self.responses)
            return responses

        self.response_media_types = self.map_renderers(path, method)

        serializer = self.get_serializer(path, method)

        if not isinstance(serializer, serializers.Serializer):
            item_schema = {}
        else:
            item_schema = self._get_reference(serializer)

        if is_list_view(path, method, self.view):
            response_schema = {
                'type': 'array',
                'items': item_schema,
            }
            paginator = self.get_paginator()
            if paginator:
                response_schema = paginator.get_paginated_response_schema(
                    response_schema
                )
        else:
            response_schema = item_schema

        status_code = '201' if method == 'POST' else '200'

        return {
            status_code: {
                'content': {
                    ct: {'schema': response_schema}
                    for ct in self.response_media_types
                },
                # description is a mandatory property,
                # https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#responseObject
                # TODO: put something meaningful into it
                'description': ""
            }
        }

    def get_request_body(self, path, method):
        if method not in ('PUT', 'PATCH', 'POST'):
            return {}

        self.request_media_types = self.map_parsers(path, method)

        serializer, item_schema = self._custom_get_serializer(path, method)

        return {
            'content': {
                ct: {'schema': item_schema}
                for ct in self.request_media_types
            }
        }

    def _custom_get_serializer(self, path, method):
        if self.request_serializer:
            serializer = self.request_serializer()
            item_schema = self._get_reference(serializer)
            return serializer, item_schema

        elif self.request_serializer_exception:
            for version in self.request_serializer_exception.keys():
                if version in path:
                    serializer = self.request_serializer_exception[version]()
                    item_schema = self._get_reference(serializer)
                    return serializer, item_schema

        serializer = self.get_serializer(path, method)

        if not isinstance(serializer, serializers.Serializer):
            item_schema = {}
        else:
            item_schema = self._get_reference(serializer)
        return serializer, item_schema

    def _update_parameters(self, parameters):
        for cust_parameter, parameter in itertools.product(self.customize_parameters, parameters):
            if cust_parameter['name'] == parameter['name']:
                parameter['description'] = cust_parameter['description']

        return parameters

    def _default_parameters(self, parameters):
        if self.required_authorization:
            parameters += [{
                'name': 'Authorization',
                'in': 'header',
                'required': True,
                'description': 'The structure to authenticate is: "JWT " + idToken or "TWT " + adminToken)',
                'schema': {'type': 'string'}
            }]

        if self.required_locale:
            parameters += [{
                'name': 'Accept-Language',
                'in': 'header',
                'required': True,
                'description': 'Example: Accept-Language=pt-PT',
                'schema': {'type': 'string'}
            }]

        if self.required_software_type:
            parameters += [{
                'name': 'Software-Type',
                'in': 'header',
                'required': True,
                'description': 'Options are: Web or Application or Backoffice. Example: Software-Type=Web.',
                'schema': {'type': 'string'}
            }]
        return parameters

    def _custom_response(self, responses):
        custom_response = {}
        for status, res in responses.items():
            if 'serializer' not in res.keys():
                custom_response[status] = res
                continue

            serializer = res['serializer']()
            description = res['description'] if 'description' not in res.keys() else ''
            custom_response[status] = {
                'content': {
                    'application/json': {
                        'schema': {
                            '$ref': '#/components/schemas/{}'.format(self.get_component_name(serializer))
                        }
                    }
                },
                'description': description
            }

        return custom_response
