from fastapi import APIRouter, Depends
from typing import List
from app.domain.schemas.role import RoleResponse
from app.infrastructure.database.implementations.in_memory_role_repository import InMemoryRoleRepository

router = APIRouter()

def get_role_repository():
    return InMemoryRoleRepository()

@router.get("/roles", response_model=List[RoleResponse])
def get_all_roles(repo = Depends(get_role_repository)):
    roles = repo.get_all()
    return [RoleResponse.model_validate(role) for role in roles]