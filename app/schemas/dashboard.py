from pydantic import BaseModel


class DashboardStatsResponse(BaseModel):
    employees: int
    students: int
    representatives: int

    approved_employees: int
    approved_students: int
    approved_representatives: int

    pending_employees: int
    pending_students: int
    pending_representatives: int