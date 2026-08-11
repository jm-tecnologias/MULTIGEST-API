from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from utils.schema import EntityRecordSchema, EntityAnswerSchema
from utils.baseDao import BaseDAO



class EntityRecordDAO(BaseDAO[EntityRecordSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=EntityRecordSchema
        )

    def find_entities_records_by_entity_id(self,entity_id:int) -> list[EntityRecordSchema]:
        stmt = select(EntityRecordSchema).where(EntityRecordSchema.entity_id == entity_id).options(
            selectinload(EntityRecordSchema.entities_answers).selectinload(
                EntityAnswerSchema.entity_field
            )
        ).order_by(
            EntityRecordSchema.id.asc()
        )
        return list(self.database.scalars(stmt).all())