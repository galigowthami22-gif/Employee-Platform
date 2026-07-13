"""Phase 14: Leave Management System

Revision ID: 0006_phase14_leave_management
Revises: 0005_phase13_attendance
Create Date: 2026-07-09 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '0006_phase14_leave_management'
down_revision = '0005_phase13_attendance'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'leave_requests',
        sa.Column('leave_request_id', sa.String(36), nullable=False),
        sa.Column('company_id', sa.String(36), nullable=False),
        sa.Column('employee_id', sa.String(36), nullable=False),
        sa.Column('leave_type', sa.Enum('casual_leave', 'sick_leave', 'earned_leave', 'medical_leave', 'maternity_leave', 'paternity_leave', 'bereavement_leave', 'compensatory_off', 'unpaid_leave', 'other', name='leave_type'), nullable=False),
        sa.Column('start_date', sa.Date, nullable=False),
        sa.Column('end_date', sa.Date, nullable=False),
        sa.Column('days_requested', sa.Integer, nullable=False),
        sa.Column('reason', sa.Text, nullable=True),
        sa.Column('status', sa.Enum('draft', 'pending', 'approved', 'rejected', 'cancelled', 'revoked', name='leave_status'), nullable=False, server_default='pending'),
        sa.Column('approved_by', sa.String(36), nullable=True),
        sa.Column('approved_at', sa.DateTime, nullable=True),
        sa.Column('rejection_reason', sa.Text, nullable=True),
        sa.Column('rejected_at', sa.DateTime, nullable=True),
        sa.Column('attachments', sa.JSON, nullable=True),
        sa.Column('notes', sa.Text, nullable=True),
        sa.Column('is_deleted', sa.Boolean, server_default='0', nullable=False),
        sa.Column('deleted_at', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.ForeignKeyConstraint(['company_id'], ['companies.company_id']),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.employee_id']),
        sa.PrimaryKeyConstraint('leave_request_id')
    )

    op.create_table(
        'leave_balances',
        sa.Column('balance_id', sa.String(36), nullable=False),
        sa.Column('company_id', sa.String(36), nullable=False),
        sa.Column('employee_id', sa.String(36), nullable=False),
        sa.Column('leave_type', sa.Enum('casual_leave', 'sick_leave', 'earned_leave', 'medical_leave', 'maternity_leave', 'paternity_leave', 'bereavement_leave', 'compensatory_off', 'unpaid_leave', 'other', name='leave_type'), nullable=False),
        sa.Column('financial_year', sa.String(9), nullable=False),
        sa.Column('total_allocated', sa.Integer, nullable=False, server_default='0'),
        sa.Column('used', sa.Integer, nullable=False, server_default='0'),
        sa.Column('pending', sa.Integer, nullable=False, server_default='0'),
        sa.Column('balance', sa.Integer, nullable=False, server_default='0'),
        sa.Column('carried_forward', sa.Integer, nullable=False, server_default='0'),
        sa.Column('last_updated', sa.DateTime, server_default=sa.func.now(), nullable=True),
        sa.Column('is_deleted', sa.Boolean, server_default='0', nullable=False),
        sa.Column('deleted_at', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.ForeignKeyConstraint(['company_id'], ['companies.company_id']),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.employee_id']),
        sa.PrimaryKeyConstraint('balance_id')
    )

    op.create_index('idx_leave_company_employee', 'leave_requests', ['company_id', 'employee_id'])
    op.create_index('idx_leave_company_status', 'leave_requests', ['company_id', 'status'])
    op.create_index('idx_leave_employee_dates', 'leave_requests', ['employee_id', 'start_date', 'end_date'])
    op.create_index('idx_leave_type', 'leave_requests', ['leave_type'])
    op.create_index('idx_leave_is_deleted', 'leave_requests', ['is_deleted'])
    op.create_index('idx_leave_balance_company_employee', 'leave_balances', ['company_id', 'employee_id'])
    op.create_index('idx_leave_balance_year', 'leave_balances', ['financial_year'])


def downgrade() -> None:
    op.drop_index('idx_leave_balance_year', table_name='leave_balances')
    op.drop_index('idx_leave_balance_company_employee', table_name='leave_balances')
    op.drop_index('idx_leave_is_deleted', table_name='leave_requests')
    op.drop_index('idx_leave_type', table_name='leave_requests')
    op.drop_index('idx_leave_employee_dates', table_name='leave_requests')
    op.drop_index('idx_leave_company_status', table_name='leave_requests')
    op.drop_index('idx_leave_company_employee', table_name='leave_requests')
    op.drop_table('leave_balances')
    op.drop_table('leave_requests')
