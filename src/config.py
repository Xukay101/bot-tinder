from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Getting .env variables
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra='ignore'
    )

    BOT_NAME: str = 'bot-tinder'

    TINDER_URL: str  = 'https://tinder.com'
    # TINDER_USERNAME: str
    # TINDER_PASSWORD: str

settings = Settings()
