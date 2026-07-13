"""
Employee Router (HRMS - Phase 12)
REST API endpoints for employee management.
"""

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from core.database import get_db
from core.response import APIResponse
from core.permission import PermissionRequired, RoleRequired
from dependencies.pagination import PaginationParams
from schemas.employee_schema import (
    EmployeeCreateRequest, EmployeeUpdateRequest, EmployeeResponse,
    EmployeeListResponse, DesignationCreateRequest, DesignationUpdateRequest,
    DesignationResponse, BulkEmployeeResponse, BulkDesignationResponse
)
from services.employee_service import EmployeeService, DesignationService
from core.exceptions import NotFoundException, ValidationException, DuplicateException
from middlewares.multi_tenancy_middleware import get_tenant_id, get_user_id

router = APIRouter(prefix="/api/v1/employees", tags=["HRMS - Employee Management"])


# ============================================================================
# EMPLOYEE ENDPOINTS
# ============================================================================

@router.post("", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
@PermissionRequired("employee_create")
def create_employee(
    request: EmployeeCreateRequest,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_user_id)
):
    """
    Create a new employee.
    
    Required Permission: employee_create
    
    Returns: Created employee details
    """
    try:
        employee = EmployeeService.create_employee(
            db=db,
            company_id=request.company_id,
            employee_code=request.employee_code,
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            date_of_joining=request.date_of_joining,
            middle_name=request.middle_name,
            personal_email=request.personal_email,
            phone=request.phone,
            mobile=request.mobile,
            id_type=request.id_type,
            id_number=request.id_number,
            tax_id=request.tax_id,
            date_of_birth=request.date_of_birth,
            gender=request.gender,
            marital_status=request.marital_status,
            nationality=request.nationality,
            blood_group=request.blood_group,
            employment_type=request.employment_type,
            employment_status=request.employment_status,
            date_of_confirmation=request.date_of_confirmation,
            department_id=request.department_id,
            designation_id=request.designation_id,
            manager_id=request.manager_id,
            cost_center_id=request.cost_center_id,
            current_address=request.current_address,
            permanent_address=request.permanent_address,
            city=request.city,
            state=request.state,
            country=request.country,
            postal_code=request.postal_code,
            ctc=request.ctc,
            salary=request.salary,
            salary_frequency=request.salary_frequency,
            currency=request.currency,
            reporting_manager_id=request.reporting_manager_id,
            emergency_contact=request.emergency_contact,
            emergency_phone=request.emergency_phone,
            work_location=request.work_location
        )

        return APIResponse(
            success=True,
            message="Employee created successfully",
            data=EmployeeResponse.from_orm(employee)
        )
    except DuplicateException as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_409_CONFLICT)
    except ValidationException as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{employee_id}", response_model=APIResponse)
@PermissionRequired("employee_read")
def get_employee(
    employee_id: str,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """
    Get employee by ID.
    
    Required Permission: employee_read
    
    Returns: Employee details
    """
    try:
        employee = EmployeeService.get_employee(db, employee_id, company_id)
        return APIResponse(success=True, data=EmployeeResponse.from_orm(employee))
    except NotFoundException as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_404_NOT_FOUND)


@router.get("", response_model=APIResponse)
@PermissionRequired("employee_read")
def list_employees(
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id),
    department_id: Optional[str] = Query(None),
    employment_status: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """
    List employees with filtering.
    
    Required Permission: employee_read
    
    Query Parameters:
    - department_id: Filter by department
    - employment_status: Filter by status (active, inactive, terminated, etc.)
    - is_active: Filter by active status
    - skip: Pagination offset
    - limit: Pagination limit (max 100)
    
    Returns: List of employees with total count
    """
    try:
        employees, total = EmployeeService.list_employees(
            db=db,
            company_id=company_id,
            department_id=department_id,
            employment_status=employment_status,
            is_active=is_active,
            skip=skip,
            limit=limit
        )

        return APIResponse(
            success=True,
            data={
                "employees": [EmployeeListResponse.from_orm(e) for e in employees],
                "total": total,
                "skip": skip,
                "limit": limit
            }
        )
    except Exception as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/{employee_id}", response_model=APIResponse)
@PermissionRequired("employee_update")
def update_employee(
    employee_id: str,
    request: EmployeeUpdateRequest,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """
    Update employee details.
    
    Required Permission: employee_update
    
    Returns: Updated employee details
    """
    try:
        update_data = request.model_dump(exclude_unset=True)
        employee = EmployeeService.update_employee(
            db=db,
            employee_id=employee_id,
            company_id=company_id,
            **update_data
        )

        return APIResponse(
            success=True,
            message="Employee updated successfully",
            data=EmployeeResponse.from_orm(employee)
        )
    except NotFoundException as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_404_NOT_FOUND)
    except DuplicateException as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/{employee_id}/deactivate", response_model=APIResponse)
@PermissionRequired("employee_deactivate")
def deactivate_employee(
    employee_id: str,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """
    Deactivate employee (termination/resignation).
    
    Required Permission: employee_deactivate
    
    Returns: Updated employee with terminated status
    """
    try:
        employee = EmployeeService.deactivate_employee(db, employee_id, company_id)
        return APIResponse(
            success=True,
            message="Employee deactivated successfully",
            data=EmployeeResponse.from_orm(employee)
        )
    except NotFoundException as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_404_NOT_FOUND)


@router.get("/{manager_id}/subordinates", response_model=APIResponse)
@PermissionRequired("employee_read")
def get_manager_subordinates(
    manager_id: str,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """
    Get all subordinates of a manager.
    
    Required Permission: employee_read
    
    Returns: List of subordinate employees
    """
    try:
        subordinates = EmployeeService.get_manager_subordinates(db, manager_id, company_id)
        return APIResponse(
            success=True,
            data=[EmployeeListResponse.from_orm(s) for s in subordinates]
        )
    except Exception as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/department/{department_id}/employees", response_model=APIResponse)
@PermissionRequired("employee_read")
def get_department_employees(
    department_id: str,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """
    Get all employees in a department.
    
    Required Permission: employee_read
    
    Returns: List of employees in department
    """
    try:
        employees = EmployeeService.get_department_employees(db, department_id, company_id)
        return APIResponse(
            success=True,
            data=[EmployeeListResponse.from_orm(e) for e in employees]
        )
    except Exception as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================================================
# DESIGNATION ENDPOINTS
# ============================================================================

@router.post("/designations", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
@PermissionRequired("designation_create")
def create_designation(
    request: DesignationCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new designation (job title).
    
    Required Permission: designation_create
    
    Returns: Created designation details
    """
    try:
        designation = DesignationService.create_designation(
            db=db,
            company_id=request.company_id,
            code=request.code,
            name=request.name,
            description=request.description,
            level=request.level,
            ctc_range_min=request.ctc_range_min,
            ctc_range_max=request.ctc_range_max
        )

        return APIResponse(
            success=True,
            message="Designation created successfully",
            data=DesignationResponse.from_orm(designation)
        )
    except DuplicateException as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/designations/{designation_id}", response_model=APIResponse)
@PermissionRequired("designation_read")
def get_designation(
    designation_id: str,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """
    Get designation by ID.
    
    Required Permission: designation_read
    
    Returns: Designation details
    """
    try:
        designation = DesignationService.get_designation(db, designation_id, company_id)
        return APIResponse(success=True, data=DesignationResponse.from_orm(designation))
    except NotFoundException as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_404_NOT_FOUND)


@router.get("/designations", response_model=APIResponse)
@PermissionRequired("designation_read")
def list_designations(
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id),
    is_active: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """
    List designations.
    
    Required Permission: designation_read
    
    Query Parameters:
    - is_active: Filter by active status
    - skip: Pagination offset
    - limit: Pagination limit
    
    Returns: List of designations with total count
    """
    try:
        designations, total = DesignationService.list_designations(
            db=db,
            company_id=company_id,
            is_active=is_active,
            skip=skip,
            limit=limit
        )

        return APIResponse(
            success=True,
            data={
                "designations": [DesignationResponse.from_orm(d) for d in designations],
                "total": total,
                "skip": skip,
                "limit": limit
            }
        )
    except Exception as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/designations/{designation_id}", response_model=APIResponse)
@PermissionRequired("designation_update")
def update_designation(
    designation_id: str,
    request: DesignationUpdateRequest,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """
    Update designation details.
    
    Required Permission: designation_update
    
    Returns: Updated designation details
    """
    try:
        update_data = request.model_dump(exclude_unset=True)
        designation = DesignationService.update_designation(
            db=db,
            designation_id=designation_id,
            company_id=company_id,
            **update_data
        )

        return APIResponse(
            success=True,
            message="Designation updated successfully",
            data=DesignationResponse.from_orm(designation)
        )
    except NotFoundException as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_404_NOT_FOUND)
    except DuplicateException as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/designations/{designation_id}", response_model=APIResponse)
@PermissionRequired("designation_delete")
def delete_designation(
    designation_id: str,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id)
):
    """
    Delete designation (soft delete).
    
    Required Permission: designation_delete
    
    Returns: Success message
    """
    try:
        DesignationService.delete_designation(db, designation_id, company_id)
        return APIResponse(success=True, message="Designation deleted successfully")
    except NotFoundException as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return APIResponse(success=False, message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)