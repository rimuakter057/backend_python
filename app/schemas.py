from pydantic import BaseModel,EmailStr, ConfigDict, Field
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)



class UserRes(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Intro(BaseModel):
    name: str
    profession: str
    class_: str
    website: str
    duration: int


class Course(BaseModel):
    name: str
    title: str
    instructor: str
    duration: int
    description: str
