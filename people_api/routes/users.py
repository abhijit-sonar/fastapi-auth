from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from typing_extensions import Annotated
from typing import Any
from io import BytesIO
import aiohttp
import os

from .. import deps
from ..models.user import User, UserUpdate, UserPage, DbUser
from ..models.pyobjectid import PyObjectId
from .. import security

Collection = Annotated[Any, Depends(deps.get_collection)]

users_router = APIRouter()

avatar_api_url = os.environ.get("AVATAR_API_URL")
if avatar_api_url is None:
    raise ValueError("AVATAR_API_URL not set")

http_client_session = aiohttp.ClientSession()


@users_router.get("/me", response_model=User)
async def current_user(
    current_user: Annotated[User, Depends(security.get_current_user)]
):
    print(current_user)
    return current_user


async def _avatar(name: str):
    image_response = await http_client_session.get(avatar_api_url, params={"name": name})
    image_bytes = await image_response.read()
    image_stream = BytesIO(image_bytes)

    return StreamingResponse(image_stream, media_type="image/png")


@users_router.get("/me/avatar")
async def current_user_avatar(current_user: Annotated[User, Depends(security.get_current_user)]):
    return await _avatar(current_user.name)


@users_router.get("/{user_id}/avatar")
async def user_avatar(user_id: PyObjectId, collection: Collection):
    user = await collection.find_one({"_id": user_id})
    return await _avatar(user["name"])


@users_router.get("/", response_model=UserPage, response_description="A paged list of all the users")
async def get_all_users(
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


@users_router.delete("/")
async def delete_all(collection: Collection):
    await collection.delete_many({})


@users_router.get("/{user_id}", response_model=User, response_description="The user given by the ID")
async def get_user_by_id(user_id: PyObjectId, collection: Collection):
    user = await collection.find_one({"_id": user_id})
    return user


@users_router.patch("/edit-profile", response_model=User, response_description="The updated user")
async def edit_profile(user: UserUpdate, current_user: Annotated[DbUser, Depends(security.get_current_user)], collection: Collection):

    user_dict = user.dict()

    await collection.replace_one({"_id": current_user.id}, user_dict)

    return dict(_id=current_user.id, **user_dict)
