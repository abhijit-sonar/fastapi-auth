from pydantic import BaseModel, Field
from typing import List
from bson import ObjectId

from .pyobjectid import PyObjectId


class UserUpdate(BaseModel):
    name: str
    email: str
    hobbies: List[str]


class User(UserUpdate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True


class DbUser(User):
    password_hash: str

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True


class SignupBody(UserUpdate):
    password: str

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True


class UserPage(BaseModel):
    page: int
    next: int
    items: List[User]

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
