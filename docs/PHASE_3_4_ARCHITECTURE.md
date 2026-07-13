# PHASES 3-4: SYSTEM ARCHITECTURE & DATABASE DESIGN

---

## PHASE 3: SYSTEM ARCHITECTURE

### 1. HIGH-LEVEL ARCHITECTURE (HLD)

#### 1.1 System Components Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Web Browser  │  │ Mobile App   │  │ Third-party  │          │
│  │              │  │              │  │ Integrations │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
└─────────┼──────────────────┼──────────────────┼──────────────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │ HTTPS/WSS
┌─────────────────────────────┼──────────────────────────────────────┐
│                    API GATEWAY & LOAD BALANCER                     │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Rate Limiting │ CORS │ Authentication │ Request Logging   │  │
│  └────────────────────────────────────────────────────────────┘  │
└─────────────────────────────┼──────────────────────────────────────┘
                             │
┌─────────────────────────────┼──────────────────────────────────────┐
│                    APPLICATION TIER (FASTAPI)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  Router      │  │  Router      │  │  Router      │           │
│  │  (Auth)      │  │  (Employee)  │  │  (Finance)   │           │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘           │
│         │                  │                  │                   │
│  ┌──────▼──────────────────▼──────────────────▼───────┐          │
│  │              SERVICE LAYER                          │          │
│  │  ┌─────────────────────────────────────────┐       │          │
│  │  │ Auth Service  │ Employee Service        │       │          │
│  │  │ Leave Service │ Payroll Service         │       │          │
│  │  │ Inventory Svc │ Finance Service         │       │          │
│  │  │ CRM Service   │ Project Service         │       │          │
│  │  │ Report Svc    │ Notification Service    │       │          │
│  │  └─────────────────────────────────────────┘       │          │
│  │                                                      │          │
│  │  ┌─────────────────────────────────────────┐       │          │
│  │  │     MIDDLEWARE & UTILITIES LAYER        │       │          │
│  │  │  ┌──────────────────────────────────┐   │       │          │
│  │  │  │ Auth Middleware (JWT Validation) │   │       │          │
│  │  │  │ Audit Middleware (Logging)       │   │       │          │
│  │  │  │ Rate Limiting Middleware         │   │       │          │
│  │  │  │ CORS Middleware                  │   │       │          │
│  │  │  └──────────────────────────────────┘   │       │          │
│  │  └─────────────────────────────────────────┘       │          │
│  │                                                      │          │
│  │  ┌─────────────────────────────────────────┐       │          │
│  │  │     DEPENDENCY INJECTION                │       │          │
│  │  │  • Database connections               │       │          │
│  │  │  • Service instances                   │       │          │
│  │  │  • Configuration objects               │       │          │
│  │  └─────────────────────────────────────────┘       │          │
│  └────────────────────────────────────────────────────┘          │
└─────────────────────────────┼──────────────────────────────────────┘
                             │
┌─────────────────────────────┼──────────────────────────────────────┐
│                    DATA ACCESS TIER                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ Repository   │  │ Repository   │  │ Repository   │           │
│  │ (Abstraction)│  │ (Abstraction)│  │ (Abstraction)│           │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘           │
│         │                  │                  │                   │
│  ┌──────▼──────────────────▼──────────────────▼───────┐          │
│  │    SQLALCHEMY ORM LAYER                            │          │
│  │  • Model mapping to tables                         │          │
│  │  • Query optimization                              │          │
│  │  • Relationship management                         │          │
│  └──────┬───────────────────────────────────────────┘          │
└─────────┼──────────────────────────────────────────────────────────┘
          │
┌─────────┼──────────────────────────────────────────────────────────┐
│         │                  DATABASE TIER                            │
│  ┌──────▼──────────────────────────────────────────┐              │
│  │            MYSQL DATABASE (Primary)              │              │
│  │  ┌──────────────────────────────────────────┐   │              │
│  │  │ 200+ Normalized Tables                   │   │              │
│  │  │ • Master Tables                          │   │              │
│  │  │ • Transaction Tables                     │   │              │
│  │  │ • Audit & Logging Tables                 │   │              │
│  │  └──────────────────────────────────────────┘   │              │
│  │                                                  │              │
│  │  Replication & Backup                           │              │
│  │  • Master-Slave replication                      │              │
│  │  • Daily incremental backups                     │              │
│  │  • Weekly full backups                           │              │
│  └──────────────────────────────────────────────────┘              │
│         │              │                │                          │
│    ┌────▼────┐    ┌────▼────┐    ┌────▼────┐                     │
│    │ Cache   │    │ Search  │    │ Archive │                     │
│    │ Redis   │    │ Elastic │    │ Storage │                     │
│    └─────────┘    └─────────┘    └─────────┘                     │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                  EXTERNAL SERVICES & INTEGRATIONS                    │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────┐  │
│  │  Email       │ │  SMS Service │ │ Payment     │ │ Analytics│  │
│  │  Service     │ │              │ │ Gateway     │ │ Service  │  │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────┘  │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│              BACKGROUND PROCESSING & MESSAGE QUEUE                   │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Message Queue (RabbitMQ / Celery)                             │  │
│  │  • Email notifications                                         │  │
│  │  • Payroll processing                                          │  │
│  │  • Report generation                                           │  │
│  │  • Data synchronization                                        │  │
│  │  • Scheduled tasks                                             │  │
│  └───────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                    MONITORING & LOGGING                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐               │
│  │  Logs        │ │  Metrics     │ │  Tracing     │               │
│  │  (ELK Stack) │ │  (Prometheus)│ │  (Jaeger)    │               │
│  └──────────────┘ └──────────────┘ └──────────────┘               │
└──────────────────────────────────────────────────────────────────────┘
```

#### 1.2 Architectural Layers

**1. Client Layer**
- Web browser (React/Vue.js)
- Mobile app (React Native/Flutter)
- Third-party integrations
- Desktop applications

**2. API Gateway & Load Balancer**
- Nginx/HAProxy for request distribution
- Rate limiting and throttling
- Request/Response logging
- SSL/TLS termination
- CORS handling

**3. Application Tier (FastAPI)**
- Request routing
- Dependency injection
- Middleware stack
- Business logic orchestration

**4. Service Layer**
- Business logic encapsulation
- Transaction management
- Workflow orchestration
- External service integration

**5. Repository/Data Access Layer**
- SQLAlchemy ORM abstractions
- Query optimization
- Connection pooling
- Cache layer integration

**6. Database Tier**
- MySQL primary database
- Redis cache (sessions, frequently accessed data)
- Elasticsearch (full-text search)
- Archive storage (old records)

**7. External Services**
- Email (SendGrid, AWS SES)
- SMS (Twilio)
- Payment gateways (Stripe, PayPal)
- Analytics services

**8. Background Processing**
- Celery + RabbitMQ
- Scheduled jobs (APScheduler)
- Event-driven processing
- Async task execution

**9. Monitoring & Observability**
- Structured logging (ELK Stack)
- Metrics (Prometheus)
- Distributed tracing (Jaeger)
- Health checks

#### 1.3 Multi-Tenancy Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Multi-Tenant Architecture                      │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ TENANT ISOLATION LAYER                                │ │
│  │ • Tenant ID from JWT                                 │ │
│  │ • Query filtering (WHERE tenant_id = :tid)           │ │
│  │ • Schema isolation (optional schema per tenant)       │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐         │
│  │  Tenant 1  │  │  Tenant 2  │  │  Tenant N  │         │
│  │  (Company1)│  │  (Company2)│  │  (CompanyN)│         │
│  │            │  │            │  │            │         │
│  │ Databases  │  │ Databases  │  │ Databases  │         │
│  │ Isolated   │  │ Isolated   │  │ Isolated   │         │
│  │            │  │            │  │            │         │
│  └────────────┘  └────────────┘  └────────────┘         │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ SHARED INFRASTRUCTURE                                │ │
│  │ • API Gateway                                        │ │
│  │ • Cache (Redis)                                      │ │
│  │ • Search Engine (Elasticsearch)                      │ │
│  │ • Message Queue                                      │ │
│  │ • Monitoring Stack                                   │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 1.4 Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PRODUCTION ENVIRONMENT                    │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │               KUBERNETES CLUSTER                     │ │
│  │                                                      │ │
│  │  Ingress (TLS Termination, Routing)                 │ │
│  │     │                                                │ │
│  │  ┌──▼─────────────────────────────────────────┐    │ │
│  │  │      FASTAPI POD REPLICAS (n=5)            │    │ │
│  │  │  • Horizontal auto-scaling                 │    │ │
│  │  │  • Load balancing                          │    │ │
│  │  │  • Health checks                           │    │ │
│  │  │  • Resource limits (CPU, Memory)           │    │ │
│  │  └──┬─────────────────────────────────────────┘    │ │
│  │     │                                                │ │
│  │  ┌──▼──────────────────────────────────────────┐   │ │
│  │  │    ConfigMaps & Secrets                    │   │ │
│  │  │  • Environment variables                   │   │ │
│  │  │  • Database credentials                    │   │ │
│  │  │  • API keys                                │   │ │
│  │  └───────────────────────────────────────────┘   │ │
│  │                                                      │ │
│  │  ┌──────────────────────────────────────────┐    │ │
│  │  │    PERSISTENT VOLUMES                    │    │ │
│  │  │  • Database storage                      │    │ │
│  │  │  • File uploads                          │    │ │
│  │  │  • Logs                                  │    │ │
│  │  └──────────────────────────────────────────┘    │ │
│  │                                                      │ │
│  │  ┌──────────────────────────────────────────┐    │ │
│  │  │    STATEFUL SERVICES                     │    │ │
│  │  │  • MySQL (Primary + Replicas)            │    │ │
│  │  │  • Redis (Cache)                         │    │ │
│  │  │  • Elasticsearch (Search)                │    │ │
│  │  │  • RabbitMQ (Message Broker)             │    │ │
│  │  └──────────────────────────────────────────┘    │ │
│  │                                                      │ │
│  └──────────────────────────────────────────────────┘ │
│                                                             │
│  Monitoring & Logging                                      │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  • Prometheus (Metrics Collection)                  │ │
│  │  • Grafana (Visualization)                          │ │
│  │  • ELK Stack (Logging)                              │ │
│  │  • Jaeger (Distributed Tracing)                     │ │
│  │  • AlertManager (Alerts)                            │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 1.5 Security Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                   SECURITY LAYERS                            │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 1. PERIMETER SECURITY                                 │ │
│  │    • DDoS Protection (Cloudflare/AWS Shield)          │ │
│  │    • WAF (Web Application Firewall)                   │ │
│  │    • SSL/TLS Encryption                              │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 2. APPLICATION SECURITY                               │ │
│  │    • JWT Authentication                              │ │
│  │    • RBAC Authorization                              │ │
│  │    • Input Validation                                │ │
│  │    • Output Encoding                                 │ │
│  │    • SQL Injection Prevention                        │ │
│  │    • XSS Protection                                  │ │
│  │    • CSRF Tokens                                     │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 3. DATA SECURITY                                       │ │
│  │    • Encryption at Rest (AES-256)                    │ │
│  │    • Encryption in Transit (TLS 1.3)                │ │
│  │    • Database Encryption                            │ │
│  │    • Secure Key Management                          │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 4. ACCESS CONTROL                                      │ │
│  │    • Resource-Level Authorization                    │ │
│  │    • Multi-Tenancy Isolation                         │ │
│  │    • Audit Trails                                    │ │
│  │    • Activity Logging                                │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 5. INFRASTRUCTURE SECURITY                            │ │
│  │    • Firewall Rules                                  │ │
│  │    • VPC/Network Segmentation                        │ │
│  │    • Secret Management                              │ │
│  │    • Regular Patching                               │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 2. LOW-LEVEL DESIGN (LLD)

#### 2.1 Detailed Component Architecture

**Authentication Module**
```python
# Components:
- JWT Token Generator
- Password Hasher (bcrypt)
- OAuth2 Provider
- MFA Handler (TOTP/SMS)
- Session Manager
- Refresh Token Manager

# Interfaces:
- authenticate(username, password)
- validate_token(token)
- refresh_token(refresh_token)
- verify_mfa(mfa_code)
- generate_jwt(user_id)
```

**Authorization Module**
```python
# Components:
- Permission Checker
- Role Evaluator
- Resource-Level Authorization
- Policy Engine
- Audit Logger

# Interfaces:
- check_permission(user, permission, resource)
- has_role(user, role)
- evaluate_policy(user, action, resource)
- log_auth_attempt(user, result)
```

**Employee Management Service**
```python
# Components:
- Employee Repository
- Department Repository
- Designation Repository
- Employee Service
- Validation Engine
- Notification Service

# Interfaces:
- create_employee(data)
- update_employee(emp_id, data)
- get_employee(emp_id)
- delete_employee(emp_id)
- get_department_employees(dept_id)
```

**Attendance Service**
```python
# Components:
- Attendance Repository
- Attendance Service
- Working Hours Calculator
- Overtime Calculator
- Attendance Validator
- Notification Service

# Interfaces:
- check_in(employee_id, location)
- check_out(employee_id)
- get_daily_attendance(employee_id, date)
- approve_attendance(att_id, status)
- calculate_working_hours(check_in, check_out)
```

**Leave Management Service**
```python
# Components:
- Leave Request Repository
- Leave Balance Repository
- Leave Service
- Balance Calculator
- Approval Workflow Engine
- Notification Service

# Interfaces:
- apply_leave(employee_id, data)
- approve_leave(leave_id, approved_by)
- get_leave_balance(employee_id)
- calculate_leave_entitlement(employee)
```

**Payroll Service**
```python
# Components:
- Salary Structure Repository
- Payroll Repository
- Payroll Service
- Salary Calculator
- Tax Calculator
- Payslip Generator
- Notification Service

# Interfaces:
- process_payroll(month, year)
- calculate_salary(employee_id, month)
- calculate_tax(gross_salary, tax_slab)
- generate_payslip(payroll_id)
- approve_payroll(payroll_id)
```

**CRM Service**
```python
# Components:
- Lead Repository
- Opportunity Repository
- Customer Repository
- CRM Service
- Lead Scoring Engine
- Opportunity Pipeline Manager

# Interfaces:
- create_lead(data)
- convert_lead_to_opportunity(lead_id)
- update_opportunity_stage(opp_id, stage)
- get_sales_pipeline()
- calculate_lead_score(lead_id)
```

**Inventory Service**
```python
# Components:
- Product Repository
- Warehouse Repository
- Inventory Repository
- Stock Movement Repository
- Inventory Service
- Stock Calculator
- Alert Generator

# Interfaces:
- add_stock(warehouse_id, product_id, quantity)
- reduce_stock(warehouse_id, product_id, quantity)
- get_stock_level(warehouse_id, product_id)
- transfer_stock(source_wh, dest_wh, product_id, qty)
- check_low_stock_alert(product_id)
```

**Procurement Service**
```python
# Components:
- Purchase Request Repository
- Purchase Order Repository
- Goods Receipt Repository
- Supplier Repository
- Procurement Service
- Approval Workflow Engine
- Matching Engine (3-way match)

# Interfaces:
- create_pr(data)
- create_po(pr_id, supplier_id)
- receive_goods(po_id, grn_data)
- match_po_invoice_grn(po_id, invoice_id, grn_id)
- process_payment(invoice_id)
```

**Sales Service**
```python
# Components:
- Quotation Repository
- Sales Order Repository
- Invoice Repository
- Sales Service
- Quotation Generator
- Invoice Generator
- Payment Tracker

# Interfaces:
- create_quotation(data)
- convert_quote_to_so(quote_id)
- create_invoice(so_id)
- track_payment(invoice_id, payment_data)
- generate_invoice_pdf(invoice_id)
```

**Finance Service**
```python
# Components:
- GL Account Repository
- Journal Entry Repository
- Finance Service
- Account Validator
- Financial Report Generator
- Reconciliation Engine

# Interfaces:
- create_journal_entry(data)
- post_entry(entry_id)
- generate_trial_balance(period)
- generate_balance_sheet(period)
- generate_profit_loss(period)
```

**Project Management Service**
```python
# Components:
- Project Repository
- Task Repository
- Milestone Repository
- Timesheet Repository
- Project Service
- Resource Allocator
- Progress Calculator

# Interfaces:
- create_project(data)
- create_task(project_id, data)
- assign_task(task_id, employee_id)
- log_timesheet(task_id, hours, work_date)
- update_task_progress(task_id, progress)
```

**Notification Service**
```python
# Components:
- Notification Repository
- Email Service
- SMS Service
- Push Notification Service
- Template Engine
- Queue Handler

# Interfaces:
- send_email(to, subject, template, data)
- send_sms(phone, message)
- send_push_notification(user_id, title, body)
- create_notification(user_id, type, data)
- get_user_notifications(user_id)
```

**Report Service**
```python
# Components:
- Report Repository
- Report Builder
- Chart Generator
- Export Service (PDF/Excel/CSV)
- Schedule Manager
- Analytics Engine

# Interfaces:
- generate_report(report_config)
- export_to_pdf(report_data)
- export_to_excel(report_data)
- schedule_report(config, frequency)
- generate_kpi_report(period)
```

---

## PHASE 4: DATABASE ARCHITECTURE

### 3. DATABASE DESIGN

#### 3.1 Complete ER Diagram Overview

The database consists of 200+ normalized tables across 15 major modules:

1. **Authentication & Authorization** (7 tables)
2. **Organization Management** (8 tables)
3. **HRMS** (25 tables)
4. **Attendance** (5 tables)
5. **Leave Management** (8 tables)
6. **Payroll** (12 tables)
7. **Recruitment** (8 tables)
8. **CRM** (15 tables)
9. **Inventory & Warehouse** (20 tables)
10. **Procurement** (18 tables)
11. **Sales** (15 tables)
12. **Finance & Accounting** (25 tables)
13. **Project Management** (15 tables)
14. **Workflow Engine** (12 tables)
15. **Audit & Logging** (12 tables)

#### 3.2 Comprehensive Table List (200+ Tables)

**MODULE 1: Authentication & Authorization**
```
1. users (user_id, email, username, password_hash, is_active, created_at)
2. user_profiles (profile_id, user_id, first_name, last_name, phone, photo_url)
3. user_devices (device_id, user_id, device_name, device_type, last_login)
4. roles (role_id, company_id, name, description, is_system_role)
5. permissions (permission_id, permission_code, module, action, description)
6. role_permissions (role_permission_id, role_id, permission_id)
7. user_roles (user_role_id, user_id, role_id, assigned_date)
```

**MODULE 2: Organization Management**
```
8. companies (company_id, name, registration_no, gst_no, established_date, status)
9. company_settings (setting_id, company_id, setting_key, setting_value)
10. branches (branch_id, company_id, name, manager_id, address, city, state)
11. branch_contacts (contact_id, branch_id, phone, email, fax)
12. cost_centers (cost_center_id, company_id, name, manager_id, budget)
13. departments (dept_id, branch_id, name, manager_id, cost_center_id)
14. teams (team_id, dept_id, name, lead_id, created_at)
15. team_members (member_id, team_id, employee_id, role_in_team)
```

**MODULE 3: HRMS - Employee Records**
```
16. employees (employee_id, company_id, emp_code, user_id, first_name, last_name)
17. employee_addresses (address_id, employee_id, address_type, full_address)
18. employee_contacts (contact_id, employee_id, phone, email, emergency_contact)
19. employee_documents (doc_id, employee_id, doc_type, doc_path, upload_date)
20. employee_education (edu_id, employee_id, qualification, institution, year)
21. employee_experience (exp_id, employee_id, company_name, designation, years)
22. employee_languages (lang_id, employee_id, language, proficiency)
23. employee_skills (skill_id, employee_id, skill_name, proficiency_level)
24. designations (designation_id, company_id, name, description, salary_range)
25. designation_hierarchy (hierarchy_id, parent_designation_id, child_designation_id)
26. job_roles (job_role_id, company_id, title, description, responsibilities)
27. employment_types (emp_type_id, name, description)
28. employment_contracts (contract_id, employee_id, emp_type_id, start_date, end_date)
29. employee_bank_info (bank_info_id, employee_id, bank_name, account_no, ifsc)
30. employee_tax_info (tax_info_id, employee_id, pan, aadhar, uan, esi_no)
31. employee_insurance (insurance_id, employee_id, policy_type, policy_no, amount)
32. employee_benefits (benefit_id, employee_id, benefit_type, start_date, end_date)
33. emergency_contacts (emerg_contact_id, employee_id, name, relation, phone)
34. employee_dependents (dependent_id, employee_id, name, relation, dob)
35. employee_status_history (hist_id, employee_id, status, from_date, to_date)
36. employee_promotions (promo_id, employee_id, old_designation, new_designation, date)
37. employee_transfers (transfer_id, employee_id, from_branch, to_branch, date)
38. employee_exit (exit_id, employee_id, exit_date, reason, settlement_amount)
39. reporting_structure (report_id, employee_id, manager_id, from_date, to_date)
40. employee_work_location (loc_id, employee_id, location, from_date, to_date)
```

**MODULE 4: Attendance**
```
41. attendance (attendance_id, employee_id, attendance_date, check_in, check_out)
42. attendance_approvals (approval_id, attendance_id, approver_id, status, remarks)
43. attendance_exceptions (exception_id, employee_id, exception_date, reason)
44. shift_definitions (shift_id, company_id, name, start_time, end_time)
45. employee_shifts (emp_shift_id, employee_id, shift_id, from_date, to_date)
```

**MODULE 5: Leave Management**
```
46. leave_types (leave_type_id, company_id, name, description, color_code)
47. leave_policies (policy_id, company_id, leave_type_id, annual_entitlement)
48. leave_accruals (accrual_id, employee_id, leave_type_id, accrued_date, quantity)
49. leave_balances (balance_id, employee_id, leave_type_id, current_balance)
50. leave_requests (leave_id, employee_id, leave_type_id, start_date, end_date)
51. leave_approvals (leave_approval_id, leave_id, approver_id, status)
52. leave_cancellations (cancel_id, leave_id, cancelled_by, reason)
53. leave_carry_forward (cf_id, employee_id, leave_type_id, amount, year)
```

**MODULE 6: Payroll**
```
54. salary_structures (struct_id, company_id, name, effective_date)
55. salary_components (component_id, struct_id, component_name, component_type)
56. employee_salary_structures (emp_struct_id, employee_id, struct_id, from_date)
57. payroll_runs (run_id, company_id, month, year, status, run_date)
58. payroll_records (payroll_id, run_id, employee_id, gross_salary, net_salary)
59. payroll_components (payroll_comp_id, payroll_id, component_id, amount)
60. payroll_deductions (deduction_id, payroll_id, deduction_type, amount)
61. payroll_taxes (tax_id, payroll_id, tax_type, amount, jurisdiction)
62. payslips (payslip_id, payroll_id, generated_date, pdf_path)
63. tax_slabs (tax_slab_id, company_id, financial_year, income_range, tax_rate)
64. provident_fund (pf_id, employee_id, month, year, pf_amount, employer_contribution)
65. bonus_records (bonus_id, employee_id, bonus_month, amount, approved_by)
```

**MODULE 7: Recruitment**
```
66. job_openings (opening_id, company_id, job_title, dept_id, no_of_positions)
67. job_descriptions (jd_id, opening_id, description, responsibilities, qualifications)
68. candidates (candidate_id, opening_id, first_name, last_name, email, phone)
69. candidate_documents (candidate_doc_id, candidate_id, doc_type, doc_path)
70. candidate_evaluations (eval_id, candidate_id, evaluator_id, rating, feedback)
71. interview_schedules (interview_id, candidate_id, scheduled_date, interviewer_id)
72. interview_results (result_id, interview_id, rating, feedback, status)
73. offer_letters (offer_id, candidate_id, approved_date, salary, offer_document)
```

**MODULE 8: Performance & Training**
```
74. performance_reviews (review_id, employee_id, reviewer_id, review_period)
75. performance_metrics (metric_id, review_id, metric_name, rating, comments)
76. performance_goals (goal_id, employee_id, goal_description, target_value)
77. goal_tracking (tracking_id, goal_id, tracking_date, progress_percentage)
78. training_programs (program_id, company_id, name, duration, trainer)
79. training_schedules (schedule_id, program_id, start_date, end_date, location)
80. employee_trainings (emp_training_id, employee_id, program_id, completion_status)
81. training_feedback (feedback_id, emp_training_id, rating, comments)
82. competency_matrix (competency_id, job_role_id, competency_name, level)
83. employee_competencies (emp_competency_id, employee_id, competency_id, level)
```

**MODULE 9: CRM - Lead Management**
```
84. leads (lead_id, company_id, lead_name, company_name, email, phone)
85. lead_sources (source_id, lead_id, source_type, reference)
86. lead_status_history (status_hist_id, lead_id, status, changed_date)
87. lead_scoring (score_id, lead_id, score_value, last_updated)
88. lead_activities (activity_id, lead_id, activity_type, activity_date)
89. lead_attachments (attach_id, lead_id, file_path, upload_date)
90. customers (customer_id, lead_id, company_id, business_type)
91. customer_addresses (cust_addr_id, customer_id, addr_type, address)
92. customer_contacts (cust_contact_id, customer_id, person_name, designation)
93. customer_interactions (interaction_id, customer_id, interaction_type, date)
94. customer_preferences (preference_id, customer_id, preference_key, value)
95. opportunities (opportunity_id, customer_id, opp_name, estimated_value)
96. opportunity_stages (opp_stage_id, opportunity_id, stage_name, entered_date)
97. opportunity_competitors (competitor_id, opportunity_id, competitor_name)
98. opportunity_activities (opp_activity_id, opportunity_id, activity, activity_date)
99. follow_ups (followup_id, customer_id, scheduled_date, follow_up_type, status)
100. customer_documents (cust_doc_id, customer_id, doc_type, doc_path)
```

**MODULE 10: Inventory & Warehouse**
```
101. categories (category_id, company_id, name, description, parent_category_id)
102. brands (brand_id, company_id, name, description)
103. products (product_id, category_id, brand_id, name, description, sku)
104. product_variants (variant_id, product_id, variant_name, variant_sku)
105. product_pricing (pricing_id, product_id, cost_price, selling_price, currency)
106. product_tax_info (tax_id, product_id, tax_type, tax_rate)
107. product_images (image_id, product_id, image_url, is_primary)
108. product_specifications (spec_id, product_id, spec_key, spec_value)
109. product_documents (prod_doc_id, product_id, doc_type, doc_path)
110. warehouses (warehouse_id, company_id, name, manager_id, address, city)
111. warehouse_zones (zone_id, warehouse_id, zone_name, zone_type)
112. warehouse_racks (rack_id, zone_id, rack_code, rack_type, capacity)
113. warehouse_bins (bin_id, rack_id, bin_code, bin_type)
114. inventory (inventory_id, warehouse_id, product_id, quantity, reorder_level)
115. inventory_bins (inventory_bin_id, bin_id, inventory_id, quantity)
116. inventory_movements (movement_id, from_inventory_id, to_inventory_id, qty)
117. stock_transfers (transfer_id, from_warehouse_id, to_warehouse_id, transfer_date)
118. stock_transfer_details (detail_id, transfer_id, product_id, quantity)
119. physical_stock_count (count_id, warehouse_id, count_date, verified_by)
120. physical_count_details (count_detail_id, count_id, product_id, counted_qty)
```

**MODULE 11: Procurement**
```
121. suppliers (supplier_id, company_id, name, registration_no, gst_no)
122. supplier_addresses (supp_addr_id, supplier_id, addr_type, address)
123. supplier_contacts (supp_contact_id, supplier_id, person_name, designation)
124. supplier_bank_info (bank_info_id, supplier_id, bank_name, account_no)
125. supplier_documents (supp_doc_id, supplier_id, doc_type, doc_path)
126. supplier_ratings (rating_id, supplier_id, rating_date, quality, delivery, service)
127. supplier_payment_terms (term_id, supplier_id, term_type, days, discount_percent)
128. purchase_requests (pr_id, company_id, dept_id, requested_by, request_date)
129. purchase_request_items (pr_item_id, pr_id, product_id, quantity, unit_price)
130. purchase_request_approvals (pr_approval_id, pr_id, approver_id, status)
131. quotation_requests (qtn_req_id, pr_id, supplier_id, request_date)
132. quotations (quotation_id, qtn_req_id, supplier_id, quote_date, validity_date)
133. quotation_items (qtn_item_id, quotation_id, product_id, qty, unit_price)
134. purchase_orders (po_id, pr_id, supplier_id, po_date, delivery_date)
135. purchase_order_items (po_item_id, po_id, product_id, qty, unit_price)
136. purchase_order_approvals (po_approval_id, po_id, approver_id, status)
137. goods_receipt_notes (grn_id, po_id, receipt_date, received_by)
138. grn_items (grn_item_id, grn_id, po_item_id, qty_received, qty_accepted)
139. purchase_invoices (invoice_id, po_id, supplier_id, invoice_date, invoice_no)
140. purchase_invoice_items (inv_item_id, invoice_id, grn_item_id, qty, unit_price)
141. supplier_payments (payment_id, invoice_id, payment_date, amount, payment_method)
```

**MODULE 12: Sales**
```
142. quotations (sales_quote_id, customer_id, quote_date, validity_date)
143. quotation_items (quote_item_id, sales_quote_id, product_id, qty, unit_price)
144. quotation_approvals (quote_approval_id, sales_quote_id, approver_id, status)
145. sales_orders (so_id, customer_id, sales_quote_id, order_date)
146. sales_order_items (so_item_id, so_id, product_id, qty, unit_price)
147. sales_order_approvals (so_approval_id, so_id, approver_id, status)
148. sales_invoices (si_id, so_id, invoice_date, invoice_no)
149. sales_invoice_items (si_item_id, si_id, so_item_id, qty, unit_price)
150. sales_invoice_tax (tax_id, si_id, tax_type, tax_amount)
151. sales_returns (return_id, si_id, return_date, reason)
152. return_items (return_item_id, return_id, si_item_id, qty_returned)
153. credit_notes (credit_note_id, return_id, issue_date)
154. sales_discounts (discount_id, so_id, discount_type, discount_amount)
155. sales_payments (payment_id, si_id, payment_date, amount, payment_method)
156. payment_tracking (tracking_id, payment_id, status, updated_date)
```

**MODULE 13: Finance & Accounting**
```
157. chart_of_accounts (coa_id, company_id, account_code, account_name, type)
158. account_hierarchy (hierarchy_id, parent_account_id, child_account_id)
159. journal_entries (entry_id, company_id, entry_date, reference, description)
160. journal_entry_lines (line_id, entry_id, coa_id, debit_amount, credit_amount)
161. general_ledger (gl_id, coa_id, posting_date, entry_id, amount, balance)
162. trial_balance (tb_id, company_id, period, coa_id, debit, credit)
163. accounts_payable (ap_id, supplier_id, invoice_no, invoice_date, due_date)
164. accounts_payable_aging (aging_id, ap_id, aging_bucket, amount)
165. accounts_receivable (ar_id, customer_id, invoice_no, invoice_date, due_date)
166. accounts_receivable_aging (ar_aging_id, ar_id, aging_bucket, amount)
167. expense_claims (expense_id, employee_id, expense_date, category, amount)
168. expense_claim_items (item_id, expense_id, description, amount, receipt_path)
169. expense_approvals (approval_id, expense_id, approver_id, status)
170. fixed_assets (asset_id, company_id, asset_name, asset_type, cost)
171. asset_depreciation (depr_id, asset_id, month, depreciation_amount)
172. bank_accounts (bank_id, company_id, bank_name, account_no, balance)
173. bank_reconciliation (recon_id, bank_id, recon_date, cleared_balance)
174. cost_allocation (allocation_id, cost_center_id, gl_account_id, percentage)
175. budgets (budget_id, company_id, budget_period, total_amount, created_date)
176. budget_lines (budget_line_id, budget_id, coa_id, budgeted_amount)
177. budget_variance (variance_id, budget_line_id, actual_amount, variance)
```

**MODULE 14: Project Management**
```
178. projects (project_id, company_id, client_id, project_name, start_date, end_date)
179. project_milestones (milestone_id, project_id, milestone_name, target_date)
180. project_resources (resource_id, project_id, employee_id, role, allocation)
181. project_budgets (project_budget_id, project_id, total_budget, used_budget)
182. tasks (task_id, project_id, milestone_id, task_name, priority)
183. task_assignments (assignment_id, task_id, employee_id, assignment_date)
184. task_dependencies (dep_id, task_id, dependent_task_id, dependency_type)
185. task_progress (progress_id, task_id, progress_date, progress_percentage)
186. task_comments (comment_id, task_id, commented_by, comment_text, comment_date)
187. task_attachments (attach_id, task_id, file_path, upload_date)
188. timesheets (timesheet_id, employee_id, week_starting, submit_date)
189. timesheet_entries (entry_id, timesheet_id, task_id, hours, entry_date)
190. timesheet_approvals (approval_id, timesheet_id, approver_id, status)
191. project_expenses (proj_expense_id, project_id, expense_date, amount)
192. project_invoices (proj_invoice_id, project_id, invoice_date, invoice_amount)
193. project_risks (risk_id, project_id, risk_description, impact_level)
194. project_documents (proj_doc_id, project_id, doc_type, doc_path)
```

**MODULE 15: Workflow Engine**
```
195. workflow_definitions (workflow_id, company_id, name, trigger_event)
196. workflow_steps (step_id, workflow_id, step_number, step_name, action)
197. workflow_conditions (condition_id, step_id, field, operator, value)
198. workflow_approvers (approver_id, step_id, approver_role, level)
199. workflow_instances (instance_id, workflow_id, entity_type, entity_id)
200. workflow_step_approvals (approval_id, instance_id, step_id, approver_id, status)
201. escalation_rules (escalation_id, workflow_id, days, escalate_to_level)
202. notification_templates (template_id, company_id, template_name, subject)
203. template_variables (var_id, template_id, variable_name, placeholder)
204. sla_definitions (sla_id, workflow_id, target_time, escalation_time)
205. sla_tracking (tracking_id, instance_id, sla_id, created_at, target_time)
206. sla_breaches (breach_id, tracking_id, breach_date)
```

**MODULE 16: Audit & Logging**
```
207. audit_logs (audit_id, user_id, entity_type, entity_id, action, timestamp)
208. audit_changes (change_id, audit_id, field_name, old_value, new_value)
209. user_activity_logs (activity_id, user_id, activity_type, activity_date)
210. login_history (login_id, user_id, login_time, login_ip, device_info)
211. failed_login_attempts (attempt_id, username, attempt_time, ip_address)
212. permission_change_logs (perm_log_id, user_id, permission, old_value, new_value)
213. data_access_logs (access_id, user_id, entity_type, entity_id, access_date)
214. export_logs (export_id, user_id, export_type, data_size, export_date)
215. api_request_logs (request_id, user_id, endpoint, method, status_code)
216. api_response_logs (response_id, request_id, response_time, response_size)
217. system_error_logs (error_id, error_type, error_message, stack_trace)
218. data_sync_logs (sync_id, source_system, target_system, sync_status)
```

#### 3.3 Indexing Strategy

**Primary Indexes:**
- All tables: Primary Key (PK)
- All tables: Foreign Keys (FK)

**Business Logic Indexes:**
```sql
-- Authentication
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_company ON users(company_id);
CREATE INDEX idx_user_roles_user ON user_roles(user_id);

-- Employees
CREATE INDEX idx_employees_company ON employees(company_id);
CREATE INDEX idx_employees_dept ON employees(dept_id);
CREATE INDEX idx_employees_emp_code ON employees(emp_code);

-- Attendance
CREATE INDEX idx_attendance_employee ON attendance(employee_id);
CREATE INDEX idx_attendance_date ON attendance(attendance_date);
CREATE INDEX idx_attendance_emp_date ON attendance(employee_id, attendance_date);

-- Leave
CREATE INDEX idx_leave_employee ON leave_requests(employee_id);
CREATE INDEX idx_leave_dates ON leave_requests(start_date, end_date);
CREATE INDEX idx_leave_status ON leave_requests(status);

-- Payroll
CREATE INDEX idx_payroll_run ON payroll_records(run_id);
CREATE INDEX idx_payroll_employee ON payroll_records(employee_id);

-- CRM
CREATE INDEX idx_leads_company ON leads(company_id);
CREATE INDEX idx_leads_source ON leads(source_id);
CREATE INDEX idx_opportunities_customer ON opportunities(customer_id);

-- Inventory
CREATE INDEX idx_inventory_warehouse ON inventory(warehouse_id);
CREATE INDEX idx_inventory_product ON inventory(product_id);
CREATE INDEX idx_product_category ON products(category_id);

-- Orders
CREATE INDEX idx_po_supplier ON purchase_orders(supplier_id);
CREATE INDEX idx_so_customer ON sales_orders(customer_id);
CREATE INDEX idx_po_date ON purchase_orders(po_date);
CREATE INDEX idx_so_date ON sales_orders(order_date);

-- Finance
CREATE INDEX idx_journal_entry_date ON journal_entries(entry_date);
CREATE INDEX idx_journal_entry_coa ON journal_entry_lines(coa_id);
CREATE INDEX idx_gl_account_date ON general_ledger(posting_date);

-- Projects
CREATE INDEX idx_tasks_project ON tasks(project_id);
CREATE INDEX idx_tasks_assigned ON task_assignments(employee_id);

-- Audit
CREATE INDEX idx_audit_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_date ON audit_logs(timestamp);
```

#### 3.4 Partitioning Strategy

**By Company (Multi-Tenancy):**
```sql
-- Partition large tables by company_id for better query performance
ALTER TABLE employees PARTITION BY RANGE (company_id) (
    PARTITION p1 VALUES LESS THAN (100),
    PARTITION p2 VALUES LESS THAN (1000),
    PARTITION p3 VALUES LESS THAN (MAXVALUE)
);

ALTER TABLE attendance PARTITION BY RANGE (YEAR(attendance_date)) (
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p2026 VALUES LESS THAN (MAXVALUE)
);
```

#### 3.5 Data Archival Strategy

**Retention Policy:**
- Active data: Current year + 2 years online
- Archive data: 3-7 years in cold storage
- Deleted data: 30 days in soft-delete tables (compliance)

**Archive Tables:**
```sql
-- Archive tables for historical data
CREATE TABLE employees_archive LIKE employees;
CREATE TABLE payroll_archive LIKE payroll_records;
CREATE TABLE purchase_orders_archive LIKE purchase_orders;
CREATE TABLE sales_orders_archive LIKE sales_orders;

-- Scheduled archival job (yearly)
-- Transfer records older than 3 years to archive tables
-- Delete from active tables
```

#### 3.6 Backup Strategy

- **Daily**: Incremental backups (11 PM)
- **Weekly**: Full backups (Sunday 1 AM)
- **Monthly**: Archive to cloud storage
- **Replication**: Master-Slave replication for HA
- **Recovery**: RPO (Recovery Point Objective) < 1 hour, RTO < 30 minutes

---

### 4. PERFORMANCE TARGETS

| Metric | Target | Notes |
|---|---|---|
| API Response Time (p95) | < 200ms | Excludes file uploads/exports |
| Database Query (p95) | < 100ms | With proper indexing |
| Login Response | < 500ms | Including 2FA |
| Page Load | < 2 seconds | With caching |
| Concurrent Users | 10,000+ | Per deployment |
| Transactions/sec | 10,000+ | During peak hours |
| Database Size | 500GB+ | Grows with data volume |
| Cache Hit Ratio | > 95% | Redis caching strategy |

---

## COMPLETION STATUS

- ✅ Phase 3: High-Level Design (HLD) - COMPLETE
- ✅ Phase 4: Low-Level Design (LLD) & Database Design - COMPLETE

**Next Phases**: Configuration Framework (Phase 5-6), Authentication Platform (Phase 7), Authorization Engine (Phase 8)

---
