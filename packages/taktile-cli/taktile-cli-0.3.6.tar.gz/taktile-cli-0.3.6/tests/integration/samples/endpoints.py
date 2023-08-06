from tktl import Tktl

from .endpoint_defs.structured import tktl as tktl_structured
from .endpoint_defs.unstructured import tktl as tktl_unstructured

tktl = Tktl()
tktl.endpoints = tktl_structured.endpoints + tktl_unstructured.endpoints
