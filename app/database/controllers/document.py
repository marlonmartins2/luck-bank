from datetime import datetime

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from pymongo.errors import (
    ServerSelectionTimeoutError,
    ConnectionFailure,
    OperationFailure,
    PyMongoError
)

from utils import ExistOneInDatabase
from utils.logger import Logger

from database import database, Collections

from models import DocumentTypeEnum
from models.users.users_documents_model import Documents


logger = Logger.init("DocumentControllerLogger")


def create_document(user_id, document):
    """
    Create document from user create request.
    Args:
        user_id (str): The user id.
        document (Documents): The document data.
    """
    logger.info(f"Create document from user_id ->: {user_id}")
    try:
        if document.document_type not in [DocumentTypeEnum.PASSPORT.value, DocumentTypeEnum.CNPJ.value]:
            has_cpf_on_database = database[Collections.USER_DOCUMENTS].find_one(
                {"document_type":document.document_type},
                {"_id": 0}
            )

            if has_cpf_on_database:
                raise ExistOneInDatabase(
                    "the selected document type already exists in the database"
                        "and there can only be one of them. Please contact support."
                )

        document_has_exist = database[Collections.USER_DOCUMENTS].find_one(
            {
                "user_id": user_id,
                "document_type": document.document_type,
                "document_number": document.document_number,
            },
            {"_id": 0}
        )
        if document_has_exist and document_has_exist["deleted_at"] == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Document already exists",
                    "address": jsonable_encoder(document_has_exist),
                }
            )
        
        if document_has_exist and document_has_exist["deleted_at"] != "":
            database[Collections.USER_DOCUMENTS].update_one(
                {"_id": document_has_exist["_id"]},
                {
                    "$set": {
                        "deleted_at": "",
                        "updated_at": datetime.now()
                    }
                }
            )

            return document_has_exist

        document = Documents(
            user_id=user_id,
            document_type=document.document_type,
            document_number=document.document_number
        ).dict()

        database[Collections.USER_DOCUMENTS].insert_one(document)

        document.pop("_id")

        return document

    except ExistOneInDatabase as error:
        logger.error(f"ExistOneInDatabase: {error}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "the selected document type already exists in the database"
                    "and there can only be one of them. Please contact support."
            }
        )

    except ServerSelectionTimeoutError as error:
        logger.error(f"ServerSelectionTimeoutError: {error}")

    except ConnectionFailure as error:
        logger.error(f"ConnectionFailure: {error}")

    except OperationFailure as error:
        logger.error(f"OperationFailure: {error}")

    except PyMongoError as error:
        logger.error(f"PyMongoError: {error}")


def get_documents_per_user(user_id):
    """
    Get documents per user.
    Args:
        user_id (str): The user id.
    """
    logger.info(f"Get documents per user_id ->: {user_id}")
    payload = []
    try:
        documents = database[Collections.USER_DOCUMENTS].find(
            {"user_id": user_id, "deleted_at": ""},
            {"_id": 0}
        )

        for document in documents:
            payload.append(document)
        return payload

    except ServerSelectionTimeoutError as error:
        logger.error(f"ServerSelectionTimeoutError: {error}")

    except ConnectionFailure as error:
        logger.error(f"ConnectionFailure: {error}")

    except OperationFailure as error:
        logger.error(f"OperationFailure: {error}")

    except PyMongoError as error:
        logger.error(f"PyMongoError: {error}")


def get_document_by_id(user_id , document_id):
    """
    Get document by id.
    Args:
        document_id (str): The document id.
    """
    logger.info(f"Get document detail user id: ->: {user_id}")

    try:
        document = database[Collections.USER_DOCUMENTS].find_one(
            {"id": document_id, "user_id": user_id},
            {"_id": 0}
        )

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Document not found",
                }
            )

        return document

    except ServerSelectionTimeoutError as error:
        logger.error(f"ServerSelectionTimeoutError: {error}")

    except ConnectionFailure as error:
        logger.error(f"ConnectionFailure: {error}")

    except OperationFailure as error:
        logger.error(f"OperationFailure: {error}")

    except PyMongoError as error:
        logger.error(f"PyMongoError: {error}")


def delete_document(document_id, user_id):
    """
    Delete document per user.
    Args:
        document_id (str): The document id.
    """
    logger.info(f"Delete document per user id: ->: {user_id}")

    try:
        database[Collections.USER_DOCUMENTS].update_one(
            {"id": document_id},
            {"$set": {"deleted_at": datetime.now()}}
        )

        return True

    except ServerSelectionTimeoutError as error:
        logger.error(f"ServerSelectionTimeoutError: {error}")

    except ConnectionFailure as error:
        logger.error(f"ConnectionFailure: {error}")

    except OperationFailure as error:
        logger.error(f"OperationFailure: {error}")

    except PyMongoError as error:
        logger.error(f"PyMongoError: {error}")
