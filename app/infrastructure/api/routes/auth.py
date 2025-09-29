from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.session import get_db
from app.infrastructure.database.implementations.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.application.auth_service import AuthService
from app.domain.schemas.auth import TokenResponse

router = APIRouter()

auth_limiter = Limiter(key_func=get_remote_address)


def get_auth_service(session: AsyncSession = Depends(get_db)):
    user_repo = SQLAlchemyUserRepository(session)
    return AuthService(user_repo)


@router.post("/auth/login", response_model=TokenResponse, tags=["public"])
@auth_limiter.limit("5/minute")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.authenticate_user(form_data)