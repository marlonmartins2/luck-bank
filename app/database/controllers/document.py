import logging

from database import database, Collections

from models.users import Documents


logger = logging.getLogger("DocumentControllerLogger")


def create_document(user_id, document):
    document = Documents(
        user_id=user_id,
        document_type=document.document_type,
        document_number=document.document_number
    ).dict(),

    database[Collections.USER_DOCUMENTS].insert_one(document)
