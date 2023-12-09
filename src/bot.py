from time import sleep

import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from config import settings

class TinderBot:

    def __init__(self): 
        self.driver = uc.Chrome(use_subprocess=True)
        self.tinder_url = settings.TINDER_URL

    def start(self):
        self.driver.get(self.tinder_url)
        self.allow_location()
        self.login()

        sleep(20)

    def login(self):
        tinder_login_button = self.driver.find_element(By.XPATH, settings.XPATH_TINDER_LOGIN_BUTTON)
        tinder_login_button.click()

        
        google_login_button = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, settings.XPATH_GOOGLE_LOGIN_BUTTON)))
        google_login_button.click()

        # Handle google login window
        main_page = self.driver.current_window_handle 
        for handle in self.driver.window_handles: 
            self.driver.switch_to.window(handle)
            if "sign in" in self.driver.title.lower():
                login_page = handle
                break

        # Enter data in inputs
        email_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, settings.XPATH_GOOGLE_EMAIL_INPUT)))
        email_input.send_keys(settings.GOOGLE_EMAIL)
        email_input.send_keys(Keys.ENTER)

        password_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, settings.XPATH_GOOGLE_PASSWORD_INPUT)))
        password_input.send_keys(settings.GOOGLE_PASSWORD)
        password_input.send_keys(Keys.ENTER)

        self.driver.switch_to.window(main_page)

        
    def allow_location(self):
        self.driver.execute_cdp_cmd(
            "Browser.grantPermissions",
            {
                "origin": self.tinder_url,
                "permissions": ["geolocation"],
            },
        )
        self.driver.execute_cdp_cmd(
            "Emulation.setGeolocationOverride",
            {
                "latitude": -34.603722,
                "longitude": -58.381592,
                "accuracy": 100,
            },
        )

    def close(self):
        self.driver.quit()
