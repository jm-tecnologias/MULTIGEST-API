from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette import status

from company.model import CompanyResponse, CompanyCreate, CompanyUpdate
from company.service import CompanyService
from utils.database import get_database

company_router = APIRouter(prefix="/company", tags=["Companies"])

def get_company_service(database: Session = Depends(get_database)) -> CompanyService:
    return CompanyService(database)

@company_router.post("/register", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(company: CompanyCreate, service: CompanyService = Depends(get_company_service)) ->CompanyResponse:
    return service.create(company)

@company_router.get("/find-all", response_model=list[CompanyResponse], status_code=status.HTTP_200_OK)
async def find_all(skip: int = Query(default=0, ge=0),
                   limit: int = Query(default=100, ge=1, le=500),
                   service: CompanyService = Depends(get_company_service)) -> list[CompanyResponse]:
    return service.find_all(skip, limit)

@company_router.patch("/update/{company_id}", response_model=CompanyResponse, status_code=status.HTTP_200_OK)
async def update_company(company_id: int, company: CompanyUpdate, service: CompanyService = Depends(get_company_service)) -> CompanyResponse:
    return service.update(company_id, company)
