from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing_extensions import Annotated
from typing import Any, Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
import os

from .deps import get_collection
from .models.user import DbUser

Collection = Annotated[Any, Depends(get_collection)]

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "068796e19106febb575fbccf7ec9ba0482576fb54157989d8c7dbb8df10107c1"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 60 * 60 * 24 * 15  # 15 days

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, password_hash):
    return password_context.verify(plain_password, password_hash)


def generate_password_hash(password: str):
    return password_context.hash(password)


async def get_user_by_email(collection: Any, email: str) -> Optional[DbUser]:
    user_dict: dict = await collection.find_one({"email": email})

    if user_dict is None:
        return None

    return DbUser(**user_dict)


async def authenticate_user(collection: Any, email: str, password: str) -> DbUser:
    print(email, password)
    user = await get_user_by_email(collection, email)

    if user is None:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], collection: Collection):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise credential_exception

    email = payload.get("email")
    if email is None:
        raise credential_exception

    user = await get_user_by_email(collection, email)
    if user is None:
        raise credential_exception

    return user
