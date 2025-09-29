from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.schemas.role import RoleResponse
from app.infrastructure.database.implementations.sqlalchemy_role_repository import SQLAlchemyRoleRepository
from app.infrastructure.database.session import get_db
from app.infrastructure.api.dependencies.auth import get_current_admin_user

router = APIRouter()

def get_role_repository(session: AsyncSession = Depends(get_db)):
    return SQLAlchemyRoleRepository(session)

@router.get("/roles", response_model=List[RoleResponse], tags=["admin"])
async def get_all_roles(
    repo = Depends(get_role_repository),
    current_user = Depends(get_current_admin_user)
):
    roles = await repo.get_all()
    return [RoleResponse(id=role.id, name=role.name, ghibli_endpoint=role.ghibli_endpoint) for role in roles]