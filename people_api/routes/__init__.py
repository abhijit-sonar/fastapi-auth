from fastapi import APIRouter

from .people import people_router


router = APIRouter(prefix="/api")
router.include_router(people_router, prefix="/people")
