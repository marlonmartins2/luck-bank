import logging

from database import database, Collections

from models.users.users_documents_model import Documents


logger = logging.getLogger("DocumentControllerLogger")


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
    documents = database[Collections.USER_DOCUMENTS].find({"user_id": user_id})

    return list(documents)
