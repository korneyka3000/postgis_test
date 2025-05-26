from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


__all__ = (
    "ImmutableDTO",
    "MutableDTO",
    "ConfigDict",
    "AuditMixin",
)


MODEL_CONFIG = ConfigDict(
    str_strip_whitespace=True,
    use_enum_values=True,
    from_attributes=True,
    alias_generator=to_camel,
    allow_inf_nan=False,
    ser_json_timedelta="iso8601",
    ser_json_bytes="base64",
    validate_return=True,
    coerce_numbers_to_str=True,
    regex_engine="python-re",
    use_attribute_docstrings=True,
    extra="ignore",
    populate_by_name=True,
)


class DTO(BaseModel):
    model_config = MODEL_CONFIG


class ImmutableDTO(DTO, frozen=True):
    pass


class MutableDTO(DTO, frozen=False):
    pass


class AuditMixin(DTO):
    created_at: datetime
    updated_at: datetime | None = None
