from sqlalchemy.orm import Session
from utils.schema import CompanySchema
from utils.baseDao import BaseDAO


class CompanyDAO(BaseDAO[CompanySchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=CompanySchema
        )