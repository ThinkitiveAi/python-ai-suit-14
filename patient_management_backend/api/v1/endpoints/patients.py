from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas.patient import PatientCreate, PatientRead, PatientUpdate
from crud import patient as crud_patient
from api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[PatientRead])
def list_patients(skip: int = 0, limit: int = 10, user: dict = Depends(get_current_user)):
    patients = crud_patient.get_patients(skip=skip, limit=limit)
    return patients

@router.get("/by-provider/{provider_id}", response_model=List[PatientRead])
def list_patients_by_provider(provider_id: str, skip: int = 0, limit: int = 10, user: dict = Depends(get_current_user)):
    patients = crud_patient.get_patients_by_provider(provider_id, skip=skip, limit=limit)
    return patients

@router.get("/{patient_id}", response_model=PatientRead)
def get_patient(patient_id: str, user: dict = Depends(get_current_user)):
    patient = crud_patient.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.post("/", response_model=PatientRead, status_code=status.HTTP_201_CREATED)
def create_patient(patient: PatientCreate, user: dict = Depends(get_current_user)):
    """
    Create a new patient with the following fields:
    - first_name (required)
    - middle_name (optional)
    - last_name (required)
    - preferred_name (optional)
    - dob (required)
    - legal_sex (optional)
    - gender_identity (optional)
    - ethnicity (optional)
    - race (optional)
    - phone (required)
    - email (optional)
    - address_line_1 (optional)
    - address_line_2 (optional)
    - city (optional)
    - state (optional)
    - zipcode (optional)
    - preferred_language (optional)
    - provider_id (optional)
    """
    try:
        return crud_patient.create_patient(patient)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{patient_id}", response_model=PatientRead)
def update_patient(patient_id: str, patient: PatientUpdate, user: dict = Depends(get_current_user)):
    db_patient = crud_patient.update_patient(patient_id, patient)
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: str, user: dict = Depends(get_current_user)):
    deleted = crud_patient.delete_patient(patient_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Patient not found")
    return None
