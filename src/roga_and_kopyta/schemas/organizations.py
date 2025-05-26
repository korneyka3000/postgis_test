from __future__ import annotations

from itertools import batched
from typing import Annotated
from uuid import UUID

from pydantic import Field, field_validator, model_validator

from roga_and_kopyta.core.schemas import AuditMixin, ImmutableDTO, MutableDTO
from roga_and_kopyta.core.types.geo import CoordinatesArr

from .activity import ActivitiesOutDTO
from .building import BuildingOutDTO


__all__ = (
    "BaseOrganizationDTO",
    "PhoneNumberOutDTO",
    "FilterParams",
)


class PhoneNumberOutDTO(AuditMixin, ImmutableDTO):
    id: UUID
    value: str


class BaseOrganizationDTO(AuditMixin, ImmutableDTO):
    id: UUID
    name: str
    phone_numbers: list[PhoneNumberOutDTO]
    building: BuildingOutDTO
    activities: list[ActivitiesOutDTO]


class FilterParams(MutableDTO, extra="forbid"):
    building_id: UUID | None = None
    activity_id: UUID | None = None
    name: str | None = None
    include_subtree: bool = False
    point: CoordinatesArr = None
    radius: Annotated[int | None, Field(gt=0, le=6_357_000)] = None
    polygon: Annotated[
        tuple[CoordinatesArr, ...] | None,
        Field(
            min_length=4,
            description="At least 4 points(pairs), first and last pairs must match",
            example=[37.61, 57.61],
        ),
    ] = None

    @field_validator("polygon", mode="before")
    @classmethod
    def _to_tuples_list(
        cls,
        v: str | None,
    ) -> list[tuple[float | str, ...]] | None:
        if v is None:
            return None
        if len(v) % 2 != 0:
            raise ValueError(f"Wrong number of coordinates: {len(v)}, should be even")
        return list(batched(v, 2))

    @model_validator(mode="after")
    def _model_validate(self) -> FilterParams:
        if self.polygon:
            if self.polygon[0] != self.polygon[-1]:
                raise ValueError("First and last points must match in Polygon")
        if self.activity_id is None and self.include_subtree is True:
            raise ValueError("`activity_id` is required if include_subtree is True")
        if self.point and self.polygon:
            raise ValueError("Choose `point` or `polygon`")
        if self.point and not self.radius:
            raise ValueError("`radius` is required if `point` used")
        if self.radius and self.polygon:
            raise ValueError("Use `radius` with `point`")
        return self
