from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Getting .env variables
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra='ignore'
    )

    BOT_NAME: str = 'bot-tinder'

    HEADLESS: bool = False
    TEST_MODE: bool = False # For check xpaths
    TINDER_URL: str  = 'https://tinder.com'    
    GOOGLE_EMAIL: str # Get of the .env
    GOOGLE_PASSWORD: str # Get of the .env
    LIKE_PROBABILITY: float = 0.8

    # Location // default in Buenos Aires
    LATITUDE: float = -34.603722
    LONGITUDE: float = -58.381592

    # XPath configurations
    XPATH_GOOGLE_LOGIN_BUTTON: str = '//*[@id="u-837590668"]' # Iframe grandfather   
    XPATH_GOOGLE_EMAIL_INPUT: str = '//*[@id="identifierId"]'
    XPATH_GOOGLE_PASSWORD_INPUT: str = '//*[@id="password"]/div[1]/div/div[1]/input' # '//input[@type="password"]' 
    XPATH_TINDER_LOGIN_BUTTON: str = '//*[@id="u-1919424827"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a'
    XPATH_TINDER_PHOTOS_CONTAINER: str = '//*[@id="u-1919424827"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]'
    # -- Modals
    XPATH_TINDER_IGNORE_MATCH_BUTTON: str = '//*[@id="o-1843744223"]/main/div/div[1]/div/div[4]/button'
    XPATH_TINDER_IGNORE_ADD_TO_DESKTOP_BUTTON: str = '//*[@id="u647161393"]/main/div[1]/div[2]/button[1]'
    XPATH_TINDER_IGNORE_BUY_PREMIUM_BUTTON: str = '//*[@id="u647161393"]/main/div[1]/div/div[3]/button[2]'
    XPATH_TINDER_IGNORE_LIMITED_LIKES_BUTTON: str = '//*[@id="u647161393"]/main/div/div[2]/button'
    XPATH_TINDER_IGNORE_NOTIFICATIONS_BUTTON: str = '//*[@id="u647161393"]/main/div[1]/div/div/div[3]/button[2]'

settings = Settings()
