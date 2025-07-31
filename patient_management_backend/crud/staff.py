from pymongo.collection import Collection
from bson import ObjectId
from schemas.provider import StaffCreate, StaffRead
from core.security import get_password_hash, verify_password
from typing import Optional, Dict, Any, List
from core.database import get_database
from datetime import date, datetime
from schemas.provider import StaffRole

def to_mongo_dict(obj):
    d = obj.dict() if hasattr(obj, "dict") else dict(obj)
    for k, v in d.items():
        if isinstance(v, date) and not isinstance(v, datetime):
            d[k] = v.isoformat()
    return d

def sanitize_role(role):
    try:
        return StaffRole(role)
    except ValueError:
        return StaffRole.provider

def get_staff_by_email(email: str) -> Optional[Dict[str, Any]]:
    db = get_database()
    staff = db["staff"].find_one({"email": email})
    if staff:
        staff["id"] = str(staff["_id"])
    return staff

def get_staff_by_id(staff_id: str) -> Optional[Dict[str, Any]]:
    db = get_database()
    staff = db["staff"].find_one({"_id": ObjectId(staff_id)})
    if staff:
        staff["id"] = str(staff["_id"])
    return staff

def get_all_staff(skip: int = 0, limit: int = 100) -> list[StaffRead]:
    db = get_database()
    staff_list = list(db["staff"].find().skip(skip).limit(limit))
    result = []
    for staff in staff_list:
        staff["id"] = str(staff.get("_id", ""))
        staff.setdefault("is_active", True)
        staff.setdefault("created_at", None)
        staff.setdefault("updated_at", None)
        staff.setdefault("patients", None)
        # Fill missing optional fields
        for field in ["phone", "npi_number", "work_locations", "languages_spoken", "supervising_clinician"]:
            staff.setdefault(field, None)
        staff["role"] = sanitize_role(staff.get("role", "provider"))
        result.append(StaffRead(**staff))
    return result

def get_all_providers(skip: int = 0, limit: int = 100) -> list[StaffRead]:
    db = get_database()
    providers = list(db["staff"].find({"role": "provider"}).skip(skip).limit(limit))
    result = []
    for provider in providers:
        provider["id"] = str(provider.get("_id", ""))
        provider.setdefault("is_active", True)
        provider.setdefault("created_at", None)
        provider.setdefault("updated_at", None)
        provider.setdefault("patients", None)
        for field in ["phone", "npi_number", "work_locations", "languages_spoken", "supervising_clinician"]:
            provider.setdefault(field, None)
        provider["role"] = sanitize_role(provider.get("role", "provider"))
        result.append(StaffRead(**provider))
    return result

def create_staff(staff: StaffCreate) -> Dict[str, Any]:
    db = get_database()
    hashed_password = get_password_hash(staff.password)
    staff_dict = {
        "email": staff.email,
        "hashed_password": hashed_password,
        "first_name": staff.first_name,
        "last_name": staff.last_name,
        "phone": staff.phone,
        "role": staff.role.value if hasattr(staff.role, 'value') else str(staff.role),
        "is_active": True
    }
    result = db["staff"].insert_one(staff_dict)
    staff_dict["id"] = str(result.inserted_id)
    return staff_dict

def authenticate_staff(email: str, password: str) -> Optional[Dict[str, Any]]:
    staff = get_staff_by_email(email)
    if staff and verify_password(password, staff["hashed_password"]):
        return staff
    return None

def get_patients_for_provider(provider_id: str, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
    db = get_database()
    patients = list(db["patients"].find({"provider_id": provider_id}).skip(skip).limit(limit))
    for patient in patients:
        patient["id"] = str(patient["_id"])
    return patients 