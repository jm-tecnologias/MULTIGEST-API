from contextlib import asynccontextmanager
from fastapi import FastAPI

from entity.routes import entity_router
from utils.database import create_database_tables
from company.routes import company_router
from fields.routes import field_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database_tables()
    yield

app = FastAPI(title="Multi-Gest", version="1.0.0", lifespan=lifespan)

@app.get("/")
def root():
    return {"Hello": "World"}


app.include_router(company_router)
app.include_router(entity_router)
app.include_router(field_router)
