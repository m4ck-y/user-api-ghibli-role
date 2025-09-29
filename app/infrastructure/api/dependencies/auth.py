from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.session import get_db
from app.infrastructure.database.implementations.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.application.auth import verify_token
from app.domain.models.user import User
from app.domain.schemas.auth import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user_optional(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)) -> Optional[User]:
    try:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        token_data = verify_token(token, credentials_exception)

        user_repo = SQLAlchemyUserRepository(session)
        user = await user_repo.get(token_data.user_id)
        if user is None:
            raise credentials_exception
        return user
    except HTTPException:
        return None


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)

    user_repo = SQLAlchemyUserRepository(session)
    user = await user_repo.get(token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


async def get_current_normal_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role.name == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin users cannot access /me endpoints"
        )
    return current_user