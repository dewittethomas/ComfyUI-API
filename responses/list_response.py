from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar("T")

class ListResponse(BaseModel, Generic[T]):
    object: str = "list"
    data: List[T]