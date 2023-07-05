import logging


class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.args and len(record.args) >= 3 and record.args[2] != "/health_check"


logging.getLogger("uvicorn.access").addFilter(EndpointFilter())
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
consoleHandler.setFormatter(logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(consoleHandler)


class Logger:
    _instance = None

    def __init__(self) -> None:
        self.logger = None

    @classmethod
    def init(cls, name: str):
        if cls._instance is not None:
            return cls._instance.logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        cls.logger = logger
        cls._instance = cls
        return logger
