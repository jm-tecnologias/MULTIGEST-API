from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from fields.model import EntityFieldResponse
from records.model import EntityRecordResponse



# ================================================================================
class EntityCreate(BaseModel):
    name: str
    description: str | None= None
    company_id: int = Field(gt=0)

class EntityResponse(EntityCreate):
    id:int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        from_attributes=True
    )

class EntityDetailsResponse(EntityResponse):
    entities_fields: list[EntityFieldResponse] = Field(
        default_factory=list
    )
class EntityFullResponse(EntityDetailsResponse):
    entities_records: list[EntityRecordResponse] = Field(
        default_factory=list
    )