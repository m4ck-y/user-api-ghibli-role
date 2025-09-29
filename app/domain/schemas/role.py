from pydantic import BaseModel


class RoleResponse(BaseModel):
    id: int
    name: str
    ghibli_endpoint: str

    class Config:
        from_attributes = True