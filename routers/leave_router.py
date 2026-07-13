"""
Leave Management Router (HRMS - Phase 14)
REST API endpoints for leave request and balance management.
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from core.database import get_db
from core.response import APIResponse, success_response, error_response
from core.permission import PermissionRequired
from dependencies.dependency import get_current_user
from middlewares.multi_tenancy_middleware import get_tenant_id, get_user_id
from schemas.leave_schema import (
    LeaveRequestCreateRequest,
    LeaveRequestApproveRequest,
    LeaveRequestResponse,
    LeaveRequestListResponse,
    LeaveBalanceResponse,
    EmployeeLeaveBalanceResponse,
    LeaveAnalyticsResponse
)
from services.leave_service import LeaveService
from core.exceptions import NotFoundException, ValidationException

router = APIRouter(
    prefix="/api/v1/leave",
    tags=["Leave Management"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/request", response_model=APIResponse)
@PermissionRequired("leave.apply")
def create_leave_request(
    request: LeaveRequestCreateRequest,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """Create a new leave request."""
    try:
        leave_request = LeaveService.create_leave_request(
            db=db,
            company_id=company_id,
            employee_id=request.employee_id,
            leave_type=request.leave_type,
            start_date=request.start_date,
            end_date=request.end_date,
            reason=request.reason,
            attachments=request.attachments
        )
        return success_response(
            message="Leave request created successfully",
            data=LeaveRequestResponse.from_orm(leave_request),
            status_code=201
        )
    except (NotFoundException, ValidationException) as e:
        return error_response(message=str(e), status_code=e.status_code if hasattr(e, 'status_code') else 400)


@router.get("/request/{leave_request_id}", response_model=APIResponse)
@PermissionRequired("leave.view")
def get_leave_request(
    leave_request_id: str,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """Get a leave request by ID."""
    try:
        leave_request = LeaveService.get_leave_request(db, company_id, leave_request_id)
        return success_response(
            message="Leave request retrieved",
            data=LeaveRequestResponse.from_orm(leave_request)
        )
    except NotFoundException as e:
        return error_response(message=str(e), status_code=404)


@router.get("/requests", response_model=APIResponse)
@PermissionRequired("leave.view")
def list_leave_requests(
    employee_id: str = Query(None),
    status: str = Query(None),
    from_date: date = Query(None),
    to_date: date = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """List leave requests with filtering."""
    try:
        records, total = LeaveService.list_leave_requests(
            db=db,
            company_id=company_id,
            employee_id=employee_id,
            status=status,
            from_date=from_date,
            to_date=to_date,
            skip=skip,
            limit=limit
        )
        
        response_data = LeaveRequestListResponse(
            data=[LeaveRequestResponse.from_orm(r) for r in records],
            total=total,
            skip=skip,
            limit=limit
        )
        
        return success_response(
            message="Leave requests retrieved",
            data=response_data.model_dump()
        )
    except Exception as e:
        return error_response(message=str(e), status_code=500)


@router.post("/request/{leave_request_id}/approve", response_model=APIResponse)
@PermissionRequired("leave.approve")
def approve_leave_request(
    leave_request_id: str,
    request: LeaveRequestApproveRequest,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """Approve or reject a leave request."""
    try:
        leave_request = LeaveService.approve_leave_request(
            db=db,
            company_id=company_id,
            leave_request_id=leave_request_id,
            is_approved=request.is_approved,
            rejection_reason=request.rejection_reason
        )
        return success_response(
            message="Leave request approval processed",
            data=LeaveRequestResponse.from_orm(leave_request)
        )
    except (NotFoundException, ValidationException) as e:
        return error_response(message=str(e), status_code=getattr(e, 'status_code', 400))


@router.post("/request/{leave_request_id}/cancel", response_model=APIResponse)
@PermissionRequired("leave.cancel")
def cancel_leave_request(
    leave_request_id: str,
    reason: str = Query(None),
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """Cancel an approved leave request."""
    try:
        leave_request = LeaveService.cancel_leave_request(
            db=db,
            company_id=company_id,
            leave_request_id=leave_request_id,
            reason=reason
        )
        return success_response(
            message="Leave request cancelled",
            data=LeaveRequestResponse.from_orm(leave_request)
        )
    except (NotFoundException, ValidationException) as e:
        return error_response(message=str(e), status_code=getattr(e, 'status_code', 400))


@router.get("/balance/{employee_id}/{leave_type}/{financial_year}", response_model=APIResponse)
@PermissionRequired("leave.view")
def get_leave_balance(
    employee_id: str,
    leave_type: str,
    financial_year: str,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """Get leave balance for a specific type and financial year."""
    try:
        balance = LeaveService.get_leave_balance(
            db=db,
            company_id=company_id,
            employee_id=employee_id,
            leave_type=leave_type,
            financial_year=financial_year
        )
        return success_response(
            message="Leave balance retrieved",
            data=LeaveBalanceResponse.from_orm(balance)
        )
    except NotFoundException as e:
        return error_response(message=str(e), status_code=404)


@router.get("/balances/{employee_id}", response_model=APIResponse)
@PermissionRequired("leave.view")
def get_employee_leave_balances(
    employee_id: str,
    financial_year: str = Query(None),
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """Get all leave balances for an employee."""
    try:
        balances = LeaveService.get_employee_leave_balances(
            db=db,
            company_id=company_id,
            employee_id=employee_id,
            financial_year=financial_year
        )
        
        response_data = EmployeeLeaveBalanceResponse(
            employee_id=employee_id,
            balances=[LeaveBalanceResponse.from_orm(b) for b in balances]
        )
        
        return success_response(
            message="Employee leave balances retrieved",
            data=response_data.model_dump()
        )
    except Exception as e:
        return error_response(message=str(e), status_code=500)


@router.get("/analytics", response_model=APIResponse)
@PermissionRequired("leave.analytics")
def get_leave_analytics(
    from_date: date = Query(None),
    to_date: date = Query(None),
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """Get leave analytics for the company."""
    try:
        analytics = LeaveService.get_leave_analytics(
            db=db,
            company_id=company_id,
            from_date=from_date,
            to_date=to_date
        )
        return success_response(
            message="Leave analytics retrieved",
            data=analytics
        )
    except Exception as e:
        return error_response(message=str(e), status_code=500)