import os
from sqlalchemy.orm import Session

from fastapi import Depends, File, Form, UploadFile
from app.models.member import Member


from app.core.database import get_db
from fastapi import APIRouter

UPLOAD_DIR = "uploads"
router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/")
def upload_file(
    membership_id: str = Form(...),
    file_type: str = Form(...),   # profile_pic / id_front / id_back
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    member = db.query(Member).filter(
        Member.membership_id == membership_id
    ).first()

    if not member:
        return {"error": "Member not found"}

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = f"{UPLOAD_DIR}/{membership_id}_{file_type}_{file.filename}"

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # ✅ handle multiple file types
    if file_type == "profile_pic":
        member.profile_pic = file_path

    elif file_type == "id_front":
        member.id_front = file_path

    elif file_type == "id_back":
        member.id_back = file_path

    db.commit()

    return {
        "message": "Uploaded successfully",
        "file_path": file_path
    }