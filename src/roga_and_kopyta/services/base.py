__all__ = ("BaseService",)


from collections.abc import Sequence
from typing import Any, Generic, TypeVar, cast

from pydantic import BaseModel, TypeAdapter
from sqlalchemy.util import classproperty

from roga_and_kopyta.models.base.annotated_types import BaseDBT
from roga_and_kopyta.repository.base import BaseRepository


T = TypeVar("T", bound=BaseModel)


class BaseService(Generic[T]):
    repo: type[BaseRepository[Any]]
    scheme: type[T] | None = None
    plural_scheme: Sequence[type[T]] | None = None
    _scheme: TypeAdapter[T]
    _plural_scheme: TypeAdapter[Sequence[T]]

    @classproperty
    def model(cls) -> type[BaseDBT]:
        return cls.repo.model

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if not getattr(cls, "scheme", None):
            raise ValueError("scheme should be set in subclass of BaseService")
        if not getattr(cls, "repo", None):
            raise ValueError("Repository should be set in subclass of BaseService")
        if cls.plural_scheme is None:
            cls._plural_scheme = TypeAdapter(list[cls.scheme])  # type: ignore [name-defined]
        else:
            cls._plural_scheme = TypeAdapter(cls.plural_scheme)
        cls._scheme = TypeAdapter(cls.scheme)

    @classmethod
    def to_scheme(
        cls,
        data: BaseDBT | Sequence[BaseDBT],
        schema_type: BaseModel | None = None,
    ) -> T | Sequence[T]:
        if schema_type is None:
            if isinstance(data, Sequence):
                validator = cls._plural_scheme.validate_python
            else:
                validator = cls._scheme.validate_python
            return validator(data)
        return cast(T, schema_type.model_validate(data))
