from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int
    role_name: str


class RoleResponse(BaseModel):
    id: int
    name: str
    ghibli_endpoint: str