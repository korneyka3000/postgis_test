from __future__ import annotations

from uuid import UUID

from sqlalchemy import VARCHAR, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .activity import Activity
from .base import Base


__all__ = (
    "Organization",
    "PhoneNumber",
)


class Organization(Base):
    name: Mapped[str]
    building_id: Mapped[UUID] = mapped_column(ForeignKey("building.id"))

    building: Mapped["Building"] = relationship(  # type: ignore [name-defined] # noqa
        argument="Building",
        back_populates="organizations",
    )
    phone_numbers: Mapped[list[PhoneNumber]] = relationship(
        argument="PhoneNumber",
        back_populates="organizations",
    )
    activities: Mapped[list[Activity]] = relationship(
        argument="Activity",
        secondary="organization_activity",
        back_populates="organizations",
    )

    def __repr__(self) -> str:
        return (
            f"Organization<"
            f"id:{self.id},"
            f"name:{self.name},"
            f"building_id:{self.building_id}"
            f">)"
        )


class PhoneNumber(Base):
    value: Mapped[str] = mapped_column(VARCHAR(20), unique=True)
    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organization.id"))

    organizations: Mapped[Organization] = relationship(
        argument="Organization",
        back_populates="phone_numbers",
    )
