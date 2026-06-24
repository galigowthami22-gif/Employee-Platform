from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.employee_model import Employee

def create_employee(db: Session, payload):
    employee = Employee(**payload.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

def get_employee(db: Session, employee_id: int):
    return (db.query(Employee).filter(Employee.id == employee_id).first())

def get_employees(db: Session):
    return (db.query(Employee).all())

def update_employee(db: Session, employee_id: int, payload):
    employee = get_employee(db, employee_id)
    if not employee:
        return None
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(employee, key, value)
    db.commit()
    db.refresh(employee)
    return employee

def delete_employee(db: Session, employee_id: int):
    employee = get_employee(db, employee_id)
    if not employee:
        return False
    db.delete(employee)
    db.commit()
    return True

def search_employees(db: Session, keyword: str):
    return (db.query(Employee).filter(or_(Employee.first_name.ilike(f"%{keyword}%"), Employee.last_name.ilike(f"%{keyword}%"), Employee.email.ilike(f"%{keyword}%"))).all())

def get_employees_paginated(db: Session, page: int, size: int):
    offset = (page - 1) * size
    return (db.query(Employee).offset(offset).limit(size).all())

def filter_by_department(db: Session, department_id: int):
    return (db.query(Employee).filter(Employee.department_id == department_id).all())

def filter_by_designation(db: Session, designation_id: int):
    return (db.query(Employee).filter(Employee.designation_id == designation_id).all())

def employee_statistics(db: Session):
    total_employees = (db.query(Employee).count())
    active_employees = (db.query(Employee).filter(Employee.is_active == True).count())
    inactive_employees = (db.query(Employee).filter(Employee.is_active == False).count())
    return {"total_employees":total_employees, "active_employees":active_employees, "inactive_employees":inactive_employees}