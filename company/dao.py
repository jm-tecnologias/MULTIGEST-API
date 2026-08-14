from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.schema import CompanySchema
from utils.baseDao import BaseDAO


class CompanyDAO(BaseDAO[CompanySchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=CompanySchema
        )

    def find_all_companies(self, skip:int = 0, limit: int = 100) -> list[CompanySchema]:
        stmt = select(CompanySchema).offset(skip).limit(limit).order_by(CompanySchema.name)
        return list(self.database.scalars(stmt).all())
