"""
Organization Router
API endpoints for organization management (companies, branches, departments, teams).
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from core.authorization import authorization_engine, PermissionRequired, RoleRequired
from core.response import APIResponse
from middlewares.multi_tenancy_middleware import get_tenant_id, get_user_id
from services.organization_service import (
    CompanyService, BranchService, DepartmentService, TeamService
)
from schemas.company_schema import (
    CompanyCreateRequest, CompanyUpdateRequest, CompanyResponse, CompanyListResponse
)
from schemas.branch_schema import (
    BranchCreateRequest, BranchUpdateRequest, BranchResponse, BranchListResponse
)
from schemas.organization_schema import (
    DepartmentCreateRequest, DepartmentUpdateRequest, DepartmentResponse, DepartmentListResponse,
    TeamCreateRequest, TeamUpdateRequest, TeamResponse, TeamListResponse,
    TeamMemberCreateRequest, TeamMemberResponse
)

router = APIRouter(prefix="/api/v1/organization", tags=["Organization"])


# ============================================================================
# COMPANY ENDPOINTS
# ============================================================================

@router.post(
    "/companies",
    response_model=APIResponse[CompanyResponse],
    status_code=201,
    summary="Create Company",
    description="Create a new company (multi-tenant)",
    tags=["Companies"]
)
@RoleRequired("Super Admin", "Company Admin")
def create_company(
    request: CompanyCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new company."""
    try:
        company = CompanyService.create_company(
            db=db,
            name=request.name,
            short_name=request.short_name,
            description=request.description,
            legal_entity=request.legal_entity,
            registration_number=request.registration_number,
            tax_id=request.tax_id,
            industry=request.industry,
            website=request.website,
            phone=request.phone,
            email=request.email,
            country=request.country,
            state=request.state,
            city=request.city,
            address=request.address,
            postal_code=request.postal_code,
            currency=request.currency,
            timezone=request.timezone,
            language=request.language,
            plan=request.plan
        )
        return APIResponse(
            data=CompanyResponse.model_validate(company),
            message="Company created successfully",
            status_code=201
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/companies/{company_id}",
    response_model=APIResponse[CompanyResponse],
    summary="Get Company",
    description="Get company details by ID",
    tags=["Companies"]
)
@PermissionRequired("organization.read")
def get_company(
    company_id: str,
    db: Session = Depends(get_db)
):
    """Get company by ID."""
    try:
        company = CompanyService.get_company(db, company_id)
        return APIResponse(
            data=CompanyResponse.model_validate(company),
            message="Company retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/companies",
    response_model=APIResponse[List[CompanyListResponse]],
    summary="List Companies",
    description="List all companies with pagination",
    tags=["Companies"]
)
@PermissionRequired("organization.read")
def list_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List companies."""
    try:
        companies, total = CompanyService.list_companies(db, skip=skip, limit=limit)
        return APIResponse(
            data=[CompanyListResponse.model_validate(c) for c in companies],
            message=f"Retrieved {len(companies)} companies",
            metadata={"total": total, "skip": skip, "limit": limit}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/companies/{company_id}",
    response_model=APIResponse[CompanyResponse],
    summary="Update Company",
    description="Update company details",
    tags=["Companies"]
)
@RoleRequired("Super Admin", "Company Admin")
def update_company(
    company_id: str,
    request: CompanyUpdateRequest,
    db: Session = Depends(get_db)
):
    """Update company."""
    try:
        company = CompanyService.update_company(
            db=db,
            company_id=company_id,
            **request.model_dump(exclude_unset=True)
        )
        return APIResponse(
            data=CompanyResponse.model_validate(company),
            message="Company updated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/companies/{company_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Company",
    description="Soft delete company (archive)",
    tags=["Companies"]
)
@RoleRequired("Super Admin")
def delete_company(
    company_id: str,
    db: Session = Depends(get_db)
):
    """Delete company."""
    try:
        CompanyService.delete_company(db, company_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# BRANCH ENDPOINTS
# ============================================================================

@router.post(
    "/branches",
    response_model=APIResponse[BranchResponse],
    status_code=201,
    summary="Create Branch",
    description="Create a new branch",
    tags=["Branches"]
)
@PermissionRequired("organization.write")
def create_branch(
    request: BranchCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new branch."""
    try:
        branch = BranchService.create_branch(
            db=db,
            company_id=request.company_id,
            name=request.name,
            code=request.code,
            branch_type=request.type,
            description=request.description,
            manager_id=request.manager_id,
            phone=request.phone,
            email=request.email,
            website=request.website,
            country=request.country,
            state=request.state,
            city=request.city,
            address=request.address,
            postal_code=request.postal_code,
            latitude=request.latitude,
            longitude=request.longitude,
            capacity=request.capacity,
            timezone=request.timezone
        )
        return APIResponse(
            data=BranchResponse.model_validate(branch),
            message="Branch created successfully",
            status_code=201
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/branches/{branch_id}",
    response_model=APIResponse[BranchResponse],
    summary="Get Branch",
    description="Get branch details by ID",
    tags=["Branches"]
)
@PermissionRequired("organization.read")
def get_branch(
    branch_id: str,
    company_id: str = Query(...),
    db: Session = Depends(get_db)
):
    """Get branch by ID."""
    try:
        branch = BranchService.get_branch(db, branch_id, company_id)
        return APIResponse(
            data=BranchResponse.model_validate(branch),
            message="Branch retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/companies/{company_id}/branches",
    response_model=APIResponse[List[BranchListResponse]],
    summary="List Branches",
    description="List branches for a company",
    tags=["Branches"]
)
@PermissionRequired("organization.read")
def list_branches(
    company_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List branches for a company."""
    try:
        branches, total = BranchService.list_branches(db, company_id, skip, limit)
        return APIResponse(
            data=[BranchListResponse.model_validate(b) for b in branches],
            message=f"Retrieved {len(branches)} branches",
            metadata={"total": total, "skip": skip, "limit": limit}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/branches/{branch_id}",
    response_model=APIResponse[BranchResponse],
    summary="Update Branch",
    description="Update branch details",
    tags=["Branches"]
)
@PermissionRequired("organization.write")
def update_branch(
    branch_id: str,
    request: BranchUpdateRequest,
    company_id: str = Query(...),
    db: Session = Depends(get_db)
):
    """Update branch."""
    try:
        branch = BranchService.update_branch(
            db=db,
            branch_id=branch_id,
            company_id=company_id,
            **request.model_dump(exclude_unset=True)
        )
        return APIResponse(
            data=BranchResponse.model_validate(branch),
            message="Branch updated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/branches/{branch_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Branch",
    description="Soft delete branch (close)",
    tags=["Branches"]
)
@PermissionRequired("organization.write")
def delete_branch(
    branch_id: str,
    company_id: str = Query(...),
    db: Session = Depends(get_db)
):
    """Delete branch."""
    try:
        BranchService.delete_branch(db, branch_id, company_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# DEPARTMENT ENDPOINTS
# ============================================================================

@router.post(
    "/departments",
    response_model=APIResponse[DepartmentResponse],
    status_code=201,
    summary="Create Department",
    description="Create a new department",
    tags=["Departments"]
)
@PermissionRequired("organization.write")
def create_department(
    request: DepartmentCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new department."""
    try:
        department = DepartmentService.create_department(
            db=db,
            company_id=request.company_id,
            code=request.code,
            name=request.name,
            branch_id=request.branch_id,
            parent_department_id=request.parent_department_id,
            description=request.description,
            head_id=request.head_id,
            email=request.email,
            phone=request.phone,
            location=request.location,
            budget=request.budget
        )
        return APIResponse(
            data=DepartmentResponse.model_validate(department),
            message="Department created successfully",
            status_code=201
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/departments/{department_id}",
    response_model=APIResponse[DepartmentResponse],
    summary="Get Department",
    description="Get department details by ID",
    tags=["Departments"]
)
@PermissionRequired("organization.read")
def get_department(
    department_id: str,
    company_id: str = Query(...),
    db: Session = Depends(get_db)
):
    """Get department by ID."""
    try:
        department = DepartmentService.get_department(db, department_id, company_id)
        return APIResponse(
            data=DepartmentResponse.model_validate(department),
            message="Department retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/companies/{company_id}/departments",
    response_model=APIResponse[List[DepartmentListResponse]],
    summary="List Departments",
    description="List departments for a company",
    tags=["Departments"]
)
@PermissionRequired("organization.read")
def list_departments(
    company_id: str,
    branch_id: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List departments."""
    try:
        departments, total = DepartmentService.list_departments(
            db, company_id, branch_id, skip, limit
        )
        return APIResponse(
            data=[DepartmentListResponse.model_validate(d) for d in departments],
            message=f"Retrieved {len(departments)} departments",
            metadata={"total": total, "skip": skip, "limit": limit}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/departments/{department_id}",
    response_model=APIResponse[DepartmentResponse],
    summary="Update Department",
    description="Update department details",
    tags=["Departments"]
)
@PermissionRequired("organization.write")
def update_department(
    department_id: str,
    request: DepartmentUpdateRequest,
    company_id: str = Query(...),
    db: Session = Depends(get_db)
):
    """Update department."""
    try:
        department = DepartmentService.update_department(
            db=db,
            department_id=department_id,
            company_id=company_id,
            **request.model_dump(exclude_unset=True)
        )
        return APIResponse(
            data=DepartmentResponse.model_validate(department),
            message="Department updated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/departments/{department_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Department",
    description="Soft delete department (archive)",
    tags=["Departments"]
)
@PermissionRequired("organization.write")
def delete_department(
    department_id: str,
    company_id: str = Query(...),
    db: Session = Depends(get_db)
):
    """Delete department."""
    try:
        DepartmentService.delete_department(db, department_id, company_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# TEAM ENDPOINTS
# ============================================================================

@router.post(
    "/teams",
    response_model=APIResponse[TeamResponse],
    status_code=201,
    summary="Create Team",
    description="Create a new team",
    tags=["Teams"]
)
@PermissionRequired("organization.write")
def create_team(
    request: TeamCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new team."""
    try:
        team = TeamService.create_team(
            db=db,
            company_id=request.company_id,
            department_id=request.department_id,
            code=request.code,
            name=request.name,
            branch_id=request.branch_id,
            description=request.description,
            lead_id=request.lead_id,
            email=request.email,
            phone=request.phone,
            location=request.location,
            capacity=request.capacity
        )
        return APIResponse(
            data=TeamResponse.model_validate(team),
            message="Team created successfully",
            status_code=201
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/teams/{team_id}",
    response_model=APIResponse[TeamResponse],
    summary="Get Team",
    description="Get team details by ID",
    tags=["Teams"]
)
@PermissionRequired("organization.read")
def get_team(
    team_id: str,
    company_id: str = Query(...),
    db: Session = Depends(get_db)
):
    """Get team by ID."""
    try:
        team = TeamService.get_team(db, team_id, company_id)
        return APIResponse(
            data=TeamResponse.model_validate(team),
            message="Team retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/companies/{company_id}/teams",
    response_model=APIResponse[List[TeamListResponse]],
    summary="List Teams",
    description="List teams for a company",
    tags=["Teams"]
)
@PermissionRequired("organization.read")
def list_teams(
    company_id: str,
    department_id: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List teams."""
    try:
        teams, total = TeamService.list_teams(
            db, company_id, department_id, skip, limit
        )
        return APIResponse(
            data=[TeamListResponse.model_validate(t) for t in teams],
            message=f"Retrieved {len(teams)} teams",
            metadata={"total": total, "skip": skip, "limit": limit}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/teams/{team_id}",
    response_model=APIResponse[TeamResponse],
    summary="Update Team",
    description="Update team details",
    tags=["Teams"]
)
@PermissionRequired("organization.write")
def update_team(
    team_id: str,
    request: TeamUpdateRequest,
    company_id: str = Query(...),
    db: Session = Depends(get_db)
):
    """Update team."""
    try:
        from services.organization_service import TeamService
        team = TeamService.get_team(db, team_id, company_id)

        for key, value in request.model_dump(exclude_unset=True).items():
            if hasattr(team, key) and value is not None:
                setattr(team, key, value)

        db.commit()
        db.refresh(team)

        return APIResponse(
            data=TeamResponse.model_validate(team),
            message="Team updated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/teams/{team_id}/members",
    response_model=APIResponse[TeamMemberResponse],
    status_code=201,
    summary="Add Team Member",
    description="Add a member to a team",
    tags=["Teams"]
)
@PermissionRequired("organization.write")
def add_team_member(
    team_id: str,
    request: TeamMemberCreateRequest,
    company_id: str = Query(...),
    db: Session = Depends(get_db)
):
    """Add a member to a team."""
    try:
        member = TeamService.add_team_member(
            db=db,
            team_id=team_id,
            employee_id=request.employee_id,
            company_id=company_id,
            role=request.role,
            allocation_percentage=request.allocation_percentage,
            is_lead=request.is_lead
        )
        return APIResponse(
            data=TeamMemberResponse.model_validate(member),
            message="Team member added successfully",
            status_code=201
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/team-members/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove Team Member",
    description="Remove a member from a team",
    tags=["Teams"]
)
@PermissionRequired("organization.write")
def remove_team_member(
    member_id: str,
    db: Session = Depends(get_db)
):
    """Remove a member from a team."""
    try:
        TeamService.remove_team_member(db, member_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
