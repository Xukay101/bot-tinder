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
    LIKE_PROBABILITY: float = 0.8

    # Location // default in Buenos Aires
    LATITUDE: float = -34.603722
    LONGITUDE: float = -58.381592

    # XPath configurations
    XPATH_GOOGLE_LOGIN_BUTTON: str = '//*[@id="o-1092281265"]'    
    XPATH_GOOGLE_EMAIL_INPUT: str = '//*[@id="identifierId"]'
    XPATH_GOOGLE_PASSWORD_INPUT: str = '//*[@id="password"]/div[1]/div/div[1]/input'
    XPATH_TINDER_LOGIN_BUTTON: str = '//*[@id="o2120851872"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a'
    XPATH_TINDER_ALLOW_LOCATION_BUTTON: str = '//*[@id="q-1240333203"]/main/div/div/div/div[3]/button[1]/div[2]/div[2]'
    XPATH_TINDER_PHOTOS_CONTAINER: str = '//*[@id="o2120851872"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]'
    XPATH_TINDER_IGNORE_MATCH_BUTTON: str = '//*[@id="o-1843744223"]/main/div/div[1]/div/div[4]/button'
    # XPATH_TINDER_NEXT_PHOTO_BUTTON: str = '' # Unused
    # XPATH_TINDER_LIKE_BUTTON: str = '' # Unused
    # XPATH_TINDER_DENY_BUTTON: str = '' # Unused
    XPATH_TINDER_IGNORE_ADD_TO_DESKTOP_BUTTON: str = '//*[@id="q-1240333203"]/main/div[1]/div[2]/button[2]'
    XPATH_TINDER_IGNORE_BUY_PREMIUM_BUTTON: str = '//*[@id="o392470796"]/main/div/div/div[3]/button[2]/div[2]/div[2]'
    XPATH_TINDER_IGNORE_LIMITED_LIKES_BUTTON: str = '//*[@id="o392470796"]/main/div/div[2]/button'

settings = Settings()
