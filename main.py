from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import Base, engine
from routers.auth_router import router as auth_router
from routers.role_router import router as role_router
from routers.department_router import router as department_router
from routers.designation_router import router as designation_router
from routers.employee_router import router as employee_router
from routers.attendance_router import router as attendance_router
from routers.leave_router import router as leave_router
from routers.salary_router import router as salary_router
from routers.category_router import router as category_router
from routers.product_router import router as product_router
from routers.supplier_router import router as supplier_router
from routers.inventory_router import router as inventory_router
from routers.project_router import router as project_router
from routers.task_router import router as task_router
from routers.timesheet_router import router as timesheet_router
from routers.client_router import router as client_router
from routers.lead_router import router as lead_router
from routers.opportunity_router import router as opportunity_router
from routers.ticket_router import router as ticket_router
from routers.notification_router import router as notification_router
from routers.audit_log_router import router as audit_router
from routers.report_router import router as report_router
from routers.dashboard_router import router as dashboard_router
from middlewares.audit_middleware import AuditMiddleware

Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Authentication",
        "description": "Authentication & Authorization APIs"
    },
    {
        "name": "Roles",
        "description": "Role & Permission Management"
    },
    {
        "name": "Employees",
        "description": "Employee Management"
    },
    {
        "name": "Attendance",
        "description": "Attendance Management"
    },
    {
        "name": "Leave",
        "description": "Leave Management"
    },
    {
        "name": "Payroll",
        "description": "Payroll Management"
    },
    {
        "name": "Inventory",
        "description": "Inventory Management"
    },
    {
        "name": "Projects",
        "description": "Project Management"
    },
    {
        "name": "CRM",
        "description": "Customer Relationship Management"
    },
    {
        "name": "Support",
        "description": "Ticketing System"
    },
    {
        "name": "Reports",
        "description": "Reports APIs"
    },
    {
        "name": "Dashboard",
        "description": "Dashboard APIs"
    },
    {
        "name": "Audit",
        "description": "Audit Logs"
    }]

app = FastAPI(
    title="ERP Management System",
    version="1.0.0",
    description="""
    Enterprise Resource Planning System

    Modules:
    - Authentication
    - Employee Management
    - Attendance
    - Leave
    - Payroll
    - Inventory
    - Project Management
    - CRM
    - Support Tickets
    - Notifications
    - Audit Logs
    - Reports
    - Dashboard
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=tags_metadata
)

app.add_middleware(AuditMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
def health_check():
    return {
        "message": "ERP API Running Successfully",
        "version": "1.0.0"}

app.include_router(auth_router)
app.include_router(role_router)
app.include_router(department_router)
app.include_router(designation_router)
app.include_router(employee_router)
app.include_router(attendance_router)
app.include_router(leave_router)
app.include_router(salary_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(supplier_router)
app.include_router(inventory_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(timesheet_router)
app.include_router(client_router)
app.include_router(lead_router)
app.include_router(opportunity_router)
app.include_router(ticket_router)
app.include_router(notification_router)
app.include_router(audit_router)
app.include_router(report_router)
app.include_router(dashboard_router)

@app.get("/ping", tags=["Health"])
def ping():
    return {"status": "success", "message": "pong"}