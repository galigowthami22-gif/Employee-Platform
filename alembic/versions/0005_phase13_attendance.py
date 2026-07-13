"""Phase 13: Attendance Management System

Revision ID: 0005_phase13_attendance
Revises: 0004_phase12_hrms
Create Date: 2026-01-16 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = '0005_phase13_attendance'
down_revision = '0004_phase12_hrms'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Upgrade migration to create Attendance table and supporting structures.
    """
    # Create Attendance table
    op.create_table(
        'attendance',
        sa.Column('attendance_id', sa.String(36), nullable=False),
        sa.Column('company_id', sa.String(36), nullable=False),
        sa.Column('employee_id', sa.String(36), nullable=False),
        sa.Column('attendance_date', sa.Date, nullable=False),
        
        # Check-in Details
        sa.Column('check_in_time', sa.DateTime, nullable=True),
        sa.Column('check_in_location', sa.String(255), nullable=True),
        sa.Column('check_in_type', sa.Enum('biometric', 'web', 'mobile', 'manual', 'api', name='checkin_type'), nullable=True),
        
        # Check-out Details
        sa.Column('check_out_time', sa.DateTime, nullable=True),
        sa.Column('check_out_location', sa.String(255), nullable=True),
        sa.Column('check_out_type', sa.Enum('biometric', 'web', 'mobile', 'manual', 'api', name='checkout_type'), nullable=True),
        
        # Status & Duration
        sa.Column('status', sa.Enum(
            'present', 'absent', 'leave', 'half_day', 'work_from_home', 'holiday',
            'sick_leave', 'medical_leave', 'compensatory_off', 'emergency_leave',
            name='attendance_status'
        ), nullable=False, server_default='absent'),
        sa.Column('working_hours', sa.String(10), nullable=True),
        sa.Column('is_early_checkout', sa.CHAR(1), server_default='N', nullable=False),
        
        # Notes & Metadata
        sa.Column('notes', sa.Text, nullable=True),
        sa.Column('reason', sa.String(255), nullable=True),
        sa.Column('metadata', sa.JSON, nullable=True),
        
        # Approval Information
        sa.Column('approved_by', sa.String(36), nullable=True),
        sa.Column('approved_at', sa.DateTime, nullable=True),
        sa.Column('is_approved', sa.CHAR(1), server_default='N', nullable=False),
        
        # Soft Delete & Audit Fields
        sa.Column('is_deleted', sa.Boolean, server_default='0', nullable=False),
        sa.Column('deleted_at', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        
        sa.ForeignKeyConstraint(['company_id'], ['companies.company_id']),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.employee_id']),
        sa.PrimaryKeyConstraint('attendance_id'),
        mysql_collate='utf8mb4_unicode_ci'
    )

    # Create indexes for Attendance
    op.create_index('idx_attendance_company_employee', 'attendance', ['company_id', 'employee_id'])
    op.create_index('idx_attendance_company_date', 'attendance', ['company_id', 'attendance_date'])
    op.create_index('idx_attendance_employee_date', 'attendance', ['employee_id', 'attendance_date'])
    op.create_index('idx_attendance_status', 'attendance', ['status'])
    op.create_index('idx_attendance_is_deleted', 'attendance', ['is_deleted'])
    op.create_index('idx_attendance_approved', 'attendance', ['is_approved'])


def downgrade() -> None:
    """
    Downgrade migration to drop Attendance table.
    """
    # Drop indexes
    op.drop_index('idx_attendance_approved', table_name='attendance')
    op.drop_index('idx_attendance_is_deleted', table_name='attendance')
    op.drop_index('idx_attendance_status', table_name='attendance')
    op.drop_index('idx_attendance_employee_date', table_name='attendance')
    op.drop_index('idx_attendance_company_date', table_name='attendance')
    op.drop_index('idx_attendance_company_employee', table_name='attendance')
    
    # Drop table
    op.drop_table('attendance')
