from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Dict, Any
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.application.ghibli_service import GhibliService
from app.infrastructure.api.dependencies.auth import get_current_user
from app.domain.models.user import User

def ghibli_user_key_func(request: Request) -> str:
    from app.infrastructure.api.dependencies.auth import verify_token
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return get_remote_address(request)
    try:
        payload = verify_token(token, lambda: Exception())
        return str(payload.user_id)
    except:
        return get_remote_address(request)

ghibli_limiter = Limiter(key_func=ghibli_user_key_func)

router = APIRouter()

def get_ghibli_service():
    return GhibliService()

@router.get("/ghibli-api/resources/", tags=["normal_user"])
@ghibli_limiter.limit("10/minute")
async def get_all_resources(
    request: Request,
    service: GhibliService = Depends(get_ghibli_service),
    current_user: User = Depends(get_current_user)
):
    try:
        return await service.get_all_resources(current_user)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching Ghibli resources")

@router.get("/ghibli-api/resources/{resource_id}/", tags=["normal_user"])
@ghibli_limiter.limit("10/minute")
async def get_resource_by_id(
    request: Request,
    resource_id: str,
    service: GhibliService = Depends(get_ghibli_service),
    current_user: User = Depends(get_current_user)
):
    try:
        return await service.get_resource_by_id(current_user, resource_id)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching Ghibli resource")