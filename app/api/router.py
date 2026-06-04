from fastapi import APIRouter

from app.modules.system.handlers import router as system_router
from app.modules.rmq_module.handlers import router as rmq_router
from app.modules.file_module.handlers import router as file_router
from app.modules.taskiq_module.config import taskiq_settings
from app.modules.taskiq_module.handlers import router as taskiq_router

router = APIRouter(prefix="/api")

# Built-in infrastructure and feature routers live here.
router.include_router(system_router)
router.include_router(rmq_router)
router.include_router(file_router)

# taskiq debug router is opt-in: only wired when debug mode and the dedicated
# flag are enabled, mirroring the rmq debug endpoints policy.
if taskiq_settings.debug and taskiq_settings.debug_endpoints_enabled:
    router.include_router(taskiq_router)
