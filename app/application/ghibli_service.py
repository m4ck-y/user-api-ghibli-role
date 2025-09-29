import httpx
from typing import Dict, Any
from app.domain.models.user import User


class GhibliService:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=10.0)

    async def get_all_resources(self, user: User) -> Dict[str, Any]:
        if user.role.name == "admin":
            raise ValueError("Admin users cannot access Ghibli resources through this endpoint")

        if not user.role.ghibli_endpoint:
            raise ValueError("User role has no Ghibli endpoint configured")

        async with self.client as client:
            response = await client.get(user.role.ghibli_endpoint)
            response.raise_for_status()
            return response.json()

    async def get_resource_by_id(self, user: User, resource_id: str) -> Dict[str, Any]:
        if user.role.name == "admin":
            raise ValueError("Admin users cannot access Ghibli resources through this endpoint")

        if not user.role.ghibli_endpoint:
            raise ValueError("User role has no Ghibli endpoint configured")

        url = f"{user.role.ghibli_endpoint}/{resource_id}"

        async with self.client as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()