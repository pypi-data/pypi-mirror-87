import dataclasses
from types import MethodType
from typing import (  # type: ignore
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    _TypedDictMeta,
)

from dictdaora import DictDaora

from .decorator import jsondaora
from .exceptions import DeserializationError


class StringField(DictDaora):
    max_length: int
    min_length: int
    value: str
    validate: Callable[[Type['StringField'], str], None]

    def __init__(self, value: Any):
        self.value = value.decode() if isinstance(value, bytes) else str(value)
        type(self).validate(self.value)  # type: ignore

    def __init_subclass__(
        cls, min_length: Optional[int] = None, max_length: Optional[int] = None
    ) -> None:
        if max_length is None and min_length is not None:
            cls.validate = MethodType(validate_min_length, cls)

        elif max_length is not None and min_length is None:
            cls.validate = MethodType(validate_max_length, cls)

        elif max_length is not None and min_length is not None:
            cls.validate = MethodType(validate_min_length_max_length, cls)

        elif min_length is None and max_length is None:
            cls.validate = MethodType(lambda c, v: v, cls)

        if min_length is not None:
            cls.min_length = min_length

        if max_length is not None:
            cls.max_length = max_length


class IntegerField(DictDaora):
    maximum: int
    minimum: int
    value: int
    validate: Callable[[Type['IntegerField'], int], None]

    def __init__(self, value: Any):
        self.value = int(value)
        type(self).validate(self.value)  # type: ignore

    def __init_subclass__(
        cls, minimum: Optional[int] = None, maximum: Optional[int] = None
    ) -> None:
        if maximum is None and minimum is not None:
            cls.validate = MethodType(validate_minimum, cls)

        elif maximum is not None and minimum is None:
            cls.validate = MethodType(validate_maximum, cls)

        elif maximum is not None and minimum is not None:
            cls.validate = MethodType(validate_minimum_maximum, cls)

        elif maximum is None and minimum is None:
            cls.validate = MethodType(lambda c, v: v, cls)

        if minimum is not None:
            cls.minimum = minimum

        if maximum is not None:
            cls.maximum = maximum


def validate_minimum(cls: Type[IntegerField], value: int) -> None:
    if not cls.minimum <= value:
        raise DeserializationError(
            f'Invalid minimum integer value: {cls.minimum} < {value}'
        )


def validate_maximum(cls: Type[IntegerField], value: int) -> None:
    if not cls.maximum >= value:
        raise DeserializationError(
            f'Invalid maximum integer value: {value} < {cls.maximum}'
        )


def validate_minimum_maximum(cls: Type[IntegerField], value: int) -> None:
    if not cls.minimum <= value <= cls.maximum:
        raise DeserializationError(
            f'Invalid minimum and maximum integer value: '
            f'{cls.minimum} < {value} < {cls.maximum}'
        )


def validate_min_length(cls: Type[StringField], value: str) -> None:
    if not cls.min_length <= len(value):
        raise DeserializationError(
            f'Invalid min_length string value: {cls.min_length} < {len(value)}'
        )


def validate_max_length(cls: Type[StringField], value: str) -> None:
    if not cls.max_length >= len(value):
        raise DeserializationError(
            f'Invalid max_length string value: {len(value)} < {cls.max_length}'
        )


def validate_min_length_max_length(cls: Type[StringField], value: str) -> None:
    if not cls.min_length <= len(value) <= cls.max_length:
        raise DeserializationError(
            f'Invalid min_length and max_length string value: '
            f'{cls.min_length} < {len(value)} < {cls.max_length}'
        )


def string(
    min_length: Optional[int] = None, max_length: Optional[int] = None
) -> Type[StringField]:
    min_length_str = '' if min_length is None else str(min_length)
    max_length_str = '' if max_length is None else str(max_length)
    cls_name = f'String{min_length_str}{max_length_str}'
    return type(
        cls_name,
        (StringField,),
        {'min_length': min_length, 'max_length': max_length},
    )


def integer(
    minimum: Optional[int] = None, maximum: Optional[int] = None
) -> Type[IntegerField]:
    minimum_str = '' if minimum is None else str(minimum)
    maximum_str = '' if maximum is None else str(maximum)
    cls_name = f'String{minimum_str}{maximum_str}'
    return type(
        cls_name, (IntegerField,), {'minimum': minimum, 'maximum': maximum},
    )


def jsonschema_asdataclass(
    id_: str, schema: Dict[str, Any], bases: Tuple[type, ...] = ()
) -> Type[Any]:
    is_dict = any([issubclass(base, dict) for base in bases])
    subschema_bases = (dict,) if is_dict else tuple()
    extracted_annotations = [
        extract_annotations(
            id_,
            is_dict,
            prop_name,
            prop,
            subschema_bases,
            schema.get('required', []),
            subschema_bases,
        )
        for prop_name, prop in schema.get('properties', {}).items()
    ]

    type_ = make_type_from_extracted_annotations(
        id_, is_dict, extracted_annotations, bases
    )

    if is_dict:
        type_.__additional_properties__ = schema.get(
            'additionalProperties', True
        )

        if isinstance(type_.__additional_properties__, dict):
            extracted_annotations_ = extract_annotations(
                id_,
                is_dict,
                'additional_properties',
                schema['additionalProperties'],
                subschema_bases,
                schema['additionalProperties'].get('required', []),
            )
            type_.__additional_properties__ = extracted_annotations_[1]
    else:
        type_.__additional_properties__ = schema.get(
            'additionalProperties', False
        )

    return type_  # type: ignore


def extract_annotations(
    id_: str,
    is_dict: bool,
    prop_name: str,
    prop: Dict[str, Any],
    bases: Tuple[type, ...],
    required: List[str],
    subschema_bases: Tuple[type, ...] = (),
) -> Tuple[str, Type[Any], Any]:
    return (
        prop_name,
        Optional[
            jsonschema_asdataclass(
                f'{id_}_{prop_name}', prop, subschema_bases  # noqa
            )
        ]
        if prop['type'] == 'object'
        else (
            (
                jsonschema_array(id_, prop_name, prop, subschema_bases)
                if prop['type'] == 'array'
                else SCALARS[prop['type']]
            )
            if prop_name in required
            else (
                Optional[
                    jsonschema_array(id_, prop_name, prop, subschema_bases)
                ]
                if prop['type'] == 'array'
                else Optional[SCALARS[prop['type']]]
            )
        ),
        prop.get('default')
        if is_dict
        else dataclasses.field(default=prop.get('default')),
    )


def make_type_from_extracted_annotations(
    id_: str,
    is_dict: bool,
    extracted_annotations: List[Tuple[str, Type[Any], Any]],
    bases: Tuple[type, ...],
) -> Any:
    if is_dict:
        type_annotations = {}
        type_attributes = {}

        for prop_name, prop_type, prop_default in extracted_annotations:
            type_annotations[prop_name] = prop_type

            if prop_default is not None:
                type_attributes[prop_name] = prop_default

        type_attributes['__annotations__'] = type_annotations
        schema_type = type(id_, (dict,), type_attributes)
        return jsondaora(_TypedDictMeta(id_, bases + (schema_type,), {}))

    else:
        return dataclasses.make_dataclass(
            id_, extracted_annotations, bases=bases,
        )


def jsonschema_array(
    id_: str, prop_name: str, prop: Any, bases: Tuple[type, ...],
) -> Any:
    DynamicType: Type[Any] = (
        jsonschema_asdataclass(
            f'{id_}_{prop_name}', prop['items'], bases
        )  # noqa
        if (array_type := prop['items']['type']) == 'object'  # noqa
        else jsonschema_array(id_, prop_name, prop['items'], bases)  # noqa
        if array_type == 'array'  # noqa
        else SCALARS[array_type]
    )
    list_type = List[DynamicType]  # type: ignore

    if 'additionalItems' in prop:
        list_type.__additional_items__ = prop['additionalItems']  # type: ignore

    return list_type


SCALARS = {
    'boolean': bool,
    'string': str,
    'integer': int,
    'number': float,
}
