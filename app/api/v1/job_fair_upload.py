

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


@router.post("/upload/image")
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

    filename = (
        f"{uuid.uuid4()}.{extension}"
    )

    filepath = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(filepath, "wb") as buffer:
        buffer.write(
            await file.read()
        )

    return {
        "message": "Image uploaded successfully",
        "file_url": f"/uploads/{filename}"
    }

@router.post("/upload/pdf")
async def upload_pdf(
    file: UploadFile = File(...)
):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    filename = (
        f"{uuid.uuid4()}.pdf"
    )

    filepath = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(filepath, "wb") as buffer:
        buffer.write(
            await file.read()
        )

    return {
        "message": "PDF uploaded successfully",
        "file_url": f"/uploads/{filename}"
    }