from collections.abc import AsyncIterator
from functools import partial
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from roga_and_kopyta.config import settings
from roga_and_kopyta.core.adapters.database import async_session_maker
from roga_and_kopyta.core.types.annotated_types import ApiKeyDepT
from roga_and_kopyta.core.utils import api_key_header_dep
from roga_and_kopyta.repository.base.ctx_session_keeper import cxt_session


__all__ = (
    "provide_db_session",
    "SessionDep",
    "APIKeyDepV1",
)


async def provide_db_session() -> AsyncIterator[AsyncSession]:
    async with async_session_maker() as session:
        cxt_session.set(session)
        yield session
        cxt_session.set(None)


SessionDep = Annotated[AsyncSession, Depends(dependency=provide_db_session)]


APIKeyDepV1: ApiKeyDepT = partial(
    api_key_header_dep,
    scheme_name=settings.API_KEY_V1_SCOPE,
)
