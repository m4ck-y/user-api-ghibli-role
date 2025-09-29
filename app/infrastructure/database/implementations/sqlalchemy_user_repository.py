from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.repositories.user_repository import UserRepository
from app.domain.models.user import User
from app.domain.models.role import Role
from app.domain.schemas.user import UserCreate
from app.infrastructure.database.models.user_model import UserModel
from app.infrastructure.database.models.role_model import RoleModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_data: UserCreate, role: Role) -> User:
        user_model = UserModel(
            name=user_data.name,
            email=user_data.email,
            password_hash=user_data.password,
            role_id=role.id
        )
        self.session.add(user_model)
        await self.session.flush()
        await self.session.commit()

        user = User(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            password_hash=user_data.password,
            role=role
        )
        return user

    async def get(self, user_id: int) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        user_model = result.scalar_one_or_none()
        if not user_model:
            return None

        role_stmt = select(RoleModel).where(RoleModel.id == user_model.role_id)
        role_result = await self.session.execute(role_stmt)
        role_model = role_result.scalar_one()

        role = Role(
            id=role_model.id,
            name=role_model.name,
            ghibli_endpoint=role_model.ghibli_endpoint
        )

        return User(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            password_hash=user_model.password_hash,
            role=role
        )

    async def find_by_email(self, email: str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        user_model = result.scalar_one_or_none()
        if not user_model:
            return None

        role_stmt = select(RoleModel).where(RoleModel.id == user_model.role_id)
        role_result = await self.session.execute(role_stmt)
        role_model = role_result.scalar_one()

        role = Role(
            id=role_model.id,
            name=role_model.name,
            ghibli_endpoint=role_model.ghibli_endpoint
        )

        return User(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            password_hash=user_model.password_hash,
            role=role
        )

    async def get_all(self) -> List[User]:
        stmt = select(UserModel)
        result = await self.session.execute(stmt)
        user_models = result.scalars().all()

        users = []
        for user_model in user_models:
            role_stmt = select(RoleModel).where(RoleModel.id == user_model.role_id)
            role_result = await self.session.execute(role_stmt)
            role_model = role_result.scalar_one()

            role = Role(
                id=role_model.id,
                name=role_model.name,
                ghibli_endpoint=role_model.ghibli_endpoint
            )

            users.append(User(
                id=user_model.id,
                name=user_model.name,
                email=user_model.email,
                password_hash=user_model.password_hash,
                role=role
            ))

        return users

    async def update(self, user: User) -> User:
        stmt = select(UserModel).where(UserModel.id == user.id)
        result = await self.session.execute(stmt)
        user_model = result.scalar_one()

        user_model.name = user.name
        user_model.email = user.email
        user_model.password_hash = user.password_hash

        if user_model.role_id != user.role.id:
            user_model.role_id = user.role.id

        await self.session.flush()
        await self.session.commit()

        return user

    async def patch(self, user_id: int, patch_data) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        user_model = result.scalar_one_or_none()
        if not user_model:
            return None

        for key, value in patch_data.dict(exclude_unset=True).items():
            if key == "role_name":

                role_stmt = select(RoleModel).where(RoleModel.name == value)
                role_result = await self.session.execute(role_stmt)
                role_model = role_result.scalar_one()
                user_model.role_id = role_model.id
            else:
                setattr(user_model, key, value)

        await self.session.flush()
        await self.session.commit()

        return await self.get(user_id)

    async def delete(self, user_id: int) -> None:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        user_model = result.scalar_one_or_none()
        if user_model:
            await self.session.delete(user_model)
            await self.session.flush()
            await self.session.commit()