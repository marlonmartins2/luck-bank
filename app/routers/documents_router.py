from fastapi import status, APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from utils.logger import Logger

from services.oauth2 import require_user, AuthJWT

from models.users.users_documents_model import DocumentsCreateRequest

from database.controllers.document import (
    create_document,
    get_documents_per_user,
    get_document_by_id,
    delete_document,
)

logger = Logger.init("DocumentRouteLogger")


documents_router = APIRouter(tags=["Document"], dependencies=[Depends(require_user)])


@documents_router.get("/users/{user_id}/documents/", status_code=status.HTTP_200_OK)
def get_user_documents(user_id: str):
    """
    Get user documents endpoint:

    Returns:
    - **UserResponse** (Documents): Documents data to database return.
    """
    logger.info(f"Get user documents")

    documents = get_documents_per_user(user_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(documents)
    )


@documents_router.post("/users/{user_id}/documents/", status_code=status.HTTP_201_CREATED)
def create_user_document(user_id: str, payload: DocumentsCreateRequest):
    """
    Create user document endpoint:

    Returns:
    - **UserResponse** (Documents): Documents data to database return.
    """
    logger.info(f"Create user document")

    new_document = create_document(user_id, payload)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "User document created successfully",
            "data": jsonable_encoder(new_document)
        }
    )


@documents_router.get("/users/{user_id}/documents/{document_id}/", status_code=status.HTTP_200_OK)
def get_user_document_detail(user_id: str, document_id: str):
    """
    Get user document detail endpoint:

    Returns:
    - **DocumentResponse** (Document): Document data to database return.
    """
    logger.info(f"Get user document detail")

    document = get_document_by_id(user_id, document_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(document)
    )


@documents_router.delete("/users/{user_id}/documents/{document_id}/", status_code=status.HTTP_200_OK)
def delete_user_document(user_id: str, document_id: str):
    """
    Delete user document endpoint:

    Returns:
    - **DocumentResponse** (Document): Document data to database return.
    """
    logger.info(f"Delete user document")

    delete_document(document_id, user_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "User document deleted successfully.",}
    )