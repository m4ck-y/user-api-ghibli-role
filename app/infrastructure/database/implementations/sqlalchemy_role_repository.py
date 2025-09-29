from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.repositories.role_repository import RoleRepository
from app.domain.models.role import Role
from app.infrastructure.database.models.role_model import RoleModel


class SQLAlchemyRoleRepository(RoleRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_name(self, name: str) -> Optional[Role]:
        stmt = select(RoleModel).where(RoleModel.name == name)
        result = await self.session.execute(stmt)
        role_model = result.scalar_one_or_none()
        if not role_model:
            return None

        return Role(
            id=role_model.id,
            name=role_model.name,
            ghibli_endpoint=role_model.ghibli_endpoint
        )

    async def get_all(self) -> List[Role]:
        stmt = select(RoleModel)
        result = await self.session.execute(stmt)
        role_models = result.scalars().all()

        return [
            Role(
                id=role_model.id,
                name=role_model.name,
                ghibli_endpoint=role_model.ghibli_endpoint
            )
            for role_model in role_models
        ]