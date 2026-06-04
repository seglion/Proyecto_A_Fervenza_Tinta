from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.core.dependencies import get_current_user, get_storage_service
from app.core.services.i_storage_service import IStorageService
from app.users.domain.entities import User

router = APIRouter(prefix="/files", tags=["files"])

_MAX_SIZE = 5 * 1024 * 1024  # 5 MB
_ALLOWED_TYPES = {"image/png", "image/jpeg"}


@router.post("/upload-image", status_code=status.HTTP_200_OK)
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    storage: IStorageService = Depends(get_storage_service),
):
    if file.content_type not in _ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Solo se permiten imágenes PNG o JPEG.",
        )
    data = await file.read()
    if len(data) > _MAX_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="La imagen no puede superar 5 MB.",
        )
    url = await storage.upload_image(data, file.filename or "image.jpg", file.content_type)
    return {"url": url}
