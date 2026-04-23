from sqlalchemy.orm import Session
from app.repositories.admin_repository import AdminRepository
from app.models.board_member import BoardMember
from app.models.member_benefit import MemberBenefit
from app.models.black_profile import BlackProfile



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
    from sqlalchemy.orm import Session


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
        member = db.query(BoardMember).filter(BoardMember.id == member_id).first()
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
        return benefit

    @staticmethod
    def get_benefits(db: Session, role: str):
        return db.query(MemberBenefit).filter(MemberBenefit.role == role).all()

    @staticmethod
    def delete_benefit(db: Session, benefit_id: int):
        benefit = db.query(MemberBenefit).get(benefit_id)
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
        return profile

    @staticmethod
    def get_black_profiles(db: Session):
        return db.query(BlackProfile).all()

    @staticmethod
    def delete_black_profile(db: Session, profile_id: int):
        profile = db.query(BlackProfile).get(profile_id)
        if profile:
            db.delete(profile)
            db.commit()
        return True