"""Add organization management models for Phase 10-11

Revision ID: 0003
Revises: 0002
Create Date: 2026-07-08 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade: Create organization management tables."""
    
    # Create companies table
    op.create_table(
        'companies',
        sa.Column('company_id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('short_name', sa.String(50), nullable=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('legal_entity', sa.String(100), nullable=True),
        sa.Column('registration_number', sa.String(100), nullable=True),
        sa.Column('tax_id', sa.String(50), nullable=True),
        sa.Column('fiscal_year_start', sa.Integer, nullable=False, server_default='1'),
        sa.Column('status', sa.String(50), nullable=False, server_default='active'),
        sa.Column('plan', sa.String(50), nullable=False, server_default='starter'),
        sa.Column('industry', sa.String(100), nullable=True),
        sa.Column('website', sa.String(255), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('logo_url', sa.String(500), nullable=True),
        sa.Column('founded_date', sa.DateTime, nullable=True),
        sa.Column('employee_count', sa.Integer, nullable=True),
        sa.Column('currency', sa.String(3), nullable=False, server_default='USD'),
        sa.Column('timezone', sa.String(50), nullable=False, server_default='UTC'),
        sa.Column('language', sa.String(10), nullable=False, server_default='en'),
        sa.Column('country', sa.String(100), nullable=True),
        sa.Column('state', sa.String(100), nullable=True),
        sa.Column('city', sa.String(100), nullable=True),
        sa.Column('address', sa.Text, nullable=True),
        sa.Column('postal_code', sa.String(20), nullable=True),
        sa.Column('metadata', sa.JSON, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.PrimaryKeyConstraint('company_id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('registration_number'),
        sa.UniqueConstraint('tax_id'),
    )
    
    op.create_index('idx_companies_status', 'companies', ['status'])
    op.create_index('idx_companies_created_at', 'companies', ['created_at'])
    op.create_index('idx_companies_created_by', 'companies', ['created_by'])
    op.create_index('idx_companies_name', 'companies', ['name'])
    op.create_index('idx_companies_country', 'companies', ['country'])
    
    # Create company_settings table
    op.create_table(
        'company_settings',
        sa.Column('setting_id', sa.String(36), nullable=False),
        sa.Column('company_id', sa.String(36), nullable=False),
        sa.Column('attendance_policy', sa.JSON, nullable=True),
        sa.Column('leave_policy', sa.JSON, nullable=True),
        sa.Column('payroll_frequency', sa.String(50), nullable=False, server_default='monthly'),
        sa.Column('salary_structure', sa.String(100), nullable=True),
        sa.Column('max_employees', sa.Integer, nullable=False, server_default='100'),
        sa.Column('max_departments', sa.Integer, nullable=False, server_default='20'),
        sa.Column('max_projects', sa.Integer, nullable=False, server_default='50'),
        sa.Column('max_users', sa.Integer, nullable=False, server_default='50'),
        sa.Column('enable_mfa', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('enable_audit_logs', sa.Boolean, nullable=False, server_default='true'),
        sa.Column('enable_two_factor', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('max_failed_login_attempts', sa.Integer, nullable=False, server_default='5'),
        sa.Column('session_timeout_minutes', sa.Integer, nullable=False, server_default='30'),
        sa.Column('password_policy', sa.JSON, nullable=True),
        sa.Column('api_rate_limit', sa.Integer, nullable=False, server_default='1000'),
        sa.Column('allow_bulk_operations', sa.Boolean, nullable=False, server_default='true'),
        sa.Column('allow_api_access', sa.Boolean, nullable=False, server_default='true'),
        sa.Column('max_file_upload_size_mb', sa.Integer, nullable=False, server_default='100'),
        sa.Column('backup_frequency', sa.String(50), nullable=False, server_default='daily'),
        sa.Column('retention_days', sa.Integer, nullable=False, server_default='365'),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('setting_id'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.company_id'], ),
        sa.UniqueConstraint('company_id'),
    )
    
    op.create_index('idx_company_settings_company_id', 'company_settings', ['company_id'])
    
    # Create branches table
    op.create_table(
        'branches',
        sa.Column('branch_id', sa.String(36), nullable=False),
        sa.Column('company_id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('code', sa.String(20), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='active'),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('manager_id', sa.String(36), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('website', sa.String(255), nullable=True),
        sa.Column('country', sa.String(100), nullable=True),
        sa.Column('state', sa.String(100), nullable=True),
        sa.Column('city', sa.String(100), nullable=True),
        sa.Column('address', sa.Text, nullable=True),
        sa.Column('postal_code', sa.String(20), nullable=True),
        sa.Column('latitude', sa.String(20), nullable=True),
        sa.Column('longitude', sa.String(20), nullable=True),
        sa.Column('capacity', sa.String(50), nullable=True),
        sa.Column('established_date', sa.DateTime, nullable=True),
        sa.Column('timezone', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.PrimaryKeyConstraint('branch_id'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.company_id'], ),
    )
    
    op.create_index('idx_branches_company_id', 'branches', ['company_id'])
    op.create_index('idx_branches_status', 'branches', ['status'])
    op.create_index('idx_branches_company_status', 'branches', ['company_id', 'status'])
    op.create_index('idx_branches_company_code', 'branches', ['company_id', 'code'])
    
    # Create branch_contacts table
    op.create_table(
        'branch_contacts',
        sa.Column('contact_id', sa.String(36), nullable=False),
        sa.Column('branch_id', sa.String(36), nullable=False),
        sa.Column('company_id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('title', sa.String(100), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('department', sa.String(100), nullable=True),
        sa.Column('is_primary', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('contact_id'),
        sa.ForeignKeyConstraint(['branch_id'], ['branches.branch_id'], ),
        sa.ForeignKeyConstraint(['company_id'], ['companies.company_id'], ),
    )
    
    op.create_index('idx_branch_contacts_branch_id', 'branch_contacts', ['branch_id'])
    op.create_index('idx_branch_contacts_branch_primary', 'branch_contacts', ['branch_id', 'is_primary'])
    op.create_index('idx_branch_contacts_company_id', 'branch_contacts', ['company_id'])
    
    # Create departments table
    op.create_table(
        'departments',
        sa.Column('department_id', sa.String(36), nullable=False),
        sa.Column('company_id', sa.String(36), nullable=False),
        sa.Column('branch_id', sa.String(36), nullable=True),
        sa.Column('parent_department_id', sa.String(36), nullable=True),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('head_id', sa.String(36), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='active'),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('location', sa.String(100), nullable=True),
        sa.Column('budget', sa.Float, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.PrimaryKeyConstraint('department_id'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.company_id'], ),
        sa.ForeignKeyConstraint(['branch_id'], ['branches.branch_id'], ),
        sa.ForeignKeyConstraint(['parent_department_id'], ['departments.department_id'], ),
    )
    
    op.create_index('idx_departments_company_id', 'departments', ['company_id'])
    op.create_index('idx_departments_company_status', 'departments', ['company_id', 'status'])
    op.create_index('idx_departments_company_code', 'departments', ['company_id', 'code'])
    op.create_index('idx_departments_parent_id', 'departments', ['parent_department_id'])
    op.create_index('idx_departments_name', 'departments', ['name'])
    op.create_index('idx_departments_created_at', 'departments', ['created_at'])
    
    # Create teams table
    op.create_table(
        'teams',
        sa.Column('team_id', sa.String(36), nullable=False),
        sa.Column('company_id', sa.String(36), nullable=False),
        sa.Column('department_id', sa.String(36), nullable=False),
        sa.Column('branch_id', sa.String(36), nullable=True),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('lead_id', sa.String(36), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='active'),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('location', sa.String(100), nullable=True),
        sa.Column('capacity', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.PrimaryKeyConstraint('team_id'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.company_id'], ),
        sa.ForeignKeyConstraint(['department_id'], ['departments.department_id'], ),
        sa.ForeignKeyConstraint(['branch_id'], ['branches.branch_id'], ),
    )
    
    op.create_index('idx_teams_company_id', 'teams', ['company_id'])
    op.create_index('idx_teams_company_status', 'teams', ['company_id', 'status'])
    op.create_index('idx_teams_department_status', 'teams', ['department_id', 'status'])
    op.create_index('idx_teams_company_code', 'teams', ['company_id', 'code'])
    op.create_index('idx_teams_created_at', 'teams', ['created_at'])
    
    # Create team_members table
    op.create_table(
        'team_members',
        sa.Column('member_id', sa.String(36), nullable=False),
        sa.Column('team_id', sa.String(36), nullable=False),
        sa.Column('company_id', sa.String(36), nullable=False),
        sa.Column('employee_id', sa.String(36), nullable=False),
        sa.Column('role', sa.String(100), nullable=True),
        sa.Column('allocation_percentage', sa.Integer, nullable=False, server_default='100'),
        sa.Column('is_lead', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('joining_date', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('member_id'),
        sa.ForeignKeyConstraint(['team_id'], ['teams.team_id'], ),
        sa.ForeignKeyConstraint(['company_id'], ['companies.company_id'], ),
    )
    
    op.create_index('idx_team_members_team_id', 'team_members', ['team_id'])
    op.create_index('idx_team_members_employee_id', 'team_members', ['employee_id'])
    op.create_index('idx_team_members_company_id', 'team_members', ['company_id'])
    op.create_index('idx_team_members_team_employee', 'team_members', ['team_id', 'employee_id'])
    
    # Create cost_centers table
    op.create_table(
        'cost_centers',
        sa.Column('cost_center_id', sa.String(36), nullable=False),
        sa.Column('company_id', sa.String(36), nullable=False),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('manager_id', sa.String(36), nullable=True),
        sa.Column('budget', sa.DECIMAL(15, 2), nullable=True),
        sa.Column('spent', sa.DECIMAL(15, 2), nullable=False, server_default='0'),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.PrimaryKeyConstraint('cost_center_id'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.company_id'], ),
    )
    
    op.create_index('idx_cost_centers_company_id', 'cost_centers', ['company_id'])
    op.create_index('idx_cost_centers_company_active', 'cost_centers', ['company_id', 'is_active'])
    op.create_index('idx_cost_centers_company_code', 'cost_centers', ['company_id', 'code'])
    op.create_index('idx_cost_centers_created_at', 'cost_centers', ['created_at'])


def downgrade() -> None:
    """Downgrade: Drop organization management tables."""
    op.drop_index('idx_cost_centers_created_at', 'cost_centers')
    op.drop_index('idx_cost_centers_company_code', 'cost_centers')
    op.drop_index('idx_cost_centers_company_active', 'cost_centers')
    op.drop_index('idx_cost_centers_company_id', 'cost_centers')
    op.drop_table('cost_centers')
    
    op.drop_index('idx_team_members_team_employee', 'team_members')
    op.drop_index('idx_team_members_company_id', 'team_members')
    op.drop_index('idx_team_members_employee_id', 'team_members')
    op.drop_index('idx_team_members_team_id', 'team_members')
    op.drop_table('team_members')
    
    op.drop_index('idx_teams_created_at', 'teams')
    op.drop_index('idx_teams_company_code', 'teams')
    op.drop_index('idx_teams_department_status', 'teams')
    op.drop_index('idx_teams_company_status', 'teams')
    op.drop_index('idx_teams_company_id', 'teams')
    op.drop_table('teams')
    
    op.drop_index('idx_departments_created_at', 'departments')
    op.drop_index('idx_departments_name', 'departments')
    op.drop_index('idx_departments_parent_id', 'departments')
    op.drop_index('idx_departments_company_code', 'departments')
    op.drop_index('idx_departments_company_status', 'departments')
    op.drop_index('idx_departments_company_id', 'departments')
    op.drop_table('departments')
    
    op.drop_index('idx_branch_contacts_company_id', 'branch_contacts')
    op.drop_index('idx_branch_contacts_branch_primary', 'branch_contacts')
    op.drop_index('idx_branch_contacts_branch_id', 'branch_contacts')
    op.drop_table('branch_contacts')
    
    op.drop_index('idx_branches_company_code', 'branches')
    op.drop_index('idx_branches_company_status', 'branches')
    op.drop_index('idx_branches_status', 'branches')
    op.drop_index('idx_branches_company_id', 'branches')
    op.drop_table('branches')
    
    op.drop_index('idx_company_settings_company_id', 'company_settings')
    op.drop_table('company_settings')
    
    op.drop_index('idx_companies_country', 'companies')
    op.drop_index('idx_companies_name', 'companies')
    op.drop_index('idx_companies_created_by', 'companies')
    op.drop_index('idx_companies_created_at', 'companies')
    op.drop_index('idx_companies_status', 'companies')
    op.drop_table('companies')
