from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from entity.model import EntityResponse


class CompanyCreate(BaseModel):
    name: str
    reson: str | None = None
    nuit: int | None = None
    description: str | None = None
    deleted_status: bool = False

class CompanyUpdate(BaseModel):
    name: str | None = None
    reson: str | None = None
    nuit: int | None = None
    description: str | None = None
    deleted_status: bool = False

class CompanyResponse(CompanyCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        from_attributes=True
    )

class CompanyDetailsResponse(CompanyResponse):
    entities: list[EntityResponse] = Field(
        default_factory=list
    )