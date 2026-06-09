import os
import shutil
import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Depends
)

from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.core.database import get_db
from app.models.black_profile import BlackProfile
from app.schemas.black_profile import BlackProfileDocumentResponse, BlackProfileResponse

UPLOAD_DIR = "uploads/black_profiles"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)
router = APIRouter(prefix="/black_profiles", tags=["Black_Profiles"])

@router.post(
    "/admin/upload-black-profile-document"
)
async def admin_upload_document(
    file: UploadFile = File(...)
):

    filename = f"{uuid.uuid4()}_{file.filename}"

    filepath = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "document_name": file.filename,
        "document_url": f"/uploads/black_profiles/{filename}"
    }
@router.post(
    "/hr/upload-black-profile-document"
)
async def hr_upload_document(
    file: UploadFile = File(...)
):
    filename = f"{uuid.uuid4()}_{file.filename}"

    filepath = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "document_name": file.filename,
        "document_url": f"/uploads/black_profiles/{filename}"
    }
@router.get(
    "/admin/black-profiles/{profile_id}/document",
    response_model=BlackProfileDocumentResponse
)
def get_black_profile_document(
    profile_id: int,
    db: Session = Depends(get_db)
):

    profile = (
        db.query(BlackProfile)
        .filter(BlackProfile.id == profile_id)
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Black profile not found"
        )

    if not profile.document_url:
        raise HTTPException(
            status_code=404,
            detail="No document uploaded"
        )

    return {
        "profile_id": profile.id,
        "employee_name": profile.employee_name,
        "document_name": profile.document_name,
        "document_url": profile.document_url
    }
@router.get(
    "/hr/black-profiles/{profile_id}/document",
    response_model=BlackProfileDocumentResponse
)
def get_my_black_profile_document(
    profile_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    profile = (
        db.query(BlackProfile)
        .filter(
            BlackProfile.id == profile_id,
            BlackProfile.created_by == "HR",
            BlackProfile.created_by_id == current_user.id
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Black profile not found"
        )

    if not profile.document_url:
        raise HTTPException(
            status_code=404,
            detail="No document uploaded"
        )

    return {
        "profile_id": profile.id,
        "employee_name": profile.employee_name,
        "document_name": profile.document_name,
        "document_url": profile.document_url
    }