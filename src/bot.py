from time import sleep
from datetime import datetime, timedelta
from random import random, randint

import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from config import settings

class TinderBot:

    def __init__(self): 
        self.driver = uc.Chrome(use_subprocess=True)
        self.tinder_url = settings.TINDER_URL

        self.in_hibernation = False

    def start(self):
        self.driver.get(self.tinder_url)
        self.allow_location()
        self.login()
        self.give_likes()

    @staticmethod
    def wait_for_element(driver, by, locator, timeout=10):
        try:
            return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, locator)))
        except TimeoutException:
            raise Exception(f'Element not found: {locator}')

    @staticmethod
    def is_element_present(driver, by, locator, timeout=0):
        try:
            WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, locator)))
            return True
        except TimeoutException:
            return False

    def login(self):
        tinder_login_button = self.wait_for_element(self.driver, By.XPATH, settings.XPATH_TINDER_LOGIN_BUTTON)
        tinder_login_button.click()

        google_login_button = self.wait_for_element(self.driver, By.XPATH, settings.XPATH_GOOGLE_LOGIN_BUTTON)
        google_login_button.click()

        # Handle google login window
        main_page = self.driver.current_window_handle 
        for handle in self.driver.window_handles: 
            self.driver.switch_to.window(handle)
            if 'sign in' in self.driver.title.lower():
                login_page = handle
                break

        # Enter data in inputs
        email_input = self.wait_for_element(self.driver, By.XPATH, settings.XPATH_GOOGLE_EMAIL_INPUT)
        email_input.send_keys(settings.GOOGLE_EMAIL)
        email_input.send_keys(Keys.ENTER)

        password_input = self.wait_for_element(self.driver, By.XPATH, settings.XPATH_GOOGLE_PASSWORD_INPUT)
        password_input.send_keys(settings.GOOGLE_PASSWORD)
        password_input.send_keys(Keys.ENTER)

        self.driver.switch_to.window(main_page)
        sleep(10) # [Important] These 10 seconds are to load the main tinder page
                
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
        while True:
            # Check if any modal is present
            self.is_modal_present()

            # Check hibernation
            if self.in_hibernation:
                print('Retrying 12 hours')
                sleep(10) # 43220 = 12hours 20segs
                while self.is_out_of_likes_modal_present():
                    print('Retrying 15 minutes')
                    sleep(5) # 900 = 15mins
                self.in_hibernation = False
                
            # Browse photos
            self.browse_photos()

            # Probability of like
            if random() < settings.LIKE_PROBABILITY:
                # Like
                self.driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.ARROW_RIGHT)
            else:
                # Dislike
                self.driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.ARROW_LEFT)

    def is_modal_present(self):
        modal_xpaths = [
            settings.XPATH_TINDER_IGNORE_ADD_TO_DESKTOP_BUTTON,
            settings.XPATH_TINDER_IGNORE_BUY_PREMIUM_BUTTON,
            settings.XPATH_TINDER_IGNORE_LIMITED_LIKES_BUTTON,
            settings.XPATH_TINDER_IGNORE_MATCH_BUTTON,
        ]

        for xpath in modal_xpaths:
            sleep(0.15)
            if self.is_element_present(self.driver, By.XPATH, xpath):
                if xpath == settings.XPATH_TINDER_IGNORE_LIMITED_LIKES_BUTTON:
                    print("Detected limited likes modal. Entering hibernation...")
                    self.in_hibernation = True

                element_button = self.driver.find_element(By.XPATH, xpath)
                element_button.click()

    def is_out_of_likes_modal_present(self):
        xpath = settings.XPATH_TINDER_IGNORE_LIMITED_LIKES_BUTTON
        self.driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.ARROW_RIGHT)

        sleep(0.2)
        if self.is_element_present(self.driver, By.XPATH, xpath):
            element_button = self.driver.find_element(By.XPATH, xpath)
            element_button.click()
            return True
        return False

    def browse_photos(self):
        photos_container = self.wait_for_element(self.driver, By.XPATH, settings.XPATH_TINDER_PHOTOS_CONTAINER)
        sleep(1) # [Important] Wait for all the photos to load
        number_of_photos = len(photos_container.find_elements(By.TAG_NAME, 'span'))

        for _ in range(randint(1, number_of_photos-1)):
            self.driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.SPACE)
            sleep(0.5)

    def close(self):
        self.driver.quit()
