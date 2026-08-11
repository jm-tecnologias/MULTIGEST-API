from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from entity.dao import EntityDAO
from dao import EntityFieldDAO
from model import EntityFieldCreate, EntityFieldResponse
from utils.schema import EntityFieldSchema



class EntityFieldService:
    def __init__(self, database: Session):
        self.entity_field_dao = EntityFieldDAO(database)
        self.entity_dao = EntityDAO(database)

    def create(self, entity_field: EntityFieldCreate) -> EntityFieldResponse:
        entity = self.entity_dao.find_by_id(entity_field.entity_id)
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found")
        new_field = EntityFieldSchema(
            label=entity_field.label,
            field_type=entity_field.field_type,
            required=entity_field.required,
            entity_id=entity_field.entity_id,
            config=entity_field.config,
        )
        return self.entity_field_dao.create(new_field)



from utils.database import SessionLocal
database = SessionLocal()


# try:
#     service = EntityFieldService(database)
#     data = EntityFieldCreate(
#         label="Apelido",
#         field_type="text",
#         required=True,
#         entity_id=1,
#         config={
#             "min":3,
#             "max":20
#         }
#     )
#     result = service.create(data)
#     print("ID:", result.id)
#     print("Label:", result.label)
#     print("Tipo:", result.field_type)
#     print("Required:", result.required)
#     print("Config:", result.config)
#     print("Entity ID:", result.entity_id)
#
# finally:
#     database.close()


