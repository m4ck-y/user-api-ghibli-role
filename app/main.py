from fastapi import FastAPI
from app.infrastructure.api.routes.users import router as users_router
from app.infrastructure.api.routes.roles import router as roles_router

app = FastAPI(
    title="API de Usuarios con Roles de Ghibli",
    description="API para gestión de usuarios con acceso basado en roles de Studio Ghibli",
    version="1.0.0"
)

app.include_router(users_router)
app.include_router(roles_router)

@app.get("/")
def read_root():
    return {"message": "API de Usuarios con Roles de Ghibli"}
