from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.schemas.user import UserCreate, UserUpdate, UserPatch, UserResponse
from app.application.user_service import UserService
from app.infrastructure.database.implementations.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.infrastructure.database.implementations.sqlalchemy_role_repository import SQLAlchemyRoleRepository
from app.infrastructure.database.session import get_db
from app.infrastructure.api.dependencies.auth import get_current_user, get_current_admin_user, get_current_user_optional, get_current_normal_user
from app.domain.models.user import User

router = APIRouter()

def get_user_service(session: AsyncSession = Depends(get_db)):
    user_repo = SQLAlchemyUserRepository(session)
    role_repo = SQLAlchemyRoleRepository(session)
    return UserService(user_repo, role_repo)

@router.post("/users", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    if current_user and current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Authenticated users cannot register new accounts. Please logout first.")
    try:
        return await service.create_user(user_data, current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        role_name=current_user.role.name
    )

@router.put("/users/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_normal_user)
):
    try:
        updated = await service.update_user(current_user.id, user_data)
        if not updated:
            raise HTTPException(status_code=404, detail="User not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/users/me", response_model=UserResponse)
async def patch_current_user(
    patch_data: UserPatch,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_normal_user)
):
    try:
        patched = await service.patch_user(current_user.id, patch_data)
        if not patched:
            raise HTTPException(status_code=404, detail="User not found")
        return patched
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/users/me")
async def delete_current_user(
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_normal_user)
):
    try:
        success = await service.delete_user(current_user.id, current_user)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_admin_user)
):
    return await service.get_all_users()

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_admin_user)
):
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_admin_user)
):
    try:
        updated = await service.update_user(user_id, user_data, current_user)
        if not updated:
            raise HTTPException(status_code=404, detail="User not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/users/{user_id}", response_model=UserResponse)
async def patch_user(
    user_id: int,
    patch_data: UserPatch,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_admin_user)
):
    try:
        patched = await service.patch_user(user_id, patch_data, current_user)
        if not patched:
            raise HTTPException(status_code=404, detail="User not found")
        return patched
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_admin_user)
):
    try:
        success = await service.delete_user(user_id, current_user)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))