# PHASES 1-2: BUSINESS REQUIREMENT ANALYSIS & SOFTWARE REQUIREMENT SPECIFICATION

---

## PHASE 1: BUSINESS REQUIREMENT ANALYSIS (BRD)

### 1. EXECUTIVE SUMMARY

**Project Name:** Stackly Enterprise Resource Planning (ERP) Platform
**Version:** 1.0
**Date:** 2026-07-08
**Status:** In Development

The Stackly ERP is a comprehensive, multi-tenant enterprise resource planning platform designed to streamline and integrate all critical business processes including HRMS, CRM, Finance, Inventory, Sales, Procurement, Project Management, and Analytics.

---

### 2. STAKEHOLDER ANALYSIS

#### 2.1 Stakeholder Identification

| Stakeholder | Role | Responsibilities | Interest Level |
|---|---|---|---|
| **Super Admin** | System Administrator | System configuration, user management, security policies | Critical |
| **Company Admin** | Organizational Lead | Company settings, branch management, reporting | Critical |
| **HR Manager** | Personnel Management | Employee lifecycle, payroll, attendance, leave | High |
| **Finance Manager** | Financial Operations | GL, AP/AR, reporting, budgeting | High |
| **Project Manager** | Project Oversight | Project creation, task allocation, milestone tracking | High |
| **Department Manager** | Team Lead | Department operations, resource allocation | Medium |
| **Inventory Manager** | Warehouse Operations | Stock management, procurement, inventory balance | High |
| **Sales Manager** | Revenue Operations | Quotes, orders, customer management | High |
| **Procurement Officer** | Purchasing | Purchase requests, vendor management, receipts | High |
| **Employee** | End User | Attendance, leave requests, timesheets, updates | Medium |
| **Customer** | External User | Portal access, order tracking, communication | Low |
| **Supplier/Vendor** | External User | Collaboration, quotations, order management | Low |

#### 2.2 Stakeholder Needs

- **System-Level**: Scalability, reliability, security, compliance
- **Business-Level**: Integration, reporting, workflow automation, cost reduction
- **User-Level**: Ease of use, fast response, accessibility, mobile support

---

### 3. BUSINESS OBJECTIVES

1. **Centralize Operations** - Consolidate all business processes in a single platform
2. **Improve Efficiency** - Automate workflows and reduce manual processes by 70%
3. **Enable Analytics** - Provide real-time dashboards and insights for decision-making
4. **Support Growth** - Design for multi-tenancy to support enterprise scaling
5. **Ensure Security** - Implement enterprise-grade security and audit trails
6. **Reduce Costs** - Optimize resource utilization and operational costs
7. **Enhance Compliance** - Maintain audit trails and regulatory compliance

---

### 4. FUNCTIONAL REQUIREMENTS

#### 4.1 Authentication & Authorization Module
- JWT-based authentication with refresh tokens
- Multi-factor authentication (MFA) support
- OAuth2 integration for third-party services
- Role-Based Access Control (RBAC)
- Permission matrix system
- Device management and session tracking
- Password policies and account recovery

#### 4.2 Organization Management
- Multi-company support with isolation
- Branch/location management
- Department and team hierarchy
- Cost center management
- Organizational reporting structures

#### 4.3 Human Resources Management System (HRMS)
- Employee onboarding/offboarding
- Employee records management
- Attendance tracking (biometric/manual/GPS)
- Leave management (multiple types, workflows)
- Payroll processing and tax calculations
- Recruitment and candidate management
- Performance reviews and evaluations
- Training and development tracking

#### 4.4 Customer Relationship Management (CRM)
- Lead management and tracking
- Opportunity pipeline management
- Customer contact management
- Interaction history
- Follow-up scheduling
- Customer lifecycle management

#### 4.5 Inventory & Warehouse Management
- Multi-warehouse support
- Product categorization and management
- Stock level monitoring
- Inventory movements tracking
- Barcode/QR code support
- Batch and serial number tracking
- Stock reconciliation and cycle counting
- Low stock alerts

#### 4.6 Procurement Management
- Purchase request creation
- Quotation management
- Purchase order generation
- Goods receipt and quality inspection
- Vendor management
- Purchase history and analysis
- Approval workflows

#### 4.7 Sales Management
- Quotation generation
- Sales order creation
- Invoice generation
- Discount and promotion management
- Payment tracking
- Sales forecasting

#### 4.8 Finance & Accounting
- General ledger management
- Accounts payable (AP) management
- Accounts receivable (AR) tracking
- Journal entry posting
- Financial statements generation
- Budget vs actual analysis
- Tax compliance

#### 4.9 Project Management
- Project creation and planning
- Task assignment and tracking
- Milestone management
- Resource allocation
- Time tracking and timesheets
- Project budgeting and costing
- Status reporting

#### 4.10 Workflow Engine
- Configurable approval workflows
- Multi-level approvals
- Escalation policies
- SLA management
- Notification triggers
- Conditional logic

#### 4.11 Notification System
- Email notifications
- SMS alerts (optional)
- Push notifications
- In-app notifications
- Notification templates
- Webhook support

#### 4.12 Reporting & Analytics
- Pre-built dashboard reports
- Custom report builder
- Scheduled report generation
- Export to PDF/Excel/CSV
- Drill-down capabilities
- KPI tracking
- Analytics and forecasting

#### 4.13 Document Management
- File upload and storage
- Document versioning
- Access control
- OCR integration
- Metadata indexing

#### 4.14 Audit & Compliance
- Comprehensive audit trails
- User activity logging
- Data change tracking
- Compliance reporting
- Export audit logs

---

### 5. NON-FUNCTIONAL REQUIREMENTS

#### 5.1 Performance
- API response time < 200ms (p95)
- Support 10,000+ concurrent users
- Handle 1M+ transactions per day
- Query optimization with caching
- Connection pooling
- Load balancing

#### 5.2 Scalability
- Horizontal scaling capability
- Microservices-ready architecture
- Database partitioning support
- CDN integration
- Multi-region deployment

#### 5.3 Security
- OWASP Top 10 compliance
- End-to-end encryption
- Secure headers (CSP, HSTS, etc.)
- API rate limiting
- DDoS protection
- Regular security audits
- Penetration testing

#### 5.4 Availability & Reliability
- 99.9% uptime SLA
- Automated failover
- Backup and disaster recovery
- Database replication
- Health monitoring

#### 5.5 Maintainability
- Clean code architecture
- Comprehensive documentation
- Logging and monitoring
- Error handling and reporting
- Version control best practices

#### 5.6 Usability
- Intuitive UI/UX
- Mobile responsiveness
- Accessibility compliance (WCAG)
- Multi-language support
- Dark mode support

---

### 6. USE CASES

#### 6.1 Authentication & Authorization
**UC1: User Login**
- Actor: Employee
- Precondition: User has valid credentials
- Steps: Enter username/password → System validates → Generate JWT
- Postcondition: User logged in with session

**UC2: Multi-Factor Authentication**
- Actor: Employee
- Precondition: MFA enabled on account
- Steps: Enter username/password → Receive OTP → Verify OTP → Login
- Postcondition: User authenticated with enhanced security

**UC3: Permission Checking**
- Actor: System
- Precondition: User logged in
- Steps: User accesses resource → System checks permissions → Allow/Deny
- Postcondition: Resource access controlled

#### 6.2 Employee Management
**UC4: Add New Employee**
- Actor: HR Manager
- Steps: Fill employee form → Upload documents → Set designation → Save
- Postcondition: Employee record created, notifications sent

**UC5: Employee Onboarding**
- Actor: HR Manager
- Steps: Create employee → Assign to department → Configure access → Send credentials
- Postcondition: Employee setup complete

**UC6: Employee Offboarding**
- Actor: HR Manager
- Steps: Mark employee as inactive → Disable access → Archive data → Generate exit report
- Postcondition: Employee records archived

#### 6.3 Attendance Management
**UC7: Mark Attendance**
- Actor: Employee/Manager
- Steps: Check-in (capture location) → Work → Check-out
- Postcondition: Attendance recorded with working hours

**UC8: Approve Attendance**
- Actor: Manager
- Steps: Review pending attendance → Approve/Reject with remarks
- Postcondition: Attendance finalized

#### 6.4 Leave Management
**UC9: Apply for Leave**
- Actor: Employee
- Steps: Select leave type → Choose dates → Add reason → Submit
- Postcondition: Leave request submitted for approval

**UC10: Approve/Reject Leave**
- Actor: Manager
- Steps: Review leave request → Check balance → Approve/Reject
- Postcondition: Leave status updated, employee notified

#### 6.5 Payroll Management
**UC11: Generate Payroll**
- Actor: HR/Finance Manager
- Steps: Select month → Calculate salaries → Deductions → Tax → Approve → Generate slips
- Postcondition: Payroll processed, slips generated

#### 6.6 CRM Operations
**UC12: Create Lead**
- Actor: Sales Executive
- Steps: Enter lead info → Set source → Add tags → Save
- Postcondition: Lead created in pipeline

**UC13: Convert Lead to Opportunity**
- Actor: Sales Manager
- Steps: Select lead → Create opportunity → Set value → Stage
- Postcondition: Lead converted, opportunity tracked

#### 6.7 Inventory Management
**UC14: Add Product**
- Actor: Inventory Manager
- Steps: Enter product info → Set pricing → Define warehouse levels → Save
- Postcondition: Product added to catalog

**UC15: Stock Transfer**
- Actor: Warehouse Manager
- Steps: Select product → Enter quantity → Choose source/destination warehouse → Confirm
- Postcondition: Stock moved, history tracked

#### 6.8 Purchase Management
**UC16: Create Purchase Order**
- Actor: Procurement Officer
- Steps: Create PR → Get quotations → Create PO → Send to vendor → Track delivery
- Postcondition: PO sent, goods receipt awaited

#### 6.9 Sales Management
**UC17: Create Sales Order**
- Actor: Sales Executive
- Steps: Create quote → Customer review → Convert to SO → Generate invoice → Track payment
- Postcondition: Sale recorded, revenue recognized

#### 6.10 Project Management
**UC18: Create Project**
- Actor: Project Manager
- Steps: Define project → Set dates/budget → Create milestones → Assign team
- Postcondition: Project setup, team notified

**UC19: Track Task Progress**
- Actor: Team Lead
- Steps: Assign tasks → Track progress → Update status → Log hours
- Postcondition: Task metrics updated

#### 6.11 Reporting
**UC20: Generate Report**
- Actor: Manager
- Steps: Select report type → Apply filters → Generate → Export (PDF/Excel)
- Postcondition: Report generated and available

---

### 7. ACCEPTANCE CRITERIA

#### 7.1 Functional Acceptance
- [ ] All APIs return correct HTTP status codes
- [ ] All CRUD operations work correctly
- [ ] User permissions enforced on all endpoints
- [ ] Pagination, sorting, filtering work as specified
- [ ] Validation errors returned with clear messages
- [ ] Audit trails capture all data modifications
- [ ] Notifications sent per configured templates

#### 7.2 Performance Acceptance
- [ ] API response time within SLA (< 200ms p95)
- [ ] Database queries optimized with proper indexing
- [ ] Caching implemented for frequently accessed data
- [ ] Concurrent user load tests pass (10K+ users)
- [ ] No memory leaks detected in stress testing

#### 7.3 Security Acceptance
- [ ] All sensitive data encrypted at rest and in transit
- [ ] JWT tokens expire properly and refresh works
- [ ] Password policies enforced and hashing secured
- [ ] SQL injection and XSS protections in place
- [ ] Rate limiting prevents abuse
- [ ] CORS properly configured

#### 7.4 Usability Acceptance
- [ ] UI responsive on mobile/tablet/desktop
- [ ] All forms have clear labels and help text
- [ ] Error messages are user-friendly
- [ ] Navigation is intuitive
- [ ] Accessibility standards met (WCAG 2.1)

#### 7.5 Documentation Acceptance
- [ ] API documentation (Swagger) complete
- [ ] Database schema documented
- [ ] Setup and deployment guides provided
- [ ] User manual provided
- [ ] Code comments explain complex logic

---

### 8. BUSINESS RULES

1. **Company Isolation**: Data strictly isolated per company/tenant
2. **User Roles**: Super Admin > Company Admin > Department Managers > Employees
3. **Leave Balance**: Cannot approve leaves exceeding available balance
4. **Purchase Approval**: POs over threshold require higher-level approval
5. **Payroll Lock**: Payroll cannot be modified after finalization
6. **Audit Immutability**: Audit logs cannot be deleted or modified
7. **Duplicate Prevention**: System prevents duplicate entries (employees, products, vendors)
8. **Cascading Deletes**: Prevented for referential integrity
9. **Data Retention**: Historical data retained per compliance requirements
10. **Transaction Integrity**: All financial transactions ACID-compliant

---

### 9. CONSTRAINTS

#### 9.1 Technical Constraints
- Python 3.12+ (FastAPI framework)
- MySQL 8.0+ database
- Deployment on Linux servers
- Docker containerization required

#### 9.2 Regulatory Constraints
- GDPR compliance for EU data
- Local tax law compliance for payroll
- Financial reporting standards (IFRS/GAAP)
- Data residency requirements

#### 9.3 Budget & Timeline Constraints
- Development timeline: 6-9 months
- MVP delivery in 3 months
- Budget allocated for infrastructure, licenses, resources

#### 9.4 Organizational Constraints
- Existing system integration required
- Third-party API integrations (payments, email, SMS)
- Multi-timezone support
- Multi-language support (initially 3 languages)

---

### 10. RISKS & MITIGATION

| Risk | Impact | Probability | Mitigation |
|---|---|---|---|
| Data Migration Failure | High | Medium | Staged migration, rollback plan |
| Performance Issues | High | Low | Load testing, optimization early |
| Security Breach | Critical | Low | Security audits, pen testing |
| User Adoption | High | Medium | Training, change management |
| Third-party API Failures | Medium | Low | Fallback mechanisms, redundancy |
| Database Scaling Issues | High | Low | Partitioning strategy, optimization |

---

## PHASE 2: SOFTWARE REQUIREMENT SPECIFICATION (SRS)

### 11. SYSTEM OVERVIEW

The Stackly ERP is a multi-tenant, cloud-native enterprise platform built with FastAPI (Python), MySQL, and modern web technologies. It provides integrated management of all business operations with role-based access, real-time notifications, comprehensive reporting, and audit capabilities.

**Key Characteristics:**
- Multi-tenant SaaS architecture
- RESTful API-first design
- Real-time data synchronization
- Workflow automation capabilities
- Comprehensive reporting engine
- Mobile-responsive interface
- Enterprise-grade security

---

### 12. DETAILED USER STORIES

#### 12.1 Authentication & Authorization
**US1: User Registration**
```
As a new Super Admin
I want to register and set up the system
So that I can initialize the platform
Acceptance Criteria:
- Super Admin can create initial account
- Email verification required
- Password complexity enforced (min 12 chars, upper, lower, digit, special)
- Account locked after 5 failed attempts
- Login attempt logged with timestamp and IP
```

**US2: Role-Based Access**
```
As a Company Admin
I want to assign roles to users
So that I can control system access
Acceptance Criteria:
- Only Super Admin can create roles
- Roles can be assigned/revoked dynamically
- Permission matrix shown visually
- Changes logged in audit trail
- Permission cache refreshed within 30 seconds
```

**US3: Multi-Factor Authentication**
```
As a Security Manager
I want to enforce MFA for sensitive users
So that I can enhance security
Acceptance Criteria:
- MFA can be mandatory or optional per role
- Support TOTP (Google Authenticator) and SMS
- Recovery codes provided during setup
- MFA bypass only by Super Admin with audit
```

#### 12.2 Employee Management
**US4: Employee Onboarding Workflow**
```
As an HR Manager
I want to execute an automated onboarding workflow
So that employee setup is consistent and complete
Acceptance Criteria:
- Workflow steps: Create record → Verify data → Assign role → Send credentials
- System sends credentials automatically
- Employee marked ready when all steps complete
- Email/SMS reminders for pending approvals
- Onboarding status tracked with timestamps
```

**US5: Employee Directory**
```
As an Employee
I want to search and view colleague profiles
So that I can find contact information
Acceptance Criteria:
- Search by name, email, department, location
- View profile includes org hierarchy
- Contact information displayed appropriately
- Privacy settings respected (hide/show fields)
```

**US6: Department Hierarchy**
```
As a Company Admin
I want to manage organizational structure
So that I can reflect current hierarchy
Acceptance Criteria:
- Create/Edit/Delete departments
- Set department managers
- View hierarchy tree visualization
- Reporting relationships enforced
- Data consistency maintained
```

#### 12.3 Attendance Management
**US7: Attendance Tracking**
```
As an Employee
I want to mark my attendance quickly
So that I can record my work hours
Acceptance Criteria:
- Check-in: 1 click, captures timestamp and location
- Check-out: 1 click, calculates working hours
- Manual entry allowed for emergency/absence
- Automatic over-time calculation
- Weekly report auto-generated
- Bulk operations for team leads
```

**US8: Attendance Approval**
```
As a Manager
I want to approve/reject attendance
So that I can ensure accuracy
Acceptance Criteria:
- Daily pending list visible
- Bulk approve/reject capability
- Add remarks for rejection
- Email notification of status
- Exception handling for outliers
- Historical tracking of changes
```

#### 12.4 Leave Management
**US9: Leave Request & Approval**
```
As an Employee
I want to request leave easily
So that I can plan time off
Acceptance Criteria:
- Self-service leave request form
- Real-time balance display
- Date range selection with weekend exclusion
- Reason required with optional attachments
- Email notification to manager
- Mobile-optimized form
- Calendar integration showing blackout dates
```

**US10: Leave Balance Management**
```
As an HR Manager
I want to manage leave balances
So that I can track leaves accurately
Acceptance Criteria:
- Annual reset on specific date
- Carry-forward rules configurable (max 10 days)
- Leaves accrued monthly
- Encashment rules defined
- Leave types include: Annual, Sick, Personal, Maternity, etc.
- Negative balance prevention
```

#### 12.5 Payroll Management
**US11: Payroll Processing**
```
As a Finance Manager
I want to process payroll efficiently
So that employees get paid on time
Acceptance Criteria:
- Monthly payroll run (customizable date)
- Automatic calculations: Gross → Deductions → Net
- Tax calculations per employee and jurisdiction
- Attendance/Leave deductions applied
- Bonus/Incentive additions applied
- Payroll lock after processing
- Audit trail for all changes
- Payslip generation in PDF
```

**US12: Salary Structure Configuration**
```
As an HR Manager
I want to define salary structures
So that I can manage compensation
Acceptance Criteria:
- Create structure with components: Basic, HRA, DA, Allowances, Deductions
- Assign to employees/departments
- Effective date management
- Version control for historical tracking
```

#### 12.6 CRM Operations
**US13: Lead Management**
```
As a Sales Executive
I want to manage leads in a pipeline
So that I can track sales opportunities
Acceptance Criteria:
- Create lead with: Name, Company, Email, Phone, Source
- Status pipeline: New → Contacted → Qualified → Proposal → Closed
- Lead assignment to sales team
- Follow-up reminders
- Activity history (calls, emails, meetings)
- Lead scoring based on interaction
```

**US14: Opportunity Pipeline**
```
As a Sales Manager
I want to view sales pipeline visually
So that I can forecast revenue
Acceptance Criteria:
- Kanban board showing opportunities by stage
- Drag-drop to update stage
- Probability and expected value displayed
- Forecast calculations (weighted by probability)
- Win/loss analysis
- Sales cycle metrics
```

#### 12.7 Inventory Management
**US15: Stock Level Management**
```
As an Inventory Manager
I want to track stock levels
So that I can prevent stockouts
Acceptance Criteria:
- Real-time stock updates across warehouses
- Low stock alerts (configurable threshold)
- Reorder point and quantity auto-calculated
- ABC analysis for prioritization
- Stock valuation (FIFO, LIFO, weighted average)
- Physical vs system stock reconciliation
```

**US16: Stock Transfers**
```
As a Warehouse Manager
I want to transfer stock between warehouses
So that I can optimize distribution
Acceptance Criteria:
- Create transfer request with approval workflow
- Track in-transit status
- Received confirmation with variance handling
- Transfer history with cost tracking
- Serial number tracking for high-value items
```

#### 12.8 Procurement
**US17: Purchase Request Workflow**
```
As a Department Manager
I want to create purchase requests
So that I can procure needed items
Acceptance Criteria:
- Self-service PR creation
- Approval based on amount threshold
- Budget check before approval
- Email notification to procurement
- PR tracking from creation to receipt
- Attachment support for specifications
```

**US18: Purchase Order Management**
```
As a Procurement Officer
I want to manage purchase orders
So that I can track supplier deliveries
Acceptance Criteria:
- Create PO from PR or standalone
- Add payment terms, delivery address
- Generate official PO document
- Email to supplier
- Goods Receipt matching (3-way match: PO, Invoice, Receipt)
- Invoice validation and payment processing
```

#### 12.9 Sales Management
**US19: Quotation Generation**
```
As a Sales Executive
I want to generate professional quotations
So that I can close sales
Acceptance Criteria:
- Template-based generation
- Product/Service selection with quantities
- Discount/Tax calculation
- Valid till date
- Generate PDF
- Email to customer
- Convert to Sales Order (1-click)
- Version control for changes
```

**US20: Invoice Processing**
```
As a Sales Manager
I want to manage invoices
So that I can track revenue
Acceptance Criteria:
- Generate from Sales Order automatically
- Invoice number auto-increment
- Tax calculation (VAT/GST)
- Payment terms tracking
- Payment reconciliation
- Credit note support
- Generate PDF and email to customer
```

#### 12.10 Project Management
**US21: Project Planning**
```
As a Project Manager
I want to create and plan projects
So that I can organize team work
Acceptance Criteria:
- Project creation with: Name, Client, Start/End date, Budget
- Milestone creation and tracking
- Task breakdown
- Resource allocation
- Budget tracking
- Gantt chart visualization
- Critical path analysis
```

**US22: Task Management & Tracking**
```
As a Team Lead
I want to manage team tasks
So that I can track progress
Acceptance Criteria:
- Task creation with: Title, Description, Assigned to, Priority, Due date
- Status updates (To-do, In Progress, Blocked, Done)
- Time logging for tasks
- Dependency management
- Comments and collaboration
- Notification on assignment/updates
- Activity history
```

#### 12.11 Financial Management
**US23: General Ledger Management**
```
As an Accountant
I want to maintain the general ledger
So that I can track all transactions
Acceptance Criteria:
- Create chart of accounts (Assets, Liabilities, Equity, Revenue, Expenses)
- Post journal entries
- Generate trial balance
- Period closing process
- Automated reconciliation
- Drill-down to source documents
```

**US24: Financial Reporting**
```
As a Finance Manager
I want to generate financial reports
So that I can analyze performance
Acceptance Criteria:
- Generate Balance Sheet
- Generate P&L Statement
- Generate Cash Flow Statement
- Compare periods (MoM, YoY)
- Export to PDF/Excel
- Print-ready format
```

#### 12.12 Reporting & Analytics
**US25: Custom Report Builder**
```
As a Manager
I want to create custom reports
So that I can analyze business metrics
Acceptance Criteria:
- Drag-drop column selection
- Filter by multiple criteria
- Group by fields
- Aggregation functions (Sum, Avg, Count, Max, Min)
- Sort by multiple columns
- Export to PDF/Excel/CSV
- Schedule recurring reports
```

**US26: Executive Dashboard**
```
As an Executive
I want to view key business metrics
So that I can monitor performance
Acceptance Criteria:
- Dashboard widgets (KPIs, Charts, Tables)
- Real-time data updates
- Customizable widget layout
- Drill-down capabilities
- Date range selector
- Export dashboard as PDF
```

---

### 13. BUSINESS RULES

#### 13.1 Employee Management
- No duplicate employee records (PAN/email unique)
- Employee must have designation and department
- Salary cannot be negative
- DOB cannot be future date
- Joining date cannot be before company establishment

#### 13.2 Attendance
- Check-in time must be after midnight of previous day
- Check-out cannot be before check-in
- Working hours calculated as (Check-out - Check-in) - Breaks
- Overtime triggered if working hours > 8 hours
- Attendance cannot be marked for future dates (except approved exceptions)

#### 13.3 Leave
- No leave before probation period (6 months)
- Leave balance cannot go negative
- Overlapping leaves not allowed
- Leave must be applied 2 days in advance (except emergency)
- Maternity leave cannot exceed policy limits

#### 13.4 Payroll
- Payroll finalized cannot be modified
- Tax calculated per government rates
- Gross cannot exceed max salary cap
- Deductions cannot exceed 50% of gross
- Bonus requires manager approval

#### 13.5 CRM
- Lead source is mandatory
- Duplicate leads checked by email/phone
- Lead cannot be deleted (only archived)
- Opportunity requires customer and product
- Closed opportunities cannot be reopened

#### 13.6 Inventory
- Stock level cannot go negative
- Reorder Point < Max Level
- Stock transfer quantity cannot exceed source warehouse balance
- Barcode unique per product
- SKU unique per company

#### 13.7 Procurement
- PO creation requires approved PR (except special cases)
- PO quantity cannot exceed PR quantity by > 10%
- Three-way match required: PO, Invoice, GRN
- Goods Receipt quantity cannot exceed PO quantity
- Payment cannot exceed invoice amount

#### 13.8 Sales
- Quotation requires customer and minimum 1 line item
- Quotation valid for 30 days (configurable)
- Discount cannot exceed 50% (policy-based)
- Sales Order requires approved Quotation
- Invoice cannot be generated until SO is confirmed

#### 13.9 Project
- Project end date must be after start date
- Budget cannot be negative
- Task cannot be assigned to unassigned PM
- Milestone date must be within project timeline
- Completed tasks cannot be reopened

#### 13.10 Finance
- Accounting entry must balance (Debit = Credit)
- No entry in restricted periods
- Currency must match GL
- All GL entries require audit trail
- Financial period cannot be opened without closing previous

---

### 14. CONSTRAINTS

#### 14.1 Data Constraints
- Employee ID: 10 alphanumeric, unique per company
- Email: RFC 5321 compliant
- Phone: Min 7, Max 15 digits
- Amounts: Max precision 2 decimals
- Dates: YYYY-MM-DD format
- Text fields: Max 500 chars unless specified

#### 14.2 Operational Constraints
- System maintenance window: 2 AM - 4 AM (daily, optional)
- No payroll processing during maintenance
- No critical data migration during business hours
- Maximum 1000 concurrent operations per tenant

#### 14.3 External Constraints
- Payment gateway API: Max 100 requests/minute
- Email service: Max 1000 emails/minute
- SMS service: Max 500 SMS/minute
- Third-party API timeouts: 30 seconds

#### 14.4 Compliance Constraints
- GDPR: Personal data deletion within 30 days of request
- Data residency: India-based servers only
- Audit retention: 7 years minimum
- Payroll compliance: Per government regulations
- GST: 5% to 28% (India-specific)

---

### 15. EDGE CASES & EXCEPTION HANDLING

#### 15.1 Employee Management
- **Edge Case**: Employee with no department → Error: Department required
- **Exception**: Mass leave approval by department during festival → Bulk operations
- **Edge Case**: Employee DOB update after data entry → Audit trail captured
- **Exception**: Employee retirement at 60 years → Auto-offboarding workflow

#### 15.2 Attendance
- **Edge Case**: Employee check-in twice same day → Latest check-in used
- **Exception**: No check-out recorded (overnight duty) → Manual entry allowed
- **Edge Case**: Check-in at 23:59 and check-out next day at 00:01 → Calculated correctly
- **Exception**: Holiday marked but employee worked → Manual correction

#### 15.3 Leave
- **Edge Case**: Leave applied for past dates (retroactive) → Only HR can approve
- **Exception**: Medical emergency leave approval (after return) → HR discretion
- **Edge Case**: Leave spanning multiple years → Deducted from current year first
- **Exception**: Leave on declared holiday → Treated as regular leave

#### 15.4 Payroll
- **Edge Case**: Mid-month salary revision → Prorated calculation
- **Exception**: Negative balance correction (overpayment) → Next month deduction
- **Edge Case**: Payroll with employee joining mid-month → Prorated salary
- **Exception**: Payroll with employee leaving mid-month → Final settlement

#### 15.5 CRM
- **Edge Case**: Lead without company name → Auto-generate from email domain
- **Exception**: Bulk lead import from CSV → Error handling per row
- **Edge Case**: Duplicate detection by fuzzy matching → Manual review required
- **Exception**: Lead conversion failure → Rollback to lead state

#### 15.6 Inventory
- **Edge Case**: Inventory adjustment with negative quantity → Audit required
- **Exception**: Stock transfer when source inventory insufficient → Error or partial transfer option
- **Edge Case**: Barcode duplication → Error prevention
- **Exception**: Physical count variance > 5% → Flag for investigation

#### 15.7 Procurement
- **Edge Case**: PO for discontinued product → Warning issued
- **Exception**: Rush procurement without full approval → Limited functionality
- **Edge Case**: Goods receipt without matching PO → Exception entry required
- **Exception**: Partial delivery → Multiple receipts allowed

#### 15.8 Sales
- **Edge Case**: Quotation for customer with no payment history → COD only
- **Exception**: Sale to blacklisted customer → Override with audit
- **Edge Case**: Invoice cancellation after payment → Refund processing
- **Exception**: Return after payment cleared → Credit note generation

#### 15.9 Project
- **Edge Case**: Task assigned to project without resources → Warning
- **Exception**: Task deadline missed → Escalation workflow
- **Edge Case**: Project completion before all tasks done → Warning required
- **Exception**: Project restart after closure → Re-open with audit

#### 15.10 Finance
- **Edge Case**: Entry in previous closed month → Reopening required
- **Exception**: Balance sheet discrepancy → Reconciliation workflow
- **Edge Case**: Currency conversion mid-period → Spot rate or average rate
- **Exception**: Duplicate entry detection → Prevent and alert

---

### 16. TECHNICAL SPECIFICATIONS

#### 16.1 API Design
- **Base URL**: `/api/v1`
- **Response Format**: JSON
- **Authentication**: Bearer Token (JWT)
- **Error Format**: 
  ```json
  {
    "status": "error",
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "errors": [{"field": "email", "message": "Invalid email format"}]
  }
  ```

#### 16.2 Database Schema Approach
- **Total Tables**: 200+ normalized tables
- **Normalization**: 3NF minimum
- **Indexing Strategy**: Primary key + Foreign keys + Business logic indices
- **Partitioning**: By company_id for multi-tenancy
- **Backup**: Daily incremental, weekly full backup
- **Archival**: Data > 5 years to archive tables

#### 16.3 Performance Targets
- API response: < 200ms (p95)
- Database query: < 100ms (p95)
- Page load: < 2 seconds
- Concurrent users: 10,000+
- Transactions/sec: 10,000+

#### 16.4 Security Specifications
- **Password**: Min 12 chars, 4 character types, hash with bcrypt
- **JWT**: 15-minute expiry, 7-day refresh token
- **HTTPS**: TLS 1.3
- **CORS**: Whitelist specific domains
- **Rate Limiting**: 100 requests/minute per user
- **Encryption**: AES-256 at rest, TLS in transit

---

### 17. ACCEPTANCE CRITERIA MATRIX

| Feature | Functional | Performance | Security | Usability |
|---|---|---|---|---|
| Employee Management | ✓ CRUD ops | < 100ms queries | Role-based access | Simple form |
| Attendance | ✓ Check-in/out | < 50ms | GPS optional | 1-click marking |
| Leave | ✓ Request/Approve | < 150ms | Approval trail | Calendar view |
| Payroll | ✓ Calculate/Process | < 500ms | Secure slips | Excel export |
| CRM | ✓ Leads/Oppty | < 100ms | Customer private | Kanban board |
| Inventory | ✓ Stock tracking | < 150ms | Multi-warehouse | Real-time updates |
| Procurement | ✓ PR to PO | < 200ms | 3-way match | Workflow visual |
| Sales | ✓ Quote to Invoice | < 200ms | Customer data secure | PDF generation |
| Project | ✓ Tasks/Milestones | < 150ms | Team access | Gantt chart |
| Finance | ✓ GL entries | < 100ms | Audit-proof | Statement report |

---

### 18. GLOSSARY

- **BRD**: Business Requirement Document
- **SRS**: Software Requirement Specification
- **ERP**: Enterprise Resource Planning
- **RBAC**: Role-Based Access Control
- **JWT**: JSON Web Token
- **ORM**: Object-Relational Mapping
- **API**: Application Programming Interface
- **GL**: General Ledger
- **AP**: Accounts Payable
- **AR**: Accounts Receivable
- **PO**: Purchase Order
- **GRN**: Goods Receipt Note
- **PR**: Purchase Request
- **KPI**: Key Performance Indicator
- **SLA**: Service Level Agreement
- **MFA**: Multi-Factor Authentication
- **GDPR**: General Data Protection Regulation
- **WCAG**: Web Content Accessibility Guidelines

---

## COMPLETION STATUS

- ✅ Phase 1: Business Requirement Analysis - COMPLETE
- ✅ Phase 2: Software Requirement Specification - COMPLETE

**Next Phases**: System Architecture (Phase 3-4), Design Documents, Implementation

---
