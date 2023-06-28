from fastapi import FastAPI

from . import routes
from . import deps


app = FastAPI()
app.include_router(routes.router)
