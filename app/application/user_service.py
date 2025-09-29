import uuid
from typing import List, Optional
from app.domain.repositories.user_repository import UserRepository
from app.domain.repositories.role_repository import RoleRepository
from app.domain.models.user import User
from app.domain.models.role import Role
from app.domain.schemas.user import UserCreate, UserUpdate, UserPatch, UserResponse
from app.domain.enums.role_type import RoleType
from app.application.utils import hash_password


class UserService:
    def __init__(self, user_repo: UserRepository, role_repo: RoleRepository):
        self.user_repo = user_repo
        self.role_repo = role_repo

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        existing_user = await self.user_repo.find_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")

        role = await self.role_repo.get_by_name(user_data.role_name.value)
        if not role:
            raise ValueError(f"Role {user_data.role_name} not found")

        user_data.password = hash_password(user_data.password)

        created_user = await self.user_repo.create(user_data, role)
        return UserResponse(
            id=created_user.id,
            name=created_user.name,
            email=created_user.email,
            role_name=created_user.role.name
        )
    async def get_user(self, user_id: int) -> Optional[UserResponse]:
        user = await self.user_repo.get(user_id)
        if not user:
            return None
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            role_name=user.role.name
        )

    async def get_all_users(self) -> List[UserResponse]:
        users = await self.user_repo.get_all()
        return [
            UserResponse(
                id=user.id,
                name=user.name,
                email=user.email,
                role_name=user.role.name
            )
            for user in users
        ]

    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        user = await self.user_repo.get(user_id)
        if not user:
            return None

        role = user.role
        if user_data.role_name:
            role = await self.role_repo.get_by_name(user_data.role_name.value)
            if not role:
                raise ValueError(f"Role {user_data.role_name} not found")

        password_hash = hash_password(user_data.password) if user_data.password else user.password_hash

        updated_user = User(
            id=user.id,
            name=user_data.name,
            email=user_data.email,
            password_hash=password_hash,
            role=role
        )

        updated = await self.user_repo.update(updated_user)
        return UserResponse(
            id=updated.id,
            name=updated.name,
            email=updated.email,
            role_name=updated.role.name
        )

    async def patch_user(self, user_id: int, patch_data: UserPatch) -> Optional[UserResponse]:
        user = await self.user_repo.get(user_id)
        if not user:
            return None

        name = patch_data.name if patch_data.name is not None else user.name
        email = patch_data.email if patch_data.email is not None else user.email
        password_hash = hash_password(patch_data.password) if patch_data.password is not None else user.password_hash
        role = user.role
        if patch_data.role_name:
            role = await self.role_repo.get_by_name(patch_data.role_name.value)
            if not role:
                raise ValueError(f"Role {patch_data.role_name} not found")

        patched_user = User(
            id=user.id,
            name=name,
            email=email,
            password_hash=password_hash,
            role=role
        )

        updated = await self.user_repo.update(patched_user)
        return UserResponse(
            id=updated.id,
            name=updated.name,
            email=updated.email,
            role_name=updated.role.name
        )

    async def delete_user(self, user_id: int, current_user: Optional[User]) -> bool:
        user = await self.user_repo.get(user_id)
        if not user:
            return False

        if current_user and user.id == current_user.id and current_user.role.name == "admin":
            raise ValueError("An admin user cannot delete their own account")

        await self.user_repo.delete(user_id)
        return True