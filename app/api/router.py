from fastapi import APIRouter

from app.modules.system.handlers import router as system_router
from app.modules.telegram.handlers import router as telegram_router

router = APIRouter(prefix="/api")

# Сюда импортировать и подключать роутеры модулей modules/
router.include_router(system_router)
router.include_router(telegram_router)
