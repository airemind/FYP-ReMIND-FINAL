from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "ReMIND"
    DEBUG: bool = True
    DATABASE_URL: str
    SECRET_KEY: str
    ADMIN_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REDIS_URL: str
    REACT_BASE_URL: str
    REACT_BASE_URL_ALTERNATIVE: str
    AI_IMAGE_PATH: str
    AI_TEXT_PATH: str
    AI_VOICE_PATH: str

    # GOOGLE
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""

    # GROK
    GROK_API_KEY: str = ""

    # CLOUDINARY
    CLOUDINARY_URL: str = ""
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    # ELEVENLABS
    ELEVENLABS_API_KEY: str = ""

    # STORAGE
    UPLOAD_DIR: str = "uploads/"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
