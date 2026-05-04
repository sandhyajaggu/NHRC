from sqlalchemy.orm import Session
from app.models.member import Member
from sqlalchemy.sql import func


class AdminRepository:

    @staticmethod
    def get_dashboard_stats(db: Session):

        return {
            "employees": db.query(Member).filter(
                Member.candidate_type == "employee"
            ).count(),

            "students": db.query(Member).filter(
                Member.candidate_type == "student"
            ).count(),

            "representatives": db.query(Member).filter(
                Member.candidate_type == "representative"
            ).count(),

            "approved_employees": db.query(Member).filter(
                Member.candidate_type == "employee",
                Member.status == "approved"
            ).count(),

            "approved_students": db.query(Member).filter(
                Member.candidate_type == "student",
                Member.status == "approved"
            ).count(),

            "approved_representatives": db.query(Member).filter(
                Member.candidate_type == "representative",
                Member.status == "approved"
            ).count(),

            "pending_employees": db.query(Member).filter(
                Member.candidate_type == "employee",
                Member.status == "pending"
            ).count(),

            "pending_students": db.query(Member).filter(
                Member.candidate_type == "student",
                Member.status == "pending"
            ).count(),

            "pending_representatives": db.query(Member).filter(
                Member.candidate_type == "representative",
                Member.status == "pending"
            ).count(),
        }

    @staticmethod
    def get_users_by_role(db: Session, role: str):
        return db.query(Member).filter(
            Member.candidate_type == role
        ).all()

    #  FIXED APPROVE
    @staticmethod
    def approve_user(db: Session, membership_id: str):

        user = db.query(Member).filter(
            Member.membership_id == membership_id
        ).first()

        if not user:
            return None

        user.status = "approved"
        user.approved_at = func.now()

        db.commit()
        db.refresh(user)

        return user

    #  FIXED REJECT
    @staticmethod
    def reject_user(db: Session, membership_id: str):

        user = db.query(Member).filter(
            Member.membership_id == membership_id
        ).first()

        if not user:
            return None

        user.status = "rejected"

        db.commit()
        db.refresh(user)

        return user

    #  FIXED DELETE
    @staticmethod
    def delete_user(db: Session, membership_id: str):

        user = db.query(Member).filter(
            Member.membership_id == membership_id
        ).first()

        if not user:
            return False

        db.delete(user)
        db.commit()

        return True