from typing import TypeVar, Generic, Type

from sqlalchemy import select
from sqlalchemy.orm import Session

T = TypeVar("T")

class BaseDAO(Generic[T]):

    def __init__(self, database: Session, model: Type[T]):
        self.database = database
        self.model = model

    def create(self, obj: T) -> T:
        self.database.add(obj)
        self.database.commit()
        self.database.refresh(obj)
        return obj

    def update(self, obj: T) -> T:
        self.database.add(obj)
        self.database.commit()
        self.database.refresh(obj)
        return obj

    def find_all(self) -> list[T]:
        stmt = select(self.model)
        return list(self.database.scalars(stmt).all())

    def find_by_id(self, obj_id: int) -> T:
        stmt = select(self.model).where(self.model.id == obj_id)
        return self.database.scalar(stmt)


    def find_by_name(self, obj_name: str) -> T:
        stmt = select(self.model).where(self.model.name == obj_name)
        return self.database.scalar(stmt)

    def delete(self, obj: T) -> None:
        self.database.delete(obj)
        self.database.commit()

    def rollback(self) -> None:
        self.database.rollback()