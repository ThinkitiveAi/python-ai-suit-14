from pymongo.collection import Collection
from bson import ObjectId
from schemas.user import UserCreate
from core.security import get_password_hash, verify_password
from typing import Optional, Dict, Any
from core.database import get_database

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    db = get_database()
    user = db["users"].find_one({"email": email})
    if user:
        user["id"] = str(user["_id"])
    return user

def create_user(user: UserCreate) -> Dict[str, Any]:
    db = get_database()
    hashed_password = get_password_hash(user.password)
    user_dict = {
        "email": user.email,
        "hashed_password": hashed_password,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_active": True
    }
    result = db["users"].insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return user_dict

def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    user = get_user_by_email(email)
    if user and verify_password(password, user["hashed_password"]):
        return user
    return None 