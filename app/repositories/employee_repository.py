from sqlalchemy.orm import Session
from app.models.member import Member
from app.models.employee import Employee
from fastapi.encoders import jsonable_encoder



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
            Member,
            Employee
        ).join(
            Employee,
            Employee.member_id == Member.id
        ).filter(
            Member.candidate_type == "employee"
        ).all()

        return jsonable_encoder([
            {
                "member": member,
                "details": employee
            }
            for member, employee in results
        ])