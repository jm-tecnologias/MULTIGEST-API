from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from company.dao import CompanyDAO
from company.model import CompanyCreate, CompanyResponse, CompanyDetailsResponse, CompanyUpdate
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

    def update(self, company_id:int, company_data: CompanyUpdate) -> CompanyResponse:
        company = self.dao.find_by_id(company_id)
        updated_data = company_data.model_dump(exclude_unset=True)

        for field, value in updated_data.items():
            setattr(company, field, value)

        try:
            return self.dao.update(company)
        except InterruptedError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Was not possible to update company data")




    def find_all(self, skip: int = 0, limit: int = 100) -> list[CompanyResponse]:
        return self.dao.find_all_companies(skip=skip, limit=limit)



from utils.database import SessionLocal
database = SessionLocal()
# try:
#     service = CompanyService(database)
#     company_data = CompanyCreate(
#         name="MJunior&Mula Tecnologias",
#         reson="JM-Tecnologias SU, LDA",
#         nuit=123456789,
#         description="Empresa de soluções tecnológicas",
#         deleted_status=True
#     )
#     company = service.create(company_data)
#     print("Empresa criada:",company)
#     # print("ID:", company.id)
#     # print("Nome:", company.name)
#     # print("Descrição:", company.description)
# finally:
#     database.close()

# try:
#     service = CompanyService(database)
#
#     companies = service.find_all(0, 100)
#     for company in companies:
#         print("Empresa: ",company)
#         print("ID:", company.id)
#         print("Nome:", company.name)
#         print("Descrição:", company.description)
# finally:
#     database.close()

# try:
#     service = CompanyService(database)
#     company_data = CompanyUpdate(
#         name="JM Tecnologias",
#         reson="JM Tecnologias SU, LDA",
#         nuit=999999999,
#         description="A Empresa de soluções tecnológicas",
#         deleted_status=False
#     )
#     company = service.update(1,company_data)
#     print("Empresa criada:",company)
#     print("ID:", company.id)
#     print("Nome:", company.name)
#     print("Descrição:", company.description)
# finally:
#     database.close()

