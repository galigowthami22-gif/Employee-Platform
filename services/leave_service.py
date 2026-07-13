"""
Leave Management Service (HRMS - Phase 14)
Business logic for leave request and balance management.
"""

from typing import List, Optional, Tuple
from uuid import uuid4
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from core.exceptions import NotFoundException, ValidationException, DuplicateException
from models.leave_model import LeaveRequest, LeaveBalance, LeaveStatus, LeaveType
from models.employee_model import Employee
from middlewares.multi_tenancy_middleware import get_tenant_id, get_user_id


class LeaveService:
    """Service for leave management."""

    @staticmethod
    def create_leave_request(
        db: Session,
        company_id: str,
        employee_id: str,
        leave_type: str,
        start_date: date,
        end_date: date,
        reason: Optional[str] = None,
        attachments: Optional[list] = None
    ) -> LeaveRequest:
        """Create a new leave request."""
        
        # Verify employee exists
        employee = db.query(Employee).filter(
            Employee.employee_id == employee_id,
            Employee.company_id == company_id
        ).first()
        if not employee:
            raise NotFoundException(f"Employee '{employee_id}' not found")

        # Validate dates
        if end_date < start_date:
            raise ValidationException("End date cannot be before start date")

        # Check for overlapping requests
        existing = db.query(LeaveRequest).filter(
            LeaveRequest.employee_id == employee_id,
            LeaveRequest.company_id == company_id,
            LeaveRequest.status.in_([LeaveStatus.PENDING, LeaveStatus.APPROVED]),
            LeaveRequest.is_deleted == False,
            LeaveRequest.start_date <= end_date,
            LeaveRequest.end_date >= start_date
        ).first()

        if existing:
            raise ValidationException("Overlapping leave request exists")

        # Calculate days
        days = (end_date - start_date).days + 1

        # Create request
        request_id = str(uuid4())
        leave_request = LeaveRequest(
            leave_request_id=request_id,
            company_id=company_id,
            employee_id=employee_id,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            days_requested=days,
            reason=reason,
            attachments=attachments,
            status=LeaveStatus.PENDING,
            created_by=get_user_id(),
            updated_by=get_user_id()
        )

        db.add(leave_request)
        db.commit()
        db.refresh(leave_request)
        return leave_request

    @staticmethod
    def get_leave_request(
        db: Session,
        company_id: str,
        leave_request_id: str
    ) -> LeaveRequest:
        """Get leave request by ID."""
        request = db.query(LeaveRequest).filter(
            LeaveRequest.leave_request_id == leave_request_id,
            LeaveRequest.company_id == company_id,
            LeaveRequest.is_deleted == False
        ).first()

        if not request:
            raise NotFoundException(f"Leave request '{leave_request_id}' not found")

        return request

    @staticmethod
    def list_leave_requests(
        db: Session,
        company_id: str,
        employee_id: Optional[str] = None,
        status: Optional[str] = None,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 50
    ) -> Tuple[List[LeaveRequest], int]:
        """List leave requests with filtering."""
        query = db.query(LeaveRequest).filter(
            LeaveRequest.company_id == company_id,
            LeaveRequest.is_deleted == False
        )

        if employee_id:
            query = query.filter(LeaveRequest.employee_id == employee_id)

        if status:
            query = query.filter(LeaveRequest.status == status)

        if from_date:
            query = query.filter(LeaveRequest.end_date >= from_date)

        if to_date:
            query = query.filter(LeaveRequest.start_date <= to_date)

        total = query.count()
        records = query.order_by(
            LeaveRequest.created_at.desc()
        ).offset(skip).limit(limit).all()

        return records, total

    @staticmethod
    def approve_leave_request(
        db: Session,
        company_id: str,
        leave_request_id: str,
        is_approved: bool,
        rejection_reason: Optional[str] = None
    ) -> LeaveRequest:
        """Approve or reject a leave request."""
        request = LeaveService.get_leave_request(db, company_id, leave_request_id)

        if request.status not in [LeaveStatus.PENDING, LeaveStatus.DRAFT]:
            raise ValidationException(f"Cannot approve request with status '{request.status}'")

        if is_approved:
            request.status = LeaveStatus.APPROVED
            request.approved_by = get_user_id()
            request.approved_at = datetime.utcnow()
        else:
            request.status = LeaveStatus.REJECTED
            request.rejection_reason = rejection_reason
            request.rejected_at = datetime.utcnow()

        request.updated_by = get_user_id()
        db.commit()
        db.refresh(request)
        return request

    @staticmethod
    def cancel_leave_request(
        db: Session,
        company_id: str,
        leave_request_id: str,
        reason: Optional[str] = None
    ) -> LeaveRequest:
        """Cancel an approved leave request."""
        request = LeaveService.get_leave_request(db, company_id, leave_request_id)

        if request.status != LeaveStatus.APPROVED:
            raise ValidationException("Only approved requests can be cancelled")

        request.status = LeaveStatus.CANCELLED
        if reason:
            request.notes = reason
        request.updated_by = get_user_id()
        
        db.commit()
        db.refresh(request)
        return request

    @staticmethod
    def get_leave_balance(
        db: Session,
        company_id: str,
        employee_id: str,
        leave_type: str,
        financial_year: str
    ) -> LeaveBalance:
        """Get leave balance for an employee."""
        balance = db.query(LeaveBalance).filter(
            LeaveBalance.employee_id == employee_id,
            LeaveBalance.company_id == company_id,
            LeaveBalance.leave_type == leave_type,
            LeaveBalance.financial_year == financial_year
        ).first()

        if not balance:
            raise NotFoundException(f"Leave balance not found for {leave_type} in {financial_year}")

        return balance

    @staticmethod
    def get_employee_leave_balances(
        db: Session,
        company_id: str,
        employee_id: str,
        financial_year: Optional[str] = None
    ) -> List[LeaveBalance]:
        """Get all leave balances for an employee."""
        query = db.query(LeaveBalance).filter(
            LeaveBalance.employee_id == employee_id,
            LeaveBalance.company_id == company_id
        )

        if financial_year:
            query = query.filter(LeaveBalance.financial_year == financial_year)

        return query.all()

    @staticmethod
    def update_leave_balance(
        db: Session,
        company_id: str,
        employee_id: str,
        leave_type: str,
        financial_year: str,
        days_used: int
    ) -> LeaveBalance:
        """Update leave balance after approval."""
        balance = db.query(LeaveBalance).filter(
            LeaveBalance.employee_id == employee_id,
            LeaveBalance.company_id == company_id,
            LeaveBalance.leave_type == leave_type,
            LeaveBalance.financial_year == financial_year
        ).first()

        if not balance:
            raise NotFoundException("Leave balance not found")

        balance.used += days_used
        balance.balance = balance.total_allocated - balance.used
        balance.last_updated = datetime.utcnow()

        db.commit()
        db.refresh(balance)
        return balance

    @staticmethod
    def get_leave_analytics(
        db: Session,
        company_id: str,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None
    ) -> dict:
        """Generate leave analytics."""
        if not from_date:
            from_date = date.today() - timedelta(days=30)
        if not to_date:
            to_date = date.today()

        query = db.query(LeaveRequest).filter(
            LeaveRequest.company_id == company_id,
            LeaveRequest.is_deleted == False,
            LeaveRequest.start_date >= from_date,
            LeaveRequest.end_date <= to_date
        )

        total_requests = query.count()
        approved = query.filter(LeaveRequest.status == LeaveStatus.APPROVED).count()
        pending = query.filter(LeaveRequest.status == LeaveStatus.PENDING).count()
        rejected = query.filter(LeaveRequest.status == LeaveStatus.REJECTED).count()

        # Most used leave type
        leave_types = db.query(
            LeaveRequest.leave_type,
            func.count(LeaveRequest.leave_request_id).label('count')
        ).filter(
            LeaveRequest.company_id == company_id,
            LeaveRequest.status == LeaveStatus.APPROVED,
            LeaveRequest.is_deleted == False
        ).group_by(LeaveRequest.leave_type).order_by(func.count(LeaveRequest.leave_request_id).desc()).first()

        most_used = leave_types[0] if leave_types else "N/A"

        # Employee count
        employees = db.query(func.count(LeaveRequest.employee_id.distinct())).filter(
            LeaveRequest.company_id == company_id,
            LeaveRequest.is_deleted == False
        ).scalar() or 1

        return {
            "period": f"{from_date} to {to_date}",
            "total_leave_requests": total_requests,
            "approved": approved,
            "pending": pending,
            "rejected": rejected,
            "average_leave_per_employee": total_requests / employees if employees > 0 else 0,
            "most_used_leave_type": most_used
        }