from typing import Callable, Dict, List, Optional, Union

from pyarrow import Schema, Table
from pydantic import BaseModel

from tktl.core.t import EndpointKinds


class EndpointInfoSchema(BaseModel):
    name: str
    kind: EndpointKinds
    profiling_supported: bool = False
    profiling_columns: Optional[List[str]] = []
    explain_input_names: Optional[List[str]] = []
    explain_input_example: Optional[List[Dict]] = []
    input_names: List[str] = []
    output_names: Union[str, List[str]] = None


class EndpointDefinition(BaseModel):
    name: str
    kind: str
    func: Callable
    input_schema: Schema
    output_schema: Schema

    class Config:
        arbitrary_types_allowed = True
