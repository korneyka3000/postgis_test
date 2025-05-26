from collections.abc import Callable, Coroutine, Sequence
from typing import Any, TypeVar

from pydantic import BaseModel, SecretStr, TypeAdapter
from sqlalchemy import Delete, Insert, Select, Update


__all__ = (
    "BasePydantic",
    "StmtT",
    "PydOrAdapter",
    "ApiKeyDepT",
    "ApiKeyDepReturnT",
)


BasePydantic = TypeVar("BasePydantic", bound=BaseModel)
StmtT = TypeVar("StmtT", Select[Any], Insert, Update, Delete)
T = TypeVar("T")


PydOrAdapter = TypeVar(
    "PydOrAdapter",
    bound=type[BaseModel] | TypeAdapter[type[BaseModel] | Sequence[type[BaseModel]]],
)

ApiKeyDepReturnT = Callable[[str], Coroutine[Any, Any, str]]
ApiKeyDepT = Callable[[SecretStr, str], ApiKeyDepReturnT]
