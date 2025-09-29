from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.role import Role


class RoleRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Role]:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Role]:
        pass