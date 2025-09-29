from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.domain.repositories.user_repository import UserRepository
from app.domain.schemas.auth import TokenResponse
from app.application.utils import verify_password
from app.application.auth import create_access_token


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def authenticate_user(self, form_data: OAuth2PasswordRequestForm) -> TokenResponse:
        user = await self.user_repo.find_by_email(form_data.username)
        if not user:
            raise HTTPException(status_code=401, detail="Incorrect email or password")

        if not verify_password(form_data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Incorrect email or password")

        access_token = create_access_token(
            data={"user_id": user.id, "role_name": user.role.name}
        )
        return TokenResponse(access_token=access_token)