from fastapi import APIRouter
from .user_api import router as user_router
from .task_api import router as task_router

router = APIRouter()

# Including the User and task router
router.include_router(user_router)
router.include_router(task_router)