from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/dabase_name"
    admin_name: str = "Admin User"
    admin_email: str = "admin@ghibli.com"
    admin_password: str = "admin123"

    class Config:
        env_file = ".env"


settings = Settings()