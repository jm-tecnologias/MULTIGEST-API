from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.schema import EntitySchema
from utils.baseDao import BaseDAO


class EntityDAO(BaseDAO[EntitySchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=EntitySchema
        )

    def find_by_company_id(self,company_id:int) -> list[EntitySchema]:
        stmt = select(EntitySchema).where(EntitySchema.company_id == company_id).order_by(EntitySchema.name)
        return list(self.database.scalars(stmt).all())

    def check_entity_in_company(self,entity_name: str,company_id:int) -> Any | None:
        stmt = select(EntitySchema).where(EntitySchema.name == entity_name).where(EntitySchema.company_id == company_id)
        return self.database.scalar(stmt)