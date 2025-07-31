from fastapi import APIRouter
from api.v1.endpoints import patients
from api.v1.endpoints import auth
from api.v1.endpoints import provider

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(provider.router, prefix="/provider", tags=["provider"])
