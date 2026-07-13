Module 1: Authentication & Authorization

users

id (PK)
employee_id (FK)
username
email
password_hash
is_active
is_verified
last_login
created_at
updated_at

roles

id
name
description
created_at

permissions

id
permission_name
module_name
action
description

role_permissions

id
role_id (FK)
permission_id (FK)

user_roles

id
user_id (FK)
role_id (FK)

Module 2: Company Management

companies

id
company_name
registration_number
gst_number
email
phone
website
address
city
state
country
postal_code
logo
status

branches

id
company_id (FK)
branch_name
manager_id (FK)
address
city
state
phone
email
status

Module 3: HRMS

departments

id
company_id
department_name
description

designations

id
department_id
designation_name
description

employees

id
employee_code
first_name
last_name
gender
dob
email
phone
address
joining_date
designation_id
department_id
branch_id
reporting_manager
employment_type
salary
profile_image
status

Module 4: Attendance

attendance

id
employee_id
attendance_date
check_in
check_out
working_hours
overtime_hours
status
Module 5: Leave
leave_types
id
leave_name
max_days

leave_requests

id
employee_id
leave_type_id
start_date
end_date
reason
approval_status
approved_by

Module 6: Payroll

payroll

id
employee_id
month
year
basic_salary
hra
allowances
deductions
tax
net_salary
payment_status

Module 7: Recruitment

jobs

id
title
department_id
openings
description
status

candidates

id
job_id
first_name
last_name
email
phone
resume
status

Module 8: Performance

performance_reviews

id
employee_id
reviewer_id
review_period
rating
remarks

Module 9: Training

trainings

id
training_name
trainer
duration
start_date
end_date

employee_trainings

id
employee_id
training_id
completion_status

Module 10: Project Management

projects

id
project_name
client_id
manager_id
start_date
end_date
budget
status

tasks

id
project_id
assigned_to
task_name
priority
due_date
progress
status

timesheets

id
employee_id
project_id
task_id
hours
work_date

Module 11: CRM

leads
id
lead_name
company
email
phone
source
status

clients

id
company_name
contact_person
email
phone
address

Module 12: Inventory

categories

id
category_name
description

products

id
category_id
product_name
sku
barcode
purchase_price
selling_price
reorder_level

warehouses

id
warehouse_name
location

inventory

id
warehouse_id
product_id
quantity
available_stock

Module 13: Procurement

suppliers

id
supplier_name
email
phone
address

purchase_orders

id
supplier_id
order_date
expected_date
total_amount
status

purchase_items

id
purchase_order_id
product_id
quantity
unit_price

Module 14: Sales

customers
id
customer_name
email
phone

sales_orders

id
customer_id
order_date
total_amount
status

invoices

id
sales_order_id
invoice_number
invoice_date
total_amount

payments

id
invoice_id
payment_date
amount
payment_method

Module 15: Finance

expenses

id
category
amount
expense_date
description

accounts

id
account_name
account_type
balance

transactions

id
account_id
amount
transaction_type
transaction_date

Module 16: Asset Management

assets

id
asset_name
asset_code
purchase_date
cost
assigned_employee
status

Module 17: Help Desk

tickets

id
employee_id
subject
priority
status
assigned_to

Module 18: Notifications

notifications

id
user_id
title
message
is_read

Module 19: Audit Logs

audit_logs

id
user_id
module
action
record_id
ip_address
created_at

Module 20: System Settings

settings

id
company_id
setting_key
setting_value