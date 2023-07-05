from utils.logger import Logger

from database import database, Collections

from models.users.users_documents_model import Documents

from pymongo.errors import (
    ServerSelectionTimeoutError,
    ConnectionFailure,
    OperationFailure,
    PyMongoError
)


logger = Logger.init("DocumentControllerLogger")


def create_document(user_id, document):
    """
    Create document from user create request.
    Args:
        user_id (str): The user id.
        document (Documents): The document data.
    """
    logger.info(f"Create document from user_id ->: {user_id}")
    document = Documents(
        user_id=user_id,
        document_type=document.document_type,
        document_number=document.document_number
    ).dict()

    database[Collections.USER_DOCUMENTS].insert_one(document)


def get_documents_per_user(user_id):
    """
    Get documents per user.
    Args:
        user_id (str): The user id.
    """
    logger.info(f"Get documents per user_id ->: {user_id}")
    payload = []
    try:
        documents = database[Collections.USER_DOCUMENTS].find({"user_id": user_id}, {"_id": 0})

        for document in documents:
            payload.append(document)
        return payload
    except ServerSelectionTimeoutError as error:
        logger.debug(f"ServerSelectionTimeoutError: {error}")

    except ConnectionFailure as error:
        logger.debug(f"ConnectionFailure: {error}")

    except OperationFailure as error:
        logger.debug(f"OperationFailure: {error}")

    except PyMongoError as error:
        logger.debug(f"PyMongoError: {error}")
