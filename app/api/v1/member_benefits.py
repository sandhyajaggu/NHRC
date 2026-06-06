# app/api/v1/member_benefits.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.member_benefit import MemberBenefit

router = APIRouter(
    prefix="/member-benefits",
    tags=["Member Benefits"]
)

@router.get("/landing-page")
def get_landing_page_benefits(
    db: Session = Depends(get_db)
):
    return {
        "employee": db.query(MemberBenefit)
            .filter(
                MemberBenefit.category == "EMPLOYEE",
                MemberBenefit.is_active == True
            ).all(),

        "student": db.query(MemberBenefit)
            .filter(
                MemberBenefit.category == "STUDENT",
                MemberBenefit.is_active == True
            ).all(),

        "tpo": db.query(MemberBenefit)
            .filter(
                MemberBenefit.category == "TPO",
                MemberBenefit.is_active == True
            ).all()
    }