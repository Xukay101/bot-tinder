from time import sleep
from random import random

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
        self.give_likes()

        sleep(100)

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
                "latitude": settings.LATITUDE,
                "longitude": settings.LONGITUDE,
                "accuracy": 100,
            },
        )

    def give_likes(self):
        html_element = self.driver.find_element(By.TAG_NAME, 'html')
        while True:
            # Browse photos
            self.browse_photos()
            sleep(1)

            # Probability of like
            if random() < settings.LIKE_PROBABILITY:
                # like_button = self.driver.find_element(By.XPATH, settings.XPATH_TINDER_LIKE_BUTTON)
                # like_button.click()
                html_element.send_keys(Keys.ARROW_RIGHT)

                # Ignore if matching
                # if self.is_math():
                #     ignore_button = self.driver.find_element(By.XPATH, settings.XPATH_TINDER_MATH_IGNORE_BUTTON)
            else:
                # deny_button = self.driver.find_element(By.XPATH, settings.XPATH_TINDER_DENY_BUTTON)
                # deny_button.click()
                html_element.send_keys(Keys.ARROW_LEFT)


    def browse_photos(self):
        photos_container = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, settings.XPATH_TINDER_PHOTOS_CONTAINER)))
        # REFACTORIZAR
        html_element = self.driver.find_element(By.TAG_NAME, 'html')
        for _ in range(6):
            html_element.send_keys(Keys.SPACE)
            sleep(1)

        # next_photo_button = self.driver.find_element(By.XPATH, settings.XPATH_TINDER_NEXT_PHOTO_BUTTON)
        # for _ in range(len(photos_elements)-1):
        #     next_photo_button.click()

    def is_math(self):
        try:
            math_element = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.XPATH, settings.XPATH_TINDER_MATH_CONTAINER)))
            return True
        except:
            return False
        
    def close(self):
        self.driver.quit()
