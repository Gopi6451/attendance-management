from pydantic import BaseModel, EmailStr
from datetime import date


# =========================================================
# EMPLOYEE SCHEMAS
# =========================================================

class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


# =========================================================
# ATTENDANCE SCHEMAS
# =========================================================

class AttendanceCreate(BaseModel):
    employee_id: int
    date: date
    status: str


class AttendanceResponse(BaseModel):
    id: int
    employee_id: int
    date: date
    status: str

    class Config:
        from_attributes = True


# =========================================================
# ATTENDANCE REPORT
# =========================================================

class AttendanceReport(BaseModel):
    employee_id: int
    employee_name: str
    total_days: int
    present: int
    absent: int
    leave: int
    attendance_percentage: float