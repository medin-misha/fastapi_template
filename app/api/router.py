from fastapi import APIRouter

from app.modules.system.handlers import router as system_router
from app.modules.file_module.handlers import router as file_router
from app.modules.rmq_module.handlers import router as rmq_router

router = APIRouter(prefix="/api")

# Built-in infrastructure and feature routers live here.
router.include_router(system_router)
router.include_router(file_router)
router.include_router(rmq_router)
