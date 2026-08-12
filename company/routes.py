from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from company.model import CompanyResponse, CompanyDetailsResponse, CompanyCreate
from company.service import CompanyService
from utils.database import get_database

company_router = APIRouter(prefix="/company", tags=["Companies"])

def get_company_service(database: Session = Depends(get_database)) -> CompanyService:
    return CompanyService(database)

@company_router.post("/register", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company(company: CompanyCreate, service: CompanyService = Depends(get_company_service)) ->CompanyResponse:
    return service.create(company)