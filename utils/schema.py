from typing import Any
from sqlalchemy.orm import relationship
from utils.base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON


class CompanySchema(Base):
    __tablename__ = "company"
    id = Column("id",Integer, primary_key=True, index=True)
    name = Column("name",String, nullable=False)
    reson = Column("reson", String, nullable=True)
    nuit = Column("nuit", Integer, nullable=True)
    description = Column("description",String, nullable=True)
    deleted_status = Column("deleted_status", Boolean, nullable=False, default=False)
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

    def __init__(self, name:str, reson:str | None, nuit:int | None, description: str | None,  deleted_status: bool | None):
        self.name = name
        self.reson = reson
        self.nuit = nuit
        self.description = description
        self.deleted_status = deleted_status


class AddressSchema(Base):
    __tablename__ = "address"

    id = Column("id", Integer, primary_key=True)
    province = Column("province", String, nullable=False)
    city = Column("city", String, nullable=False)
    neighborhood = Column("neighborhood", String, nullable=True)
    avenue = Column("avenue", String, nullable=True)
    number = Column("number", Integer, nullable=True)
    postal_code = Column("postal_code", String, nullable=True)
    company_id = Column("company_id", Integer, ForeignKey("company.id"), nullable=False)
    deleted_status = Column("deleted_Status", Boolean, nullable=False, default=False)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, province:str, city:str, neighborhood:str | None, avenue:str | None,
                 number:int | None, postal_code: int | None,
                 company_id: int, deleted_status: bool | None):
        self.province = province
        self.city = city
        self.neighborhood = neighborhood
        self.avenue = avenue
        self.number = number
        self.postal_code = postal_code
        self.company_id = company_id
        self.deleted_status = deleted_status

class ContactShema(Base):
    __tablename__ = "contact"
    id = Column("id", Integer, primary_key=True)
    phone = Column("phone", String, nullable=False)
    email = Column("email", String, nullable=True)
    website = Column("website", String, nullable=True)
    company_id = Column("company_id", Integer, ForeignKey("company.id"), nullable=False)
    deleted_status = Column("deleted_status", Boolean, nullable=False, default=False)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, phone:str, email:str | None, website:str | None, company_id:int,
                 deleted_status:bool | False):
        self.phone = phone
        self.email = email
        self.website = website
        self.company_id = company_id
        self.deleted_status = deleted_status

class EntitySchema(Base):
    __tablename__ = "entity"
    id = Column("id",Integer, primary_key=True)
    name = Column("name",String, nullable=False)
    description = Column("description",String, nullable=True)
    company_id = Column("company_id",Integer, ForeignKey("company.id"), nullable=False)
    deleted_status = Column("deleted_status", Boolean, nullable=False, default=False)
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

    def __init__(self, name:str, company_id:int, description:str | None , deleted_status:bool | False):
        self.name = name
        self.description = description
        self.company_id = company_id
        self.deleted_status = deleted_status

class EntityFieldSchema(Base):
    __tablename__ = "entity_field"
    id = Column("id",Integer, primary_key=True)
    label = Column("label",String, nullable=False)
    field_type = Column("field_type",String, nullable=False)
    required = Column("required",Boolean, nullable=False, default=False)
    config = Column("config", JSON, nullable=True)
    entity_id = Column("entity_id", Integer, ForeignKey("entity.id"), nullable=False)
    deleted_status = Column("deleted_status", Boolean, nullable=False, default=False)
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

    def __init__(self,label: str, field_type:str, entity_id:int, required:bool | False, config:dict[str, Any] | None,
                 deleted_status:bool | False):
        self.label = label
        self.field_type = field_type
        self.required = required
        self.config = config
        self.entity_id = entity_id
        self.deleted_status = deleted_status

class EntityRecordSchema(Base):
    __tablename__ = "entity_record"
    id = Column("id",Integer, primary_key=True)
    entity_id = Column("entity_id",Integer, ForeignKey("entity.id"), nullable=False)
    company_id = Column("company_id",Integer, ForeignKey("company.id"), nullable=False)
    deleted_status = Column("deleted_status", Boolean, nullable=False, default=False)
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

    def __init__(self, entity_id, company_id, deleted_status:bool | False):
        self.entity_id =  entity_id
        self.company_id = company_id
        self.deleted_status = deleted_status

class EntityAnswerSchema(Base):
    __tablename__ = "entity_answer"

    id = Column("id",Integer, primary_key=True)
    entity_record_id = Column("entity_record_id",Integer, ForeignKey("entity_record.id"), nullable=False)
    entity_field_id = Column("entity_field_id",Integer, ForeignKey("entity_field.id"), nullable=False)
    value = Column("value",JSON, nullable=True)
    deleted_status = Column("deleted_status", Boolean, nullable=False, default=False)
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

    def __init__(self, entity_record_id:int, entity_field_id:int, value, deleted_status:bool | False):
        self.entity_record_id = entity_record_id
        self.entity_field_id = entity_field_id
        self.value = value
        self.deleted_status = deleted_status