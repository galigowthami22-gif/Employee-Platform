"""
Attendance Router (HRMS - Phase 13)
REST API endpoints for attendance management.
"""

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from core.database import get_db
from core.response import APIResponse
from core.permission import PermissionRequired, RoleRequired
from schemas.attendance_schema import (
    AttendanceCheckInRequest, AttendanceCheckOutRequest,
    AttendanceMarkRequest, AttendanceApproveRequest,
    AttendanceResponse, AttendanceListResponse,
    DailyAttendanceReportResponse, EmployeeAttendanceStatsResponse
)
from services.attendance_service import AttendanceService
from core.exceptions import NotFoundException, ValidationException, DuplicateException
from middlewares.multi_tenancy_middleware import get_tenant_id, get_user_id

router = APIRouter(prefix="/api/v1/attendance", tags=["HRMS - Attendance Management"])


# ============================================================================
# CHECK-IN / CHECK-OUT ENDPOINTS
# ============================================================================

@router.post("/check-in", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
@PermissionRequired("attendance.mark")
def check_in(
    request: AttendanceCheckInRequest,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """
    Employee check-in for the day.
    
    Required Permission: attendance.mark
    
    Returns: Attendance record with check-in details
    """
    try:
        attendance = AttendanceService.check_in(
            db=db,
            company_id=company_id,
            employee_id=request.employee_id,
            check_in_location=request.check_in_location,
            check_in_type=request.check_in_type,
            metadata=request.metadata
        )

        return APIResponse(
            success=True,
            message="Check-in recorded successfully",
            data=AttendanceResponse.from_orm(attendance)
        )
    except ValidationException as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
    except NotFoundException as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/check-out", response_model=APIResponse)
@PermissionRequired("attendance.mark")
def check_out(
    request: AttendanceCheckOutRequest,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """
    Employee check-out for the day.
    
    Required Permission: attendance.mark
    
    Returns: Attendance record with check-out details
    """
    try:
        attendance = AttendanceService.check_out(
            db=db,
            company_id=company_id,
            employee_id=request.employee_id,
            check_out_location=request.check_out_location,
            check_out_type=request.check_out_type,
            metadata=request.metadata
        )

        return APIResponse(
            success=True,
            message="Check-out recorded successfully",
            data=AttendanceResponse.from_orm(attendance)
        )
    except ValidationException as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
    except NotFoundException as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================================================
# ATTENDANCE MARKING ENDPOINTS
# ============================================================================

@router.post("/mark", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
@PermissionRequired("attendance.mark")
def mark_attendance(
    request: AttendanceMarkRequest,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """
    Manually mark attendance for a specific date.
    
    Required Permission: attendance.mark (typically HR/Manager)
    
    Returns: Created/Updated attendance record
    """
    try:
        attendance = AttendanceService.mark_attendance(
            db=db,
            company_id=company_id,
            employee_id=request.employee_id,
            attendance_date=request.attendance_date,
            status=request.status,
            check_in_time=request.check_in_time,
            check_out_time=request.check_out_time,
            reason=request.reason,
            notes=request.notes
        )

        return APIResponse(
            success=True,
            message="Attendance marked successfully",
            data=AttendanceResponse.from_orm(attendance)
        )
    except ValidationException as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
    except NotFoundException as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================================================
# ATTENDANCE RETRIEVAL ENDPOINTS
# ============================================================================

@router.get("/{attendance_id}", response_model=APIResponse)
@PermissionRequired("attendance.view")
def get_attendance(
    attendance_id: str,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """
    Get attendance record by ID.
    
    Required Permission: attendance.view
    
    Returns: Attendance details
    """
    try:
        attendance = AttendanceService.get_attendance(
            db=db,
            company_id=company_id,
            attendance_id=attendance_id
        )

        return APIResponse(
            success=True,
            message="Attendance record retrieved",
            data=AttendanceResponse.from_orm(attendance)
        )
    except NotFoundException as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("", response_model=APIResponse)
@PermissionRequired("attendance.view")
def list_attendance(
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id),
    employee_id: Optional[str] = Query(None, description="Filter by employee ID"),
    from_date: Optional[date] = Query(None, description="Filter from date"),
    to_date: Optional[date] = Query(None, description="Filter to date"),
    status: Optional[str] = Query(None, description="Filter by attendance status"),
    is_approved: Optional[str] = Query(None, description="Filter by approval status"),
    skip: int = Query(0, ge=0, description="Skip records"),
    limit: int = Query(50, ge=1, le=500, description="Limit records")
):
    """
    List attendance records with optional filtering.
    
    Required Permission: attendance.view
    
    Query Parameters:
    - employee_id: Filter by specific employee
    - from_date: Filter from date (YYYY-MM-DD)
    - to_date: Filter to date (YYYY-MM-DD)
    - status: Filter by status (present, absent, leave, etc.)
    - is_approved: Filter by approval status (Y/N)
    - skip: Pagination offset
    - limit: Pagination limit
    
    Returns: List of attendance records with pagination info
    """
    try:
        records, total = AttendanceService.list_attendance(
            db=db,
            company_id=company_id,
            employee_id=employee_id,
            from_date=from_date,
            to_date=to_date,
            status=status,
            is_approved=is_approved,
            skip=skip,
            limit=limit
        )

        page = (skip // limit) + 1 if limit > 0 else 1
        return APIResponse(
            success=True,
            message="Attendance records retrieved",
            data=AttendanceListResponse(
                total=total,
                page=page,
                limit=limit,
                records=[AttendanceResponse.from_orm(r) for r in records]
            )
        )
    except Exception as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/employee/{employee_id}/today", response_model=APIResponse)
@PermissionRequired("attendance.view")
def get_today_attendance(
    employee_id: str,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """
    Get today's attendance for an employee.
    
    Required Permission: attendance.view
    
    Returns: Today's attendance record or null if not marked
    """
    try:
        attendance = AttendanceService.get_today_attendance(
            db=db,
            company_id=company_id,
            employee_id=employee_id
        )

        if not attendance:
            return APIResponse(
                success=True,
                message="No attendance record for today",
                data=None
            )

        return APIResponse(
            success=True,
            message="Today's attendance retrieved",
            data=AttendanceResponse.from_orm(attendance)
        )
    except Exception as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================================================
# ATTENDANCE APPROVAL ENDPOINTS
# ============================================================================

@router.post("/{attendance_id}/approve", response_model=APIResponse)
@PermissionRequired("attendance.approve")
def approve_attendance(
    attendance_id: str,
    request: AttendanceApproveRequest,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """
    Approve or reject attendance record.
    
    Required Permission: attendance.approve (Manager/HR)
    
    Returns: Updated attendance record with approval details
    """
    try:
        attendance = AttendanceService.approve_attendance(
            db=db,
            company_id=company_id,
            attendance_id=attendance_id,
            is_approved=request.is_approved,
            notes=request.notes
        )

        return APIResponse(
            success=True,
            message="Attendance approval updated",
            data=AttendanceResponse.from_orm(attendance)
        )
    except NotFoundException as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================================================
# REPORTING ENDPOINTS
# ============================================================================

@router.get("/report/daily", response_model=APIResponse)
@PermissionRequired("attendance.view")
def get_daily_report(
    report_date: Optional[date] = Query(None, description="Report date (default: today)"),
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """
    Generate daily attendance report for the company.
    
    Required Permission: attendance.view
    
    Returns: Daily attendance statistics
    """
    try:
        if not report_date:
            report_date = date.today()

        report = AttendanceService.get_daily_report(
            db=db,
            company_id=company_id,
            report_date=report_date
        )

        return APIResponse(
            success=True,
            message="Daily attendance report generated",
            data=report
        )
    except Exception as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/employee/{employee_id}/stats", response_model=APIResponse)
@PermissionRequired("attendance.view")
def get_employee_stats(
    employee_id: str,
    from_date: Optional[date] = Query(None, description="From date (default: 30 days ago)"),
    to_date: Optional[date] = Query(None, description="To date (default: today)"),
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """
    Get attendance statistics for an employee.
    
    Required Permission: attendance.view
    
    Returns: Employee attendance statistics including present, absent, leave counts and percentage
    """
    try:
        stats = AttendanceService.get_employee_attendance_stats(
            db=db,
            company_id=company_id,
            employee_id=employee_id,
            from_date=from_date,
            to_date=to_date
        )

        return APIResponse(
            success=True,
            message="Employee attendance statistics retrieved",
            data=stats
        )
    except NotFoundException as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)