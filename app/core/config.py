from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    JWT_SECRET: str = "test-secret-key-for-ci"
    JWT_ALGORITHM: str = "HS256"
    APP_NAME: str = "LLM Code Reviewer"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
