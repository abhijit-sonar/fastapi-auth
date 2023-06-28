from fastapi import APIRouter, Depends, HTTPException, status
from typing_extensions import Annotated
from typing import Any, List

from .. import deps
from ..models.person import Person, PersonUpdate, PersonPage
from ..models.pyobjectid import PyObjectId

Collection = Annotated[Any, Depends(deps.get_collection)]

people_router = APIRouter()


@people_router.get("/", response_model=PersonPage, response_description="A paged list of all the people")
async def get_all_people(
    page_number: int,
    per_page: int,
    collection: Collection
):
    items = await collection \
        .find() \
        .skip((page_number - 1) * per_page) \
        .limit(per_page) \
        .to_list(per_page)

    return dict(items=items, page=page_number, next=page_number+1)


@people_router.get("/{person_id}", response_model=Person, response_description="The person given by the ID")
async def get_person_by_id(person_id: PyObjectId, collection: Collection):
    person = await collection.find_one({"_id": person_id})
    return person


@people_router.post("/", response_description="The updated person")
async def create_person(person: PersonUpdate, collection: Collection):
    result = await collection.insert_one(person.dict())
    return dict(_id=result.inserted_id, **person.dict())


@people_router.patch("/{person_id}", response_model=Person, response_description="The updated person")
async def update_person(person_id: PyObjectId, person: PersonUpdate, collection: Collection):

    person_dict = person.dict()

    result = await collection.replace_one({"_id": person_id}, person_dict)

    if result.modified_count < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return dict(_id=person_id, **person_dict)


@people_router.delete("/{person_id}")
async def delete_person(person_id: PyObjectId, collection: Collection):

    result = await collection.delete_one({"_id": person_id})

    if result.deleted_count < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
