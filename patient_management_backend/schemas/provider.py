from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime
import enum

class StaffRole(str, enum.Enum):
    provider = 'provider'
    staff = 'staff'
    admin = 'admin'

class StaffBase(BaseModel):
    first_name: str  # required
    last_name: str  # required
    role: StaffRole  # required
    email: EmailStr  # required
    phone: Optional[str] = None
    npi_number: Optional[str] = None
    work_locations: Optional[List[str]] = None
    languages_spoken: Optional[List[str]] = None
    supervising_clinician: Optional[str] = None

class StaffCreate(StaffBase):
    password: str  # required

class StaffRead(StaffBase):
    id: str
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    patients: Optional[List[str]] = None

class StaffLogin(BaseModel):
    email: EmailStr
    password: str 