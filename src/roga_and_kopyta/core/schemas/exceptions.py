from pydantic import BaseModel


__all__ = ("ExceptionScheme",)


class ExceptionScheme(BaseModel):
    detail: str
