"""
Employee Service (HRMS - Phase 12)
Business logic for employee management.
"""

from typing import List, Optional
from uuid import uuid4
from sqlalchemy.orm import Session
from datetime import datetime
from core.exceptions import NotFoundException, ValidationException, DuplicateException
from models.employee_model import Employee, Designation, EmploymentStatus
from middlewares.multi_tenancy_middleware import get_tenant_id, get_user_id


class EmployeeService:
    """Service for employee management."""

    @staticmethod
    def create_employee(
        db: Session,
        company_id: str,
        employee_code: str,
        first_name: str,
        last_name: str,
        email: str,
        date_of_joining,
        **kwargs
    ) -> Employee:
        """Create a new employee."""
        # Check for duplicate employee code
        existing_code = db.query(Employee).filter(
            Employee.company_id == company_id,
            Employee.employee_code == employee_code
        ).first()
        if existing_code:
            raise DuplicateException(f"Employee code '{employee_code}' already exists")

        # Check for duplicate email
        existing_email = db.query(Employee).filter(
            Employee.company_id == company_id,
            Employee.email == email
        ).first()
        if existing_email:
            raise DuplicateException(f"Email '{email}' already exists in company")

        employee_id = str(uuid4())
        created_by = get_user_id()

        employee = Employee(
            employee_id=employee_id,
            company_id=company_id,
            employee_code=employee_code,
            first_name=first_name,
            last_name=last_name,
            email=email,
            date_of_joining=date_of_joining,
            created_by=created_by,
            updated_by=created_by,
            **kwargs
        )

        db.add(employee)
        db.commit()
        db.refresh(employee)

        return employee

    @staticmethod
    def get_employee(db: Session, employee_id: str, company_id: Optional[str] = None) -> Employee:
        """Get employee by ID."""
        query = db.query(Employee).filter(Employee.employee_id == employee_id)

        if company_id:
            query = query.filter(Employee.company_id == company_id)

        employee = query.first()
        if not employee:
            raise NotFoundException(f"Employee with ID '{employee_id}' not found")

        return employee

    @staticmethod
    def get_employee_by_code(db: Session, company_id: str, employee_code: str) -> Employee:
        """Get employee by code."""
        employee = db.query(Employee).filter(
            Employee.company_id == company_id,
            Employee.employee_code == employee_code
        ).first()

        if not employee:
            raise NotFoundException(f"Employee with code '{employee_code}' not found")

        return employee

    @staticmethod
    def get_employee_by_email(db: Session, company_id: str, email: str) -> Employee:
        """Get employee by email."""
        employee = db.query(Employee).filter(
            Employee.company_id == company_id,
            Employee.email == email
        ).first()

        if not employee:
            raise NotFoundException(f"Employee with email '{email}' not found")

        return employee

    @staticmethod
    def list_employees(
        db: Session,
        company_id: str,
        department_id: Optional[str] = None,
        employment_status: Optional[str] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 10
    ) -> tuple[List[Employee], int]:
        """List employees with filtering."""
        query = db.query(Employee).filter(Employee.company_id == company_id)

        if department_id:
            query = query.filter(Employee.department_id == department_id)

        if employment_status:
            query = query.filter(Employee.employment_status == employment_status)

        if is_active is not None:
            query = query.filter(Employee.is_active == is_active)

        total = query.count()
        employees = query.order_by(Employee.created_at.desc()).offset(skip).limit(limit).all()

        return employees, total

    @staticmethod
    def update_employee(
        db: Session,
        employee_id: str,
        company_id: str,
        **kwargs
    ) -> Employee:
        """Update employee."""
        employee = EmployeeService.get_employee(db, employee_id, company_id)

        # Check for email duplicate if updating email
        if "email" in kwargs and kwargs["email"] != employee.email:
            existing = db.query(Employee).filter(
                Employee.company_id == company_id,
                Employee.email == kwargs["email"],
                Employee.employee_id != employee_id
            ).first()
            if existing:
                raise DuplicateException(f"Email '{kwargs['email']}' already exists")

        updated_by = get_user_id()
        kwargs["updated_by"] = updated_by
        kwargs["updated_at"] = datetime.utcnow()

        for key, value in kwargs.items():
            if hasattr(employee, key) and value is not None:
                setattr(employee, key, value)

        db.commit()
        db.refresh(employee)

        return employee

    @staticmethod
    def deactivate_employee(
        db: Session,
        employee_id: str,
        company_id: str,
        date_of_separation=None
    ) -> Employee:
        """Deactivate employee (termination/resignation)."""
        employee = EmployeeService.get_employee(db, employee_id, company_id)

        updates = {
            "is_active": False,
            "employment_status": EmploymentStatus.TERMINATED,
            "date_of_separation": date_of_separation or datetime.utcnow().date(),
            "updated_by": get_user_id(),
            "updated_at": datetime.utcnow()
        }

        for key, value in updates.items():
            setattr(employee, key, value)

        db.commit()
        db.refresh(employee)

        return employee

    @staticmethod
    def get_manager_subordinates(
        db: Session,
        manager_id: str,
        company_id: str
    ) -> List[Employee]:
        """Get all subordinates of a manager."""
        subordinates = db.query(Employee).filter(
            Employee.company_id == company_id,
            Employee.manager_id == manager_id,
            Employee.is_active == True
        ).all()

        return subordinates

    @staticmethod
    def get_department_employees(
        db: Session,
        department_id: str,
        company_id: str
    ) -> List[Employee]:
        """Get all employees in a department."""
        employees = db.query(Employee).filter(
            Employee.company_id == company_id,
            Employee.department_id == department_id,
            Employee.is_active == True
        ).all()

        return employees


class DesignationService:
    """Service for designation management."""

    @staticmethod
    def create_designation(
        db: Session,
        company_id: str,
        code: str,
        name: str,
        **kwargs
    ) -> Designation:
        """Create a new designation."""
        # Check for duplicate code in company
        existing = db.query(Designation).filter(
            Designation.company_id == company_id,
            Designation.code == code
        ).first()
        if existing:
            raise DuplicateException(f"Designation code '{code}' already exists in company")

        designation_id = str(uuid4())
        created_by = get_user_id()

        designation = Designation(
            designation_id=designation_id,
            company_id=company_id,
            code=code,
            name=name,
            created_by=created_by,
            updated_by=created_by,
            **kwargs
        )

        db.add(designation)
        db.commit()
        db.refresh(designation)

        return designation

    @staticmethod
    def get_designation(
        db: Session,
        designation_id: str,
        company_id: Optional[str] = None
    ) -> Designation:
        """Get designation by ID."""
        query = db.query(Designation).filter(Designation.designation_id == designation_id)

        if company_id:
            query = query.filter(Designation.company_id == company_id)

        designation = query.first()
        if not designation:
            raise NotFoundException(f"Designation with ID '{designation_id}' not found")

        return designation

    @staticmethod
    def get_designation_by_code(db: Session, company_id: str, code: str) -> Designation:
        """Get designation by code."""
        designation = db.query(Designation).filter(
            Designation.company_id == company_id,
            Designation.code == code
        ).first()

        if not designation:
            raise NotFoundException(f"Designation with code '{code}' not found")

        return designation

    @staticmethod
    def list_designations(
        db: Session,
        company_id: str,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 10
    ) -> tuple[List[Designation], int]:
        """List designations."""
        query = db.query(Designation).filter(Designation.company_id == company_id)

        if is_active is not None:
            query = query.filter(Designation.is_active == is_active)

        total = query.count()
        designations = query.order_by(Designation.level, Designation.name).offset(skip).limit(limit).all()

        return designations, total

    @staticmethod
    def update_designation(
        db: Session,
        designation_id: str,
        company_id: str,
        **kwargs
    ) -> Designation:
        """Update designation."""
        designation = DesignationService.get_designation(db, designation_id, company_id)

        # Check for code duplicate if updating code
        if "code" in kwargs and kwargs["code"] != designation.code:
            existing = db.query(Designation).filter(
                Designation.company_id == company_id,
                Designation.code == kwargs["code"],
                Designation.designation_id != designation_id
            ).first()
            if existing:
                raise DuplicateException(f"Designation code '{kwargs['code']}' already exists")

        updated_by = get_user_id()
        kwargs["updated_by"] = updated_by
        kwargs["updated_at"] = datetime.utcnow()

        for key, value in kwargs.items():
            if hasattr(designation, key) and value is not None:
                setattr(designation, key, value)

        db.commit()
        db.refresh(designation)

        return designation

    @staticmethod
    def delete_designation(db: Session, designation_id: str, company_id: str) -> None:
        """Soft delete designation."""
        designation = DesignationService.get_designation(db, designation_id, company_id)
        designation.is_active = False
        designation.updated_by = get_user_id()
        designation.updated_at = datetime.utcnow()
        db.commit()

    @staticmethod
    def get_designation_count(db: Session, company_id: str) -> int:
        """Get total active designations in company."""
        count = db.query(Designation).filter(
            Designation.company_id == company_id,
            Designation.is_active == True
        ).count()

        return count


class EmployeeDashboardService:
    """Helpers for employee dashboard statistics."""

    @staticmethod
    def get_employee_counts(db: Session, company_id: str) -> dict:
        """Get employee counts for a company."""
        total_employees = db.query(Employee).filter(Employee.company_id == company_id).count()
        active_employees = db.query(Employee).filter(
            Employee.company_id == company_id,
            Employee.is_active == True
        ).count()
        inactive_employees = db.query(Employee).filter(
            Employee.company_id == company_id,
            Employee.is_active == False
        ).count()

        return {
            "total_employees": total_employees,
            "active_employees": active_employees,
            "inactive_employees": inactive_employees,
        }