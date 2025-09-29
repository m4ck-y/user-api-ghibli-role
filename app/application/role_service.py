from typing import List
from app.domain.repositories.role_repository import RoleRepository
from app.domain.models.role import Role


class RoleService:
    def __init__(self, role_repo: RoleRepository):
        self.role_repo = role_repo

    def get_all_roles(self) -> List[Role]:
        return self.role_repo.get_all()

    def get_role_by_name(self, name: str) -> Role:
        role = self.role_repo.get_by_name(name)
        if not role:
            raise ValueError(f"Role {name} not found")
        return role