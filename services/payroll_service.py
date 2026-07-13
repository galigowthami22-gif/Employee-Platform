"""
Payroll Processing Service (HRMS - Phase 15)
Business logic for monthly payroll processing and salary payments.
"""

from typing import List, Optional, Tuple
from uuid import uuid4
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from core.exceptions import NotFoundException, ValidationException
from models.payroll_model import Payroll, PayrollStatus, PaymentMode
from models.employee_model import Employee
from models.salary_structure_model import SalaryStructure
from middlewares.multi_tenancy_middleware import get_tenant_id, get_user_id


class PayrollService:
    """Service for payroll management."""

    @staticmethod
    def create_payroll(
        db: Session,
        company_id: str,
        employee_id: str,
        payroll_month: date,
        working_days: float,
        basic_salary: float,
        days_present: float = 0,
        days_absent: float = 0,
        days_leave: float = 0,
        hra: float = 0,
        conveyance: float = 0,
        medical_allowance: float = 0,
        other_allowances: float = 0,
        bonus: float = 0,
        incentive: float = 0,
        professional_tax: float = 0,
        provident_fund: float = 0,
        insurance: float = 0,
        loan_deduction: float = 0,
        other_deductions: float = 0,
        advance_payment: float = 0,
        notes: Optional[str] = None
    ) -> Payroll:
        """Create a new payroll entry."""
        
        # Verify employee exists
        employee = db.query(Employee).filter(
            Employee.employee_id == employee_id,
            Employee.company_id == company_id
        ).first()
        if not employee:
            raise NotFoundException(f"Employee '{employee_id}' not found")

        # Check for duplicate payroll in same month
        existing = db.query(Payroll).filter(
            Payroll.employee_id == employee_id,
            Payroll.company_id == company_id,
            func.date_trunc('month', Payroll.payroll_month) == func.date_trunc('month', payroll_month),
            Payroll.is_deleted == False
        ).first()

        if existing and existing.status not in [PayrollStatus.DRAFT, PayrollStatus.VOIDED]:
            raise ValidationException(f"Payroll already exists for {payroll_month.strftime('%B %Y')}")

        # Calculate totals
        gross_salary = basic_salary + hra + conveyance + medical_allowance + other_allowances + bonus + incentive
        total_deductions = professional_tax + provident_fund + insurance + loan_deduction + other_deductions
        net_salary = gross_salary - total_deductions
        final_amount = net_salary - advance_payment

        # Create payroll
        payroll_id = str(uuid4())
        payroll = Payroll(
            payroll_id=payroll_id,
            company_id=company_id,
            employee_id=employee_id,
            payroll_month=payroll_month,
            working_days=working_days,
            days_present=days_present,
            days_absent=days_absent,
            days_leave=days_leave,
            basic_salary=basic_salary,
            hra=hra,
            conveyance=conveyance,
            medical_allowance=medical_allowance,
            other_allowances=other_allowances,
            bonus=bonus,
            incentive=incentive,
            gross_salary=gross_salary,
            professional_tax=professional_tax,
            provident_fund=provident_fund,
            insurance=insurance,
            loan_deduction=loan_deduction,
            other_deductions=other_deductions,
            total_deductions=total_deductions,
            net_salary=net_salary,
            advance_payment=advance_payment,
            final_amount=final_amount,
            status=PayrollStatus.DRAFT,
            notes=notes,
            created_by=get_user_id(),
            updated_by=get_user_id()
        )

        db.add(payroll)
        db.commit()
        db.refresh(payroll)
        return payroll

    @staticmethod
    def get_payroll(
        db: Session,
        company_id: str,
        payroll_id: str
    ) -> Payroll:
        """Get payroll entry by ID."""
        payroll = db.query(Payroll).filter(
            Payroll.payroll_id == payroll_id,
            Payroll.company_id == company_id,
            Payroll.is_deleted == False
        ).first()

        if not payroll:
            raise NotFoundException(f"Payroll '{payroll_id}' not found")

        return payroll

    @staticmethod
    def list_payroll(
        db: Session,
        company_id: str,
        employee_id: Optional[str] = None,
        payroll_month: Optional[date] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 50
    ) -> Tuple[List[Payroll], int]:
        """List payroll entries with filtering."""
        query = db.query(Payroll).filter(
            Payroll.company_id == company_id,
            Payroll.is_deleted == False
        )

        if employee_id:
            query = query.filter(Payroll.employee_id == employee_id)

        if payroll_month:
            query = query.filter(
                func.date_trunc('month', Payroll.payroll_month) == func.date_trunc('month', payroll_month)
            )

        if status:
            query = query.filter(Payroll.status == status)

        total = query.count()
        records = query.order_by(
            Payroll.payroll_month.desc(),
            Payroll.created_at.desc()
        ).offset(skip).limit(limit).all()

        return records, total

    @staticmethod
    def approve_payroll(
        db: Session,
        company_id: str,
        payroll_id: str,
        is_approved: bool = True
    ) -> Payroll:
        """Approve or reject payroll."""
        payroll = PayrollService.get_payroll(db, company_id, payroll_id)

        if payroll.status != PayrollStatus.PROCESSED:
            raise ValidationException(f"Cannot approve payroll with status '{payroll.status}'")

        if is_approved:
            payroll.status = PayrollStatus.APPROVED
            payroll.approved_by = get_user_id()
            payroll.approved_at = datetime.utcnow()
        else:
            payroll.status = PayrollStatus.REJECTED

        payroll.updated_by = get_user_id()
        db.commit()
        db.refresh(payroll)
        return payroll

    @staticmethod
    def mark_as_paid(
        db: Session,
        company_id: str,
        payroll_id: str,
        payment_mode: str,
        paid_date: date
    ) -> Payroll:
        """Mark payroll as paid."""
        payroll = PayrollService.get_payroll(db, company_id, payroll_id)

        if payroll.status != PayrollStatus.APPROVED:
            raise ValidationException(f"Only approved payroll can be marked as paid")

        payroll.status = PayrollStatus.PAID
        payroll.payment_mode = payment_mode
        payroll.paid_date = paid_date
        payroll.updated_by = get_user_id()

        db.commit()
        db.refresh(payroll)
        return payroll

    @staticmethod
    def process_bulk_payroll(
        db: Session,
        company_id: str,
        payroll_month: date
    ) -> dict:
        """Process payroll for all employees for a month."""
        payroll_entries = db.query(Payroll).filter(
            Payroll.company_id == company_id,
            func.date_trunc('month', Payroll.payroll_month) == func.date_trunc('month', payroll_month),
            Payroll.status == PayrollStatus.DRAFT,
            Payroll.is_deleted == False
        ).all()

        processed_count = 0
        for payroll in payroll_entries:
            payroll.status = PayrollStatus.PROCESSED
            payroll.updated_by = get_user_id()
            processed_count += 1

        db.commit()

        return {
            "period": payroll_month,
            "total_processed": processed_count,
            "message": f"Successfully processed {processed_count} payroll entries"
        }

    @staticmethod
    def get_payroll_summary(
        db: Session,
        company_id: str,
        payroll_month: date
    ) -> dict:
        """Get payroll summary for a month."""
        payroll_entries = db.query(Payroll).filter(
            Payroll.company_id == company_id,
            func.date_trunc('month', Payroll.payroll_month) == func.date_trunc('month', payroll_month),
            Payroll.is_deleted == False
        ).all()

        summary = {
            "period": payroll_month,
            "total_employees": len(payroll_entries),
            "total_salary": sum(p.gross_salary for p in payroll_entries),
            "total_deductions": sum(p.total_deductions for p in payroll_entries),
            "total_net_salary": sum(p.net_salary for p in payroll_entries),
            "processed_count": len([p for p in payroll_entries if p.status == PayrollStatus.PROCESSED]),
            "approved_count": len([p for p in payroll_entries if p.status == PayrollStatus.APPROVED]),
            "paid_count": len([p for p in payroll_entries if p.status == PayrollStatus.PAID]),
            "pending_count": len([p for p in payroll_entries if p.status in [PayrollStatus.DRAFT, PayrollStatus.PROCESSED]])
        }

        return summary
