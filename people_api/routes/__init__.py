from fastapi import APIRouter

from .users import users_router
from .auth import auth_router


router = APIRouter()

router.include_router(users_router, prefix="/api/users")
router.include_router(auth_router, prefix="/auth")
