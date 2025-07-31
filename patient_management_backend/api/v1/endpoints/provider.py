from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from schemas.provider import StaffCreate, StaffRead, StaffLogin
from crud import staff as crud_staff
from core.security import create_access_token
from api.deps import get_current_user
from datetime import date, datetime
from schemas.provider import StaffRole

router = APIRouter()

def to_mongo_dict(obj):
    d = obj.dict() if hasattr(obj, "dict") else dict(obj)
    for k, v in d.items():
        if isinstance(v, date) and not isinstance(v, datetime):
            # Convert date to ISO string (or datetime if you prefer)
            d[k] = v.isoformat()
    return d

def sanitize_role(role):
    try:
        return StaffRole(role)
    except ValueError:
        # fallback or skip, here we fallback to 'provider'
        return StaffRole.provider

@router.post("/register", response_model=StaffRead, status_code=status.HTTP_201_CREATED, tags=["provider"])
def register_provider(provider: StaffCreate):
    """
    Register a new provider with the following fields:
    - first_name (required)
    - last_name (required)
    - role (required)
    - email (required)
    - password (required)
    - phone (optional)
    - npi_number (optional)
    - work_locations (optional)
    - languages_spoken (optional)
    - supervising_clinician (optional)
    """
    existing = crud_staff.get_staff_by_email(provider.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_provider = crud_staff.create_staff(provider)
    return db_provider

@router.post("/login", tags=["provider"])
def login_provider(provider: StaffLogin):
    db_provider = crud_staff.authenticate_staff(provider.email, provider.password)
    if not db_provider:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token({"sub": str(db_provider["id"])})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/patients", status_code=200, tags=["provider"])
def get_patients_for_current_provider(user: dict = Depends(get_current_user)):
    # user['id'] is the provider_id
    patients = crud_staff.get_patients_for_provider(user["id"])
    return patients

@router.get("/", response_model=List[StaffRead], tags=["provider"])
def get_all_providers(skip: int = 0, limit: int = 100, user: dict = Depends(get_current_user)):
    return crud_staff.get_all_staff(skip=skip, limit=limit)

@router.get("/providers", response_model=List[StaffRead], tags=["provider"])
def get_all_providers_list(skip: int = 0, limit: int = 100, user: dict = Depends(get_current_user)):
    return crud_staff.get_all_providers(skip=skip, limit=limit)

@router.get("/{provider_id}", response_model=StaffRead, tags=["provider"])
def get_provider_by_id(provider_id: str, user: dict = Depends(get_current_user)):
    provider = crud_staff.get_staff_by_id(provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider 