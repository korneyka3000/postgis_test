from typing import cast
from uuid import UUID

from fastapi import HTTPException
from geoalchemy2.functions import (
    ST_DWithin,
    ST_MakePoint,
    ST_SetSRID,
    ST_Transform,
    ST_Within,
)
from geoalchemy2.shape import from_shape
from shapely import Polygon
from sqlalchemy import select
from sqlalchemy.orm import contains_eager, joinedload, selectinload
from starlette.status import HTTP_404_NOT_FOUND

from roga_and_kopyta.repository.organization import OrganizationRepo
from roga_and_kopyta.schemas import BaseOrganizationDTO, FilterParams

from ..models import Activity, Building
from .base import BaseService


__all__ = ("OrganizationService",)


class OrganizationService(BaseService[BaseOrganizationDTO]):
    repo = OrganizationRepo
    scheme: type[BaseOrganizationDTO] = BaseOrganizationDTO

    @classmethod
    async def get_by_id(cls, item_id: UUID) -> BaseOrganizationDTO:
        result = await cls.repo.get_by_id(
            item_id,
            options=(
                joinedload(cls.model.building),
                selectinload(cls.model.phone_numbers),
                selectinload(cls.model.activities),
            ),
        )
        if result is None:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Item not found",
            )
        return cast(BaseOrganizationDTO, cls.to_scheme(data=result))

    @classmethod
    async def filtered(
        cls,
        filter_query: FilterParams,
    ) -> list[BaseOrganizationDTO]:
        joins_added: set[type] = set()
        stmt = cls.repo.queryset
        if filter_query.building_id:
            stmt = stmt.where(cls.model.building_id == filter_query.building_id)
        if filter_query.name:
            stmt = stmt.where(cls.model.name.ilike(f"%{filter_query.name}%"))
        if filter_query.activity_id and not filter_query.include_subtree:
            stmt = stmt.where(cls.model.activities.any(id=filter_query.activity_id))
        if filter_query.point:
            # Note: for better accuracy transform to 3857
            point = ST_Transform(
                ST_SetSRID(
                    ST_MakePoint(
                        filter_query.point[0],
                        filter_query.point[1],
                    ),
                    4326,
                ),
                3857,
            )
            stmt = stmt.join(cls.model.building).where(
                ST_DWithin(
                    ST_Transform(Building.geo_location, 3857),
                    point,
                    filter_query.radius,
                )
            )
            joins_added.add(Building)
        if filter_query.polygon:
            polygon = Polygon(filter_query.polygon)
            polygon_geo = from_shape(polygon, srid=4326)
            # NOTE: can use ST_Contains, but switch args.
            stmt = stmt.join(cls.model.building).where(
                ST_Within(Building.geo_location, polygon_geo)
            )
            joins_added.add(Building)
        if filter_query.include_subtree and filter_query.activity_id is not None:
            stmt = stmt.join(cls.model.activities).where(
                Activity.id.in_(
                    select(
                        (
                            Activity.load_recursive_cte(
                                root_id=filter_query.activity_id
                            )
                        ).c.id
                    )
                )
            )
            joins_added.add(Activity)
        if Building in joins_added:
            stmt = stmt.options(contains_eager(cls.model.building))
        else:
            stmt = stmt.options(joinedload(cls.model.building))
        if Activity in joins_added:
            stmt = stmt.options(contains_eager(cls.model.activities))
        else:
            stmt = stmt.options(selectinload(cls.model.activities))
        result = (await cls.repo.execute(stmt)).unique().all()
        return cast(list[BaseOrganizationDTO], cls.to_scheme(data=result))
