from secrets import compare_digest
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from pydantic import SecretStr
from starlette.status import HTTP_401_UNAUTHORIZED

from roga_and_kopyta.core.types.annotated_types import ApiKeyDepReturnT


__all__ = ("api_key_header_dep",)


def api_key_header_dep(key: SecretStr, name: str, scheme_name: str) -> ApiKeyDepReturnT:
    header = APIKeyHeader(name=name, scheme_name=scheme_name)

    async def _api_key_header_dep(
        api_key: Annotated[str, Depends(header)],
    ) -> str:
        if not compare_digest(api_key, key.get_secret_value()):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
            )
        return api_key

    return _api_key_header_dep
