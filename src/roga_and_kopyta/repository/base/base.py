__all__ = ("BaseRepository", "BasePydantic")


from collections.abc import AsyncIterator, Awaitable, Callable, Sequence
from contextlib import asynccontextmanager
from typing import Any, Generic, Literal, TypeVar, cast

from sqlalchemy import ScalarResult, Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.orm.interfaces import ORMOption

from roga_and_kopyta.core.adapters.database import async_session_maker
from roga_and_kopyta.core.types import BasePydantic, StmtT
from roga_and_kopyta.models.base.annotated_types import BaseDBT

from .ctx_session_keeper import cxt_session


T = TypeVar("T")


class BaseRepository(Generic[BaseDBT]):
    model: type[BaseDBT]
    queryset: Select[tuple[BaseDBT]]
    _session_ctx = cxt_session

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if getattr(cls, "queryset", None) is None:
            cls.queryset = cls._init_queryset()

    @classmethod
    def _init_queryset(cls) -> Select[tuple[BaseDBT]]:
        return cast(Select[tuple[BaseDBT]], select(cls.model))

    @classmethod
    @asynccontextmanager
    async def with_session(cls) -> AsyncIterator[AsyncSession]:
        session = cls._session_ctx.get()
        if session is None:
            try:
                async with async_session_maker() as conn:
                    cls._session_ctx.set(conn)
                    yield conn
            finally:
                cls._session_ctx.set(None)
        else:
            yield session

    @classmethod
    async def execute(
        cls,
        stmt: StmtT,
        executor: Literal["scalars", "execute", "scalar"] = "scalars",
    ) -> Any:
        async with cls.with_session() as session:  # type: AsyncSession
            try:
                execute_as: Callable[[StmtT], Awaitable[Any]] = getattr(
                    session,
                    executor,
                )
            except AttributeError:
                raise ValueError(f"AsyncSession has no attribute {executor}")
            return await execute_as(stmt)

    @classmethod
    async def all(cls) -> list[ScalarResult[BaseDBT]]:
        query = await cls.execute(cls.queryset)
        return cast(list[ScalarResult[BaseDBT]], query.all())

    @classmethod
    async def filter_by(
        cls,
        by: InstrumentedAttribute[T],
        value: T,
        options: Sequence[ORMOption] = (),
    ) -> list[BaseDBT]:
        query = cls.queryset.where(by == value).options(*options)
        result = await cls.execute(query)
        return cast(list[BaseDBT], result.all())

    @classmethod
    async def get_by(
        cls,
        by: InstrumentedAttribute[T],
        value: T,
        options: Sequence[ORMOption] = (),
        with_for_update: bool = False,
    ) -> BaseDBT | None:
        query = select(cls.model).where(by == value).options(*options)
        if with_for_update:
            query = query.with_for_update()
        result = await cls.execute(query)
        return cast(BaseDBT | None, result.one_or_none())

    @classmethod
    async def get_by_id(
        cls,
        pk: T,
        with_for_update: dict[str, Any] | bool = False,
        options: Sequence[ORMOption] = (),
    ) -> BaseDBT | None:
        if with_for_update:
            with_for_update = {"of": cls.model}
        async with cls.with_session() as session:  # type: AsyncSession
            return await session.get(
                cls.model,
                pk,
                with_for_update=with_for_update,
                options=options,
            )
