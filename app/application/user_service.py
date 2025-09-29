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

    def create_user(self, user_data: UserCreate) -> UserResponse:

        role = self.role_repo.get_by_name(user_data.role_name.value)
        if not role:
            raise ValueError(f"Role {user_data.role_name} not found")

        existing_user = self.user_repo.find_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")

        user = User(
            id=str(uuid.uuid4()),
            name=user_data.name,
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            role=role
        )

        created_user = self.user_repo.create(user)
        return UserResponse.model_validate(created_user)

    def get_user(self, user_id: str) -> Optional[UserResponse]:
        user = self.user_repo.get(user_id)
        return UserResponse.model_validate(user) if user else None

    def get_all_users(self) -> List[UserResponse]:
        users = self.user_repo.get_all()
        return [UserResponse.model_validate(user) for user in users]

    def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[UserResponse]:
        user = self.user_repo.get(user_id)
        if not user:
            return None

        role = user.role
        if user_data.role_name:
            new_role = self.role_repo.get_by_name(user_data.role_name.value)
            if not new_role:
                raise ValueError(f"Role {user_data.role_name} not found")
            role = new_role

        password_hash = hash_password(user_data.password) if user_data.password else user.password_hash

        updated_user = User(
            id=user.id,
            name=user_data.name,
            email=user_data.email,
            password_hash=password_hash,
            role=role
        )

        updated = self.user_repo.update(updated_user)
        return UserResponse.model_validate(updated)

    def patch_user(self, user_id: str, patch_data: UserPatch) -> Optional[UserResponse]:
        user = self.user_repo.get(user_id)
        if not user:
            return None

        name = patch_data.name if patch_data.name is not None else user.name
        email = patch_data.email if patch_data.email is not None else user.email
        password_hash = hash_password(patch_data.password) if patch_data.password is not None else user.password_hash
        role = user.role
        if patch_data.role_name:
            new_role = self.role_repo.get_by_name(patch_data.role_name.value)
            if not new_role:
                raise ValueError(f"Role {patch_data.role_name} not found")
            role = new_role

        patched_user = User(
            id=user.id,
            name=name,
            email=email,
            password_hash=password_hash,
            role=role
        )

        updated = self.user_repo.patch(user_id, patch_data)
        return UserResponse.model_validate(updated) if updated else None

    def delete_user(self, user_id: str, current_user: User) -> bool:
        user = self.user_repo.get(user_id)
        if not user:
            return False

        if user.id == current_user.id and current_user.role.name == "admin":
            raise ValueError("An admin user cannot delete their own account")

        self.user_repo.delete(user_id)
        return True