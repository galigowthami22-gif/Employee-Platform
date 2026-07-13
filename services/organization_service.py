"""
Organization Service
Business logic for organization management.
"""

from typing import List, Optional
from uuid import uuid4
from sqlalchemy.orm import Session
from datetime import datetime
from core.exceptions import NotFoundException, ValidationException, DuplicateException
from models.company_model import Company, CompanySettings, CompanyStatus, CompanyPlan
from models.branch_model import Branch, BranchContact, BranchStatus
from models.department_model import Department, Team, TeamMember
from models.cost_center_model import CostCenter
from middlewares.multi_tenancy_middleware import get_tenant_id, get_user_id


class CompanyService:
    """Service for company management."""

    @staticmethod
    def create_company(
        db: Session,
        name: str,
        short_name: Optional[str] = None,
        description: Optional[str] = None,
        industry: Optional[str] = None,
        country: Optional[str] = None,
        currency: str = "USD",
        timezone: str = "UTC",
        language: str = "en",
        plan: CompanyPlan = CompanyPlan.STARTER,
        **kwargs
    ) -> Company:
        """Create a new company."""
        # Check for duplicates
        existing = db.query(Company).filter(Company.name == name).first()
        if existing:
            raise DuplicateException(f"Company with name '{name}' already exists")

        company_id = str(uuid4())
        created_by = get_user_id()

        company = Company(
            company_id=company_id,
            name=name,
            short_name=short_name,
            description=description,
            industry=industry,
            country=country,
            currency=currency,
            timezone=timezone,
            language=language,
            plan=plan,
            status=CompanyStatus.ACTIVE,
            created_by=created_by,
            updated_by=created_by,
            **kwargs
        )

        db.add(company)

        # Create default settings
        settings = CompanySettings(
            setting_id=str(uuid4()),
            company_id=company_id,
        )
        db.add(settings)
        db.commit()
        db.refresh(company)

        return company

    @staticmethod
    def get_company(db: Session, company_id: str) -> Company:
        """Get company by ID."""
        company = db.query(Company).filter(Company.company_id == company_id).first()
        if not company:
            raise NotFoundException(f"Company with ID '{company_id}' not found")
        return company

    @staticmethod
    def get_company_by_name(db: Session, name: str) -> Company:
        """Get company by name."""
        company = db.query(Company).filter(Company.name == name).first()
        if not company:
            raise NotFoundException(f"Company with name '{name}' not found")
        return company

    @staticmethod
    def list_companies(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        status: Optional[CompanyStatus] = None
    ) -> tuple[List[Company], int]:
        """List companies with pagination."""
        query = db.query(Company)

        if status:
            query = query.filter(Company.status == status)

        total = query.count()
        companies = query.offset(skip).limit(limit).all()

        return companies, total

    @staticmethod
    def update_company(
        db: Session,
        company_id: str,
        **kwargs
    ) -> Company:
        """Update company."""
        company = CompanyService.get_company(db, company_id)

        # Check for name duplicate if updating name
        if "name" in kwargs:
            existing = db.query(Company).filter(
                Company.name == kwargs["name"],
                Company.company_id != company_id
            ).first()
            if existing:
                raise DuplicateException(f"Company with name '{kwargs['name']}' already exists")

        updated_by = get_user_id()
        kwargs["updated_by"] = updated_by
        kwargs["updated_at"] = datetime.utcnow()

        for key, value in kwargs.items():
            if hasattr(company, key) and value is not None:
                setattr(company, key, value)

        db.commit()
        db.refresh(company)

        return company

    @staticmethod
    def delete_company(db: Session, company_id: str) -> None:
        """Delete company (soft delete via status)."""
        company = CompanyService.get_company(db, company_id)
        company.status = CompanyStatus.ARCHIVED
        company.updated_by = get_user_id()
        company.updated_at = datetime.utcnow()
        db.commit()

    @staticmethod
    def get_company_settings(db: Session, company_id: str) -> CompanySettings:
        """Get company settings."""
        settings = db.query(CompanySettings).filter(
            CompanySettings.company_id == company_id
        ).first()

        if not settings:
            raise NotFoundException(f"Settings for company '{company_id}' not found")

        return settings

    @staticmethod
    def update_company_settings(
        db: Session,
        company_id: str,
        **kwargs
    ) -> CompanySettings:
        """Update company settings."""
        settings = CompanyService.get_company_settings(db, company_id)

        for key, value in kwargs.items():
            if hasattr(settings, key) and value is not None:
                setattr(settings, key, value)

        settings.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(settings)

        return settings


class BranchService:
    """Service for branch management."""

    @staticmethod
    def create_branch(
        db: Session,
        company_id: str,
        name: str,
        code: str,
        branch_type: str,
        **kwargs
    ) -> Branch:
        """Create a new branch."""
        # Verify company exists
        CompanyService.get_company(db, company_id)

        # Check for duplicate code in company
        existing = db.query(Branch).filter(
            Branch.company_id == company_id,
            Branch.code == code
        ).first()
        if existing:
            raise DuplicateException(f"Branch with code '{code}' already exists in company")

        branch_id = str(uuid4())
        created_by = get_user_id()

        branch = Branch(
            branch_id=branch_id,
            company_id=company_id,
            name=name,
            code=code,
            type=branch_type,
            status=BranchStatus.ACTIVE,
            created_by=created_by,
            updated_by=created_by,
            **kwargs
        )

        db.add(branch)
        db.commit()
        db.refresh(branch)

        return branch

    @staticmethod
    def get_branch(db: Session, branch_id: str, company_id: Optional[str] = None) -> Branch:
        """Get branch by ID with optional company verification."""
        query = db.query(Branch).filter(Branch.branch_id == branch_id)

        if company_id:
            query = query.filter(Branch.company_id == company_id)

        branch = query.first()
        if not branch:
            raise NotFoundException(f"Branch with ID '{branch_id}' not found")

        return branch

    @staticmethod
    def list_branches(
        db: Session,
        company_id: str,
        skip: int = 0,
        limit: int = 10,
        status: Optional[BranchStatus] = None
    ) -> tuple[List[Branch], int]:
        """List branches for a company."""
        query = db.query(Branch).filter(Branch.company_id == company_id)

        if status:
            query = query.filter(Branch.status == status)

        total = query.count()
        branches = query.offset(skip).limit(limit).all()

        return branches, total

    @staticmethod
    def update_branch(
        db: Session,
        branch_id: str,
        company_id: str,
        **kwargs
    ) -> Branch:
        """Update branch."""
        branch = BranchService.get_branch(db, branch_id, company_id)

        # Check for code duplicate if updating code
        if "code" in kwargs:
            existing = db.query(Branch).filter(
                Branch.company_id == company_id,
                Branch.code == kwargs["code"],
                Branch.branch_id != branch_id
            ).first()
            if existing:
                raise DuplicateException(f"Branch with code '{kwargs['code']}' already exists")

        updated_by = get_user_id()
        kwargs["updated_by"] = updated_by
        kwargs["updated_at"] = datetime.utcnow()

        for key, value in kwargs.items():
            if hasattr(branch, key) and value is not None:
                setattr(branch, key, value)

        db.commit()
        db.refresh(branch)

        return branch

    @staticmethod
    def delete_branch(db: Session, branch_id: str, company_id: str) -> None:
        """Delete branch (soft delete via status)."""
        branch = BranchService.get_branch(db, branch_id, company_id)
        branch.status = BranchStatus.CLOSED
        branch.updated_by = get_user_id()
        branch.updated_at = datetime.utcnow()
        db.commit()


class DepartmentService:
    """Service for department management."""

    @staticmethod
    def create_department(
        db: Session,
        company_id: str,
        code: str,
        name: str,
        **kwargs
    ) -> Department:
        """Create a new department."""
        # Verify company exists
        CompanyService.get_company(db, company_id)

        # Check for duplicate code in company
        existing = db.query(Department).filter(
            Department.company_id == company_id,
            Department.code == code
        ).first()
        if existing:
            raise DuplicateException(f"Department with code '{code}' already exists in company")

        department_id = str(uuid4())
        created_by = get_user_id()

        department = Department(
            department_id=department_id,
            company_id=company_id,
            code=code,
            name=name,
            created_by=created_by,
            updated_by=created_by,
            **kwargs
        )

        db.add(department)
        db.commit()
        db.refresh(department)

        return department

    @staticmethod
    def get_department(db: Session, department_id: str, company_id: Optional[str] = None) -> Department:
        """Get department by ID."""
        query = db.query(Department).filter(Department.department_id == department_id)

        if company_id:
            query = query.filter(Department.company_id == company_id)

        dept = query.first()
        if not dept:
            raise NotFoundException(f"Department with ID '{department_id}' not found")

        return dept

    @staticmethod
    def list_departments(
        db: Session,
        company_id: str,
        branch_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 10
    ) -> tuple[List[Department], int]:
        """List departments."""
        query = db.query(Department).filter(Department.company_id == company_id)

        if branch_id:
            query = query.filter(Department.branch_id == branch_id)

        total = query.count()
        departments = query.offset(skip).limit(limit).all()

        return departments, total

    @staticmethod
    def update_department(
        db: Session,
        department_id: str,
        company_id: str,
        **kwargs
    ) -> Department:
        """Update department."""
        dept = DepartmentService.get_department(db, department_id, company_id)

        # Check for code duplicate if updating code
        if "code" in kwargs:
            existing = db.query(Department).filter(
                Department.company_id == company_id,
                Department.code == kwargs["code"],
                Department.department_id != department_id
            ).first()
            if existing:
                raise DuplicateException(f"Department with code '{kwargs['code']}' already exists")

        updated_by = get_user_id()
        kwargs["updated_by"] = updated_by
        kwargs["updated_at"] = datetime.utcnow()

        for key, value in kwargs.items():
            if hasattr(dept, key) and value is not None:
                setattr(dept, key, value)

        db.commit()
        db.refresh(dept)

        return dept

    @staticmethod
    def delete_department(db: Session, department_id: str, company_id: str) -> None:
        """Delete department (soft delete via status)."""
        from models.department_model import DepartmentStatus
        dept = DepartmentService.get_department(db, department_id, company_id)
        dept.status = DepartmentStatus.ARCHIVED
        dept.updated_by = get_user_id()
        dept.updated_at = datetime.utcnow()
        db.commit()


class TeamService:
    """Service for team management."""

    @staticmethod
    def create_team(
        db: Session,
        company_id: str,
        department_id: str,
        code: str,
        name: str,
        **kwargs
    ) -> Team:
        """Create a new team."""
        # Verify company and department exist
        CompanyService.get_company(db, company_id)
        DepartmentService.get_department(db, department_id, company_id)

        # Check for duplicate code in department
        existing = db.query(Team).filter(
            Team.department_id == department_id,
            Team.code == code
        ).first()
        if existing:
            raise DuplicateException(f"Team with code '{code}' already exists in department")

        team_id = str(uuid4())
        created_by = get_user_id()

        team = Team(
            team_id=team_id,
            company_id=company_id,
            department_id=department_id,
            code=code,
            name=name,
            created_by=created_by,
            updated_by=created_by,
            **kwargs
        )

        db.add(team)
        db.commit()
        db.refresh(team)

        return team

    @staticmethod
    def get_team(db: Session, team_id: str, company_id: Optional[str] = None) -> Team:
        """Get team by ID."""
        query = db.query(Team).filter(Team.team_id == team_id)

        if company_id:
            query = query.filter(Team.company_id == company_id)

        team = query.first()
        if not team:
            raise NotFoundException(f"Team with ID '{team_id}' not found")

        return team

    @staticmethod
    def list_teams(
        db: Session,
        company_id: str,
        department_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 10
    ) -> tuple[List[Team], int]:
        """List teams."""
        query = db.query(Team).filter(Team.company_id == company_id)

        if department_id:
            query = query.filter(Team.department_id == department_id)

        total = query.count()
        teams = query.offset(skip).limit(limit).all()

        return teams, total

    @staticmethod
    def add_team_member(
        db: Session,
        team_id: str,
        employee_id: str,
        company_id: str,
        role: Optional[str] = None,
        allocation_percentage: int = 100,
        is_lead: bool = False
    ) -> TeamMember:
        """Add a member to a team."""
        # Verify team exists
        TeamService.get_team(db, team_id, company_id)

        # Check for duplicate membership
        existing = db.query(TeamMember).filter(
            TeamMember.team_id == team_id,
            TeamMember.employee_id == employee_id
        ).first()
        if existing:
            raise DuplicateException(f"Employee '{employee_id}' is already a member of team")

        member_id = str(uuid4())

        member = TeamMember(
            member_id=member_id,
            team_id=team_id,
            company_id=company_id,
            employee_id=employee_id,
            role=role,
            allocation_percentage=allocation_percentage,
            is_lead=is_lead
        )

        db.add(member)
        db.commit()
        db.refresh(member)

        return member

    @staticmethod
    def remove_team_member(db: Session, member_id: str) -> None:
        """Remove a member from a team."""
        member = db.query(TeamMember).filter(TeamMember.member_id == member_id).first()
        if not member:
            raise NotFoundException(f"Team member with ID '{member_id}' not found")

        db.delete(member)
        db.commit()
