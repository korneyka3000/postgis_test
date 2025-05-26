__all__ = (
    "GEOElement",
    "Latitude",
    "Longitude",
    "CoordinatesArr",
)
from typing import Annotated, Any, cast

from geoalchemy2 import WKBElement
from geoalchemy2.shape import to_shape
from pydantic import Field, PlainSerializer
from shapely.geometry import mapping


def serialize_wkb(v: WKBElement) -> dict[str, Any]:
    geometry = to_shape(v)
    return cast(dict[str, Any], mapping(geometry))


GEOElement = Annotated[WKBElement, PlainSerializer(serialize_wkb)]

Latitude = Annotated[float, Field(ge=-90, le=90, description="Latitude in degrees")]
Longitude = Annotated[float, Field(ge=-180, le=180, description="Longitude in degrees")]


CoordinatesArr = Annotated[
    tuple[Longitude, Latitude] | None,
    Field(
        min_length=2,
        max_length=2,
        description="order [lon,lat] "
        "**-180 <= Longitude <= 180 | -90 <= Latitude <= 90**",
    ),
]
