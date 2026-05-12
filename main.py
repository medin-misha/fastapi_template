from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.core import settings
from app.api import router
from app.core.database import database
from app.modules.rmq_module import rmq_runtime


@asynccontextmanager
async def lifespan(_: FastAPI):
    await rmq_runtime.start()
    try:
        yield
    finally:
        await rmq_runtime.stop()
        await database.dispose()


app = FastAPI(title=settings.project_name, lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app")
