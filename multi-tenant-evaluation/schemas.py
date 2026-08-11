from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class CompanyCreate(BaseModel):
    name: str


class CompanyResponse(CompanyCreate):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )


class FormCreate(BaseModel):
    name: str
    description: Optional[str] = None


class FormFieldCreate(BaseModel):
    label: str

    field_type: str

    required: bool = False

    position: int = 0

    weight: Optional[int] = None

    config: Optional[dict[str, Any]] = None


class FormFieldResponse(FormFieldCreate):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )


class FormResponse(BaseModel):
    id: int

    company_id: int

    name: str

    description: Optional[str]

    active: bool

    fields: list[FormFieldResponse] = []

    model_config = ConfigDict(
        from_attributes=True
    )


class AnswerCreate(BaseModel):
    field_id: int

    value: Any


class SubmissionCreate(BaseModel):
    submitted_by: Optional[str] = None

    answers: list[AnswerCreate]


class AnswerResponse(BaseModel):
    id: int

    field_id: int

    value: Any

    model_config = ConfigDict(
        from_attributes=True
    )


class SubmissionResponse(BaseModel):
    id: int

    form_id: int

    submitted_by: Optional[str]

    answers: list[AnswerResponse]

    model_config = ConfigDict(
        from_attributes=True
    )