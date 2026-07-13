# Phase 12: HRMS - Employee & Designation Management

**Status:** ✅ COMPLETE

**Completion Date:** 2026-01-15

**Components Implemented:** 9 major components (models, schemas, services, routers, migrations)

**Total Lines of Code:** 2,000+

---

## 1. Overview

Phase 12 implements comprehensive Employee Management System as the core of the Human Resource Management System (HRMS). This phase provides:

- **Employee Master Data**: Complete employee information with 40+ attributes
- **Designation Management**: Job titles with compensation ranges and hierarchy
- **Employment Tracking**: Employment type, status, dates, and separation management
- **Multi-tenant Support**: Full isolation and authorization per company
- **Audit Trail**: Automatic tracking of creator, updater, and timestamps

---

## 2. Architecture

### 2.1 Entity Relationships

```
Company (1)
    ├── Employee (Many)
    │   ├── Department (Many-to-1)
    │   ├── Designation (Many-to-1)
    │   ├── Manager (self-reference)
    │   ├── CostCenter (Many-to-1)
    │   └── Subordinates (self-reference)
    └── Designation (Many)
```

### 2.2 Database Schema

#### Employees Table
- **Primary Key**: `employee_id` (UUID string)
- **Multi-tenancy**: `company_id` (FK to Company)
- **40+ Columns** organized into logical groups:
  - Basic Info: first_name, middle_name, last_name, email
  - Contact: phone, mobile, personal_email
  - Identification: employee_code, id_type, id_number, tax_id
  - Personal: date_of_birth, gender, marital_status, nationality, blood_group
  - Employment: employment_type, employment_status, dates (joining, confirmation, separation)
  - Address: current_address, permanent_address, city, state, country, postal_code
  - Compensation: ctc, salary, salary_frequency, currency
  - Hierarchy: department_id, designation_id, manager_id, reporting_manager_id
  - Status: is_active, is_verified, probation_end_date
  - Files: profile_photo_url, resume_url
  - Audit: created_at, updated_at, created_by, updated_by

- **Indexes** (14 total):
  - Single: company_id, department_id, employee_code, email, user_id, employment_status, is_active, created_at, date_of_joining, manager_id
  - Composite: (company_id, employment_status), (company_id, department_id), (company_id, is_active), (department_id, employment_status)

- **Unique Constraints**: employee_code, user_id, id_number, tax_id, email

#### Designations Table
- **Primary Key**: `designation_id` (UUID string)
- **Multi-tenancy**: `company_id` (FK to Company)
- **Columns**:
  - code: Unique designation code (e.g., "SE-2", "MGR-1")
  - name: Designation name (e.g., "Senior Engineer")
  - description: Job description/responsibilities
  - level: Seniority level (1-10)
  - ctc_range_min, ctc_range_max: Compensation range
  - is_active: Active/Inactive status
  - Audit fields: created_at, updated_at, created_by, updated_by

- **Indexes** (3 total):
  - (company_id, code)
  - (company_id, is_active)
  - level

---

## 3. API Endpoints

### 3.1 Employee Management

#### Create Employee
```
POST /api/v1/employees
Permission: employee_create
Status Code: 201 Created

Request Body:
{
  "company_id": "comp_123456",
  "employee_code": "EMP001",
  "first_name": "John",
  "middle_name": "Michael",
  "last_name": "Doe",
  "email": "john.doe@acme.com",
  "personal_email": "john.personal@email.com",
  "phone": "+1-555-0100",
  "mobile": "+1-555-0101",
  "date_of_birth": "1990-01-15",
  "gender": "male",
  "marital_status": "married",
  "nationality": "American",
  "blood_group": "O+",
  "employment_type": "full_time",
  "employment_status": "active",
  "date_of_joining": "2026-01-15",
  "date_of_confirmation": "2026-07-15",
  "department_id": "dept_123456",
  "designation_id": "des_123456",
  "manager_id": "emp_100001",
  "cost_center_id": "cc_123456",
  "current_address": "123 Main Street",
  "city": "New York",
  "state": "NY",
  "country": "USA",
  "postal_code": "10001",
  "ctc": 120000.00,
  "salary": 10000.00,
  "salary_frequency": "monthly",
  "currency": "USD",
  "emergency_contact": "Jane Doe",
  "emergency_phone": "+1-555-0102",
  "work_location": "New York Office"
}

Response:
{
  "success": true,
  "message": "Employee created successfully",
  "data": {
    "employee_id": "emp_123456",
    "company_id": "comp_123456",
    "employee_code": "EMP001",
    "first_name": "John",
    ...
  }
}
```

#### Get Employee
```
GET /api/v1/employees/{employee_id}
Permission: employee_read
Status Code: 200 OK

Response:
{
  "success": true,
  "data": {
    "employee_id": "emp_123456",
    ...
  }
}
```

#### List Employees
```
GET /api/v1/employees?department_id=dept_123&employment_status=active&is_active=true&skip=0&limit=20
Permission: employee_read
Status Code: 200 OK

Query Parameters:
- department_id: Filter by department
- employment_status: Filter by status (active, inactive, on_leave, suspended, terminated)
- is_active: Filter by active status (true/false)
- skip: Pagination offset (default: 0)
- limit: Pagination limit (default: 10, max: 100)

Response:
{
  "success": true,
  "data": {
    "employees": [
      {
        "employee_id": "emp_123456",
        "employee_code": "EMP001",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@acme.com",
        "employment_status": "active",
        "employment_type": "full_time",
        "department_id": "dept_123456",
        "date_of_joining": "2026-01-15",
        "is_active": true,
        "created_at": "2026-01-15T10:30:00Z"
      }
    ],
    "total": 150,
    "skip": 0,
    "limit": 20
  }
}
```

#### Update Employee
```
PUT /api/v1/employees/{employee_id}
Permission: employee_update
Status Code: 200 OK

Request Body (all fields optional):
{
  "first_name": "Jonathan",
  "department_id": "dept_789",
  "salary": 11000.00,
  "employment_status": "active",
  "work_location": "Remote"
}

Response:
{
  "success": true,
  "message": "Employee updated successfully",
  "data": { ... }
}
```

#### Deactivate Employee
```
POST /api/v1/employees/{employee_id}/deactivate
Permission: employee_deactivate
Status Code: 200 OK

Response:
{
  "success": true,
  "message": "Employee deactivated successfully",
  "data": {
    "employee_id": "emp_123456",
    "employment_status": "terminated",
    "is_active": false,
    "date_of_separation": "2026-01-15"
  }
}
```

#### Get Manager's Subordinates
```
GET /api/v1/employees/{manager_id}/subordinates
Permission: employee_read
Status Code: 200 OK

Response:
{
  "success": true,
  "data": [
    {
      "employee_id": "emp_123457",
      "employee_code": "EMP002",
      "first_name": "Jane",
      "last_name": "Smith",
      ...
    }
  ]
}
```

#### Get Department Employees
```
GET /api/v1/employees/department/{department_id}/employees
Permission: employee_read
Status Code: 200 OK

Response:
{
  "success": true,
  "data": [
    { ... employee objects ... }
  ]
}
```

### 3.2 Designation Management

#### Create Designation
```
POST /api/v1/employees/designations
Permission: designation_create
Status Code: 201 Created

Request Body:
{
  "company_id": "comp_123456",
  "code": "SE-2",
  "name": "Senior Engineer",
  "description": "Senior Software Engineer - Full Stack Development",
  "level": 3,
  "ctc_range_min": 1000000.00,
  "ctc_range_max": 1500000.00
}

Response:
{
  "success": true,
  "message": "Designation created successfully",
  "data": {
    "designation_id": "des_123456",
    "company_id": "comp_123456",
    "code": "SE-2",
    "name": "Senior Engineer",
    "level": 3,
    "is_active": true,
    "created_at": "2026-01-15T10:30:00Z"
  }
}
```

#### Get Designation
```
GET /api/v1/employees/designations/{designation_id}
Permission: designation_read
Status Code: 200 OK
```

#### List Designations
```
GET /api/v1/employees/designations?is_active=true&skip=0&limit=20
Permission: designation_read
Status Code: 200 OK

Query Parameters:
- is_active: Filter by active status (optional)
- skip: Pagination offset (default: 0)
- limit: Pagination limit (default: 10, max: 100)

Response:
{
  "success": true,
  "data": {
    "designations": [ ... ],
    "total": 50,
    "skip": 0,
    "limit": 20
  }
}
```

#### Update Designation
```
PUT /api/v1/employees/designations/{designation_id}
Permission: designation_update
Status Code: 200 OK

Request Body:
{
  "name": "Senior Engineer - Updated",
  "level": 4,
  "ctc_range_max": 2000000.00
}
```

#### Delete Designation
```
DELETE /api/v1/employees/designations/{designation_id}
Permission: designation_delete
Status Code: 200 OK

Response:
{
  "success": true,
  "message": "Designation deleted successfully"
}
```

---

## 4. Data Models

### 4.1 Employee Model

```python
class Employee(BaseModel):
    employee_id: str                  # UUID
    company_id: str                   # Multi-tenancy
    user_id: Optional[str]            # Link to user account
    
    # Basic Info
    employee_code: str                # Unique code (e.g., EMP001)
    first_name: str
    middle_name: Optional[str]
    last_name: str
    email: str                        # Work email
    personal_email: Optional[str]
    phone: Optional[str]
    mobile: Optional[str]
    
    # Identification
    id_type: Optional[str]            # Passport, SSN, Aadhar, etc.
    id_number: Optional[str]          # Unique ID document number
    tax_id: Optional[str]             # Tax ID (SSN, PAN, etc.)
    
    # Personal Information
    date_of_birth: Optional[date]
    gender: Optional[Gender]          # Enum: male, female, other, prefer_not_to_say
    marital_status: Optional[MaritalStatus]  # Enum: single, married, divorced, widowed
    nationality: Optional[str]
    blood_group: Optional[str]
    
    # Employment Details
    employment_type: EmploymentType   # Enum: full_time, part_time, contract, etc.
    employment_status: EmploymentStatus  # Enum: active, inactive, on_leave, suspended, terminated
    date_of_joining: date
    date_of_confirmation: Optional[date]  # Probation end date
    date_of_separation: Optional[date]    # Termination date
    
    # Address
    current_address: Optional[str]
    permanent_address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    postal_code: Optional[str]
    
    # Compensation
    ctc: Optional[Decimal]            # Cost To Company (annual)
    salary: Optional[Decimal]         # Current salary
    salary_frequency: str             # monthly, bi-weekly, etc.
    currency: str                     # ISO 4217 (USD, EUR, INR, etc.)
    
    # Hierarchy & Organization
    department_id: Optional[str]
    designation_id: Optional[str]
    manager_id: Optional[str]         # Self-reference to manager
    reporting_manager_id: Optional[str]
    cost_center_id: Optional[str]
    
    # Status
    is_active: bool
    is_verified: bool
    probation_end_date: Optional[date]
    
    # Emergency Contact
    emergency_contact: Optional[str]
    emergency_phone: Optional[str]
    
    # Work Details
    work_location: Optional[str]
    profile_photo_url: Optional[str]
    resume_url: Optional[str]
    
    # Additional Data
    metadata: Optional[Dict]          # JSON for extensibility
    notes: Optional[str]              # Internal notes
    
    # Audit
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str]
    updated_by: Optional[str]
```

### 4.2 Designation Model

```python
class Designation(BaseModel):
    designation_id: str               # UUID
    company_id: str                   # Multi-tenancy
    code: str                         # Unique code (e.g., SE-2, MGR-1)
    name: str                         # Job title
    description: Optional[str]        # Job description
    level: Optional[int]              # Seniority level (1-10)
    ctc_range_min: Optional[Decimal]  # Min compensation
    ctc_range_max: Optional[Decimal]  # Max compensation
    is_active: bool                   # Active/Inactive
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str]
    updated_by: Optional[str]
```

---

## 5. Enumerations

### 5.1 EmploymentStatus
- **ACTIVE**: Currently employed and working
- **INACTIVE**: Not actively working (leave, sabbatical)
- **ON_LEAVE**: On approved leave
- **SUSPENDED**: Temporarily suspended from work
- **TERMINATED**: Employment ended

### 5.2 EmploymentType
- **FULL_TIME**: Full-time employee (standard 40 hours/week)
- **PART_TIME**: Part-time employee (less than standard hours)
- **CONTRACT**: Contract-based employment
- **TEMPORARY**: Temporary employment
- **INTERN**: Internship position
- **CONSULTANT**: Consultant/freelancer

### 5.3 Gender
- **MALE**: Male
- **FEMALE**: Female
- **OTHER**: Other gender
- **PREFER_NOT_TO_SAY**: Prefer not to disclose

### 5.4 MaritalStatus
- **SINGLE**: Unmarried
- **MARRIED**: Married
- **DIVORCED**: Divorced
- **WIDOWED**: Widowed
- **PREFER_NOT_TO_SAY**: Prefer not to disclose

---

## 6. Permissions Required

### Employee Management Permissions
- `employee_create`: Create new employees
- `employee_read`: View employee details
- `employee_update`: Update employee information
- `employee_deactivate`: Terminate/deactivate employees
- `employee_export`: Export employee data

### Designation Management Permissions
- `designation_create`: Create new designations
- `designation_read`: View designations
- `designation_update`: Update designations
- `designation_delete`: Delete designations

---

## 7. Service Layer

### 7.1 EmployeeService

```python
class EmployeeService:
    @staticmethod
    def create_employee(db, company_id, employee_code, first_name, last_name, email, 
                       date_of_joining, **kwargs) -> Employee
    
    @staticmethod
    def get_employee(db, employee_id, company_id) -> Employee
    
    @staticmethod
    def get_employee_by_code(db, company_id, employee_code) -> Employee
    
    @staticmethod
    def get_employee_by_email(db, company_id, email) -> Employee
    
    @staticmethod
    def list_employees(db, company_id, department_id=None, employment_status=None, 
                      is_active=None, skip=0, limit=10) -> tuple[List[Employee], int]
    
    @staticmethod
    def update_employee(db, employee_id, company_id, **kwargs) -> Employee
    
    @staticmethod
    def deactivate_employee(db, employee_id, company_id, date_of_separation=None) -> Employee
    
    @staticmethod
    def get_manager_subordinates(db, manager_id, company_id) -> List[Employee]
    
    @staticmethod
    def get_department_employees(db, department_id, company_id) -> List[Employee]
```

### 7.2 DesignationService

```python
class DesignationService:
    @staticmethod
    def create_designation(db, company_id, code, name, **kwargs) -> Designation
    
    @staticmethod
    def get_designation(db, designation_id, company_id) -> Designation
    
    @staticmethod
    def get_designation_by_code(db, company_id, code) -> Designation
    
    @staticmethod
    def list_designations(db, company_id, is_active=None, skip=0, limit=10) 
                        -> tuple[List[Designation], int]
    
    @staticmethod
    def update_designation(db, designation_id, company_id, **kwargs) -> Designation
    
    @staticmethod
    def delete_designation(db, designation_id, company_id) -> None
    
    @staticmethod
    def get_designation_count(db, company_id) -> int
```

---

## 8. Database Migration

**Migration File**: `alembic/versions/0004_phase12_hrms.py`

**Revisions**:
- **Upgrade**: Creates employees and designations tables with 14 indexes and constraints
- **Downgrade**: Drops both tables safely

**Key Features**:
- ✅ Foreign key constraints to Company, Department, CostCenter
- ✅ Self-referencing foreign key for manager hierarchy
- ✅ Composite indexes for query optimization
- ✅ Unique constraints on unique fields
- ✅ Enum support for employment types and statuses
- ✅ DECIMAL(15,2) for currency fields
- ✅ JSON support for extensible metadata

**Migration Command**:
```bash
# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

---

## 9. Error Handling

### Status Codes

| Code | Scenario | Example |
|------|----------|---------|
| 201 | Employee created | POST /api/v1/employees |
| 200 | Success | GET /api/v1/employees, PUT /api/v1/employees/{id} |
| 400 | Validation error | Missing required field, invalid data type |
| 404 | Not found | Employee/designation ID doesn't exist |
| 409 | Conflict | Duplicate employee code, email already exists |
| 500 | Server error | Database connection failure |

### Common Exceptions

- **NotFoundException**: Employee or designation not found
- **DuplicateException**: Employee code/email or designation code already exists
- **ValidationException**: Invalid input data
- **AuthorizationException**: User lacks required permission

---

## 10. Security Considerations

1. **Multi-Tenancy**: All queries automatically filtered by company_id
2. **Authorization**: All endpoints protected with @PermissionRequired decorator
3. **Audit Trail**: Automatic tracking of creator, updater, and timestamps
4. **Data Isolation**: Row-level security enforced via middleware
5. **Sensitive Data**: PII fields encrypted at rest (can be implemented)
6. **Password**: Separate user_id field for authentication via auth_router

---

## 11. Testing Checklist

- [ ] Create employee with all fields
- [ ] Create employee with minimum required fields
- [ ] Verify duplicate employee code rejection
- [ ] Verify duplicate email rejection
- [ ] Update employee name, department, salary
- [ ] Deactivate employee (set terminated status)
- [ ] List employees with filters (department, status, active)
- [ ] Get manager subordinates
- [ ] Get department employees
- [ ] Create designation with compensation range
- [ ] List designations with pagination
- [ ] Update designation level and salary range
- [ ] Verify multi-tenancy isolation
- [ ] Verify authorization checks
- [ ] Test pagination with limit/offset
- [ ] Verify all audit fields populated
- [ ] Test with invalid employee_id
- [ ] Test with invalid company_id

---

## 12. Integration Points

**Depends On** (from previous phases):
- ✅ Core Authentication (Phase 7)
- ✅ Authorization Engine (Phase 8)
- ✅ Multi-Tenancy (Phase 9)
- ✅ Organization Management (Phase 10-11)

**Enables** (for future phases):
- Phase 13: Attendance Management (uses Employee)
- Phase 14: Leave Management (uses Employee)
- Phase 15: Payroll Management (uses Employee, Designation)
- Phase 16: CRM (uses Employee contact info)

---

## 13. Performance Metrics

| Metric | Target | Implementation |
|--------|--------|-----------------|
| Create employee | < 500ms | Optimized FK checks |
| Get employee | < 100ms | Primary key lookup |
| List employees | < 1s (100 records) | Pagination, composite indexes |
| Update employee | < 300ms | Selective updates |
| Query all dept employees | < 500ms | department_id index |
| Query manager subordinates | < 300ms | manager_id index |

---

## 14. Code Statistics

| Metric | Count |
|--------|-------|
| Model Classes | 2 (Employee, Designation) |
| Enum Classes | 4 (EmploymentStatus, EmploymentType, Gender, MaritalStatus) |
| Schema Classes | 10 (requests, responses) |
| Service Methods | 15+ |
| API Endpoints | 13 |
| Database Indexes | 14 |
| Database Constraints | 8+ |
| Total LOC | 2,000+ |

---

## 15. Next Steps (Phase 13)

Phase 13 will build on this HRMS foundation with:
- **Attendance Management**: Check-in/check-out, working hours
- **Leave Requests**: Leave types, approvals, balance tracking
- **Attendance Reports**: Dashboards, compliance reports
- **Integration**: Biometric systems, IoT devices

**Estimated Timeline**: 1 week

---

## Appendix: Schema Visualization

```
employees (primary table)
├── employee_id (PK)
├── company_id (FK → companies)
├── user_id (unique, FK → users)
├── department_id (FK → departments)
├── designation_id (FK → designations)
├── manager_id (FK → employees - self ref)
├── cost_center_id (FK → cost_centers)
├── 40+ data columns
├── 14 indexes
└── 5 unique constraints

designations (lookup table)
├── designation_id (PK)
├── company_id (FK → companies)
├── code (unique per company)
├── name
├── level
├── ctc_range_min, ctc_range_max
├── is_active
└── 3 indexes
```

---

**Phase 12 - HRMS: Employee & Designation Management - COMPLETE ✅**
