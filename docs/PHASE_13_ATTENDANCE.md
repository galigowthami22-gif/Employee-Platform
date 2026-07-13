# Phase 13: Attendance Management System

## Overview

Phase 13 implements a comprehensive attendance management system for the ERP platform. This module tracks employee attendance with check-in/check-out functionality, status marking, approval workflows, and detailed reporting capabilities.

## Key Features

### 1. **Check-In/Check-Out System**
- Real-time employee check-in and check-out recording
- Support for multiple check-in methods (biometric, web, mobile, manual, API)
- Location and device tracking
- Automatic working hours calculation

### 2. **Attendance Status Management**
- Multiple status types: Present, Absent, Leave, Half Day, Work From Home, Holiday, Sick Leave, Medical Leave, Compensatory Off, Emergency Leave
- Flexible status marking for different scenarios
- Reason and notes for non-standard attendance

### 3. **Approval Workflow**
- Manager approval/verification of attendance
- Approval tracking with timestamp and approver details
- Audit trail of all changes

### 4. **Reporting & Analytics**
- Daily attendance reports by company
- Employee-level attendance statistics
- On-time vs. late tracking
- Attendance percentage calculations
- Custom date range reporting

### 5. **Multi-Tenancy & Security**
- Complete multi-tenancy support via company_id
- Role-based permission control
- Soft delete for data retention compliance
- Comprehensive audit logging

## Database Schema

### Attendance Table

```sql
CREATE TABLE attendance (
    attendance_id VARCHAR(36) PRIMARY KEY,
    company_id VARCHAR(36) NOT NULL,
    employee_id VARCHAR(36) NOT NULL,
    attendance_date DATE NOT NULL,
    
    -- Check-in Details
    check_in_time DATETIME,
    check_in_location VARCHAR(255),
    check_in_type ENUM('biometric', 'web', 'mobile', 'manual', 'api'),
    
    -- Check-out Details
    check_out_time DATETIME,
    check_out_location VARCHAR(255),
    check_out_type ENUM('biometric', 'web', 'mobile', 'manual', 'api'),
    
    -- Status & Duration
    status ENUM('present', 'absent', 'leave', 'half_day', 'work_from_home', 
                'holiday', 'sick_leave', 'medical_leave', 'compensatory_off', 
                'emergency_leave') NOT NULL DEFAULT 'absent',
    working_hours VARCHAR(10),
    is_early_checkout CHAR(1) DEFAULT 'N',
    
    -- Notes & Metadata
    notes TEXT,
    reason VARCHAR(255),
    metadata JSON,
    
    -- Approval Information
    approved_by VARCHAR(36),
    approved_at DATETIME,
    is_approved CHAR(1) DEFAULT 'N',
    
    -- Soft Delete & Audit
    is_deleted BOOLEAN DEFAULT 0,
    deleted_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    
    FOREIGN KEY (company_id) REFERENCES companies(company_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    INDEX idx_attendance_company_employee (company_id, employee_id),
    INDEX idx_attendance_company_date (company_id, attendance_date),
    INDEX idx_attendance_employee_date (employee_id, attendance_date),
    INDEX idx_attendance_status (status),
    INDEX idx_attendance_is_deleted (is_deleted),
    INDEX idx_attendance_approved (is_approved)
);
```

### Key Indexes
- **idx_attendance_company_employee**: Fast lookup by company and employee
- **idx_attendance_company_date**: Daily report generation
- **idx_attendance_employee_date**: Employee attendance history
- **idx_attendance_status**: Status-based filtering and reporting
- **idx_attendance_is_deleted**: Soft delete filtering
- **idx_attendance_approved**: Approval status filtering

## API Endpoints

### Check-In/Check-Out Operations

#### 1. Employee Check-In
```
POST /api/v1/attendance/check-in
Permission: attendance.mark

Request:
{
    "employee_id": "emp-001",
    "check_in_location": "Office Main Gate",
    "check_in_type": "biometric",
    "metadata": {"device_id": "bio-001"}
}

Response:
{
    "success": true,
    "message": "Check-in recorded successfully",
    "data": {
        "attendance_id": "att-001",
        "company_id": "comp-001",
        "employee_id": "emp-001",
        "attendance_date": "2026-07-08",
        "check_in_time": "2026-07-08T09:15:00",
        "check_in_location": "Office Main Gate",
        "status": "present",
        ...
    }
}
```

#### 2. Employee Check-Out
```
POST /api/v1/attendance/check-out
Permission: attendance.mark

Request:
{
    "employee_id": "emp-001",
    "check_out_location": "Office Main Gate",
    "check_out_type": "biometric",
    "metadata": {"device_id": "bio-001"}
}

Response:
{
    "success": true,
    "message": "Check-out recorded successfully",
    "data": {
        "attendance_id": "att-001",
        "check_out_time": "2026-07-08T17:30:00",
        "working_hours": "8.25",
        ...
    }
}
```

### Attendance Marking

#### 3. Mark Attendance (Manual)
```
POST /api/v1/attendance/mark
Permission: attendance.mark

Request:
{
    "employee_id": "emp-001",
    "attendance_date": "2026-07-08",
    "status": "present",
    "check_in_time": "2026-07-08T09:00:00",
    "check_out_time": "2026-07-08T17:30:00",
    "reason": "Regular attendance"
}

Response:
{
    "success": true,
    "message": "Attendance marked successfully",
    "data": {...}
}
```

### Attendance Retrieval

#### 4. Get Attendance Record
```
GET /api/v1/attendance/{attendance_id}
Permission: attendance.view

Response:
{
    "success": true,
    "message": "Attendance record retrieved",
    "data": {...}
}
```

#### 5. List Attendance Records
```
GET /api/v1/attendance?employee_id=emp-001&from_date=2026-07-01&to_date=2026-07-31&status=present&skip=0&limit=50
Permission: attendance.view

Query Parameters:
- employee_id: Filter by employee (optional)
- from_date: Filter from date (YYYY-MM-DD, optional)
- to_date: Filter to date (YYYY-MM-DD, optional)
- status: Filter by status (optional)
- is_approved: Filter by approval status Y/N (optional)
- skip: Pagination offset (default: 0)
- limit: Pagination limit (default: 50, max: 500)

Response:
{
    "success": true,
    "message": "Attendance records retrieved",
    "data": {
        "total": 100,
        "page": 1,
        "limit": 50,
        "records": [...]
    }
}
```

#### 6. Get Today's Attendance
```
GET /api/v1/attendance/employee/{employee_id}/today
Permission: attendance.view

Response:
{
    "success": true,
    "message": "Today's attendance retrieved",
    "data": {...}
}
```

### Approval Operations

#### 7. Approve/Reject Attendance
```
POST /api/v1/attendance/{attendance_id}/approve
Permission: attendance.approve

Request:
{
    "is_approved": true,
    "notes": "Approved by manager"
}

Response:
{
    "success": true,
    "message": "Attendance approval updated",
    "data": {
        "is_approved": "Y",
        "approved_by": "mgr-001",
        "approved_at": "2026-07-08T18:00:00",
        ...
    }
}
```

### Reporting

#### 8. Daily Attendance Report
```
GET /api/v1/attendance/report/daily?report_date=2026-07-08
Permission: attendance.view

Response:
{
    "success": true,
    "message": "Daily attendance report generated",
    "data": {
        "report_date": "2026-07-08",
        "total_records": 50,
        "status_breakdown": {
            "present": 45,
            "absent": 3,
            "half_day": 1,
            "work_from_home": 1
        },
        "on_time_count": 40,
        "late_count": 5,
        "created_at": "2026-07-08T23:59:00"
    }
}
```

#### 9. Employee Attendance Statistics
```
GET /api/v1/attendance/employee/{employee_id}/stats?from_date=2026-06-08&to_date=2026-07-08
Permission: attendance.view

Response:
{
    "success": true,
    "message": "Employee attendance statistics retrieved",
    "data": {
        "employee_id": "emp-001",
        "employee_name": "John Doe",
        "from_date": "2026-06-08",
        "to_date": "2026-07-08",
        "total_days": 30,
        "present_days": 27,
        "absent_days": 1,
        "half_days": 1,
        "leave_days": 1,
        "work_from_home_days": 0,
        "average_working_hours": "8.45",
        "attendance_percentage": "90.00"
    }
}
```

## Permissions

The attendance module uses the following permissions:

| Permission Code | Name | Description | Role(s) |
|---|---|---|---|
| `attendance.mark` | Mark Attendance | Record check-in/check-out or mark attendance | Employee, Manager, HR |
| `attendance.approve` | Approve Attendance | Verify/approve attendance records | Manager, HR Manager, Admin |
| `attendance.view` | View Attendance | View attendance records and reports | All authorized users |

## Business Logic

### Check-In Flow
1. Employee initiates check-in via web/mobile/biometric
2. System validates employee exists and hasn't checked in today
3. Creates/updates attendance record with check-in time
4. Calculates working hours when check-out happens
5. Sets status to "present" automatically

### Check-Out Flow
1. Employee initiates check-out
2. System validates employee has checked in today
3. Updates attendance record with check-out time
4. Automatically calculates working hours (duration between check-in and check-out)
5. Flags early checkouts if before standard hours

### Attendance Status Determination
- **Present**: Standard working day (automatic when check-in recorded)
- **Absent**: No check-in recorded for the day
- **Leave**: Manually marked by HR/Manager
- **Half Day**: Marked for partial working days
- **Work From Home**: Remote working
- **Holiday**: Company holiday
- **Sick/Medical Leave**: Specific leave types
- **Compensatory Off**: Time-off in lieu
- **Emergency Leave**: Unplanned urgent leave

### Working Hours Calculation
```
Working Hours = Check-out Time - Check-in Time
```
Stored as decimal hours (e.g., "8.25" = 8 hours 15 minutes)

### Approval Workflow
1. Attendance records can be auto-approved based on company policy
2. Or require manual approval by manager/HR
3. Approval timestamp and approver tracked for audit
4. Can be changed until locked by system (configurable)

## Data Models

### AttendanceStatus Enum
```python
PRESENT = "present"
ABSENT = "absent"
LEAVE = "leave"
HALF_DAY = "half_day"
WORK_FROM_HOME = "work_from_home"
HOLIDAY = "holiday"
SICK_LEAVE = "sick_leave"
MEDICAL_LEAVE = "medical_leave"
COMPENSATORY_OFF = "compensatory_off"
EMERGENCY_LEAVE = "emergency_leave"
```

### CheckInOutType Enum
```python
BIOMETRIC = "biometric"      # Biometric devices
WEB = "web"                  # Web portal
MOBILE = "mobile"            # Mobile app
MANUAL = "manual"            # Manual entry by HR/Manager
API = "api"                  # External system API
```

## Service Methods

### AttendanceService

```python
# Check-in/Check-out
check_in(db, company_id, employee_id, check_in_location, check_in_type, metadata)
check_out(db, company_id, employee_id, check_out_location, check_out_type, metadata)

# Attendance Management
mark_attendance(db, company_id, employee_id, attendance_date, status, ...)
get_attendance(db, company_id, attendance_id)
list_attendance(db, company_id, employee_id, from_date, to_date, status, ...)
get_today_attendance(db, company_id, employee_id)

# Approval
approve_attendance(db, company_id, attendance_id, is_approved, notes)

# Reporting
get_daily_report(db, company_id, report_date)
get_employee_attendance_stats(db, company_id, employee_id, from_date, to_date)
```

## Integration Points

### Employee Module
- Validates employee exists before recording attendance
- Links attendance to employee_id
- Supports employee filtering

### Company Module
- Enforces multi-tenancy via company_id
- May store attendance policies

### User Module
- Tracks who created/updated records (created_by, updated_by)
- Tracks approver details (approved_by)

### Permission Module
- Permission-based access control
- Role-based endpoint restrictions

### Audit Module
- Soft delete support via is_deleted flag
- Audit timestamps (created_at, updated_at)
- User tracking (created_by, updated_by, approved_by)

## Error Handling

### Common Exceptions

| Error | Status Code | Scenario |
|---|---|---|
| Employee not found | 404 | Invalid employee_id for company |
| Already checked in today | 400 | Duplicate check-in attempt |
| No check-in record | 400 | Check-out without check-in |
| Already checked out | 400 | Duplicate check-out attempt |
| Record not found | 404 | Invalid attendance_id |
| Permission denied | 403 | Insufficient permissions |

## Migration & Deployment

### Migration File
- Location: `alembic/versions/0005_phase13_attendance.py`
- Revision: `0005_phase13_attendance`
- Previous Revision: `0004_phase12_hrms`
- Creates attendance table and indexes

### Running Migration
```bash
# Upgrade to Phase 13
alembic upgrade 0005_phase13_attendance

# Or upgrade head
alembic upgrade head
```

## Testing Scenarios

### Basic Operations
- [ ] Employee check-in
- [ ] Employee check-out
- [ ] Calculate working hours
- [ ] Mark attendance manually
- [ ] Approve/reject attendance

### Edge Cases
- [ ] Check-out without check-in (error)
- [ ] Double check-in (error)
- [ ] Check-in/out same time (0 hours)
- [ ] Very long working day (>16 hours)
- [ ] Status change after approval

### Reports
- [ ] Daily report all employees
- [ ] Daily report specific date
- [ ] Employee stats for date range
- [ ] Attendance percentage calculation
- [ ] On-time vs late breakdown

### Multi-Tenancy
- [ ] Employee visibility by company
- [ ] Cross-company isolation
- [ ] Company-level reporting

## Future Enhancements

1. **Biometric Integration**: Direct integration with biometric devices
2. **Mobile App**: Native mobile check-in/check-out
3. **Geolocation**: GPS-based location tracking
4. **Work Schedule Management**: Different shifts and work schedules
5. **Exception Handling**: Predefined approval rules and exceptions
6. **Integration**: Payroll impact of attendance
7. **Analytics Dashboard**: Real-time analytics and trends
8. **Notifications**: Alerts for late arrivals, early departures
9. **Mobile Attendance**: QR code-based check-in
10. **Face Recognition**: Face-based biometric verification

## Compliance & Privacy

- GDPR compliant soft delete
- Audit trail for all changes
- Role-based access control
- User tracking for accountability
- Data retention policies via soft delete

---

## Files Modified/Created

### New Files
- `models/attendance_model.py` - Attendance ORM model
- `schemas/attendance_schema.py` - Pydantic schemas
- `services/attendance_service.py` - Business logic service
- `routers/attendance_router.py` - API endpoints
- `alembic/versions/0005_phase13_attendance.py` - Database migration
- `docs/PHASE_13_ATTENDANCE.md` - This documentation

### Migration History
- Phase 1-2: BRD & SRS
- Phase 3-4: Architecture & Database Design
- Phase 5-6: Config & Environment Framework
- Phase 7-8: Auth Platform & Authorization
- Phase 10-11: Organization & Company Management
- Phase 12: HRMS Employee & Designation Management
- **Phase 13: Attendance Management** ✓ (Current)
- Phase 14-15: Leave & Payroll Management (Upcoming)
- Phase 16-20: Inventory & Operations (Upcoming)
- Phase 21-35: Advanced Features & DevOps (Upcoming)
