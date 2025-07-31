from decouple import config
from pydantic import BaseModel

class Settings(BaseModel):
    DATABASE_URL: str =  "mongodb://mongo:27017/"
    JWT_SECRET_KEY: str = config('JWT_SECRET_KEY')
    JWT_ALGORITHM: str = config('JWT_ALGORITHM', default='HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config('ACCESS_TOKEN_EXPIRE_MINUTES', cast=int, default=30)

settings = Settings()
