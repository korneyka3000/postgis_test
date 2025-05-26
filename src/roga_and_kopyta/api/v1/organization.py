__all__ = ("router",)

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from roga_and_kopyta.core.deps import provide_db_session
from roga_and_kopyta.core.schemas import ExceptionScheme
from roga_and_kopyta.schemas import BaseOrganizationDTO, FilterParams
from roga_and_kopyta.services import OrganizationService


router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
    dependencies=[Depends(provide_db_session)],
)


@router.get(
    "/{item_id}",
    responses={
        HTTP_200_OK: {"model": BaseOrganizationDTO},
        HTTP_404_NOT_FOUND: {"model": ExceptionScheme},
    },
)
async def organization_info(item_id: UUID):
    """
    Вывод информации об организации по её идентификатору

    - `item_id`: уникальный идентификатор организации.
    """
    return await OrganizationService.get_by_id(item_id=item_id)


@router.get(
    "/",
    responses={HTTP_200_OK: {"model": list[BaseOrganizationDTO]}},
)
async def filter_organizations(
    filter_query: Annotated[FilterParams, Query()],
):
    """
    Универсальный эндпоинт для фильтров.

    - Список всех организаций, находящихся в конкретном здании.
        - Передать `building_id` желаемого здания для фильтра.

    - Список всех организаций, которые относятся к указанному виду деятельности.
        - Передать `activity_id` для нужной деятельности,
        не передавать `include_subtree`.

    - Список организаций, которые находятся в заданном радиусе/прямоугольной
            области относительно указанной точки на карте. Список зданий
        - Передать `point`/`polygon` координаты,
         в случае в `point` необходимо добавить `radius`.

    - Искать организации по виду деятельности. Например,
    поиск по виду деятельности «Еда»,
    которая находится на первом уровне дерева,
    и чтобы нашлись все организации,
    которые относятся к видам деятельности, лежащим внутри.
    Т.е. В результатах поиска должны отобразиться организации
    с видом деятельности Еда, Мясная продукция, Молочная продукция.
        - Передать `activity_id` нужной деятельности,
         поставить флаг `include_subtree=True`

    - Поиск организации по названию
        - Передать `name`

    - Ограничить уровень вложенности деятельностей 3 уровням
        - По умолчанию установлено как 3, можно изменить в коде или вынести как параметр
    """
    return await OrganizationService.filtered(filter_query=filter_query)
