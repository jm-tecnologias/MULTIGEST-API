from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class EntityRecordCreate(BaseModel):
    entity_id: int = Field(gt=0)
    company_id: int = Field(gt=0)

class EntityRecordResponse(EntityRecordCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        from_attributes=True
    )

# class EntityRecordDetailsResponse(EntityRecordResponse):
#     entities_answers: list[
#         EntityAnswerResponse
#     ] = Field(default_factory=list)

