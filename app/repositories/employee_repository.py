from sqlalchemy.orm import Session
from app.models.member import Member
from app.models.employee import Employee


class EmployeeRepository:

    @staticmethod
    def create(db: Session, payload: dict):
        employee = Employee(**payload)

        db.add(employee)
        db.commit()
        db.refresh(employee)

        return employee

    #  NEW METHOD (IMPORTANT)
    @staticmethod
    def get_employees_with_details(db: Session):

        results = db.query(
            Member.id,
            Member.membership_id,
            Member.full_name,
            Member.mobile,
            Member.status,
            Employee.designation
        ).join(
            Employee,
            Employee.member_id == Member.id
        ).filter(
            Member.candidate_type == "employee"
        ).all()

        # convert to response format
        return [
            {
                "membership_id": row.membership_id,
                "name": row.full_name,
                "phone": row.mobile,
                "status": row.status,
                "designation": row.designation
            }
            for row in results
        ]