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
    DRIVER_PATH: str = ''
    TINDER_URL: str  = 'https://tinder.com'    
    GOOGLE_EMAIL: str # Get of the .env
    GOOGLE_PASSWORD: str # Get of the .env
    LIKE_PROBABILITY: float = 0.6

    # Location
    LATITUDE: float = 40.71427
    LONGITUDE: float = -74.00597

    # XPath configurations
    XPATH_GOOGLE_LOGIN_BUTTON: str = '//*[@id="u-837590668"]' # Iframe grandfather   
    XPATH_GOOGLE_EMAIL_INPUT: str = '//*[@id="identifierId"]'
    
    if HEADLESS: XPATH_GOOGLE_PASSWORD_INPUT: str = '//input[@type="password"]' 
    else: XPATH_GOOGLE_PASSWORD_INPUT: str = '//*[@id="password"]/div[1]/div/div[1]/input' # 
    
    XPATH_TINDER_LOGIN_BUTTON: str = '//*[@id="u-1919424827"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a'
    XPATH_TINDER_PHOTOS_CONTAINER: str = '//*[@id="u-1919424827"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]'

    XPATH_TINDER_MESSAGE_INPUT: str = '//*[@id="u1084414182"]'
    XPATH_TINDER_MESSAGE_CLOSE: str = '//*[@id="u-1919424827"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[1]/a/button'    

    # -- Modals
    XPATH_TINDER_IGNORE_ADD_TO_DESKTOP_BUTTON: str = '//*[@id="u647161393"]/main/div[1]/div[2]/button[1]'
    XPATH_TINDER_IGNORE_BUY_PREMIUM_BUTTON: str = '//*[@id="u647161393"]/main/div[1]/div/div[3]/button[2]'
    XPATH_TINDER_IGNORE_LIMITED_LIKES_BUTTON: str = '//*[@id="u647161393"]/main/div/div[2]/button'
    XPATH_TINDER_IGNORE_NOTIFICATIONS_BUTTON: str = '//*[@id="u647161393"]/main/div[1]/div/div/div[3]/button[2]'
    XPATH_TINDER_IGNORE_OFFER_BUTTON: str = '//*[@id="u647161393"]/main/div[1]/div[1]/div[4]/button[1]'
    XPATH_TINDER_IGNORE_OFFER_2_BUTTON: str = '//*[@id="u647161393"]/main/div/div[1]/div[2]/button[2]'
    XPATH_TINDER_IGNORE_OFFER_3_BUTTON: str = '//*[@id="u-1919424827"]/div/div[1]/div/main/div[1]/div/button'

settings = Settings()
