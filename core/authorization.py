"""
PHASE 8: AUTHORIZATION ENGINE
RBAC (Role-Based Access Control), Permission matrix, and Policy engine.
"""

from typing import Optional, List, Dict, Set, Callable
from enum import Enum
from functools import wraps
from pydantic import BaseModel
from fastapi import HTTPException, status


class PermissionAction(str, Enum):
    """Standard permission actions"""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    APPROVE = "approve"
    REJECT = "reject"
    EXPORT = "export"
    IMPORT = "import"
    BULK_UPDATE = "bulk_update"
    BULK_DELETE = "bulk_delete"


class RoleType(str, Enum):
    """Predefined system roles"""
    SUPER_ADMIN = "super_admin"
    COMPANY_ADMIN = "company_admin"
    HR_MANAGER = "hr_manager"
    FINANCE_MANAGER = "finance_manager"
    PROJECT_MANAGER = "project_manager"
    DEPARTMENT_MANAGER = "department_manager"
    TEAM_LEAD = "team_lead"
    EMPLOYEE = "employee"
    CUSTOMER = "customer"
    SUPPLIER = "supplier"


class Permission(BaseModel):
    """Permission definition"""
    code: str  # e.g., "employee.profile.create"
    name: str  # e.g., "Create Employee Profile"
    module: str  # e.g., "employee"
    resource: str  # e.g., "profile"
    action: str  # e.g., "create"
    description: str


class Role(BaseModel):
    """Role definition"""
    role_id: str
    name: str
    description: str
    permissions: Set[str]  # Permission codes
    is_system_role: bool = False


class User(BaseModel):
    """User with roles and permissions"""
    user_id: str
    company_id: str
    roles: Set[str]  # Role names
    permissions: Set[str]  # Permission codes
    department_id: Optional[str] = None
    is_active: bool = True


class PermissionRegistry:
    """Registry of all system permissions"""
    
    # Authentication & Authorization
    AUTH_PERMISSIONS = {
        "auth.login": Permission(
            code="auth.login",
            name="Login",
            module="auth",
            resource="login",
            action="execute",
            description="User login"
        ),
        "auth.logout": Permission(
            code="auth.logout",
            name="Logout",
            module="auth",
            resource="login",
            action="execute",
            description="User logout"
        ),
        "auth.refresh_token": Permission(
            code="auth.refresh_token",
            name="Refresh Token",
            module="auth",
            resource="token",
            action="create",
            description="Refresh access token"
        ),
    }
    
    # Employee Management
    EMPLOYEE_PERMISSIONS = {
        "employee.create": Permission(
            code="employee.create",
            name="Create Employee",
            module="employee",
            resource="employee",
            action="create",
            description="Create new employee record"
        ),
        "employee.read": Permission(
            code="employee.read",
            name="View Employee",
            module="employee",
            resource="employee",
            action="read",
            description="View employee details"
        ),
        "employee.update": Permission(
            code="employee.update",
            name="Update Employee",
            module="employee",
            resource="employee",
            action="update",
            description="Update employee information"
        ),
        "employee.delete": Permission(
            code="employee.delete",
            name="Delete Employee",
            module="employee",
            resource="employee",
            action="delete",
            description="Delete employee record"
        ),
        "employee.bulk_import": Permission(
            code="employee.bulk_import",
            name="Bulk Import Employees",
            module="employee",
            resource="employee",
            action="import",
            description="Import multiple employees"
        ),
        "employee.export": Permission(
            code="employee.export",
            name="Export Employees",
            module="employee",
            resource="employee",
            action="export",
            description="Export employee data"
        ),
    }
    
    # Attendance
    ATTENDANCE_PERMISSIONS = {
        "attendance.mark": Permission(
            code="attendance.mark",
            name="Mark Attendance",
            module="attendance",
            resource="attendance",
            action="create",
            description="Mark own attendance"
        ),
        "attendance.approve": Permission(
            code="attendance.approve",
            name="Approve Attendance",
            module="attendance",
            resource="attendance",
            action="approve",
            description="Approve team attendance"
        ),
        "attendance.view": Permission(
            code="attendance.view",
            name="View Attendance",
            module="attendance",
            resource="attendance",
            action="read",
            description="View attendance records"
        ),
    }
    
    # Leave
    LEAVE_PERMISSIONS = {
        "leave.apply": Permission(
            code="leave.apply",
            name="Apply Leave",
            module="leave",
            resource="leave",
            action="create",
            description="Apply for leave"
        ),
        "leave.approve": Permission(
            code="leave.approve",
            name="Approve Leave",
            module="leave",
            resource="leave",
            action="approve",
            description="Approve leave requests"
        ),
        "leave.cancel": Permission(
            code="leave.cancel",
            name="Cancel Leave",
            module="leave",
            resource="leave",
            action="delete",
            description="Cancel approved leave"
        ),
        "leave.view": Permission(
            code="leave.view",
            name="View Leave",
            module="leave",
            resource="leave",
            action="read",
            description="View leave records"
        ),
    }
    
    # Payroll
    PAYROLL_PERMISSIONS = {
        "payroll.process": Permission(
            code="payroll.process",
            name="Process Payroll",
            module="payroll",
            resource="payroll",
            action="create",
            description="Process monthly payroll"
        ),
        "payroll.approve": Permission(
            code="payroll.approve",
            name="Approve Payroll",
            module="payroll",
            resource="payroll",
            action="approve",
            description="Approve payroll"
        ),
        "payroll.view": Permission(
            code="payroll.view",
            name="View Payroll",
            module="payroll",
            resource="payroll",
            action="read",
            description="View payroll information"
        ),
        "payroll.export": Permission(
            code="payroll.export",
            name="Export Payroll",
            module="payroll",
            resource="payroll",
            action="export",
            description="Export payroll data"
        ),
    }
    
    # Finance
    FINANCE_PERMISSIONS = {
        "finance.create_entry": Permission(
            code="finance.create_entry",
            name="Create Journal Entry",
            module="finance",
            resource="journal_entry",
            action="create",
            description="Create journal entry"
        ),
        "finance.approve_entry": Permission(
            code="finance.approve_entry",
            name="Approve Journal Entry",
            module="finance",
            resource="journal_entry",
            action="approve",
            description="Approve journal entry"
        ),
        "finance.view_reports": Permission(
            code="finance.view_reports",
            name="View Financial Reports",
            module="finance",
            resource="report",
            action="read",
            description="View financial reports"
        ),
    }
    
    # CRM
    CRM_PERMISSIONS = {
        "crm.lead.create": Permission(
            code="crm.lead.create",
            name="Create Lead",
            module="crm",
            resource="lead",
            action="create",
            description="Create new lead"
        ),
        "crm.lead.update": Permission(
            code="crm.lead.update",
            name="Update Lead",
            module="crm",
            resource="lead",
            action="update",
            description="Update lead information"
        ),
        "crm.opportunity.create": Permission(
            code="crm.opportunity.create",
            name="Create Opportunity",
            module="crm",
            resource="opportunity",
            action="create",
            description="Create sales opportunity"
        ),
    }
    
    # Inventory
    INVENTORY_PERMISSIONS = {
        "inventory.stock.view": Permission(
            code="inventory.stock.view",
            name="View Stock",
            module="inventory",
            resource="stock",
            action="read",
            description="View inventory stock levels"
        ),
        "inventory.stock.update": Permission(
            code="inventory.stock.update",
            name="Update Stock",
            module="inventory",
            resource="stock",
            action="update",
            description="Update stock levels"
        ),
        "inventory.transfer": Permission(
            code="inventory.transfer",
            name="Stock Transfer",
            module="inventory",
            resource="transfer",
            action="create",
            description="Transfer stock between warehouses"
        ),
    }
    
    # Procurement
    PROCUREMENT_PERMISSIONS = {
        "procurement.pr.create": Permission(
            code="procurement.pr.create",
            name="Create Purchase Request",
            module="procurement",
            resource="purchase_request",
            action="create",
            description="Create purchase request"
        ),
        "procurement.po.create": Permission(
            code="procurement.po.create",
            name="Create Purchase Order",
            module="procurement",
            resource="purchase_order",
            action="create",
            description="Create purchase order"
        ),
        "procurement.po.approve": Permission(
            code="procurement.po.approve",
            name="Approve Purchase Order",
            module="procurement",
            resource="purchase_order",
            action="approve",
            description="Approve purchase order"
        ),
    }
    
    # Reports & Admin
    ADMIN_PERMISSIONS = {
        "admin.audit.view": Permission(
            code="admin.audit.view",
            name="View Audit Logs",
            module="admin",
            resource="audit",
            action="read",
            description="View system audit logs"
        ),
        "admin.settings": Permission(
            code="admin.settings",
            name="Manage Settings",
            module="admin",
            resource="settings",
            action="update",
            description="Manage system settings"
        ),
        "admin.users": Permission(
            code="admin.users",
            name="Manage Users",
            module="admin",
            resource="user",
            action="update",
            description="Manage user accounts"
        ),
        "admin.roles": Permission(
            code="admin.roles",
            name="Manage Roles",
            module="admin",
            resource="role",
            action="update",
            description="Manage system roles"
        ),
    }
    
    ALL_PERMISSIONS = {
        **AUTH_PERMISSIONS,
        **EMPLOYEE_PERMISSIONS,
        **ATTENDANCE_PERMISSIONS,
        **LEAVE_PERMISSIONS,
        **PAYROLL_PERMISSIONS,
        **FINANCE_PERMISSIONS,
        **CRM_PERMISSIONS,
        **INVENTORY_PERMISSIONS,
        **PROCUREMENT_PERMISSIONS,
        **ADMIN_PERMISSIONS,
    }
    
    @classmethod
    def get_permission(cls, code: str) -> Optional[Permission]:
        """Get permission by code"""
        return cls.ALL_PERMISSIONS.get(code)
    
    @classmethod
    def get_module_permissions(cls, module: str) -> List[Permission]:
        """Get all permissions for a module"""
        return [p for p in cls.ALL_PERMISSIONS.values() if p.module == module]


class RoleRegistry:
    """Registry of predefined system roles and their permissions"""
    
    SUPER_ADMIN = Role(
        role_id="super_admin",
        name="Super Administrator",
        description="Full system access",
        permissions=set(PermissionRegistry.ALL_PERMISSIONS.keys()),
        is_system_role=True
    )
    
    COMPANY_ADMIN = Role(
        role_id="company_admin",
        name="Company Administrator",
        description="Full access within company",
        permissions={
            *PermissionRegistry.EMPLOYEE_PERMISSIONS.keys(),
            *PermissionRegistry.ATTENDANCE_PERMISSIONS.keys(),
            *PermissionRegistry.LEAVE_PERMISSIONS.keys(),
            *PermissionRegistry.PAYROLL_PERMISSIONS.keys(),
            *PermissionRegistry.FINANCE_PERMISSIONS.keys(),
            *PermissionRegistry.ADMIN_PERMISSIONS.keys(),
        },
        is_system_role=True
    )
    
    HR_MANAGER = Role(
        role_id="hr_manager",
        name="HR Manager",
        description="HR operations",
        permissions={
            *PermissionRegistry.EMPLOYEE_PERMISSIONS.keys(),
            *PermissionRegistry.ATTENDANCE_PERMISSIONS.keys(),
            *PermissionRegistry.LEAVE_PERMISSIONS.keys(),
            "payroll.view",
            "payroll.export",
        },
        is_system_role=True
    )
    
    FINANCE_MANAGER = Role(
        role_id="finance_manager",
        name="Finance Manager",
        description="Finance operations",
        permissions={
            *PermissionRegistry.FINANCE_PERMISSIONS.keys(),
            *PermissionRegistry.PAYROLL_PERMISSIONS.keys(),
            "employee.read",
        },
        is_system_role=True
    )
    
    PROJECT_MANAGER = Role(
        role_id="project_manager",
        name="Project Manager",
        description="Project management",
        permissions={
            "employee.read",
        },
        is_system_role=True
    )
    
    EMPLOYEE = Role(
        role_id="employee",
        name="Employee",
        description="Standard employee access",
        permissions={
            "auth.login",
            "auth.logout",
            "auth.refresh_token",
            "attendance.mark",
            "attendance.view",
            "leave.apply",
            "leave.view",
        },
        is_system_role=True
    )
    
    ALL_ROLES = {
        "super_admin": SUPER_ADMIN,
        "company_admin": COMPANY_ADMIN,
        "hr_manager": HR_MANAGER,
        "finance_manager": FINANCE_MANAGER,
        "project_manager": PROJECT_MANAGER,
        "employee": EMPLOYEE,
    }
    
    @classmethod
    def get_role(cls, role_id: str) -> Optional[Role]:
        """Get role by ID"""
        return cls.ALL_ROLES.get(role_id)


class AuthorizationEngine:
    """Authorization policy engine"""
    
    def __init__(self):
        self.permission_registry = PermissionRegistry()
        self.role_registry = RoleRegistry()
    
    def has_permission(
        self,
        user: User,
        permission_code: str
    ) -> bool:
        """Check if user has specific permission"""
        if not user.is_active:
            return False
        
        # Super admin has all permissions
        if "super_admin" in user.roles:
            return True
        
        return permission_code in user.permissions
    
    def has_role(self, user: User, role: str) -> bool:
        """Check if user has specific role"""
        if not user.is_active:
            return False
        
        return role in user.roles
    
    def has_any_permission(
        self,
        user: User,
        permission_codes: List[str]
    ) -> bool:
        """Check if user has any of the specified permissions"""
        return any(
            self.has_permission(user, code)
            for code in permission_codes
        )
    
    def has_all_permissions(
        self,
        user: User,
        permission_codes: List[str]
    ) -> bool:
        """Check if user has all specified permissions"""
        return all(
            self.has_permission(user, code)
            for code in permission_codes
        )
    
    def can_access_resource(
        self,
        user: User,
        resource_type: str,
        action: str,
        resource_owner_id: Optional[str] = None
    ) -> bool:
        """
        Check if user can access a specific resource
        Supports resource-level authorization
        """
        permission_code = f"{resource_type}.{action}"
        
        # Check if user has permission
        if not self.has_permission(user, permission_code):
            return False
        
        # Additional resource-level checks
        # Example: Employee can only view own profile
        if resource_type == "employee" and resource_owner_id:
            if user.user_id != resource_owner_id and "employee" in user.roles:
                return False
        
        return True


class PermissionRequired:
    """Decorator to require specific permission"""
    
    def __init__(self, permission_code: str):
        self.permission_code = permission_code
        self.auth_engine = AuthorizationEngine()
    
    def __call__(self, func: Callable):
        @wraps(func)
        async def wrapper(*args, current_user: User = None, **kwargs):
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated"
                )
            
            if not self.auth_engine.has_permission(current_user, self.permission_code):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission '{self.permission_code}' required"
                )
            
            return await func(*args, current_user=current_user, **kwargs)
        
        return wrapper


class RoleRequired:
    """Decorator to require one of the specified roles."""
    
    def __init__(self, *roles: str):
        self.roles = roles
        self.auth_engine = AuthorizationEngine()
    
    def __call__(self, func: Callable):
        @wraps(func)
        async def wrapper(*args, current_user: User = None, **kwargs):
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated"
                )
            
            if not any(self.auth_engine.has_role(current_user, role) for role in self.roles):
                required_roles = ", ".join(self.roles)
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"One of the following roles is required: {required_roles}"
                )
            
            return await func(*args, current_user=current_user, **kwargs)
        
        return wrapper


# Global authorization engine
authorization_engine = AuthorizationEngine()
