from uuid import UUID

from roga_and_kopyta.core.schemas import AuditMixin, ImmutableDTO
from roga_and_kopyta.core.types.geo import GEOElement


__all__ = ("BuildingOutDTO",)


class BuildingOutDTO(ImmutableDTO, AuditMixin, arbitrary_types_allowed=True):
    id: UUID
    address: str
    geo_location: GEOElement
