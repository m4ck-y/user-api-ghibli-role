from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.models.base import Base


class RoleModel(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    ghibli_endpoint: Mapped[str] = mapped_column(String(100), nullable=False)

    users: Mapped[list["UserModel"]] = relationship("UserModel", back_populates="role")