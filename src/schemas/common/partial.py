from typing import Any

from pydantic import BaseModel


class PartialSchemaMixin(BaseModel):
    """Mixin that makes all required fields optional with default=None for partial update models.
    Note: This does NOT make fields nullable — passing None explicitly will still raise ValidationError."""

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        for field in cls.model_fields.values():
            if field.is_required():
                field.default = None
        cls.model_rebuild(force=True)
