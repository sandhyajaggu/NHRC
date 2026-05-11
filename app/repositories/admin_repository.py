from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.models.member import Member
from sqlalchemy.sql import func

from app.models.representative import RepresentativeAutonomousDetails, RepresentativeBothDetails, RepresentativeUniversityDetails
from app.models.student import StudentAutonomousDetails, StudentUniversityDetails


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
    def model_to_dict(obj):
        if not obj:
            return None

        data = obj.__dict__.copy()
        data.pop("_sa_instance_state", None)

        #  remove sensitive fields
        data.pop("password", None)
        data.pop("password_hash", None)
        data.pop("email_otp", None)
        data.pop("captcha_answer", None)

        return data


    @staticmethod
    def get_member_full_details(db, membership_id: str):

        member = db.query(Member).filter(
            Member.membership_id == membership_id
        ).first()

        if not member:
            raise Exception("Member not found")

        #  MEMBER BASE DATA
        member_data = AdminRepository.model_to_dict(member)

        # =====================================
        #  EMPLOYEE
        # =====================================
        if member.candidate_type == "employee":

            emp = db.query(Employee).filter(
                Employee.member_id == member.id
            ).first()

            details = AdminRepository.model_to_dict(emp)

        # =====================================
        #  STUDENT
        # =====================================
        elif member.candidate_type == "student":

            stu_uni = db.query(StudentUniversityDetails).filter(
                StudentUniversityDetails.member_id == member.id
            ).first()

            stu_auto = db.query(StudentAutonomousDetails).filter(
                StudentAutonomousDetails.member_id == member.id
            ).first()

            details = (
                AdminRepository.model_to_dict(stu_uni)
                or AdminRepository.model_to_dict(stu_auto)
            )

        # =====================================
        #  REPRESENTATIVE
        # =====================================
        elif member.candidate_type == "representative":

            rep_uni = db.query(RepresentativeUniversityDetails).filter(
                RepresentativeUniversityDetails.member_id == member.id
            ).first()

            rep_auto = db.query(RepresentativeAutonomousDetails).filter(
                RepresentativeAutonomousDetails.member_id == member.id
            ).first()

            rep_both = db.query(RepresentativeBothDetails).filter(
                RepresentativeBothDetails.member_id == member.id
            ).first()

            details = (
                AdminRepository.model_to_dict(rep_uni)
                or AdminRepository.model_to_dict(rep_auto)
                or AdminRepository.model_to_dict(rep_both)
            )

        else:
            details = None

        #  FINAL RESPONSE (MERGED)
        return {
            "member": member_data,
            "details": details
        }
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
    @staticmethod
    def delete_member(db, membership_id: str):

        member = db.query(Member).filter(
            Member.membership_id == membership_id
        ).first()

        if not member:
            return None

        # =========================
        # DELETE RELATED DATA
        # =========================

        # Employee
        db.query(Employee).filter(
            Employee.member_id == member.id
        ).delete()

        # Student
        db.query(StudentUniversityDetails).filter(
            StudentUniversityDetails.member_id == member.id
        ).delete()

        db.query(StudentAutonomousDetails).filter(
            StudentAutonomousDetails.member_id == member.id
        ).delete()

        # Representative
        db.query(RepresentativeUniversityDetails).filter(
            RepresentativeUniversityDetails.member_id == member.id
        ).delete()

        db.query(RepresentativeAutonomousDetails).filter(
            RepresentativeAutonomousDetails.member_id == member.id
        ).delete()

        db.query(RepresentativeBothDetails).filter(
            RepresentativeBothDetails.member_id == member.id
        ).delete()

        
        db.delete(member)
        db.commit()

        return True
    
    @staticmethod
    def bulk_delete_members(db: Session, membership_ids: list):

        members = db.query(Member).filter(
            Member.membership_id.in_(membership_ids)
        ).all()

        deleted_ids = []

        for member in members:
            deleted_ids.append(member.membership_id)
            db.delete(member)

        db.commit()

        return {
            "deleted_count": len(deleted_ids),
            "deleted_ids": deleted_ids
        }