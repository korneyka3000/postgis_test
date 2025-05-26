__all__ = ("router",)

from fastapi import APIRouter, Depends

from roga_and_kopyta.config import settings
from roga_and_kopyta.core.deps import APIKeyDepV1

from .organization import router as organization_router


router = APIRouter(
    prefix="/v1",
    dependencies=[
        Depends(
            APIKeyDepV1(
                key=settings.API_KEY_V1,
                name=settings.API_KEY_V1_NAME,
            )
        )
    ],
)

router.include_router(organization_router)
