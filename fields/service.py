from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from entity.dao import EntityDAO
from fields.dao import EntityFieldDAO
from fields.model import EntityFieldCreate, EntityFieldResponse
from utils.schema import EntityFieldSchema



class EntityFieldService:
    def __init__(self, database: Session):
        self.entity_field_dao = EntityFieldDAO(database)
        self.entity_dao = EntityDAO(database)

    def create(self, field: EntityFieldCreate) -> EntityFieldResponse:
        entity = self.entity_dao.find_by_id(field.entity_id)
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found")
        new_field = EntityFieldSchema(
            label=field.label,
            field_type=field.field_type,
            required=field.required,
            entity_id=field.entity_id,
            config=field.config,
            deleted_status = field.deleted_status
        )
        return self.entity_field_dao.create(new_field)



# from utils.database import SessionLocal
# database = SessionLocal()
# try:
#     service = EntityFieldService(database)
#     data = EntityFieldCreate(
#         label="Nome",
#         field_type="text",
#         required=True,
#         entity_id=1,
#         config={
#             "min":3,
#             "max":20
#         },
#         deleted_status=False
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


