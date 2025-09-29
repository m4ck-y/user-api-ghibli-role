from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.user import User
from app.domain.schemas.user import UserPatch


class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def get(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass

    @abstractmethod
    def patch(self, user_id: str, patch_data: UserPatch) -> Optional[User]:
        pass

    @abstractmethod
    def delete(self, user_id: str) -> None:
        pass