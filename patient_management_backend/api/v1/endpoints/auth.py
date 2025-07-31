from fastapi import APIRouter, Depends, HTTPException, status
from crud import user as crud_user
from crud import patient as crud_patient
from schemas.user import UserCreate, UserRead, UserLogin
from schemas.patient import PatientCreate, PatientRead
from core.security import create_access_token

router = APIRouter()

@router.post("/register", response_model=PatientRead, status_code=status.HTTP_201_CREATED)
def register(patient: PatientCreate):
    """
    Patient self-registration. Accepts all fields from the Add Patient screen.
    """
    # Check if email already exists (if provided)
    if patient.email:
        existing = crud_user.get_user_by_email(patient.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
    db_patient = crud_patient.create_patient(patient)
    return db_patient

@router.post("/login")
def login(user: UserLogin):
    db_user = crud_user.authenticate_user(user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token({"sub": str(db_user["id"])})
    return {"access_token": access_token, "token_type": "bearer"} 