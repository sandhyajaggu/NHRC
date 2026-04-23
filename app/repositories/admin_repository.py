from sqlalchemy.orm import Session
from app.models.user import User


class AdminRepository:

    @staticmethod
    def get_dashboard_stats(db: Session):

        return {
            "employees": db.query(User).filter(
                User.role == "employee"
            ).count(),

            "students": db.query(User).filter(
                User.role == "student"
            ).count(),

            "representatives": db.query(User).filter(
                User.role == "representative"
            ).count(),

            "approved_employees": db.query(User).filter(
                User.role == "employee",
                User.is_approved == True
            ).count(),

            "approved_students": db.query(User).filter(
                User.role == "student",
                User.is_approved == True
            ).count(),

            "approved_representatives": db.query(User).filter(
                User.role == "representative",
                User.is_approved == True
            ).count(),

            "pending_employees": db.query(User).filter(
                User.role == "employee",
                User.is_approved == False
            ).count(),

            "pending_students": db.query(User).filter(
                User.role == "student",
                User.is_approved == False
            ).count(),

            "pending_representatives": db.query(User).filter(
                User.role == "representative",
                User.is_approved == False
            ).count(),
        }


    @staticmethod
    def get_users_by_role(db: Session, role: str):

        return db.query(User).filter(
            User.role == role
        ).all()


    @staticmethod
    def approve_user(db: Session, user_id: int):

        user = db.query(User).filter(User.id == user_id).first()

        if user:
            user.is_approved = True
            db.commit()
            db.refresh(user)

        return user


    @staticmethod
    def reject_user(db: Session, user_id: int):

        user = db.query(User).filter(User.id == user_id).first()

        if user:
            user.is_approved = False
            db.commit()
            db.refresh(user)

        return user


    @staticmethod
    def delete_user(db: Session, user_id: int):

        user = db.query(User).filter(User.id == user_id).first()

        if user:
            db.delete(user)
            db.commit()

        return Trues