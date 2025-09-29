from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional
from app.domain.enums.role_type import RoleType


class UserCreate(BaseModel):
    name: str = Field(..., examples=["María García"])
    email: EmailStr = Field(..., examples=["maria.garcia@gmail.com"])
    password: str = Field(..., examples=["securepassword123"])
    role_name: RoleType = Field(..., examples=["species"])


class UserUpdate(BaseModel):
    name: str = Field(..., examples=["José López"])
    email: EmailStr = Field(..., examples=["jose.lopez@hotmail.com"])
    password: str = Field(..., examples=["newpassword456"])
    role_name: RoleType = Field(..., examples=["films"])


class UserPatch(BaseModel):
    name: Optional[str] = Field(None, examples=["Ana Rodríguez"])
    email: Optional[EmailStr] = Field(None, examples=["ana.rodriguez@yahoo.com"])
    password: Optional[str] = Field(None, examples=["updatedpass789"])
    role_name: Optional[RoleType] = Field(None, examples=["people"])


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., examples=[1])
    name: str = Field(..., examples=["María García"])
    email: EmailStr = Field(..., examples=["maria.garcia@gmail.com"])
    role_name: RoleType = Field(..., examples=["locations"])

