from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from fields.model import EntityFieldResponse, EntityFieldCreate
from fields.service import EntityFieldService
from utils.database import get_database

field_router = APIRouter(prefix="/field", tags=["Fields"])

def get_field_service(database: Session = Depends(get_database)) ->EntityFieldService:
    return EntityFieldService(database)

@field_router.post("/register", response_model=EntityFieldResponse, status_code=status.HTTP_201_CREATED)
async def create_field(field: EntityFieldCreate, service: EntityFieldService = Depends(get_field_service)) -> EntityFieldResponse:
    return service.create(field)