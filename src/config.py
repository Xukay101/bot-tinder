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
    GOOGLE_EMAIL: str
    GOOGLE_PASSWORD: str

    # XPath configurations
    XPATH_TINDER_LOGIN_BUTTON: str = '//*[@id="q488047873"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a'
    XPATH_GOOGLE_LOGIN_BUTTON: str = '//*[@id="q1569882032"]'
    XPATH_GOOGLE_EMAIL_INPUT: str = '//*[@id="identifierId"]'
    XPATH_GOOGLE_PASSWORD_INPUT: str = '//*[@id="password"]/div[1]/div/div[1]/input'
    

settings = Settings()
