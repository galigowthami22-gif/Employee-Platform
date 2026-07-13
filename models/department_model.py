"""
Department & Team Models
Represents organizational structure - departments and teams within a company.
"""

from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey, Boolean, Float, Integer, Index
from sqlalchemy.orm import relationship
from core.base_model import BaseModel
import enum


class DepartmentStatus(str, enum.Enum):
    """Department status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class Department(BaseModel):
    """
    Department model representing a department within a company.
    
    Attributes:
        department_id: Primary key (UUID)
        company_id: Foreign key to Company (for multi-tenancy)
        branch_id: Foreign key to Branch (optional, if dept is specific to a branch)
        parent_department_id: Self-reference for hierarchical departments
        code: Unique department code (e.g., HR, IT, SALES)
        name: Department name
        description: Department description
        head_id: Department head/manager (User ID)
        status: Department status (active, inactive, archived)
        email: Department email
        phone: Department phone
        location: Department location
        budget: Annual budget (optional)
        created_at: Record creation timestamp
        updated_at: Last update timestamp
        created_by: User ID who created the department
        updated_by: User ID who last updated the department
    """
    __tablename__ = "departments"

    department_id = Column(String(36), primary_key=True)
    company_id = Column(String(36), ForeignKey("companies.company_id"), nullable=False, index=True)
    branch_id = Column(String(36), ForeignKey("branches.branch_id"), nullable=True, index=True)
    parent_department_id = Column(String(36), ForeignKey("departments.department_id"), nullable=True)
    
    # Basic Information
    code = Column(String(50), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Management
    head_id = Column(String(36), nullable=True, index=True)
    
    # Status
    status = Column(Enum(DepartmentStatus), default=DepartmentStatus.ACTIVE, nullable=False, index=True)
    
    # Contact Information
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    
    # Location & Budget
    location = Column(String(100), nullable=True)
    budget = Column(Float, nullable=True)
    
    # Audit Fields
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String(36), nullable=True)
    updated_by = Column(String(36), nullable=True)
    
    # Relationships
    company = relationship("Company", back_populates="departments")
    branch = relationship("Branch")
    parent_department = relationship("Department", remote_side=[department_id], backref="sub_departments")
    teams = relationship("Team", back_populates="department")
    
    # Composite Index
    __table_args__ = (
        Index('idx_department_company_status', 'company_id', 'status'),
        Index('idx_department_company_code', 'company_id', 'code'),
        Index('idx_department_parent', 'parent_department_id'),
    )
    
    def __repr__(self):
        return f"<Department(department_id={self.department_id}, code={self.code}, name={self.name})>"


class Team(BaseModel):
    """
    Team model representing a team within a department.
    Provides finer-grained organizational structure.
    
    Attributes:
        team_id: Primary key (UUID)
        company_id: Foreign key to Company (for multi-tenancy)
        department_id: Foreign key to Department
        branch_id: Foreign key to Branch (optional)
        code: Unique team code
        name: Team name
        description: Team description
        lead_id: Team lead/manager (User ID)
        status: Team status
        email: Team email
        phone: Team phone
        location: Team location
        capacity: Team member capacity
        created_at: Record creation timestamp
        updated_at: Last update timestamp
        created_by: User ID who created the team
        updated_by: User ID who last updated the team
    """
    __tablename__ = "teams"

    team_id = Column(String(36), primary_key=True)
    company_id = Column(String(36), ForeignKey("companies.company_id"), nullable=False, index=True)
    department_id = Column(String(36), ForeignKey("departments.department_id"), nullable=False, index=True)
    branch_id = Column(String(36), ForeignKey("branches.branch_id"), nullable=True, index=True)
    
    # Basic Information
    code = Column(String(50), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Management
    lead_id = Column(String(36), nullable=True, index=True)
    
    # Status
    status = Column(Enum(DepartmentStatus), default=DepartmentStatus.ACTIVE, nullable=False, index=True)
    
    # Contact Information
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    
    # Operational
    location = Column(String(100), nullable=True)
    capacity = Column(String(50), nullable=True)
    
    # Audit Fields
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String(36), nullable=True)
    updated_by = Column(String(36), nullable=True)
    
    # Relationships
    company = relationship("Company", back_populates="teams")
    department = relationship("Department", back_populates="teams")
    branch = relationship("Branch")
    members = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")
    
    # Composite Index
    __table_args__ = (
        Index('idx_team_company_status', 'company_id', 'status'),
        Index('idx_team_department_status', 'department_id', 'status'),
        Index('idx_team_company_code', 'company_id', 'code'),
    )
    
    def __repr__(self):
        return f"<Team(team_id={self.team_id}, code={self.code}, name={self.name})>"


class TeamMember(BaseModel):
    """
    Team Member model representing a member of a team.
    Links employees to teams.
    
    Attributes:
        member_id: Primary key (UUID)
        team_id: Foreign key to Team
        company_id: Foreign key to Company (for multi-tenancy)
        employee_id: Foreign key to Employee (User ID)
        role: Role within the team (developer, designer, manager, etc.)
        joining_date: Date employee joined the team
        allocation_percentage: Work allocation percentage (0-100)
        is_lead: Is this person a team lead (backup lead)
        created_at: Record creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "team_members"

    member_id = Column(String(36), primary_key=True)
    team_id = Column(String(36), ForeignKey("teams.team_id"), nullable=False, index=True)
    company_id = Column(String(36), ForeignKey("companies.company_id"), nullable=False, index=True)
    employee_id = Column(String(36), nullable=False, index=True)
    
    # Role & Allocation
    role = Column(String(100), nullable=True)
    allocation_percentage = Column(Integer, default=100)
    is_lead = Column(Boolean, default=False)
    
    # Timeline
    joining_date = Column(DateTime, nullable=True)
    
    # Audit Fields
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    team = relationship("Team", back_populates="members")
    
    # Composite Index
    __table_args__ = (
        Index('idx_team_member_team_employee', 'team_id', 'employee_id'),
        Index('idx_team_member_company', 'company_id'),
        Index('idx_team_member_employee', 'employee_id'),
    )
    
    def __repr__(self):
        return f"<TeamMember(member_id={self.member_id}, team_id={self.team_id}, employee_id={self.employee_id})>"