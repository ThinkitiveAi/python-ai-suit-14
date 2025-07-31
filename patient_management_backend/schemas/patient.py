from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import date, datetime
import enum

class GenderEnum(str, enum.Enum):
    male = 'male'
    female = 'female'
    other = 'other'

class PatientBase(BaseModel):
    first_name: str  # required
    middle_name: Optional[str] = None
    last_name: str  # required
    preferred_name: Optional[str] = None
    dob: date  # required
    legal_sex: Optional[str] = None
    gender_identity: Optional[str] = None
    ethnicity: Optional[str] = None
    race: Optional[str] = None
    phone: str  # required
    email: Optional[EmailStr] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zipcode: Optional[str] = None
    preferred_language: Optional[str] = None
    provider_id: Optional[str] = None

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if not v.isdigit() or not (10 <= len(v) <= 15):
            raise ValueError('Phone must be numeric and 10-15 digits long')
        return v

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    gender: Optional[GenderEnum] = None
    dob: Optional[date] = None
    provider_id: Optional[str] = None

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if v is not None and (not v.isdigit() or not (10 <= len(v) <= 15)):
            raise ValueError('Phone must be numeric and 10-15 digits long')
        return v

class PatientRead(PatientBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
