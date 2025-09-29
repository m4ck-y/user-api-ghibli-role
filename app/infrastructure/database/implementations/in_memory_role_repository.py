from typing import List, Optional
from app.domain.repositories.role_repository import RoleRepository
from app.domain.models.role import Role


class InMemoryRoleRepository(RoleRepository):
    def __init__(self):
        self._roles = [
            Role(id=1, name="admin", ghibli_endpoint=""),
            Role(id=2, name="films", ghibli_endpoint="/films"),
            Role(id=3, name="people", ghibli_endpoint="/people"),
            Role(id=4, name="locations", ghibli_endpoint="/locations"),
            Role(id=5, name="species", ghibli_endpoint="/species"),
            Role(id=6, name="vehicles", ghibli_endpoint="/vehicles"),
        ]
        self._roles_by_name = {role.name: role for role in self._roles}

    def get_all(self) -> List[Role]:
        return self._roles.copy()

    def get_by_name(self, name: str) -> Optional[Role]:
        return self._roles_by_name.get(name)