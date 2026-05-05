from fastapi import HTTPException

from app.models.member import Member
from app.models.user import User, UserRole
from app.core.security import hash_password
import random
import string
from sqlalchemy.orm import Session
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.representative_repository import RepresentativeRepository
from app.repositories.admin_repository import AdminRepository



from app.repositories.admin_repository import AdminRepository


def generate_password(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


class AdminService:

    @staticmethod
    def dashboard_stats(db: Session):
        return AdminRepository.get_dashboard_stats(db)
    
    @staticmethod
    def get_member_full_details(db, membership_id: str):
        return AdminRepository.get_member_full_details(db, membership_id)

    @staticmethod
    def list_users(db: Session, role: str):

        if role == "employee":
            return EmployeeRepository.get_employees_with_details(db)

        elif role == "student":
            return StudentRepository.get_students_with_details(db)

        elif role == "representative":
            return RepresentativeRepository.get_representatives_with_details(db)
    

    @staticmethod
    def approve_user(db: Session, membership_id: str):
        return AdminRepository.approve_user(db, membership_id)

    @staticmethod
    def reject_user(db: Session, membership_id: str):
        return AdminRepository.reject_user(db, membership_id)

    @staticmethod
    def delete_user(db: Session, membership_id: str):
        deleted = AdminRepository.delete_user(db, membership_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Member not found")

        return {
            "success": True,
            "message": "Member deleted successfully",
            "membership_id": membership_id
        }
    @staticmethod
    def bulk_delete_members(db: Session, membership_ids: list):
        return AdminRepository.bulk_delete_members(db, membership_ids)

    # NEW FUNCTION (STEP 3)
    @staticmethod
    def approve_member(db: Session, member_id: int):

        # 1. Get member
        member = db.query(Member).filter(Member.id == member_id).first()
        

        if not member:
            raise Exception("Member not found")

        # 2. Check already exists in users
        existing_user = db.query(User).filter(User.email == member.email).first()
        if existing_user:
            raise Exception("User already exists")

        # 3. Generate password
        raw_password = generate_password()
        hashed_password = hash_password(raw_password)

        # 4. Create user
        user = User(
            full_name=member.full_name,
            email=member.email,
            mobile=member.mobile,
            password=hashed_password,
            role=UserRole.member,   
            membership_id=member.membership_id,
            is_active=True,
            is_approved=True
        )

        db.add(user)

        # 5. Optional: mark member approved
        # (add column if needed)
        # member.is_approved = True

        db.commit()

        return {
            "message": "Member approved successfully",
            "email": member.email,
            "password": raw_password
        }