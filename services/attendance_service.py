"""
Attendance Service (HRMS - Phase 13)
Business logic for attendance management.
"""

from typing import List, Optional, Tuple
from uuid import uuid4
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from core.exceptions import NotFoundException, ValidationException, DuplicateException
from models.attendance_model import Attendance, AttendanceStatus, CheckInOutType
from models.employee_model import Employee
from middlewares.multi_tenancy_middleware import get_tenant_id, get_user_id


class AttendanceService:
    """Service for attendance management."""

    @staticmethod
    def check_in(
        db: Session,
        company_id: str,
        employee_id: str,
        check_in_location: Optional[str] = None,
        check_in_type: str = "web",
        metadata: Optional[dict] = None
    ) -> Attendance:
        """Record employee check-in for today."""
        
        # Verify employee exists
        employee = db.query(Employee).filter(
            Employee.employee_id == employee_id,
            Employee.company_id == company_id
        ).first()
        if not employee:
            raise NotFoundException(f"Employee '{employee_id}' not found")

        # Check if already checked in today
        today = date.today()
        existing = db.query(Attendance).filter(
            Attendance.employee_id == employee_id,
            Attendance.attendance_date == today,
            Attendance.is_deleted == False
        ).first()

        if existing and existing.check_in_time:
            raise ValidationException(f"Employee already checked in at {existing.check_in_time}")

        # Create new attendance record or update existing
        if existing:
            # Update existing record with check-in details
            existing.check_in_time = datetime.utcnow()
            existing.check_in_location = check_in_location
            existing.check_in_type = check_in_type
            existing.status = AttendanceStatus.PRESENT
            existing.metadata = metadata or {}
            existing.updated_by = get_user_id()
            db.commit()
            db.refresh(existing)
            return existing
        else:
            # Create new attendance record
            attendance_id = str(uuid4())
            attendance = Attendance(
                attendance_id=attendance_id,
                company_id=company_id,
                employee_id=employee_id,
                attendance_date=today,
                check_in_time=datetime.utcnow(),
                check_in_location=check_in_location,
                check_in_type=check_in_type,
                status=AttendanceStatus.PRESENT,
                metadata=metadata or {},
                is_approved='N',
                created_by=get_user_id(),
                updated_by=get_user_id()
            )
            db.add(attendance)
            db.commit()
            db.refresh(attendance)
            return attendance

    @staticmethod
    def check_out(
        db: Session,
        company_id: str,
        employee_id: str,
        check_out_location: Optional[str] = None,
        check_out_type: str = "web",
        metadata: Optional[dict] = None
    ) -> Attendance:
        """Record employee check-out for today."""
        
        # Verify employee exists
        employee = db.query(Employee).filter(
            Employee.employee_id == employee_id,
            Employee.company_id == company_id
        ).first()
        if not employee:
            raise NotFoundException(f"Employee '{employee_id}' not found")

        # Get today's attendance record
        today = date.today()
        attendance = db.query(Attendance).filter(
            Attendance.employee_id == employee_id,
            Attendance.attendance_date == today,
            Attendance.is_deleted == False
        ).first()

        if not attendance:
            raise NotFoundException(f"No check-in record found for employee today")

        if not attendance.check_in_time:
            raise ValidationException(f"Employee has not checked in yet")

        if attendance.check_out_time:
            raise ValidationException(f"Employee already checked out at {attendance.check_out_time}")

        # Update checkout details and calculate working hours
        attendance.check_out_time = datetime.utcnow()
        attendance.check_out_location = check_out_location
        attendance.check_out_type = check_out_type
        
        # Calculate working hours
        if attendance.check_in_time:
            duration = attendance.check_out_time - attendance.check_in_time
            hours = duration.total_seconds() / 3600
            attendance.working_hours = f"{hours:.2f}"
        
        attendance.metadata = metadata or {}
        attendance.updated_by = get_user_id()
        
        db.commit()
        db.refresh(attendance)
        return attendance

    @staticmethod
    def mark_attendance(
        db: Session,
        company_id: str,
        employee_id: str,
        attendance_date: date,
        status: str,
        check_in_time: Optional[datetime] = None,
        check_out_time: Optional[datetime] = None,
        reason: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Attendance:
        """Manually mark attendance for a specific date."""
        
        # Verify employee exists
        employee = db.query(Employee).filter(
            Employee.employee_id == employee_id,
            Employee.company_id == company_id
        ).first()
        if not employee:
            raise NotFoundException(f"Employee '{employee_id}' not found")

        # Check for existing record
        existing = db.query(Attendance).filter(
            Attendance.employee_id == employee_id,
            Attendance.attendance_date == attendance_date,
            Attendance.is_deleted == False
        ).first()

        if existing:
            # Update existing record
            existing.status = status
            existing.check_in_time = check_in_time
            existing.check_out_time = check_out_time
            existing.reason = reason
            existing.notes = notes
            existing.updated_by = get_user_id()
            
            # Calculate working hours if both times provided
            if check_in_time and check_out_time:
                duration = check_out_time - check_in_time
                hours = duration.total_seconds() / 3600
                existing.working_hours = f"{hours:.2f}"
            
            db.commit()
            db.refresh(existing)
            return existing
        else:
            # Create new record
            attendance_id = str(uuid4())
            attendance = Attendance(
                attendance_id=attendance_id,
                company_id=company_id,
                employee_id=employee_id,
                attendance_date=attendance_date,
                status=status,
                check_in_time=check_in_time,
                check_out_time=check_out_time,
                reason=reason,
                notes=notes,
                is_approved='N',
                created_by=get_user_id(),
                updated_by=get_user_id()
            )
            
            # Calculate working hours if both times provided
            if check_in_time and check_out_time:
                duration = check_out_time - check_in_time
                hours = duration.total_seconds() / 3600
                attendance.working_hours = f"{hours:.2f}"
            
            db.add(attendance)
            db.commit()
            db.refresh(attendance)
            return attendance

    @staticmethod
    def get_attendance(
        db: Session,
        company_id: str,
        attendance_id: str
    ) -> Attendance:
        """Get attendance record by ID."""
        attendance = db.query(Attendance).filter(
            Attendance.attendance_id == attendance_id,
            Attendance.company_id == company_id,
            Attendance.is_deleted == False
        ).first()

        if not attendance:
            raise NotFoundException(f"Attendance record '{attendance_id}' not found")

        return attendance

    @staticmethod
    def list_attendance(
        db: Session,
        company_id: str,
        employee_id: Optional[str] = None,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        status: Optional[str] = None,
        is_approved: Optional[str] = None,
        skip: int = 0,
        limit: int = 50
    ) -> Tuple[List[Attendance], int]:
        """List attendance records with filtering."""
        query = db.query(Attendance).filter(
            Attendance.company_id == company_id,
            Attendance.is_deleted == False
        )

        if employee_id:
            query = query.filter(Attendance.employee_id == employee_id)

        if from_date:
            query = query.filter(Attendance.attendance_date >= from_date)

        if to_date:
            query = query.filter(Attendance.attendance_date <= to_date)

        if status:
            query = query.filter(Attendance.status == status)

        if is_approved:
            query = query.filter(Attendance.is_approved == is_approved)

        total = query.count()
        records = query.order_by(
            Attendance.attendance_date.desc(),
            Attendance.created_at.desc()
        ).offset(skip).limit(limit).all()

        return records, total

    @staticmethod
    def get_today_attendance(
        db: Session,
        company_id: str,
        employee_id: str
    ) -> Optional[Attendance]:
        """Get today's attendance for an employee."""
        today = date.today()
        return db.query(Attendance).filter(
            Attendance.employee_id == employee_id,
            Attendance.company_id == company_id,
            Attendance.attendance_date == today,
            Attendance.is_deleted == False
        ).first()

    @staticmethod
    def approve_attendance(
        db: Session,
        company_id: str,
        attendance_id: str,
        is_approved: bool,
        notes: Optional[str] = None
    ) -> Attendance:
        """Approve or reject attendance record."""
        attendance = AttendanceService.get_attendance(db, company_id, attendance_id)

        attendance.is_approved = 'Y' if is_approved else 'N'
        attendance.approved_by = get_user_id()
        attendance.approved_at = datetime.utcnow()
        if notes:
            attendance.notes = notes
        attendance.updated_by = get_user_id()

        db.commit()
        db.refresh(attendance)
        return attendance

    @staticmethod
    def get_daily_report(
        db: Session,
        company_id: str,
        report_date: date
    ) -> dict:
        """Generate daily attendance report for company."""
        records = db.query(Attendance).filter(
            Attendance.company_id == company_id,
            Attendance.attendance_date == report_date,
            Attendance.is_deleted == False
        ).all()

        total_records = len(records)
        status_counts = {}
        on_time_count = 0
        late_count = 0

        for record in records:
            # Count by status
            status_counts[record.status] = status_counts.get(record.status, 0) + 1
            
            # Check if on-time (before 10 AM)
            if record.check_in_time:
                check_in_hour = record.check_in_time.hour
                if check_in_hour < 10:
                    on_time_count += 1
                else:
                    late_count += 1

        return {
            "report_date": report_date,
            "total_records": total_records,
            "status_breakdown": status_counts,
            "on_time_count": on_time_count,
            "late_count": late_count,
            "created_at": datetime.utcnow()
        }

    @staticmethod
    def get_employee_attendance_stats(
        db: Session,
        company_id: str,
        employee_id: str,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None
    ) -> dict:
        """Get attendance statistics for an employee."""
        if not from_date:
            from_date = date.today() - timedelta(days=30)
        if not to_date:
            to_date = date.today()

        # Get employee details
        employee = db.query(Employee).filter(
            Employee.employee_id == employee_id,
            Employee.company_id == company_id
        ).first()
        if not employee:
            raise NotFoundException(f"Employee '{employee_id}' not found")

        # Get attendance records
        records = db.query(Attendance).filter(
            Attendance.employee_id == employee_id,
            Attendance.company_id == company_id,
            Attendance.attendance_date >= from_date,
            Attendance.attendance_date <= to_date,
            Attendance.is_deleted == False
        ).all()

        # Calculate statistics
        total_days = (to_date - from_date).days + 1
        present_days = sum(1 for r in records if r.status == AttendanceStatus.PRESENT)
        absent_days = sum(1 for r in records if r.status == AttendanceStatus.ABSENT)
        half_days = sum(1 for r in records if r.status == AttendanceStatus.HALF_DAY)
        leave_days = sum(1 for r in records if r.status in [AttendanceStatus.LEAVE, AttendanceStatus.SICK_LEAVE, AttendanceStatus.MEDICAL_LEAVE])
        wfh_days = sum(1 for r in records if r.status == AttendanceStatus.WORK_FROM_HOME)

        # Calculate average working hours
        total_hours = 0
        records_with_hours = 0
        for r in records:
            if r.working_hours:
                try:
                    total_hours += float(r.working_hours)
                    records_with_hours += 1
                except (ValueError, TypeError):
                    pass

        avg_hours = f"{total_hours / records_with_hours:.2f}" if records_with_hours > 0 else "0"
        attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0

        return {
            "employee_id": employee_id,
            "employee_name": f"{employee.first_name} {employee.last_name}",
            "from_date": from_date,
            "to_date": to_date,
            "total_days": total_days,
            "present_days": present_days,
            "absent_days": absent_days,
            "half_days": half_days,
            "leave_days": leave_days,
            "work_from_home_days": wfh_days,
            "average_working_hours": avg_hours,
            "attendance_percentage": f"{attendance_percentage:.2f}"
        }