from __future__ import annotations

from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict, Field


# ================================================================================
# class EntityAnswerCreate(BaseModel):
#     entity_record_id: int = Field(gt=0)
#     entity_field_id: int = Field(gt=0)
#     value: Any
#
# class EntityAnswerResponse(EntityAnswerCreate):
#     id: int
#     created_at: datetime
#     updated_at: datetime
#     model_config = ConfigDict(
#         from_attributes=True
#     )
class EntityAnswerInput(BaseModel):
    label: str
    value: Any


class EntityRecordInput(BaseModel):
    entity_id: int = Field(gt=0)
    company_id: int = Field(gt=0)
    answers: list[EntityAnswerInput]
