from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import Employee, Attendance

from schemas import (
    EmployeeCreate,
    EmployeeResponse,
    AttendanceCreate,
    AttendanceResponse,
    AttendanceReport
)


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Attendance Management API",
    description="API for managing employees and attendance",
    version="1.0.0"
)


# =========================================================
# DATABASE DEPENDENCY
# =========================================================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():
    return {
        "message": "Attendance Management API is running"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# =========================================================
# EMPLOYEE CRUD
# =========================================================


# CREATE EMPLOYEE
@app.post(
    "/employees",
    response_model=EmployeeResponse
)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):

    existing_employee = db.query(Employee).filter(
        Employee.email == employee.email
    ).first()

    if existing_employee:
        raise HTTPException(
            status_code=400,
            detail="Employee with this email already exists"
        )

    new_employee = Employee(
        name=employee.name,
        email=employee.email
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


# GET ALL EMPLOYEES
@app.get(
    "/employees",
    response_model=list[EmployeeResponse]
)
def get_employees(
    db: Session = Depends(get_db)
):

    employees = db.query(Employee).all()

    return employees


# GET EMPLOYEE BY ID
@app.get(
    "/employees/{employee_id}",
    response_model=EmployeeResponse
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


# UPDATE EMPLOYEE
@app.put(
    "/employees/{employee_id}",
    response_model=EmployeeResponse
)
def update_employee(
    employee_id: int,
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    existing_email = db.query(Employee).filter(
        Employee.email == employee_data.email,
        Employee.id != employee_id
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Another employee already uses this email"
        )

    employee.name = employee_data.name
    employee.email = employee_data.email

    db.commit()
    db.refresh(employee)

    return employee


# DELETE EMPLOYEE
@app.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    db.delete(employee)
    db.commit()

    return {
        "message": "Employee deleted successfully"
    }


# =========================================================
# ATTENDANCE CRUD
# =========================================================


# MARK ATTENDANCE
@app.post(
    "/attendance",
    response_model=AttendanceResponse
)
def mark_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db)
):

    # Check employee
    employee = db.query(Employee).filter(
        Employee.id == attendance.employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    # Check duplicate attendance
    existing_attendance = db.query(Attendance).filter(
        Attendance.employee_id == attendance.employee_id,
        Attendance.date == attendance.date
    ).first()

    if existing_attendance:
        raise HTTPException(
            status_code=400,
            detail="Attendance already marked for this employee on this date"
        )

    # Validate status
    allowed_statuses = [
        "present",
        "absent",
        "leave"
    ]

    if attendance.status.lower() not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Status must be present, absent, or leave"
        )

    new_attendance = Attendance(
        employee_id=attendance.employee_id,
        date=attendance.date,
        status=attendance.status.lower()
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return new_attendance


# GET ALL ATTENDANCE
@app.get(
    "/attendance",
    response_model=list[AttendanceResponse]
)
def get_attendance(
    db: Session = Depends(get_db)
):

    attendance = db.query(Attendance).all()

    return attendance


# GET EMPLOYEE ATTENDANCE
@app.get(
    "/attendance/{employee_id}",
    response_model=list[AttendanceResponse]
)
def get_employee_attendance(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    attendance = db.query(Attendance).filter(
        Attendance.employee_id == employee_id
    ).all()

    return attendance


# UPDATE ATTENDANCE
@app.put(
    "/attendance/{attendance_id}",
    response_model=AttendanceResponse
)
def update_attendance(
    attendance_id: int,
    status: str,
    db: Session = Depends(get_db)
):

    attendance = db.query(Attendance).filter(
        Attendance.id == attendance_id
    ).first()

    if not attendance:
        raise HTTPException(
            status_code=404,
            detail="Attendance record not found"
        )

    allowed_statuses = [
        "present",
        "absent",
        "leave"
    ]

    if status.lower() not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Status must be present, absent, or leave"
        )

    attendance.status = status.lower()

    db.commit()
    db.refresh(attendance)

    return attendance


# DELETE ATTENDANCE
@app.delete("/attendance/{attendance_id}")
def delete_attendance(
    attendance_id: int,
    db: Session = Depends(get_db)
):

    attendance = db.query(Attendance).filter(
        Attendance.id == attendance_id
    ).first()

    if not attendance:
        raise HTTPException(
            status_code=404,
            detail="Attendance record not found"
        )

    db.delete(attendance)
    db.commit()

    return {
        "message": "Attendance deleted successfully"
    }


# =========================================================
# ATTENDANCE REPORT
# =========================================================

@app.get(
    "/attendance/report/{employee_id}",
    response_model=AttendanceReport
)
def attendance_report(
    employee_id: int,
    db: Session = Depends(get_db)
):

    # Find employee
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    # Get attendance records
    attendance_records = db.query(Attendance).filter(
        Attendance.employee_id == employee_id
    ).all()

    # Total days
    total_days = len(attendance_records)

    # Present
    present = sum(
        1
        for record in attendance_records
        if record.status.lower() == "present"
    )

    # Absent
    absent = sum(
        1
        for record in attendance_records
        if record.status.lower() == "absent"
    )

    # Leave
    leave = sum(
        1
        for record in attendance_records
        if record.status.lower() == "leave"
    )

    # Attendance percentage
    if total_days > 0:
        attendance_percentage = round(
            (present / total_days) * 100,
            2
        )
    else:
        attendance_percentage = 0.0

    return AttendanceReport(
        employee_id=employee.id,
        employee_name=employee.name,
        total_days=total_days,
        present=present,
        absent=absent,
        leave=leave,
        attendance_percentage=attendance_percentage
    )

    