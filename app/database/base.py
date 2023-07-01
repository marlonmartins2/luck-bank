from pymongo import MongoClient

from settings import settings


class Index(type):
    """
    Metaclass to create indexes in MongoDB.
    Args:
        type (type): Metaclass.
    """
    def __init__(cls, *args, **kwargs):
        if hasattr(cls, "indices"):
            cls.get_instancia().create_index(cls.indices)
        super().__init__(*args, **kwargs)


class BaseConnection:
    if settings.MONGO_SSL is True:
        connection = MongoClient(
            settings.MONGO_URL,
            tls=True,
            tlsCAFile=settings.PATH_CERT,
            tlsAllowInvalidHostnames=True,
            retryWrites=False,
            directConnection=True,
        )
    else:
        connection = MongoClient(settings.MONGO_URL)


class BaseDB(BaseConnection, metaclass=Index):
    database = settings.DATABASE_ENVIRONMENT


database = BaseDB.connection[BaseDB.database]
