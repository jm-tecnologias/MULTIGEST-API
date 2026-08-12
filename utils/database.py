from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from utils.base import Base

PROJECT_ROOT = Path(__file__).parent.parent

DATABASE_DIR = PROJECT_ROOT

DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_FLE = DATABASE_DIR/"multigest.db"


DATABASE_URL = f"sqlite:///{DATABASE_FLE.as_posix()}"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={
        "check_same_thread": False
    }
)
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# Schemas do Banco de dados
from utils.schema import CompanySchema
from utils.schema import CompanySchema
from utils.schema import ContactShema
from utils.schema import EntityAnswerSchema
from utils.schema import EntitySchema
from utils.schema import EntityFieldSchema
from utils.schema import EntityRecordSchema


def get_database() -> Generator[Session, None, None]:
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


def create_database_tables() -> None:
    """
    Importa os modelos e cria as tabelas registadas.
    """
    from utils.schema import CompanySchema
    from utils.schema import CompanySchema
    from utils.schema import ContactShema
    from utils.schema import EntityAnswerSchema
    from utils.schema import EntitySchema
    from utils.schema import EntityFieldSchema
    from utils.schema import EntityRecordSchema

    # print("Tabelas registadas:", list(Base.metadata.tables.keys()))
    Base.metadata.create_all(bind=engine)
    print("Base de dados criada com sucesso.")
    # print(f"Localização: {DATABASE_FILE}")