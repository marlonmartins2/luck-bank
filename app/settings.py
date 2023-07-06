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
    DEBUG: bool

    # Database settings
    MONGO_URL: str
    MONGO_SSL: str
    PATH_CERT: str
    DATABASE_ENVIRONMENT: str

    # JWT settings
    ACCESS_TOKEN_EXPIRES_IN: int
    REFRESH_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str
    JWT_PRIVATE_KEY: str
    JWT_PUBLIC_KEY: str

settings = Settings()
