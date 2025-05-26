__all__ = ("cxt_session",)

from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession


cxt_session: ContextVar[AsyncSession | None] = ContextVar("Session", default=None)
