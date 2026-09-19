from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    project_slug: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    project_slug: str


class AuthContext(BaseModel):
    user_id: int
    full_name: str
    email: str
    project_id: int
    project_slug: str
    role: str
