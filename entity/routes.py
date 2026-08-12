from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from entity.model import EntityResponse, EntityCreate
from entity.service import EntityService
from utils.database import get_database

entity_router = APIRouter(prefix="/entity", tags=["Entities"])

def get_entity_service(database: Session = Depends(get_database)) -> EntityService:
    return EntityService(database)

@entity_router.post("/register", response_model=EntityResponse)
def create_entity(entity: EntityCreate, service: EntityService = Depends(get_entity_service)) -> EntityResponse:
    return service.create(entity)

