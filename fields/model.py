from __future__ import annotations

from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class EntityFieldCreate(BaseModel):
    label: str
    field_type: str

    required: bool = False

    config: dict[str, Any] | None = None

    entity_id: int = Field(gt=0)


class EntityFieldResponse(EntityFieldCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        from_attributes=True
    )
