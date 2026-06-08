from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.talent_publication import TalentPublication
from app.models.talent_publication_config import TalentPublicationConfig

def create_publication(
    db,
    payload
):
    publication = TalentPublication(
        title=payload.title,
        cover_image=payload.cover_image,
        pdf_file=payload.pdf_file,
        display_order=payload.display_order
    )

    db.add(publication)
    db.commit()
    db.refresh(publication)

    return publication

from fastapi import HTTPException


def update_publication(
    db,
    publication_id,
    payload
):
    publication = (
        db.query(TalentPublication)
        .filter(
            TalentPublication.id == publication_id
        )
        .first()
    )

    if not publication:
        raise HTTPException(
            status_code=404,
            detail="Publication not found"
        )

    update_data = payload.dict(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(publication, key, value)

    db.commit()
    db.refresh(publication)

    return publication

def delete_publication(
    db,
    publication_id
):
    publication = (
        db.query(TalentPublication)
        .filter(
            TalentPublication.id == publication_id
        )
        .first()
    )

    if not publication:
        raise HTTPException(
            status_code=404,
            detail="Publication not found"
        )

    publication.is_active = False

    db.commit()

    return {
        "message": "Deleted successfully"
    }

def get_publication(
    db,
    publication_id
):
    publication = (
        db.query(TalentPublication)
        .filter(
            TalentPublication.id == publication_id
        )
        .first()
    )

    if not publication:
        raise HTTPException(
            status_code=404,
            detail="Publication not found"
        )

    return publication

def get_publication_list(
    db
):
    return (
        db.query(TalentPublication)
        .order_by(
            TalentPublication.display_order.asc()
        )
        .all()
    )

def save_config(
    db,
    payload
):
    config = (
        db.query(TalentPublicationConfig)
        .first()
    )

    if not config:
        config = TalentPublicationConfig()
        db.add(config)

    config.youtube_url = payload.youtube_url

    db.commit()
    db.refresh(config)

    return config

def get_config(db):
    return (
        db.query(TalentPublicationConfig)
        .first()
    )

def get_landing_page_data(db):

    config = (
        db.query(TalentPublicationConfig)
        .first()
    )

    publications = (
        db.query(TalentPublication)
        .filter(
            TalentPublication.is_active == True
        )
        .order_by(
            TalentPublication.display_order.asc()
        )
        .all()
    )

    return {
        "youtube_url": (
            config.youtube_url
            if config
            else None
        ),
        "publications": publications
    }