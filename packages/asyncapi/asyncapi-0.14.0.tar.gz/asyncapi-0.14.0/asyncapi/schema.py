from typing import (
    Any,
    Dict,
    Iterable,
    Sequence,
    Type,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)


def type_as_jsonschema(python_type: Type[Any]) -> Dict[str, Any]:
    if python_type is Any:
        return {}

    schema_type = SCALARS.get(python_type)

    if schema_type is None:
        origin = get_origin(python_type)

        if origin is list or origin is Sequence or origin is Iterable:
            schema = {
                'type': 'array',
                'items': type_as_jsonschema(python_type.__args__[0]),
            }

            if hasattr(python_type.__args__[0], '__additional_items__'):
                schema['additionalItems'] = python_type.__additional_items__

            return schema

        return build_object_schema(python_type)

    return {'type': schema_type}


def build_object_schema(python_type: Type[Any]) -> Dict[str, Any]:
    type_hints = get_type_hints(python_type)
    origin = get_origin(python_type)
    schema: Dict[str, Any] = {
        'type': 'object',
        'properties': {},
    }
    required = []

    for attr_name, attr_type in type_hints.items():
        origin = get_origin(attr_type)
        args = get_args(attr_type)

        if origin is Union and len(args) == 2 and type(None) in args:
            attr_schema = type_as_jsonschema(args[0])

        elif origin is Union:
            if not type(None) in args:
                required.append(attr_name)

            attr_schema = {'anyOf': [type_as_jsonschema(arg) for arg in args]}

        else:
            required.append(attr_name)
            attr_schema = type_as_jsonschema(attr_type)

        schema['properties'][attr_name] = attr_schema

    if required:
        schema['required'] = required

    if hasattr(python_type, '__additional_properties__'):
        schema['additionalProperties'] = python_type.__additional_properties__

    return schema


SCALARS = {
    int: 'integer',
    str: 'string',
    float: 'number',
    bool: 'boolean',
}
