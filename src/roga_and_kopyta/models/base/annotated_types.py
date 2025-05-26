from typing import TypeVar

from .base import Base


__all__ = ("BaseDBT",)

BaseDBT = TypeVar("BaseDBT", bound=Base)
