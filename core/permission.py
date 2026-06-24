from fastapi import Depends, HTTPException
from dependencies.dependency import get_current_user
from sqlalchemy.orm import Session
from core.database import get_db
from models.role_permission_model import RolePermission
from models.permission_model import Permission

def require_roles(*roles):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.role.name not in roles:
            raise HTTPException(status_code=403, detail="Permission denied")
        return current_user
    return role_checker

def require_permission(permission_name):
    def checker(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
        permissions = (db.query(Permission.name).join(RolePermission, Permission.id == RolePermission.permission_id).filter(RolePermission.role_id == current_user.role_id).all())
        permission_list = [p[0] for p in permissions]

        if permission_name not in permission_list:
            raise HTTPException(status_code=403, detail="Permission denied")
        return current_user
    return checker