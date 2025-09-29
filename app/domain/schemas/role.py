from pydantic import BaseModel, Field


class RoleResponse(BaseModel):
    id: int = Field(..., examples=[1])
    name: str = Field(..., examples=["admin"])
    ghibli_endpoint: str = Field(..., examples=[""])

    class Config:
        from_attributes = True