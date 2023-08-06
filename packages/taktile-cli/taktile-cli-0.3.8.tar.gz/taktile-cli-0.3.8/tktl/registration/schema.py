from abc import ABC, abstractmethod
from typing import Any, Dict, List, Sequence, Tuple, Type

import numpy
import pandas
from pydantic import BaseModel

from tktl.core.loggers import LOG
from tktl.core.serializers import to_pydantic
from tktl.core.serializers.base import CustomDeserializingModelT
from tktl.core.t import RestSchemaTypes
from tktl.registration.validation import (
    data_frame_convertible,
    input_pandas_representation,
    output_pandas_representation,
    series_convertible,
)

_SUPPORTED_TYPES = [pandas.DataFrame, pandas.Series, numpy.ndarray, Sequence, dict]


def check_supported_inputs(value):
    return any([isinstance(value, t_) for t_ in _SUPPORTED_TYPES])


class EndpointSchema(ABC):
    KIND: str

    def __init__(
        self,
        value: Any,
        endpoint_kind: str,
        endpoint_name: str,
        user_defined_model: Type[BaseModel] = None,
    ):
        self.endpoint_kind = endpoint_kind
        self.value = value
        self.is_supported = check_supported_inputs(value)
        if not self.is_supported:
            LOG.warning(
                f"Schema discovery not supported for inputs of type {type(value)}"
            )
        if user_defined_model:
            value = user_defined_model

        self.pydantic: CustomDeserializingModelT = to_pydantic(
            value, unique_id=f"{endpoint_name}__{self.KIND}"
        )

    @property
    @abstractmethod
    def pandas_convertible(self):
        raise NotImplementedError


class EndpointOutputSchema(EndpointSchema):
    KIND = "output"

    @property
    def pandas_convertible(self):
        return series_convertible(self.value)

    @property
    def names(self):
        if self.pandas_convertible:
            return output_pandas_representation(self.value).name
        else:
            return get_model_names(self.pydantic)


class EndpointInputSchema(EndpointSchema):
    KIND = "input"

    @property
    def pandas_convertible(self):
        return data_frame_convertible(self.value)

    @property
    def names(self):
        if self.pandas_convertible:
            return list(input_pandas_representation(self.value).columns)
        else:
            return get_model_names(self.pydantic)


def get_model_names(model: CustomDeserializingModelT):
    schema = model.schema()
    if schema["title"] == RestSchemaTypes.DICT.value:
        return list(schema["properties"].keys())
    elif (
        schema["title"] == RestSchemaTypes.SEQUENCE.value
        or schema["title"] == RestSchemaTypes.ARRAY.value
    ):
        return get_nested_type_names(schema)
    else:
        raise ValueError(f"Schema named: {schema['title']} is not recognized")


def get_nested_type_names(schema) -> List[str]:
    schema, inner_type = walk_sequence_schema(schema)
    n_features = schema[0]
    if len(schema) == 1:
        shapes = ""
    else:
        shapes_str = "x".join([str(dim) for dim in schema[1:]])
        shapes = f" (Shape: {shapes_str})"
    return [f"Feature {i}{shapes}" for i in range(n_features)]


def walk_sequence_schema(schema: Dict, shapes=()) -> Tuple[Tuple[int], str]:
    if schema["type"] == "array":
        shapes += (schema["maxItems"],)
        return walk_sequence_schema(schema["items"], shapes=shapes)
    if schema["type"] != "array":
        return shapes, schema["type"]
