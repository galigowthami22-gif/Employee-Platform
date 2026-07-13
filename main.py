from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from core.database import Base, engine
from core.config import settings, get_settings, config_loader, feature_manager
from middlewares.multi_tenancy_middleware import MultiTenancyMiddleware
from routers.auth_router import router as auth_router
from routers.role_router import router as role_router
from routers.organization_router import router as organization_router
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

if settings.DEBUG:
    try:
        Base.metadata.create_all(bind=engine, checkfirst=True)
    except Exception as exc:
        logging.warning("Database schema initialization skipped: %s", exc)
else:
    logging.info("Database schema creation skipped on startup; use Alembic migrations instead.")

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
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    Enterprise Resource Planning System - Complete Platform
    
    Features:
    - Multi-tenant Architecture
    - Role-Based Access Control (RBAC)
    - HR & Payroll Management
    - Inventory & Warehouse Management
    - Sales & Procurement
    - Finance & Accounting
    - Project Management
    - CRM & Lead Management
    - Reports & Analytics
    - Workflow Automation
    - Audit & Compliance
    
    Modules:
    - Authentication & Authorization
    - Employee Management
    - Attendance & Leave
    - Payroll Processing
    - Inventory Management
    - Project Management
    - CRM
    - Support Tickets
    - Notifications
    - Audit Logs
    - Reports & Dashboards
    """,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.OPENAPI_URL,
    openapi_tags=tags_metadata
)

# Add middleware stack (order matters)
# 1. CORS first
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Multi-tenancy isolation
app.add_middleware(MultiTenancyMiddleware)

# 3. Audit middleware
app.add_middleware(AuditMiddleware)

@app.get("/", tags=["Health"])
def health_check():
    return {
        "message": "ERP API Running Successfully",
        "version": "1.0.0"}

def register_router(app: FastAPI, router) -> None:
    for route in getattr(router, "routes", []):
        if not getattr(route, "path", None):
            continue
        if getattr(route, "include_in_schema", True) is False:
            continue
        app.add_api_route(
            path=route.path,
            endpoint=route.endpoint,
            methods=list(route.methods),
            name=getattr(route, "name", None),
            include_in_schema=getattr(route, "include_in_schema", True),
            response_model=getattr(route, "response_model", None),
            status_code=getattr(route, "status_code", None),
            tags=getattr(route, "tags", None),
            dependencies=getattr(route, "dependencies", None),
            summary=getattr(route, "summary", None),
            description=getattr(route, "description", None),
            responses=getattr(route, "responses", None),
            deprecated=getattr(route, "deprecated", False),
            operation_id=getattr(route, "operation_id", None),
        )


def register_routers(app: FastAPI) -> None:
    for router in [
        auth_router,
        role_router,
        organization_router,
        department_router,
        designation_router,
        employee_router,
        attendance_router,
        leave_router,
        salary_router,
        category_router,
        product_router,
        supplier_router,
        inventory_router,
        project_router,
        task_router,
        timesheet_router,
        client_router,
        lead_router,
        opportunity_router,
        ticket_router,
        notification_router,
        audit_router,
        report_router,
        dashboard_router,
    ]:
        register_router(app, router)


register_routers(app)

@app.get("/ping", tags=["Health"])
def ping():
    return {"status": "success", "message": "pong"}