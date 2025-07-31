from pymongo.collection import Collection
from bson import ObjectId
from schemas.patient import PatientCreate, PatientUpdate
from typing import List, Optional, Dict, Any
from core.database import get_database
from datetime import date, datetime

def to_mongo_dict(obj):
    d = obj.dict() if hasattr(obj, "dict") else dict(obj)
    for k, v in d.items():
        if isinstance(v, date) and not isinstance(v, datetime):
            d[k] = v.isoformat()
    return d

def get_patient(patient_id: str) -> Optional[Dict[str, Any]]:
    db = get_database()
    patient = db["patients"].find_one({"_id": ObjectId(patient_id)})
    if patient:
        patient["id"] = str(patient["_id"])
    return patient

def get_patients(skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
    db = get_database()
    patients = list(db["patients"].find().skip(skip).limit(limit))
    for patient in patients:
        patient["id"] = str(patient["_id"])
    return patients

def create_patient(patient: PatientCreate) -> Dict[str, Any]:
    db = get_database()
    patient_dict = to_mongo_dict(patient)
    result = db["patients"].insert_one(patient_dict)
    patient_dict["id"] = str(result.inserted_id)
    return patient_dict

def update_patient(patient_id: str, patient: PatientUpdate) -> Optional[Dict[str, Any]]:
    db = get_database()
    update_data = {k: v for k, v in patient.model_dump(exclude_unset=True).items() if v is not None}
    result = db["patients"].update_one({"_id": ObjectId(patient_id)}, {"$set": update_data})
    if result.modified_count == 0:
        return None
    return get_patient(patient_id)

def delete_patient(patient_id: str) -> bool:
    db = get_database()
    result = db["patients"].delete_one({"_id": ObjectId(patient_id)})
    return result.deleted_count == 1

def get_patients_by_provider(provider_id: str, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
    db = get_database()
    patients = list(db["patients"].find({"provider_id": provider_id}).skip(skip).limit(limit))
    for patient in patients:
        patient["id"] = str(patient["_id"])
    return patients
