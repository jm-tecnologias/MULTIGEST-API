from sqlalchemy.orm import Session
from utils.schema import EntityAnswerSchema
from utils.baseDao import BaseDAO



class EntityAnswerDAO(BaseDAO[EntityAnswerSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=EntityAnswerSchema
        )