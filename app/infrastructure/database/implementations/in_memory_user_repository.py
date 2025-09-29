from typing import List, Optional
from app.domain.repositories.user_repository import UserRepository
from app.domain.models.user import User
from app.domain.models.role import Role
from app.domain.schemas.user import UserCreate


class InMemoryUserRepository(UserRepository):
    _id_counter = 1

    def __init__(self):
        self._users: List[User] = []

    def create(self, user_data: UserCreate, role: Role) -> User:
        user = User(
            id=None,
            name=user_data.name,
            email=user_data.email,
            password_hash=user_data.password,
            role=role
        )

        user_id = InMemoryUserRepository._id_counter
        InMemoryUserRepository._id_counter += 1
        user.id = user_id

        self._users.append(user)
        return user

    def get(self, user_id: int) -> Optional[User]:
        for user in self._users:
            if user.id == user_id:
                return user
        return None

    def find_by_email(self, email: str) -> Optional[User]:
        for user in self._users:
            if user.email == email:
                return user
        return None

    def get_all(self) -> List[User]:
        return self._users.copy()

    def update(self, user: User) -> User:
        for i, existing_user in enumerate(self._users):
            if existing_user.id == user.id:
                if existing_user.email != user.email:
                    for other_user in self._users:
                        if other_user.id != user.id and other_user.email == user.email:
                            raise ValueError(f"Email {user.email} already in use")
                self._users[i] = user
                return user
        raise ValueError(f"User with id {user.id} not found")

    def patch(self, user_id: int, patch_data) -> Optional[User]:
        user = self.get(user_id)
        if not user:
            return None

        if patch_data.name is not None:
            user.name = patch_data.name
        if patch_data.email is not None:
            if patch_data.email != user.email:
                for other_user in self._users:
                    if other_user.id != user_id and other_user.email == patch_data.email:
                        raise ValueError(f"Email {patch_data.email} already in use")
            user.email = patch_data.email
        if patch_data.password is not None:
            user.password_hash = patch_data.password

        return user

    def delete(self, user_id: int) -> None:
        for i, user in enumerate(self._users):
            if user.id == user_id:
                self._users.pop(i)
                return