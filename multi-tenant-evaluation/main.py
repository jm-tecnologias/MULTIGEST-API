from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from database import (
    Base,
    engine,
    get_database
)

from model import (
    Company,
    Form,
    FormField,
    FormSubmission, FormAnswer,
)

from schemas import (
    CompanyCreate,
    CompanyResponse,
    FormCreate,
    FormResponse,
    FormFieldCreate,
    FormFieldResponse,
    SubmissionCreate,
    SubmissionResponse,
)


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="Dynamic Multi-Tenant Forms API"
)

origins = [
    "http://localhost:8081",
    "http://127.0.0.1:8081",
    "http://localhost:19006",
    "http://127.0.0.1:19006",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # or allow_origins=["*"], for All origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------------------------------
# COMPANY
# ----------------------------------------------------

@app.post(
    "/companies",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED
)
def create_company(
    data: CompanyCreate,
    database: Session = Depends(get_database)
):
    company = Company(
        name=data.name
    )

    database.add(company)

    database.commit()

    database.refresh(company)

    return company


@app.get(
    "/companies",
    response_model=list[CompanyResponse]
)
def get_companies(
    database: Session = Depends(get_database)
):
    return database.query(
        Company
    ).all()


# ----------------------------------------------------
# FORMS
# ----------------------------------------------------

@app.post(
    "/companies/{company_id}/forms",
    response_model=FormResponse,
    status_code=status.HTTP_201_CREATED
)
def create_form(
    company_id: int,
    data: FormCreate,
    database: Session = Depends(get_database)
):

    company = database.query(
        Company
    ).filter(
        Company.id == company_id
    ).first()

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    form = Form(
        company_id=company_id,
        name=data.name,
        description=data.description
    )

    database.add(form)

    database.commit()

    database.refresh(form)

    return form


@app.get(
    "/companies/{company_id}/forms",
    response_model=list[FormResponse]
)
def get_company_forms(
    company_id: int,
    database: Session = Depends(get_database)
):

    return database.query(
        Form
    ).filter(
        Form.company_id == company_id
    ).all()


# ----------------------------------------------------
# FIELDS
# ----------------------------------------------------

@app.post(
    "/forms/{form_id}/fields",
    response_model=FormFieldResponse,
    status_code=status.HTTP_201_CREATED
)
def create_field(
    form_id: int,
    data: FormFieldCreate,
    database: Session = Depends(get_database)
):

    form = database.query(
        Form
    ).filter(
        Form.id == form_id
    ).first()

    if not form:
        raise HTTPException(
            status_code=404,
            detail="Formulário não encontrado"
        )

    field = FormField(
        form_id=form_id,
        label=data.label,
        field_type=data.field_type,
        required=data.required,
        position=data.position,
        weight=data.weight,
        config=data.config
    )

    database.add(field)

    database.commit()

    database.refresh(field)

    return field


@app.get(
    "/forms/{form_id}",
    response_model=FormResponse
)
def get_form(
    form_id: int,
    database: Session = Depends(get_database)
): 

    form = database.query(
        Form
    ).filter(
        Form.id == form_id
    ).first()

    if not form:
        raise HTTPException(
            status_code=404,
            detail="Formulário não encontrado"
        )

    return form


# ----------------------------------------------------
# SUBMISSIONS
# ----------------------------------------------------

@app.post(
    "/forms/{form_id}/submissions",
    response_model=SubmissionResponse,
    status_code=status.HTTP_201_CREATED
)
def submit_form(
    form_id: int,
    data: SubmissionCreate,
    database: Session = Depends(get_database)
):

    form = database.query(
        Form
    ).filter(
        Form.id == form_id
    ).first()

    if not form:
        raise HTTPException(
            status_code=404,
            detail="Formulário não encontrado"
        )

    form_fields = {
        field.id: field
        for field in form.fields
    }

    received_fields = {
        answer.field_id
        for answer in data.answers
    }

    # Verificar campos obrigatórios
    for field in form.fields:

        if (
            field.required
            and field.id not in received_fields
        ):
            raise HTTPException(
                status_code=400,
                detail=f"O campo '{field.label}' é obrigatório"
            )

    submission = FormSubmission(
        form_id=form_id,
        submitted_by=data.submitted_by
    )

    database.add(submission)

    database.flush()

    for answer_data in data.answers:

        field = form_fields.get(
            answer_data.field_id
        )

        if not field:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Campo {answer_data.field_id} "
                    "não pertence ao formulário"
                )
            )

        answer = FormAnswer(
            submission_id=submission.id,
            field_id=answer_data.field_id,
            value=answer_data.value
        )

        database.add(answer)

    database.commit()

    database.refresh(submission)

    return submission


@app.get(
    "/forms/{form_id}/submissions",
    response_model=list[SubmissionResponse]
)
def get_submissions(
    form_id: int,
    database: Session = Depends(get_database)
):

    return database.query(
        FormSubmission
    ).filter(
        FormSubmission.form_id == form_id
    ).all()