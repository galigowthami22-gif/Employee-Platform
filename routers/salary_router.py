from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from core.database import get_db
from core.response import APIResponse, success_response, error_response
from core.permission import PermissionRequired
from dependencies.dependency import get_current_user
from middlewares.multi_tenancy_middleware import get_tenant_id
from schemas.salary_schema import (
    SalaryStructureCreateRequest,
    SalaryStructureResponse,
    PayrollCreateRequest,
    PayrollApproveRequest,
    PayrollPaymentRequest,
    PayrollResponse,
    PayrollListResponse,
    PayrollSummaryResponse,
)
from services.salary_service import SalaryStructureService
from services.payroll_service import PayrollService
from core.exceptions import NotFoundException, ValidationException

router = APIRouter(
    prefix="/api/v1/payroll",
    tags=["Payroll Management"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/salary-structure", response_model=APIResponse)
@PermissionRequired("payroll.create")
def create_salary_structure(
    request: SalaryStructureCreateRequest,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id),
):
    try:
        structure = SalaryStructureService.create_salary_structure(
            db=db,
            company_id=company_id,
            employee_id=request.employee_id,
            effective_from=request.effective_from,
            ctc=float(request.ctc),
            basic_salary=float(request.basic_salary),
            hra=float(request.hra or 0),
            conveyance=float(request.conveyance or 0),
            medical_allowance=float(request.medical_allowance or 0),
            other_allowances=float(request.other_allowances or 0),
            professional_tax=float(request.professional_tax or 0),
            provident_fund=float(request.provident_fund or 0),
            insurance=float(request.insurance or 0),
            other_deductions=float(request.other_deductions or 0),
            effective_to=request.effective_to,
            frequency=request.frequency.value,
            currency=request.currency,
            notes=request.notes,
        )
        return success_response(
            message="Salary structure created successfully",
            data=SalaryStructureResponse.from_orm(structure),
            status_code=201,
        )
    except (NotFoundException, ValidationException) as exc:
        return error_response(message=str(exc), status_code=getattr(exc, "status_code", 400))


@router.get("/salary-structure/{employee_id}", response_model=APIResponse)
@PermissionRequired("payroll.view")
def get_salary_structure(
    employee_id: str,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id),
):
    try:
        structure = SalaryStructureService.get_active_salary_structure(db, company_id, employee_id)
        if not structure:
            raise NotFoundException("No active salary structure found")
        return success_response(
            message="Salary structure retrieved",
            data=SalaryStructureResponse.from_orm(structure),
        )
    except NotFoundException as exc:
        return error_response(message=str(exc), status_code=404)


@router.post("", response_model=APIResponse)
@PermissionRequired("payroll.create")
def create_payroll_entry(
    request: PayrollCreateRequest,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id),
):
    try:
        payroll = PayrollService.create_payroll(
            db=db,
            company_id=company_id,
            employee_id=request.employee_id,
            payroll_month=request.payroll_month,
            working_days=float(request.working_days),
            basic_salary=float(request.basic_salary),
            days_present=float(request.days_present or 0),
            days_absent=float(request.days_absent or 0),
            days_leave=float(request.days_leave or 0),
            hra=float(request.hra or 0),
            conveyance=float(request.conveyance or 0),
            medical_allowance=float(request.medical_allowance or 0),
            other_allowances=float(request.other_allowances or 0),
            bonus=float(request.bonus or 0),
            incentive=float(request.incentive or 0),
            professional_tax=float(request.professional_tax or 0),
            provident_fund=float(request.provident_fund or 0),
            insurance=float(request.insurance or 0),
            loan_deduction=float(request.loan_deduction or 0),
            other_deductions=float(request.other_deductions or 0),
            advance_payment=float(request.advance_payment or 0),
            notes=request.notes,
        )
        return success_response(
            message="Payroll entry created successfully",
            data=PayrollResponse.from_orm(payroll),
            status_code=201,
        )
    except (NotFoundException, ValidationException) as exc:
        return error_response(message=str(exc), status_code=getattr(exc, "status_code", 400))


@router.get("/{payroll_id}", response_model=APIResponse)
@PermissionRequired("payroll.view")
def get_payroll_entry(
    payroll_id: str,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id),
):
    try:
        payroll = PayrollService.get_payroll(db, company_id, payroll_id)
        return success_response(message="Payroll retrieved", data=PayrollResponse.from_orm(payroll))
    except NotFoundException as exc:
        return error_response(message=str(exc), status_code=404)


@router.get("", response_model=APIResponse)
@PermissionRequired("payroll.view")
def list_payroll_entries(
    employee_id: str = Query(None),
    payroll_month: date = Query(None),
    status: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id),
):
    try:
        records, total = PayrollService.list_payroll(db, company_id, employee_id, payroll_month, status, skip, limit)
        response_data = PayrollListResponse(total=total, page=skip // limit + 1 if limit else 1, limit=limit, records=[PayrollResponse.from_orm(item) for item in records])
        return success_response(message="Payroll entries retrieved", data=response_data.model_dump())
    except Exception as exc:
        return error_response(message=str(exc), status_code=500)


@router.post("/{payroll_id}/approve", response_model=APIResponse)
@PermissionRequired("payroll.approve")
def approve_payroll_entry(
    payroll_id: str,
    request: PayrollApproveRequest,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id),
):
    try:
        payroll = PayrollService.approve_payroll(db, company_id, payroll_id, request.is_approved)
        return success_response(message="Payroll approval processed", data=PayrollResponse.from_orm(payroll))
    except (NotFoundException, ValidationException) as exc:
        return error_response(message=str(exc), status_code=getattr(exc, "status_code", 400))


@router.post("/{payroll_id}/pay", response_model=APIResponse)
@PermissionRequired("payroll.pay")
def mark_payroll_paid(
    payroll_id: str,
    request: PayrollPaymentRequest,
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id),
):
    try:
        payroll = PayrollService.mark_as_paid(db, company_id, payroll_id, request.payment_mode.value, request.paid_date)
        return success_response(message="Payroll marked as paid", data=PayrollResponse.from_orm(payroll))
    except (NotFoundException, ValidationException) as exc:
        return error_response(message=str(exc), status_code=getattr(exc, "status_code", 400))


@router.post("/process-month", response_model=APIResponse)
@PermissionRequired("payroll.process")
def process_monthly_payroll(
    payroll_month: date = Query(...),
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id),
):
    try:
        result = PayrollService.process_bulk_payroll(db, company_id, payroll_month)
        return success_response(message="Payroll processed", data=result)
    except Exception as exc:
        return error_response(message=str(exc), status_code=500)


@router.get("/summary", response_model=APIResponse)
@PermissionRequired("payroll.view")
def get_payroll_summary(
    payroll_month: date = Query(...),
    db: Session = Depends(get_db),
    company_id: str = Depends(get_tenant_id),
):
    try:
        summary = PayrollService.get_payroll_summary(db, company_id, payroll_month)
        return success_response(message="Payroll summary retrieved", data=PayrollSummaryResponse(**summary).model_dump())
    except Exception as exc:
        return error_response(message=str(exc), status_code=500)