from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from app.application.ghibli_service import GhibliService
from app.infrastructure.api.dependencies.auth import get_current_user
from app.domain.models.user import User

router = APIRouter()

def get_ghibli_service():
    return GhibliService()

@router.get("/ghibli-api/resources/")
async def get_all_resources(
    service: GhibliService = Depends(get_ghibli_service),
    current_user: User = Depends(get_current_user)
):
    try:
        return await service.get_all_resources(current_user)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching Ghibli resources")

@router.get("/ghibli-api/resources/{resource_id}/")
async def get_resource_by_id(
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