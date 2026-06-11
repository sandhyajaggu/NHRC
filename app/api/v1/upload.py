import os
import shutil
from sqlalchemy.orm import Session

from fastapi import Depends, File, Form, UploadFile
from app.models.member import Member


from app.core.database import get_db
from fastapi import APIRouter

from app.models.upload import UploadedFile

UPLOAD_DIR = "uploads"
router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

@router.get("/debug/uploads")
def debug_uploads():
    import os

    return {
        "path": os.path.abspath("uploads"),
        "exists": os.path.exists("uploads"),
        "files": os.listdir("uploads") if os.path.exists("uploads") else []
    }
@router.get("/upload/check")
def check_file():

    filename = "NHRC-STU-018_image_signature.jpg"

    path = os.path.join("uploads", filename)

    return {
        "exists": os.path.exists(path),
        "absolute_path": os.path.abspath(path)
    }
@router.post("/")
async def upload_file(
    membership_id: str = Form(...),
    file_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    os.makedirs("uploads", exist_ok=True)

    file_location = f"uploads/{membership_id}_{file_type}_{file.filename}"

    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # SAVE TO DATABASE
    uploaded_file = UploadedFile(
        membership_id=membership_id,
        file_type=file_type,
        file_name=file.filename,
        file_path=file_location
    )

    db.add(uploaded_file)
    db.commit()
    db.refresh(uploaded_file)

    return {
        "message": "Uploaded successfully",
        "file_path": file_location
    }

@router.get("/{membership_id}")
def get_uploaded_files(
    membership_id: str,
    db: Session = Depends(get_db)
):

    files = db.query(UploadedFile).filter(
        UploadedFile.membership_id == membership_id
    ).all()

    return {
        "membership_id": membership_id,
        "files": files
    }