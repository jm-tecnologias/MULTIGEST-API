from contextlib import asynccontextmanager
from fastapi import FastAPI
from utils.database import create_database_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database_tables()
    yield

app = FastAPI(title="Multi-Gest", version="1.0.0", lifespan=lifespan)

@app.get("/")
def root():
    return {"Hello": "World"}


