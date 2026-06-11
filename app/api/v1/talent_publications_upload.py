import os
import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

# ---------------------------------
# DEBUG
# ---------------------------------

@router.get("/talent_publications/debug")
def debug_uploads():

    return {
        "upload_dir": os.path.abspath(UPLOAD_DIR),
        "files": os.listdir(UPLOAD_DIR)
    }


# ---------------------------------
# UPLOAD IMAGE
# ---------------------------------

@router.post("/talent_publications/image")
async def upload_image(
    file: UploadFile = File(...)
):

    allowed_types = [
        "image/jpeg",
        "image/jpg",
        "image/png",
        "image/webp"
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, PNG, WEBP files are allowed"
        )

    extension = file.filename.split(".")[-1]

    filename = f"{uuid.uuid4()}.{extension}"

    filepath = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "message": "Image uploaded successfully",
        "file_url": f"/uploads/{filename}"
    }


# ---------------------------------
# UPLOAD PDF
# ---------------------------------

@router.post("/talent_publications/pdf")
async def upload_pdf(
    file: UploadFile = File(...)
):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    filename = f"{uuid.uuid4()}.pdf"

    filepath = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "message": "PDF uploaded successfully",
        "file_url": f"/uploads/{filename}"
    }


# ---------------------------------
# GET ALL IMAGES
# ---------------------------------

@router.get("/talent_publications/images")
def get_all_images():

    files = []

    for file in os.listdir(UPLOAD_DIR):

        if file.lower().endswith(
            (".jpg", ".jpeg", ".png", ".webp")
        ):
            files.append({
                "file_name": file,
                "file_url": f"/uploads/{file}"
            })

    return files


# ---------------------------------
# GET ALL PDFS
# ---------------------------------

@router.get("/talent_publications/pdfs")
def get_all_pdfs():

    files = []

    for file in os.listdir(UPLOAD_DIR):

        if file.lower().endswith(".pdf"):
            files.append({
                "file_name": file,
                "file_url": f"/uploads/{file}"
            })

    return files


# ---------------------------------
# GET ALL FILES
# ---------------------------------

@router.get("/talent_publications/files")
def get_all_files():

    return {
        "path": os.path.abspath(UPLOAD_DIR),
        "files": os.listdir(UPLOAD_DIR)
    }


