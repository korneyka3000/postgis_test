from __future__ import annotations

from uuid import UUID

from roga_and_kopyta.core.schemas import AuditMixin, ImmutableDTO


__all__ = ("ActivitiesOutDTO",)


class ActivitiesOutDTO(AuditMixin, ImmutableDTO):
    id: UUID
    name: str
    parent: ActivitiesOutDTO | None = None
