from dataclasses import dataclass
from typing import Optional
from app.domain.models.role import Role


@dataclass
class User:
    id: str
    name: str
    email: str
    password_hash: str
    role: Role

    def can_delete_self(self) -> bool:
        return self.role.name != "admin"