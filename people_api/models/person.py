from pydantic import BaseModel, Field
from typing import List
from bson import ObjectId

from .pyobjectid import PyObjectId


class PersonUpdate(BaseModel):
    name: str
    hobbies: List[str]


class Person(PersonUpdate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True


class PersonPage(BaseModel):
    page: int
    next: int
    items: List[Person]

    class Config:
        json_encoders = {ObjectId: str}
