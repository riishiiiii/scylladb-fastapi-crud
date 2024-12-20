from fastapi import APIRouter, HTTPException, Depends
import uuid

from .schema import User, UserResponse
from .service import CrudService, UserNotFound

router = APIRouter()


@router.post("/users/")
async def create_user(
    user: User, service: CrudService = Depends(CrudService)
) -> UserResponse:
    try:
        return await service.create_user(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user: {e}")


@router.get("/users/{user_id}")
async def read_user(
    user_id: uuid.UUID, service: CrudService = Depends(CrudService)
) -> UserResponse:
    try:
        return await service.read_user(user_id)
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"User not found: {e}")


@router.put("/users/{user_id}")
async def update_user(
    user_id: uuid.UUID, updated_user: User, service: CrudService = Depends(CrudService)
) -> UserResponse:
    try:
        return await service.update_user(user_id, updated_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user: {e}")


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: uuid.UUID, service: CrudService = Depends(CrudService)
) -> dict:
    try:
        await service.delete_user(user_id)
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {e}")


@router.get("/users/")
async def list_users(service: CrudService = Depends(CrudService)) -> list[UserResponse]:
    try:
        return await service.list_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list users: {e}")
