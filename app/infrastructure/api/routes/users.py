from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.domain.schemas.user import UserCreate, UserUpdate, UserPatch, UserResponse
from app.application.user_service import UserService
from app.infrastructure.database.implementations.in_memory_user_repository import InMemoryUserRepository
from app.infrastructure.database.implementations.in_memory_role_repository import InMemoryRoleRepository

router = APIRouter()

# Global instances for in-memory persistence
_user_repo = InMemoryUserRepository()
_role_repo = InMemoryRoleRepository()

def get_user_service():
    return UserService(_user_repo, _role_repo)

@router.post("/users", response_model=UserResponse)
def create_user(user_data: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        return service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users", response_model=List[UserResponse])
def get_all_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, service: UserService = Depends(get_user_service)):
    try:
        updated = service.update_user(user_id, user_data)
        if not updated:
            raise HTTPException(status_code=404, detail="User not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/users/{user_id}", response_model=UserResponse)
def patch_user(user_id: int, patch_data: UserPatch, service: UserService = Depends(get_user_service)):
    try:
        patched = service.patch_user(user_id, patch_data)
        if not patched:
            raise HTTPException(status_code=404, detail="User not found")
        return patched
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/users/{user_id}")
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    try:
        success = service.delete_user(user_id, None)  # No current_user for now
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))