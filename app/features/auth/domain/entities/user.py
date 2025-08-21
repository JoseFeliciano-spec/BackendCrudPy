from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: datetime

class UserInDB(BaseModel):
    id: str
    name: str
    email: EmailStr
    hashed_password: str
    created_at: datetime
