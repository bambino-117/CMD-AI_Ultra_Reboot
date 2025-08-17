from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    SECRET_KEY: str = Field(default="your-secret-key")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    SQLALCHEMY_DATABASE_URL: str = Field(default="sqlite:///./app.db")

settings = Settings()
