from app.models.member import Member
from app.models.user import User, UserRole
from app.core.security import hash_password
import random
import string
from sqlalchemy.orm import Session


from app.repositories.admin_repository import AdminRepository


def generate_password(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


class AdminService:

    @staticmethod
    def dashboard_stats(db: Session):
        return AdminRepository.get_dashboard_stats(db)

    @staticmethod
    def list_users(db: Session, role: str):
        return AdminRepository.get_users_by_role(db, role)

    @staticmethod
    def approve_user(db: Session, user_id: int):
        return AdminRepository.approve_user(db, user_id)

    @staticmethod
    def reject_user(db: Session, user_id: int):
        return AdminRepository.reject_user(db, user_id)

    @staticmethod
    def delete_user(db: Session, user_id: int):
        return AdminRepository.delete_user(db, user_id)

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