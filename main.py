from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.core import settings
from app.api import router
from app.core.database import database


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield
    await database.dispose()


app = FastAPI(title=settings.project_name, lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app")
