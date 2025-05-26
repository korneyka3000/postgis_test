from geoalchemy2 import Geometry, WKBElement
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


__all__ = ("Building",)


class Building(Base):
    address: Mapped[str]
    geo_location: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True),
    )

    organizations: Mapped[list["Organization"]] = relationship(  # type: ignore [name-defined] # noqa
        argument="Organization",
        back_populates="building",
    )

    def __repr__(self) -> str:
        return (
            f"<Building id:{self.id},"
            f"address:{self.address},"
            f"geo_location:{self.geo_location}>"
        )
