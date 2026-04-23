from sqlalchemy.orm import Session
from app.models.employee import EmployeeDetails


class EmployeeRepository:

    @staticmethod
    def create(db: Session, payload: dict):
        employee = EmployeeDetails(**payload)

        db.add(employee)
        db.commit()
        db.refresh(employee)

        return employee