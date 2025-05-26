from datetime import UTC, datetime, timezone


__all__ = ("now",)


def now(tz: timezone = UTC) -> datetime:
    return datetime.now(tz=tz)
