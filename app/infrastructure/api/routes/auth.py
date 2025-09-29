from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.session import get_db
from app.infrastructure.database.implementations.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.application.auth_service import AuthService
from app.domain.schemas.auth import TokenResponse

router = APIRouter()


def get_auth_service(session: AsyncSession = Depends(get_db)):
    user_repo = SQLAlchemyUserRepository(session)
    return AuthService(user_repo)


@router.post("/auth/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.authenticate_user(form_data)