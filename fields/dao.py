from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.schema import EntityFieldSchema
from utils.baseDao import BaseDAO

class EntityFieldDAO(BaseDAO[EntityFieldSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=EntityFieldSchema
        )
    def find_by_label_and_entity(self, label: str, entity_id: int):
        stmt = select(self.model).where(self.model.label == label and self.model.entity_id == entity_id)
        return self.database.scalar(stmt)
