from sqlalchemy.orm import Session
from app.repositories.admin_repository import AdminRepository
from app.models.board_member import BoardMember
from app.models.member_benefit import MemberBenefit
from app.models.black_profile import BlackProfile
from app.models.employee import Employee
from app.models.student import StudentUniversityDetails, StudentAutonomousDetails
from app.models.contact import ContactMessage
from app.models.representative import (
    RepresentativeUniversityDetails,
    RepresentativeAutonomousDetails,
    RepresentativeBothDetails 
)



# ================= MAIN ADMIN =================
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


# ================= EXTRA ADMIN =================
class AdminExtraService:

    # ---------------- BOARD MEMBERS ----------------
    @staticmethod
    def create_member(db: Session, data):
        member = BoardMember(**data.dict())
        db.add(member)
        db.commit()
        db.refresh(member)
        return member

    @staticmethod
    def get_members(db: Session):
        return db.query(BoardMember).all()

    @staticmethod
    def delete_member(db: Session, member_id: int):
        member = db.get(BoardMember, member_id)
        if member:
            db.delete(member)
            db.commit()
        return True


    # ---------------- BENEFITS ----------------
    @staticmethod
    def create_benefit(db: Session, data):
        benefit = MemberBenefit(**data.dict())
        db.add(benefit)
        db.commit()
        db.refresh(benefit)
        return benefit

    @staticmethod
    def get_benefits(db: Session, role: str):
        return db.query(MemberBenefit).filter(MemberBenefit.role == role).all()

    @staticmethod
    def delete_benefit(db: Session, benefit_id: int):
        #benefit = db.get(MemberBenefit, benefit_id)
        benefit = db.get(MemberBenefit, benefit_id)
        if benefit:
            db.delete(benefit)
            db.commit()
        return True


    # ---------------- BLACK PROFILE ----------------
    @staticmethod
    def create_black_profile(db: Session, data):
        profile = BlackProfile(**data.dict())
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def get_black_profiles(db: Session):
        return db.query(BlackProfile).all()

    @staticmethod
    def delete_black_profile(db: Session, profile_id: int):
        #profile = db.get(BlackProfile, profile_id)
        profile = db.get(BlackProfile, profile_id)
        if profile:
            db.delete(profile)
            db.commit()
        return True
    



class AdminDashboardService:

    @staticmethod
    def get_dashboard(db: Session):
        return {
            "employees": db.query(Employee).count(),
            "students": (
                db.query(StudentUniversityDetails).count() +
                db.query(StudentAutonomousDetails).count()
            ),
            "representatives": (
                db.query(RepresentativeUniversityDetails).count() +
                db.query(RepresentativeAutonomousDetails).count()
            ),
            "contacts_pending": db.query(ContactMessage).filter(
                ContactMessage.status == "pending"
            ).count(),
            "contacts_resolved": db.query(ContactMessage).filter(
                ContactMessage.status == "resolved"
            ).count(),
        }
    
from sqlalchemy import or_

class AdminFilterService:

    @staticmethod
    def search_members(db: Session, search: str = None):
        query = db.query(BoardMember)

        if search:
            query = query.filter(
                or_(
                    BoardMember.name.ilike(f"%{search}%"),
                    BoardMember.designation.ilike(f"%{search}%")
                )
            )

        return query.all()