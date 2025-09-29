from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from app.infrastructure.api.routes.users import router as users_router
from app.infrastructure.api.routes.roles import router as roles_router
from app.infrastructure.api.routes.auth import router as auth_router
from app.infrastructure.api.routes.ghibli import router as ghibli_router
from app.infrastructure.database.init_db import init_db

def auth_key_func(request: Request) -> str:
    ip = get_remote_address(request)
    user_agent = request.headers.get("User-" \
    "", "")
    return f"{ip}:{user_agent}"

def registro_key_func(request: Request) -> str:
    ip = get_remote_address(request)
    user_agent = request.headers.get("User-Agent", "")
    return f"{ip}:{user_agent}"

limiter = Limiter(key_func=get_remote_address)

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

app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(roles_router)
app.include_router(ghibli_router)

@app.get("/")
def read_root():
    return {"message": "API de Usuarios con Roles de Ghibli"}
