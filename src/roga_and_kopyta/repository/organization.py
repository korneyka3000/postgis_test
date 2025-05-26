from sqlalchemy import select
from sqlalchemy.orm import selectinload

from roga_and_kopyta.models import Organization

from .base import BaseRepository


__all__ = ("OrganizationRepo",)


class OrganizationRepo(BaseRepository[Organization]):
    model = Organization
    queryset = select(Organization).options(
        selectinload(Organization.phone_numbers),
    )
