from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.infrastructure.api.routes.users import router as users_router
from app.infrastructure.api.routes.roles import router as roles_router
from app.infrastructure.api.routes.auth import router as auth_router
from app.infrastructure.api.routes.ghibli import router as ghibli_router
from app.infrastructure.database.init_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown

app = FastAPI(
    title="API de Usuarios con Roles de Ghibli",
    description="API para gestión de usuarios con acceso basado en roles de Studio Ghibli",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(roles_router)
app.include_router(ghibli_router)

@app.get("/")
def read_root():
    return {"message": "API de Usuarios con Roles de Ghibli"}
