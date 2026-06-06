import os
import shutil

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

UPLOAD_DIR = "uploads/black_profiles"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)
router = APIRouter(prefix="/black_profiles", tags=["Black_Profiles"])

@router.post(
    "/admin/black-profiles/{profile_id}/upload-document"
)
async def admin_upload_document(
    profile_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    profile = (
        db.query(BlackProfile)
        .filter(
            BlackProfile.id == profile_id
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Black profile not found"
        )

    filename = (
        f"{profile_id}_{file.filename}"
    )

    filepath = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    profile.document_name = file.filename

    profile.document_url = (
        f"/uploads/black_profiles/{filename}"
    )

    db.commit()
    db.refresh(profile)

    return {
        "message": "Document uploaded successfully",
        "document_name": profile.document_name,
        "document_url": profile.document_url
    }

@router.post(
    "/hr/black-profiles/{profile_id}/upload-document"
)
async def hr_upload_document(
    profile_id: int,
    file: UploadFile = File(...),
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
            status_code=403,
            detail="You can upload only to your own black profiles"
        )

    filename = (
        f"{profile_id}_{file.filename}"
    )

    filepath = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    profile.document_name = file.filename

    profile.document_url = (
        f"/uploads/black_profiles/{filename}"
    )

    db.commit()
    db.refresh(profile)

    return {
        "message": "Document uploaded successfully",
        "document_name": profile.document_name,
        "document_url": profile.document_url
    }
@router.get(
    "/admin/black-profiles/{profile_id}/document"
)
def get_black_profile_document(
    profile_id: int,
    db: Session = Depends(get_db)
):

    profile = (
        db.query(BlackProfile)
        .filter(
            BlackProfile.id == profile_id
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Black profile not found"
        )

    return {
        "profile_id": profile.id,
        "employee_name": profile.employee_name,
        "document_name": profile.document_name,
        "document_url": profile.document_url
    }
@router.get(
    "/hr/black-profiles/{profile_id}/document"
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
            status_code=403,
            detail="You can view only your own black profile documents"
        )

    return {
        "profile_id": profile.id,
        "employee_name": profile.employee_name,
        "document_name": profile.document_name,
        "document_url": profile.document_url
    }