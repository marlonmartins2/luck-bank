from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Settings for the application
    Args:
        BaseSettings (BaseSettings): Base settings class
    """
    class Config:
        env_file = ".env"

    # Application settings
    APP_NAME: str
    APP_DESCRIPTION: str
    CORS_ORIGINS: list
    ENVIROMENT: str
    DEBUG: bool

    # Database settings
    MONGO_URL: str
    MONGO_SSL: str
    PATH_CERT: str
    DATABASE_ENVIROMENT: str

settings = Settings()
