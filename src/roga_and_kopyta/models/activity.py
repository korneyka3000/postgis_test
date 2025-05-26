from uuid import UUID

from sqlalchemy import VARCHAR, Column, ForeignKey, Table, literal_column, select
from sqlalchemy.orm import Mapped, aliased, mapped_column, relationship
from sqlalchemy.sql.selectable import CTE

from .base import Base


__all__ = (
    "Activity",
    "organization_activity",
)

organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("activity_id", ForeignKey("activity.id"), primary_key=True),
    Column("organization_id", ForeignKey("organization.id"), primary_key=True),
)


class Activity(Base):
    name: Mapped[str] = mapped_column(VARCHAR(255), unique=True)

    parent_id: Mapped[UUID | None] = mapped_column(ForeignKey("activity.id"))

    children: Mapped[list["Activity"]] = relationship(
        argument="Activity",
        back_populates="parent",
        remote_side=[parent_id],
        join_depth=3,
    )
    parent = relationship(
        argument="Activity",
        back_populates="children",
        remote_side="Activity.id",
        lazy="joined",
        join_depth=3,
    )
    organizations = relationship(
        "Organization",
        secondary=organization_activity,
        back_populates="activities",
    )

    def __repr__(self) -> str:
        return f"Activity<id:{self.id},name={self.name},parent_id={self.parent_id}>"

    @classmethod
    def load_recursive_cte(cls, root_id: UUID, depth: int = 3) -> CTE:
        aliased_activity = aliased(Activity)

        cte = (
            select(Activity.id.label("id"), literal_column("1").label("depth"))
            .where(Activity.id == root_id)
            .cte("activity_tree", recursive=True)
        )
        return cte.union_all(
            select(aliased_activity.id, (cte.c.depth + 1).label("depth")).where(
                aliased_activity.parent_id == cte.c.id,
                cte.c.depth < depth,
            )
        )
