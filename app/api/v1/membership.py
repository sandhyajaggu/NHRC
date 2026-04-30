from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from fastapi import Form, UploadFile, File


from app.models.member import Member
from app.models.user import User
from app.schemas.member import MemberCreate
from app.schemas.employee import EmployeeCreate
from app.schemas.representative import (
    RepresentativeUniversityCreate,
    RepresentativeAutonomousCreate,
    RepresentativeBothCreate
)

from app.services.representative_service import RepresentativeService
from app.schemas.student import (
    StudentUniversityCreate,
    StudentAutonomousCreate
)

from app.services.member_service import MemberService
from app.services.employee_service import EmployeeService
from app.services.student_service import StudentService


router = APIRouter(
    prefix="/membership",
    tags=["Membership"]
)


from app.core.security import get_current_user

@router.post("/personal")
def create_personal(
    payload: MemberCreate,
    db: Session = Depends(get_db),
):
    return MemberService.create_member(db, payload)

@router.post("/employee-details")
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db)
):
    # Find member using membership_id
    member = db.query(Member).filter(
        Member.membership_id == payload.membership_id
    ).first()

    # If not found → error
    if not member:
        raise HTTPException(status_code=404, detail="Invalid membership_id")

    #Replace membership_id with actual DB id
    payload.member_id = member.id

    # Call service
    return EmployeeService.create_employee(db, payload)



@router.post("/student-university")
def create_student_university(
    payload: StudentUniversityCreate,
    db: Session = Depends(get_db)
):
    return StudentService.create_university(db, payload)

@router.post("/student-autonomous")
def create_student_autonomous(
    payload: StudentAutonomousCreate,
    db: Session = Depends(get_db)
):
    return StudentService.create_autonomous(db, payload)

@router.post("/representative-university")
def create_rep_university(
    payload: RepresentativeUniversityCreate,
    db: Session = Depends(get_db)
):
    return RepresentativeService.create_university(
        db,
        payload
    )


@router.post("/representative-autonomous")
def create_rep_autonomous(
    payload: RepresentativeAutonomousCreate,
    db: Session = Depends(get_db)
):
    return RepresentativeService.create_autonomous(
        db,
        payload
    )

@router.post("/representative-both")
def create_rep_both(
    payload: RepresentativeBothCreate,
    db: Session = Depends(get_db)
):
    return RepresentativeService.create_both(
        db,
        payload
    )      