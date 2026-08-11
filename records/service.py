from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from dao import EntityRecordDAO
from entity.dao import EntityDAO
from company.dao import CompanyDAO
from model import EntityRecordCreate, EntityRecordResponse
from utils.schema import EntityRecordSchema



class EntityRecordService:
    def __init__(self, database: Session):
        self.record_dao = EntityRecordDAO(database)
        self.entity_dao = EntityDAO(database)
        self.company_dao = CompanyDAO(database)

    def create(self, record: EntityRecordCreate) -> EntityRecordResponse:
        entity = self.entity_dao.find_by_id(record.entity_id)
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found")
        company = self.company_dao.find_by_id(record.company_id)
        if not company:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Company not found")
        if company.id != entity.company_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company ID does not match entity Foreign Key")

        new_record = EntityRecordSchema(
            entity_id=record.entity_id,
            company_id=entity.company_id
        )
        return self.record_dao.create(new_record)

    # def find_records_by_entity_id(self, entity_id: int) -> list[EntityRecordResponse]:
    def find_records_by_entity_id(self, entity_id: int) -> list[dict[str, str | None | int | Any]]:
        entity = self.entity_dao.find_by_id(entity_id)

        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found")

        entity_records = self.record_dao.find_entities_records_by_entity_id(entity_id)

        if not entity_records:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity without records")

        result_records = [
            {
                "id": entity.id,
                "name": entity.name,
                "description": entity.description,
                "company_id": entity.company_id,
                "created_at": entity.created_at,
                "updated_at": entity.updated_at,
            },
        ]
        for record in entity_records:
            data = {}
            for answer in record.entities_answers:
                field = answer.entity_field
                data[field.label] = answer.value
            result_records.append(
                {
                    "id": record.id,
                    "created_at": record.created_at,
                    "updated_at": record.updated_at,
                    "data": data
                }
            )

        return result_records




# from utils.database import SessionLocal
# database = SessionLocal()
#
# try:
#     service = EntityRecordService(database)
#
#     records = service.find_records_by_entity_id(1)
#     print("Records: ",records)
# finally:
#     database.close()

