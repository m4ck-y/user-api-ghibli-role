from fastapi import APIRouter, Depends, Request
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.schemas.role import RoleResponse
from app.infrastructure.database.implementations.sqlalchemy_role_repository import SQLAlchemyRoleRepository
from app.infrastructure.database.session import get_db
from app.infrastructure.api.dependencies.auth import get_current_admin_user

def role_user_key_func(request: Request) -> str:
    from app.infrastructure.api.dependencies.auth import verify_token
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return get_remote_address(request)
    try:
        payload = verify_token(token, lambda: Exception())
        return str(payload.user_id)
    except:
        return get_remote_address(request)

role_limiter = Limiter(key_func=role_user_key_func)

router = APIRouter()

def get_role_repository(session: AsyncSession = Depends(get_db)):
    return SQLAlchemyRoleRepository(session)

@router.get("/roles", response_model=List[RoleResponse], tags=["admin"])
@role_limiter.limit("10/minute")
async def get_all_roles(
    request: Request,
    repo = Depends(get_role_repository),
    current_user = Depends(get_current_admin_user)
):
    roles = await repo.get_all()
    return [RoleResponse(id=role.id, name=role.name, ghibli_endpoint=role.ghibli_endpoint) for role in roles]