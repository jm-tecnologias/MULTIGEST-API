from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
    DateTime,
    JSON,
)

from sqlalchemy.orm import relationship

from database import Base

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150),nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow)
    forms = relationship(
        "Form",
        back_populates="company",
        cascade="all, delete-orphan"
    )


class Form(Base):
    __tablename__ = "forms"

    id = Column(Integer,primary_key=True,index=True)
    company_id = Column(Integer,ForeignKey("companies.id"),nullable=False)
    name = Column(String(150),nullable=False)
    description = Column(Text,nullable=True)
    active = Column(Boolean,default=True)
    created_at = Column(DateTime,default=datetime.utcnow)
    company = relationship(
"Company",
        back_populates="forms"
    )
    fields = relationship(
        "FormField",
        back_populates="form",
        cascade="all, delete-orphan",
        order_by="FormField.position"
    )
    submissions = relationship(
        "FormSubmission",
        back_populates="form",
        cascade="all, delete-orphan"
    )


class FormField(Base):
    __tablename__ = "form_fields"

    id = Column(Integer,primary_key=True,index=True)
    form_id = Column(Integer,ForeignKey("forms.id"),nullable=False)
    label = Column(String(200),nullable=False)
    field_type = Column(String(50),nullable=False)
    required = Column(Boolean,default=False)
    position = Column(Integer,default=0)
    weight = Column(Integer,nullable=True)
    config = Column(JSON,nullable=True)
    form = relationship(
        "Form",
        back_populates="fields"
    )
    answers = relationship(
        "FormAnswer",
        back_populates="field"
    )


class FormSubmission(Base):
    __tablename__ = "form_submissions"

    id = Column(Integer,primary_key=True,index=True)
    form_id = Column(Integer,ForeignKey("forms.id"),nullable=False)
    submitted_by = Column(String(150),nullable=True)
    created_at = Column(DateTime,default=datetime.utcnow)
    form = relationship(
        "Form",
        back_populates="submissions"
    )
    answers = relationship(
        "FormAnswer",
        back_populates="submission",
        cascade="all, delete-orphan"
    )


class FormAnswer(Base):
    __tablename__ = "form_answers"

    id = Column(Integer,primary_key=True,index=True)
    submission_id = Column(Integer,ForeignKey("form_submissions.id"),nullable=False)
    field_id = Column(Integer, ForeignKey("form_fields.id"), nullable=False)
    value = Column(JSON,nullable=True)
    submission = relationship(
        "FormSubmission",
        back_populates="answers")
    field = relationship(
        "FormField",
        back_populates="answers"
    )