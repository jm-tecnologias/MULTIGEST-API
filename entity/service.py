import json

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from dao import EntityDAO
from company.dao import  CompanyDAO
from model import EntityCreate, EntityResponse
from utils.schema import EntitySchema



class EntityService:
    def __init__(self, database: Session):
        self.entity_dao = EntityDAO(database)
        self.company_dao = CompanyDAO(database)

    def create(self, entity: EntityCreate) -> EntityResponse:
        company = self.company_dao.find_by_id(entity.company_id)
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        new_entity= EntitySchema(
            name=entity.name,
            company_id=entity.company_id,
            description=entity.description,
        )
        return self.entity_dao.create(new_entity)

    def find_by_company_id(self, company_id: int) -> list[EntityResponse]:
        return self.entity_dao.find_by_company_id(company_id)






from utils.database import SessionLocal
database = SessionLocal()
# try:
#     service = EntityService(database)
#     entity_data = EntityCreate(
#         name="Funcionario",
#         description="Func. da empresa JM",
#         company_id=1
#     )
#     entity = service.create(entity_data)
#     print("Entity Created:")
#     print("ID: ", entity.id)
#     print("Name: ", entity.name)
#     print("Description: ", entity.description)
#     print("Company ID: ", entity.company_id)
# finally:
#     database.close()

# try:
#     service = EntityService(database)
#
#     entities = service.find_by_company_id(1)
#
#     for entity in entities:
#         print("Entity Created:")
#         print("ID: ", entity.id)
#         print("Name: ", entity.name)
#         print("Description: ", entity.description)
#         print("Company ID: ", entity.company_id)
#         print("_____________________________________________________________")
# finally:
#     database.close()

