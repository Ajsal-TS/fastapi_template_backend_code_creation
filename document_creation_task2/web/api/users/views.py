from fastapi import APIRouter

from document_creation_task2.documents.document_controller import document_func
from document_creation_task2.users.user_controller import users_func

router = APIRouter()

router.include_router(
    users_func,
    prefix="/User",
    tags=["User"],
)

router.include_router(
    document_func,
    prefix="/document",
    tags=["Document"],
)
