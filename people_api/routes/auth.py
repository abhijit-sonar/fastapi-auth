from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from typing import Any

from ..models.user import SignupBody, User
from ..models.token import Token
from .. import security
from ..deps import get_collection


Collection = Annotated[Any, Depends(get_collection)]

auth_router = APIRouter()


@auth_router.post("/register", response_description="Sign-up", response_model=User)
async def register(user: SignupBody, collection: Collection):
    existing_user = await collection.find_one({"email": user.email})

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use"
        )

    password_hash = security.generate_password_hash(user.password)
    user_dict = user.dict(exclude={"password"})

    result = await collection.insert_one({"password_hash": password_hash, **user_dict})

    return dict(id=result.inserted_id, **user_dict)


@auth_router.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], collection: Collection):

    user = await security.authenticate_user(collection, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = security.create_access_token({"email": user.email})

    return {"access_token": token, "token_type": "bearer"}
