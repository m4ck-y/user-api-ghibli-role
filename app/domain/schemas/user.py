from pydantic import BaseModel, EmailStr
from typing import Optional
from app.domain.enums.role_type import RoleType


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role_name: RoleType


class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role_name: RoleType


class UserPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role_name: Optional[RoleType] = None


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role_name: RoleType

    class Config:
        from_attributes = True

