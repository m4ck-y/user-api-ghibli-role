import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.infrastructure.database.models.base import Base
from app.infrastructure.database.models.role_model import RoleModel
from app.infrastructure.database.models.user_model import UserModel
from app.infrastructure.database.session import engine
from app.application.utils import hash_password
from app.infrastructure.config.settings import settings


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def seed_roles():
    async with engine.begin() as conn:
        try:
            result = await conn.execute(text("SELECT COUNT(*) FROM roles"))
            count = result.scalar()
            if count > 0:
                return
        except Exception:
            pass

        roles_data = [
            {"name": "admin", "ghibli_endpoint": ""},
            {"name": "films", "ghibli_endpoint": "https://ghibliapi.vercel.app/films"},
            {"name": "people", "ghibli_endpoint": "https://ghibliapi.vercel.app/people"},
            {"name": "locations", "ghibli_endpoint": "https://ghibliapi.vercel.app/locations"},
            {"name": "species", "ghibli_endpoint": "https://ghibliapi.vercel.app/species"},
            {"name": "vehicles", "ghibli_endpoint": "https://ghibliapi.vercel.app/vehicles"},
        ]

        for role_data in roles_data:
            await conn.execute(
                text("INSERT INTO roles (name, ghibli_endpoint) VALUES (:name, :endpoint)"),
                {"name": role_data["name"], "endpoint": role_data["ghibli_endpoint"]}
            )


async def seed_admin_user():
    async with engine.begin() as conn:
        try:
            result = await conn.execute(text("SELECT COUNT(*) FROM users WHERE email = :email"), {"email": settings.admin_email})
            count = result.scalar()
            if count > 0:
                return
        except Exception:
            pass

        role_result = await conn.execute(text("SELECT id FROM roles WHERE name = 'admin'"))
        role_id = role_result.scalar()

        if role_id:
            hashed_password = hash_password(settings.admin_password)
            await conn.execute(
                text("INSERT INTO users (name, email, password_hash, role_id) VALUES (:name, :email, :password, :role_id)"),
                {
                    "name": settings.admin_name,
                    "email": settings.admin_email,
                    "password": hashed_password,
                    "role_id": role_id
                }
            )


async def init_db():
    await create_tables()
    await seed_roles()
    await seed_admin_user()


if __name__ == "__main__":
    asyncio.run(init_db())