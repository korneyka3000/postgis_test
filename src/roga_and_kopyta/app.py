from fastapi import FastAPI
from fastapi.exceptions import ValidationException
from fastapi.responses import ORJSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from roga_and_kopyta.config.logs import setup_logging

from .api import router
from .core.schemas import ExceptionScheme


setup_logging()
app = FastAPI(
    debug=True,
    responses={
        HTTP_422_UNPROCESSABLE_ENTITY: {"model": ExceptionScheme},
    },
)
app.include_router(router)


def _basic_handler(
    exc: Exception | ValidationException,
    raise_code: int,
) -> ORJSONResponse:
    if isinstance(exc, ValidationException):
        msg = exc.errors()[0].get("msg", "")
    else:
        msg = exc.args[0]
    return ORJSONResponse(
        status_code=raise_code,
        content={"detail": msg},
    )


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(
#     _: Request,
#     exc: RequestValidationError,
# ) -> ORJSONResponse:
#     return _basic_handler(
#         exc=exc,
#         raise_code=HTTP_422_UNPROCESSABLE_ENTITY,
#     )
