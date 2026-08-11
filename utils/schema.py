from typing import Any

from sqlalchemy.orm import relationship
from utils.base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON


class CompanySchema(Base):
    __tablename__ = "company"
    id = Column("id",Integer, primary_key=True, index=True)
    name = Column("name",String, nullable=False)
    description = Column("description",String, nullable=True)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    entities =  relationship(
        "EntitySchema",
        back_populates="company",
        order_by="EntitySchema.name.asc()",
        cascade="all, delete-orphan",
    )
    entities_records = relationship(
        "EntityRecordSchema",
        back_populates="company",
        order_by="EntityRecordSchema.id.asc()",
        cascade="all, delete-orphan",
    )


    def __init__(self, name:str, description: str | None = None):
        self.name = name
        self.description = description

class EntitySchema(Base):
    __tablename__ = "entity"
    id = Column("id",Integer, primary_key=True)
    name = Column("name",String, nullable=False)
    description = Column("description",String, nullable=True)
    company_id = Column("company_id",Integer, ForeignKey("company.id"), nullable=False)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    entities_records = relationship(
        "EntityRecordSchema",
        back_populates="entity",
        order_by="EntityRecordSchema.id.asc()",
        cascade="all, delete-orphan",
    )
    entities_fields = relationship(
        "EntityFieldSchema",
        back_populates="entity",
        order_by="EntityFieldSchema.label.asc()",
        cascade="all, delete-orphan",
    )
    company = relationship(
        "CompanySchema",
        back_populates="entities",
    )

    def __init__(self, name:str, company_id:int, description:str | None = None):
        self.name = name
        self.description = description
        self.company_id = company_id

class EntityFieldSchema(Base):
    __tablename__ = "entity_field"
    id = Column("id",Integer, primary_key=True)
    label = Column("label",String, nullable=False)
    field_type = Column("field_type",String, nullable=False)
    required = Column("required",Boolean, nullable=False, default=False)
    config = Column(JSON, nullable=True)
    entity_id = Column("entity_id", Integer, ForeignKey("entity.id"), nullable=False)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    entities_answers = relationship(
        "EntityAnswerSchema",
        back_populates="entity_field",
        order_by="EntityAnswerSchema.id.asc()",
        cascade="all, delete-orphan",
    )
    entity = relationship(
        "EntitySchema",
        back_populates="entities_fields",
    )

    def __init__(self,label: str, field_type:str, entity_id:int, required:bool = False, config:dict[str, Any] | None = None):
        self.label = label
        self.field_type = field_type
        self.required = required
        self.config = config
        self.entity_id = entity_id

class EntityRecordSchema(Base):
    __tablename__ = "entity_record"
    id = Column("id",Integer, primary_key=True)
    entity_id = Column("entity_id",Integer, ForeignKey("entity.id"), nullable=False)
    company_id = Column("company_id",Integer, ForeignKey("company.id"), nullable=False)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    entities_answers = relationship(
        "EntityAnswerSchema",
        back_populates="entity_record",
        order_by="EntityAnswerSchema.id.asc()",
        cascade="all, delete-orphan",
    )
    entity = relationship(
        "EntitySchema",
        back_populates="entities_records",
    )
    company = relationship(
        "CompanySchema",
        back_populates="entities_records",
    )

    def __init__(self, entity_id, company_id):
        self.entity_id =  entity_id
        self.company_id = company_id

class EntityAnswerSchema(Base):
    __tablename__ = "entity_answer"

    id = Column("id",Integer, primary_key=True)
    entity_record_id = Column("entity_record_id",Integer, ForeignKey("entity_record.id"), nullable=False)
    entity_field_id = Column("entity_field_id",Integer, ForeignKey("entity_field.id"), nullable=False)
    value = Column("value",JSON, nullable=True)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    entity_field = relationship(
        "EntityFieldSchema",
        back_populates="entities_answers",
    )
    entity_record = relationship(
        "EntityRecordSchema",
        back_populates="entities_answers",
    )

    def __init__(self, entity_record_id:int, entity_field_id:int, value):
        self.entity_record_id = entity_record_id
        self.entity_field_id = entity_field_id
        self.value = value