import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Enterprise RAG Document Assistant"
    API_V1_PREFIX: str = "/api/v1"
    SIMILARITY_THRESHOLD: float = 0.25
    TOP_K_CHUNKS: int = 4
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 100
    DATA_DIR: str = "./data"

    class Config:
        env_file = ".env"

settings = Settings()
