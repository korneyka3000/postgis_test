from pydantic.alias_generators import to_snake
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr

from .mixin import BaseMixin


__all__ = ("Base",)


class Base(BaseMixin, AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return to_snake(camel=cls.__name__)
