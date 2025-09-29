from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.schemas.user import UserCreate, UserUpdate, UserPatch, UserResponse
from app.application.user_service import UserService
from app.infrastructure.database.implementations.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.infrastructure.database.implementations.sqlalchemy_role_repository import SQLAlchemyRoleRepository
from app.infrastructure.database.session import get_db

router = APIRouter()

def get_user_service(session: AsyncSession = Depends(get_db)):
    user_repo = SQLAlchemyUserRepository(session)
    role_repo = SQLAlchemyRoleRepository(session)
    return UserService(user_repo, role_repo)

@router.post("/users", response_model=UserResponse)
async def create_user(user_data: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        return await service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(service: UserService = Depends(get_user_service)):
    return await service.get_all_users()

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserUpdate, service: UserService = Depends(get_user_service)):
    try:
        updated = await service.update_user(user_id, user_data)
        if not updated:
            raise HTTPException(status_code=404, detail="User not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/users/{user_id}", response_model=UserResponse)
async def patch_user(user_id: int, patch_data: UserPatch, service: UserService = Depends(get_user_service)):
    try:
        patched = await service.patch_user(user_id, patch_data)
        if not patched:
            raise HTTPException(status_code=404, detail="User not found")
        return patched
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    try:
        success = await service.delete_user(user_id, None)  # No current_user for now
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))