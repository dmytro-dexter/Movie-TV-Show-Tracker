from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=4)


class ShowUser(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool

    class Config():
        orm_mode = True
