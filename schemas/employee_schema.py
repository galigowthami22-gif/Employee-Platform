from pydantic import BaseModel
from datetime import date
from typing import Optional


class EmployeeCreate(BaseModel):
    employee_code: Optional[str] = None
    first_name: str
    last_name: str
    email: str
    phone: str
    gender: Optional[str] = None
    joining_date: Optional[date] = None
    department_id: Optional[int] = None
    designation_id: Optional[int] = None
    user_id: Optional[int] = None