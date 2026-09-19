from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    # tells Pydantic that it is allowed to create the schema from an object's attributes instead of user.id or soon
    model_config = {
        "from_attributes": True
    }