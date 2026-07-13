"""Phase 12: HRMS - Employee and Designation Tables

Revision ID: 0004_phase12_hrms
Revises: 0003_phase10_organization_management
Create Date: 2026-01-15 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = '0004_phase12_hrms'
down_revision = '0003_phase10_organization_management'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Upgrade migration to create Employee and Designation tables.
    """
    # Create Designation table (must be before Employee due to FK)
    op.create_table(
        'designations',
        sa.Column('designation_id', sa.String(36), nullable=False),
        sa.Column('company_id', sa.String(36), nullable=False),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('level', sa.Integer, nullable=True),
        sa.Column('ctc_range_min', sa.DECIMAL(15, 2), nullable=True),
        sa.Column('ctc_range_max', sa.DECIMAL(15, 2), nullable=True),
        sa.Column('is_active', sa.Boolean, server_default='1', nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.ForeignKeyConstraint(['company_id'], ['companies.company_id']),
        sa.PrimaryKeyConstraint('designation_id'),
        mysql_collate='utf8mb4_unicode_ci'
    )

    # Create indexes for Designation
    op.create_index('idx_designation_company_code', 'designations', ['company_id', 'code'])
    op.create_index('idx_designation_company_active', 'designations', ['company_id', 'is_active'])
    op.create_index('idx_designation_level', 'designations', ['level'])

    # Create Employee table
    op.create_table(
        'employees',
        sa.Column('employee_id', sa.String(36), nullable=False),
        sa.Column('company_id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=True),
        sa.Column('department_id', sa.String(36), nullable=True),
        sa.Column('designation_id', sa.String(36), nullable=True),
        sa.Column('manager_id', sa.String(36), nullable=True),
        sa.Column('cost_center_id', sa.String(36), nullable=True),
        
        # Basic Information
        sa.Column('employee_code', sa.String(50), nullable=False),
        sa.Column('first_name', sa.String(100), nullable=False),
        sa.Column('middle_name', sa.String(100), nullable=True),
        sa.Column('last_name', sa.String(100), nullable=False),
        
        # Contact Information
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('personal_email', sa.String(255), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('mobile', sa.String(20), nullable=True),
        
        # Identification
        sa.Column('id_type', sa.String(50), nullable=True),
        sa.Column('id_number', sa.String(100), nullable=True),
        sa.Column('tax_id', sa.String(50), nullable=True),
        
        # Personal Information
        sa.Column('date_of_birth', sa.Date, nullable=True),
        sa.Column('gender', sa.Enum('male', 'female', 'other', 'prefer_not_to_say', name='gender_enum'), nullable=True),
        sa.Column('marital_status', sa.Enum('single', 'married', 'divorced', 'widowed', 'prefer_not_to_say', name='marital_status_enum'), nullable=True),
        sa.Column('nationality', sa.String(100), nullable=True),
        sa.Column('blood_group', sa.String(10), nullable=True),
        
        # Employment Details
        sa.Column('employment_type', sa.Enum('full_time', 'part_time', 'contract', 'temporary', 'intern', 'consultant', name='employment_type_enum'), server_default='full_time', nullable=False),
        sa.Column('employment_status', sa.Enum('active', 'inactive', 'on_leave', 'suspended', 'terminated', name='employment_status_enum'), server_default='active', nullable=False),
        sa.Column('date_of_joining', sa.Date, nullable=False),
        sa.Column('date_of_confirmation', sa.Date, nullable=True),
        sa.Column('date_of_separation', sa.Date, nullable=True),
        
        # Address Information
        sa.Column('current_address', sa.Text, nullable=True),
        sa.Column('permanent_address', sa.Text, nullable=True),
        sa.Column('city', sa.String(100), nullable=True),
        sa.Column('state', sa.String(100), nullable=True),
        sa.Column('country', sa.String(100), nullable=True),
        sa.Column('postal_code', sa.String(20), nullable=True),
        
        # Employment Terms
        sa.Column('ctc', sa.DECIMAL(15, 2), nullable=True),
        sa.Column('salary', sa.DECIMAL(15, 2), nullable=True),
        sa.Column('salary_frequency', sa.String(50), server_default='monthly', nullable=True),
        sa.Column('currency', sa.String(3), server_default='USD', nullable=True),
        
        # Additional Information
        sa.Column('reporting_manager_id', sa.String(36), nullable=True),
        sa.Column('emergency_contact', sa.String(255), nullable=True),
        sa.Column('emergency_phone', sa.String(20), nullable=True),
        sa.Column('work_location', sa.String(255), nullable=True),
        
        # Status & Tracking
        sa.Column('is_active', sa.Boolean, server_default='1', nullable=False),
        sa.Column('is_verified', sa.Boolean, server_default='0', nullable=False),
        sa.Column('probation_end_date', sa.Date, nullable=True),
        
        # File References
        sa.Column('profile_photo_url', sa.String(500), nullable=True),
        sa.Column('resume_url', sa.String(500), nullable=True),
        
        # Additional Data
        sa.Column('metadata', sa.JSON, nullable=True),
        sa.Column('notes', sa.Text, nullable=True),
        
        # Audit Fields
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        
        sa.ForeignKeyConstraint(['company_id'], ['companies.company_id']),
        sa.ForeignKeyConstraint(['department_id'], ['departments.department_id']),
        sa.ForeignKeyConstraint(['manager_id'], ['employees.employee_id']),
        sa.ForeignKeyConstraint(['cost_center_id'], ['cost_centers.cost_center_id']),
        sa.PrimaryKeyConstraint('employee_id'),
        sa.UniqueConstraint('employee_code'),
        sa.UniqueConstraint('user_id'),
        sa.UniqueConstraint('id_number'),
        sa.UniqueConstraint('tax_id'),
        sa.UniqueConstraint('email'),
        mysql_collate='utf8mb4_unicode_ci'
    )

    # Create indexes for Employee
    op.create_index('idx_employee_company', 'employees', ['company_id'])
    op.create_index('idx_employee_department', 'employees', ['department_id'])
    op.create_index('idx_employee_code', 'employees', ['employee_code'])
    op.create_index('idx_employee_email', 'employees', ['email'])
    op.create_index('idx_employee_user_id', 'employees', ['user_id'])
    op.create_index('idx_employee_employment_status', 'employees', ['employment_status'])
    op.create_index('idx_employee_is_active', 'employees', ['is_active'])
    op.create_index('idx_employee_created_at', 'employees', ['created_at'])
    op.create_index('idx_employee_date_of_joining', 'employees', ['date_of_joining'])
    op.create_index('idx_employee_manager_id', 'employees', ['manager_id'])
    
    # Composite indexes
    op.create_index('idx_employee_company_status', 'employees', ['company_id', 'employment_status'])
    op.create_index('idx_employee_company_dept', 'employees', ['company_id', 'department_id'])
    op.create_index('idx_employee_company_active', 'employees', ['company_id', 'is_active'])
    op.create_index('idx_employee_dept_status', 'employees', ['department_id', 'employment_status'])


def downgrade() -> None:
    """
    Downgrade migration to drop Employee and Designation tables.
    """
    # Drop Employee table first (due to FK dependencies)
    op.drop_index('idx_employee_dept_status', table_name='employees')
    op.drop_index('idx_employee_company_active', table_name='employees')
    op.drop_index('idx_employee_company_dept', table_name='employees')
    op.drop_index('idx_employee_company_status', table_name='employees')
    op.drop_index('idx_employee_manager_id', table_name='employees')
    op.drop_index('idx_employee_date_of_joining', table_name='employees')
    op.drop_index('idx_employee_created_at', table_name='employees')
    op.drop_index('idx_employee_is_active', table_name='employees')
    op.drop_index('idx_employee_employment_status', table_name='employees')
    op.drop_index('idx_employee_user_id', table_name='employees')
    op.drop_index('idx_employee_email', table_name='employees')
    op.drop_index('idx_employee_code', table_name='employees')
    op.drop_index('idx_employee_department', table_name='employees')
    op.drop_index('idx_employee_company', table_name='employees')
    op.drop_table('employees')
    
    # Drop Designation table
    op.drop_index('idx_designation_level', table_name='designations')
    op.drop_index('idx_designation_company_active', table_name='designations')
    op.drop_index('idx_designation_company_code', table_name='designations')
    op.drop_table('designations')
