"""Phase 15: Payroll Management System

Revision ID: 0007_phase15_payroll_management
Revises: 0006_phase14_leave_management
Create Date: 2026-07-09 10:35:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '0007_phase15_payroll_management'
down_revision = '0006_phase14_leave_management'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'salary_structures',
        sa.Column('structure_id', sa.String(36), nullable=False),
        sa.Column('company_id', sa.String(36), nullable=False),
        sa.Column('employee_id', sa.String(36), nullable=False),
        sa.Column('effective_from', sa.Date, nullable=False),
        sa.Column('effective_to', sa.Date, nullable=True),
        sa.Column('ctc', sa.DECIMAL(precision=15, scale=2), nullable=False),
        sa.Column('basic_salary', sa.DECIMAL(precision=15, scale=2), nullable=False),
        sa.Column('hra', sa.DECIMAL(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('conveyance', sa.DECIMAL(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('medical_allowance', sa.DECIMAL(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('other_allowances', sa.DECIMAL(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('gross_salary', sa.DECIMAL(precision=15, scale=2), nullable=False),
        sa.Column('professional_tax', sa.DECIMAL(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('provident_fund', sa.DECIMAL(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('insurance', sa.DECIMAL(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('other_deductions', sa.DECIMAL(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('net_salary', sa.DECIMAL(precision=15, scale=2), nullable=False),
        sa.Column('frequency', sa.Enum('monthly', 'quarterly', 'half_yearly', 'annually', 'weekly', name='salary_frequency'), nullable=False, server_default='monthly'),
        sa.Column('currency', sa.String(3), nullable=False, server_default='USD'),
        sa.Column('notes', sa.Text, nullable=True),
        sa.Column('additional_details', sa.JSON, nullable=True),
        sa.Column('is_deleted', sa.Boolean, server_default='0', nullable=False),
        sa.Column('deleted_at', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.ForeignKeyConstraint(['company_id'], ['companies.company_id']),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.employee_id']),
        sa.PrimaryKeyConstraint('structure_id')
    )

    op.create_table(
        'payroll',
        sa.Column('payroll_id', sa.String(36), nullable=False),
        sa.Column('company_id', sa.String(36), nullable=False),
        sa.Column('employee_id', sa.String(36), nullable=False),
        sa.Column('salary_structure_id', sa.String(36), nullable=True),
        sa.Column('payroll_month', sa.Date, nullable=False),
        sa.Column('working_days', sa.DECIMAL(precision=5, scale=2), nullable=False),
        sa.Column('days_present', sa.DECIMAL(precision=5, scale=2), nullable=False, server_default='0'),
        sa.Column('days_absent', sa.DECIMAL(precision=5, scale=2), nullable=False, server_default='0'),
        sa.Column('days_leave', sa.DECIMAL(precision=5, scale=2), nullable=False, server_default='0'),
        sa.Column('attendance_based_salary', sa.DECIMAL(precision=15, scale=2), nullable=True),
        sa.Column('basic_salary', sa.DECIMAL(precision=15, scale=2), nullable=False),
        sa.Column('hra', sa.DECIMAL(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('conveyance', sa.DECIMAL(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('medical_allowance', sa.DECIMAL(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('other_allowances', sa.DECIMAL(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('bonus', sa.DECIMAL(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('incentive', sa.DECIMAL(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('gross_salary', sa.DECIMAL(precision=15, scale=2), nullable=False),
        sa.Column('professional_tax', sa.DECIMAL(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('provident_fund', sa.DECIMAL(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('insurance', sa.DECIMAL(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('loan_deduction', sa.DECIMAL(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('other_deductions', sa.DECIMAL(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('total_deductions', sa.DECIMAL(precision=15, scale=2), nullable=False),
        sa.Column('net_salary', sa.DECIMAL(precision=15, scale=2), nullable=False),
        sa.Column('advance_payment', sa.DECIMAL(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('final_amount', sa.DECIMAL(precision=15, scale=2), nullable=False),
        sa.Column('status', sa.Enum('draft', 'processed', 'approved', 'rejected', 'paid', 'voided', name='payroll_status'), nullable=False, server_default='draft'),
        sa.Column('approved_by', sa.String(36), nullable=True),
        sa.Column('approved_at', sa.DateTime, nullable=True),
        sa.Column('paid_date', sa.Date, nullable=True),
        sa.Column('payment_mode', sa.Enum('bank_transfer', 'cheque', 'cash', 'credit_card', 'digital_wallet', name='payment_mode'), nullable=True),
        sa.Column('reconciled', sa.String(1), nullable=True, server_default='N'),
        sa.Column('reconciliation_date', sa.DateTime, nullable=True),
        sa.Column('notes', sa.Text, nullable=True),
        sa.Column('payslip_url', sa.String(500), nullable=True),
        sa.Column('additional_data', sa.JSON, nullable=True),
        sa.Column('is_deleted', sa.Boolean, server_default='0', nullable=False),
        sa.Column('deleted_at', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column('created_by', sa.String(36), nullable=True),
        sa.Column('updated_by', sa.String(36), nullable=True),
        sa.ForeignKeyConstraint(['company_id'], ['companies.company_id']),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.employee_id']),
        sa.PrimaryKeyConstraint('payroll_id')
    )

    op.create_index('idx_salary_structure_employee', 'salary_structures', ['employee_id'])
    op.create_index('idx_salary_structure_company_active', 'salary_structures', ['company_id', 'effective_to'])
    op.create_index('idx_payroll_company_month', 'payroll', ['company_id', 'payroll_month'])
    op.create_index('idx_payroll_employee_month', 'payroll', ['employee_id', 'payroll_month'])
    op.create_index('idx_payroll_status', 'payroll', ['status'])
    op.create_index('idx_payroll_is_deleted', 'payroll', ['is_deleted'])


def downgrade() -> None:
    op.drop_index('idx_payroll_is_deleted', table_name='payroll')
    op.drop_index('idx_payroll_status', table_name='payroll')
    op.drop_index('idx_payroll_employee_month', table_name='payroll')
    op.drop_index('idx_payroll_company_month', table_name='payroll')
    op.drop_index('idx_salary_structure_company_active', table_name='salary_structures')
    op.drop_index('idx_salary_structure_employee', table_name='salary_structures')
    op.drop_table('payroll')
    op.drop_table('salary_structures')
