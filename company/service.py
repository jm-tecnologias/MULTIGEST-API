from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from dao import CompanyDAO
from model import CompanyCreate, CompanyResponse
from utils.schema import CompanySchema


class CompanyService:
    def __init__(self, database: Session):
        self.dao = CompanyDAO(database)

    def create(self, company: CompanyCreate) -> CompanyResponse:
        existing_company = self.dao.find_by_name(company.name)
        if existing_company:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Company already exists")
        new_company = CompanySchema(
            name=company.name,
            reson=company.reson,
            nuit=company.nuit,
            description=company.description,
            deleted_status=company.deleted_status,
        )
        return self.dao.create(new_company)

    def find_all(self):
        self.dao.find_all()



# from utils.database import SessionLocal
# database = SessionLocal()
# try:
#     service = CompanyService(database)
#     company_data = CompanyCreate(
#         name="JM Tech",
#         description="Empresa de soluções tecnológicas"
#     )
#     company = service.create(company_data)
#     print("Empresa criada:")
#     print("ID:", company.id)
#     print("Nome:", company.name)
#     print("Descrição:", company.description)
# finally:
#     database.close()

