"""
Salary Structure Service (HRMS - Phase 15)
Business logic for managing employee salary structures.
"""

from typing import List, Optional
from uuid import uuid4
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from core.exceptions import NotFoundException, ValidationException, DuplicateException
from models.salary_structure_model import SalaryStructure
from models.employee_model import Employee
from middlewares.multi_tenancy_middleware import get_tenant_id, get_user_id


class SalaryStructureService:
    """Service for salary structure management."""

    @staticmethod
    def create_salary_structure(
        db: Session,
        company_id: str,
        employee_id: str,
        effective_from: date,
        ctc: float,
        basic_salary: float,
        hra: float = 0,
        conveyance: float = 0,
        medical_allowance: float = 0,
        other_allowances: float = 0,
        professional_tax: float = 0,
        provident_fund: float = 0,
        insurance: float = 0,
        other_deductions: float = 0,
        effective_to: Optional[date] = None,
        frequency: str = "monthly",
        currency: str = "USD",
        notes: Optional[str] = None
    ) -> SalaryStructure:
        """Create a new salary structure."""
        
        # Verify employee exists
        employee = db.query(Employee).filter(
            Employee.employee_id == employee_id,
            Employee.company_id == company_id
        ).first()
        if not employee:
            raise NotFoundException(f"Employee '{employee_id}' not found")

        # Mark previous active structure as inactive
        existing_active = db.query(SalaryStructure).filter(
            SalaryStructure.employee_id == employee_id,
            SalaryStructure.company_id == company_id,
            SalaryStructure.effective_to == None
        ).first()

        if existing_active:
            existing_active.effective_to = effective_from - timedelta(days=1)
            existing_active.updated_by = get_user_id()

        # Calculate gross and net
        gross_salary = basic_salary + hra + conveyance + medical_allowance + other_allowances
        total_deductions = professional_tax + provident_fund + insurance + other_deductions
        net_salary = gross_salary - total_deductions

        # Create new structure
        structure_id = str(uuid4())
        structure = SalaryStructure(
            structure_id=structure_id,
            company_id=company_id,
            employee_id=employee_id,
            effective_from=effective_from,
            effective_to=effective_to,
            ctc=ctc,
            basic_salary=basic_salary,
            hra=hra,
            conveyance=conveyance,
            medical_allowance=medical_allowance,
            other_allowances=other_allowances,
            gross_salary=gross_salary,
            professional_tax=professional_tax,
            provident_fund=provident_fund,
            insurance=insurance,
            other_deductions=other_deductions,
            net_salary=net_salary,
            frequency=frequency,
            currency=currency,
            notes=notes,
            created_by=get_user_id(),
            updated_by=get_user_id()
        )

        db.add(structure)
        db.commit()
        db.refresh(structure)
        return structure

    @staticmethod
    def get_active_salary_structure(
        db: Session,
        company_id: str,
        employee_id: str
    ) -> Optional[SalaryStructure]:
        """Get active salary structure for an employee."""
        structure = db.query(SalaryStructure).filter(
            SalaryStructure.employee_id == employee_id,
            SalaryStructure.company_id == company_id,
            SalaryStructure.effective_to == None
        ).first()

        return structure

    @staticmethod
    def get_salary_structure_history(
        db: Session,
        company_id: str,
        employee_id: str
    ) -> List[SalaryStructure]:
        """Get salary structure history for an employee."""
        structures = db.query(SalaryStructure).filter(
            SalaryStructure.employee_id == employee_id,
            SalaryStructure.company_id == company_id
        ).order_by(SalaryStructure.effective_from.desc()).all()

        return structures

    @staticmethod
    def get_salary_structure(
        db: Session,
        company_id: str,
        structure_id: str
    ) -> SalaryStructure:
        """Get salary structure by ID."""
        structure = db.query(SalaryStructure).filter(
            SalaryStructure.structure_id == structure_id,
            SalaryStructure.company_id == company_id
        ).first()

        if not structure:
            raise NotFoundException(f"Salary structure '{structure_id}' not found")

        return structure

    @staticmethod
    def list_salary_structures(
        db: Session,
        company_id: str,
        employee_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 50
    ) -> tuple[List[SalaryStructure], int]:
        """List salary structures."""
        query = db.query(SalaryStructure).filter(SalaryStructure.company_id == company_id)

        if employee_id:
            query = query.filter(SalaryStructure.employee_id == employee_id)

        total = query.count()
        records = query.order_by(
            SalaryStructure.effective_from.desc()
        ).offset(skip).limit(limit).all()

        return records, total