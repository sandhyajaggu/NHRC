from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.core.dependencies import (
    get_current_admin
)

from app.models.talent_publication import TalentPublication
from app.schemas.talent_publication import (
    TalentPublicationCreate,
    TalentPublicationResponse,
    TalentPublicationUpdate,
    TalentPublicationConfigSchema
)

from app.services.talent_publication_service import (
    create_publication,
    update_publication,
    delete_publication,
    get_publication,
    get_publication_list,
    save_config,
    get_config,
    get_landing_page_data
)

router = APIRouter(
    tags=["Talent Publications"]
)

@router.post("/admin/talent-publications")
def create(
    payload: TalentPublicationCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return create_publication(
        db,
        payload
    )
@router.get("/admin/talent-publications")
def get_all(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return get_publication_list(db)
@router.get(
    "/admin/talent-publications/{publication_id}"
)
def get_one(
    publication_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return get_publication(
        db,
        publication_id
    )
@router.put(
    "/admin/talent-publications/{publication_id}",
    response_model=TalentPublicationResponse
)
def update_talent_publication(
    publication_id: int,
    payload: TalentPublicationUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return update_publication(
        db,
        publication_id,
        payload
    )
@router.delete(
    "/admin/talent-publications/{publication_id}"
)
def delete(
    publication_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return delete_publication(
        db,
        publication_id
    )

@router.post(
    "/admin/talent-publications/config"
)
def save_youtube(
    payload: TalentPublicationConfigSchema,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return save_config(
        db,
        payload
    )

@router.get(
    "/admin/talent-publications/config"
)
def get_youtube(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return get_config(db)

@router.get(
    "/landing/talent-publications"
)
def landing_page(
    db: Session = Depends(get_db)
):
    return get_landing_page_data(db)
@router.get(
    "/talent-publications",
    response_model=list[TalentPublicationResponse]
)
def get_all_talent_publications(
    db: Session = Depends(get_db)
):
    return (
        db.query(TalentPublication)
        .order_by(TalentPublication.display_order.asc())
        .all()
    )