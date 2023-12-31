import platform
import logging, sys
from time import sleep
from datetime import datetime, timedelta
from random import random, randint, choice

import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from config import settings
from logger_config import configure_logging
from utils import get_memory_usage

configure_logging()

class TinderBot:

    def __init__(self): 
        options = uc.ChromeOptions()
        if settings.HEADLESS: options.add_argument('--headless')

        os = platform.system()
        if os == 'Windows':
            self.driver = uc.Chrome(
                driver_executable_path=settings.DRIVER_PATH,
                use_subprocess=True,
                options=options
            )
        elif os == 'Linux':
            self.driver = uc.Chrome(use_subprocess=True, options=options)
            
        self.tinder_url = settings.TINDER_URL

        self.in_hibernation = False

        self.messages = self.load_messages()

    def load_messages(self):
        try:
            with open('messages.txt', 'r', encoding='utf-8') as file:
                messages = [line.strip() for line in file]
            
            if not messages:
                raise ValueError('The messages file is empty.')

            return messages
        except FileNotFoundError:
            raise FileNotFoundError('The file was not found: message.txt')
        except Exception as e:
            raise Exception(f'Error loading messages: {str(e)}')

    def start(self):
        self.driver.get(self.tinder_url)
        sleep(5)
        self.allow_location()
        self.login()

        memory_usage = get_memory_usage()
        logging.info(f'Current RAM usage for this instance: {memory_usage} MB')

        if settings.TEST_MODE:
            sleep(3000)
        else:
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
        try:
            logging.info('Logging into Tinder...')

            tinder_login_button = self.wait_for_element(self.driver, By.XPATH, settings.XPATH_TINDER_LOGIN_BUTTON)
            tinder_login_button.click()
            logging.info('Clicked Tinder login button')

            google_login_button = self.wait_for_element(self.driver, By.XPATH, settings.XPATH_GOOGLE_LOGIN_BUTTON)
            google_login_button.click()
            logging.info('Clicked Google login button')

            # Handle google login window
            sleep(3)
            main_page = self.driver.current_window_handle 
            for handle in self.driver.window_handles: 
                self.driver.switch_to.window(handle)
                if 'sign in' in self.driver.title.lower():
                    login_page = handle
                    break
            else:
                raise Exception('Google login window not found')

            sleep(3)
            # Enter data in inputs
            email_input = self.wait_for_element(self.driver, By.XPATH, settings.XPATH_GOOGLE_EMAIL_INPUT)
            email_input.send_keys(settings.GOOGLE_EMAIL)
            email_input.send_keys(Keys.ENTER)
            logging.info('Entered Google email')

            password_input = self.wait_for_element(self.driver, By.XPATH, settings.XPATH_GOOGLE_PASSWORD_INPUT)
            password_input.send_keys(settings.GOOGLE_PASSWORD)
            password_input.send_keys(Keys.ENTER)
            logging.info('Entered Google password')

            sleep(10)
            self.driver.switch_to.window(main_page)
            sleep(5) # [Important] These seconds are to load the main tinder page

        except Exception as e:
            logging.error(f'Error during login: {str(e)}')
            self.close()
                
    def allow_location(self):
        self.driver.execute_cdp_cmd(
            'Browser.grantPermissions',
            {
                'origin': self.tinder_url,
                'permissions': ['geolocation'],
            },
        )
        self.driver.execute_cdp_cmd(
            'Emulation.setGeolocationOverride',
            {
                'latitude': settings.LATITUDE,
                'longitude': settings.LONGITUDE,
                'accuracy': 100,
            },
        )

    def give_likes(self):
        logging.info('Starting to given like')
        try:
            while True:
                # Check if any modal is present
                self.is_modal_present()
                sleep(1)

                # Check hibernation
                if self.in_hibernation:
                    logging.info('Retrying in hibernation mode for 12 hours')
                    sleep(43220) # 43220 = 12hours 20segs
                    while self.is_out_of_likes_modal_present():
                        logging.info('Retrying in hibernation mode for 15 minutes')
                        sleep(900) # 900 = 15mins
                    logging.info('The bot has come out of hibernation mode')
                    self.in_hibernation = False
                
                # Browse photos
                self.browse_photos()

                # Probability of like
                if random() < settings.LIKE_PROBABILITY:
                    # Like
                    self.driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.ARROW_RIGHT)
                    self.is_match()
                else:
                    # Dislike
                    self.driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.ARROW_LEFT)
        except Exception as e:
            logging.error(f'Error during giving likes: {str(e)}')
            self.close()

    def is_modal_present(self):
        modal_xpaths = [
            settings.XPATH_TINDER_IGNORE_ADD_TO_DESKTOP_BUTTON,
            settings.XPATH_TINDER_IGNORE_BUY_PREMIUM_BUTTON,
            settings.XPATH_TINDER_IGNORE_LIMITED_LIKES_BUTTON,
            settings.XPATH_TINDER_IGNORE_NOTIFICATIONS_BUTTON,
            settings.XPATH_TINDER_IGNORE_OFFER_BUTTON,
            settings.XPATH_TINDER_IGNORE_OFFER_2_BUTTON,
            settings.XPATH_TINDER_IGNORE_OFFER_3_BUTTON,
        ]

        for xpath in modal_xpaths:
            sleep(0.15)
            if self.is_element_present(self.driver, By.XPATH, xpath):
                if xpath == settings.XPATH_TINDER_IGNORE_LIMITED_LIKES_BUTTON:
                    logging.info('Detected limited likes modal. Entering hibernation...')
                    self.in_hibernation = True

                element_button = self.driver.find_element(By.XPATH, xpath)
                element_button.click()

    def is_match(self):
        xpath = settings.XPATH_TINDER_MESSAGE_INPUT

        if self.is_element_present(self.driver, By.XPATH, xpath, 0.20):
            message_input = self.wait_for_element(self.driver, By.XPATH, xpath)

            # Get random message
            message_string = choice(self.messages)

            # Write message in input box
            message_input.send_keys(message_string)

            # Send message
            message_input.send_keys(Keys.ENTER)
            sleep(1)

    def is_out_of_likes_modal_present(self):
        xpath = settings.XPATH_TINDER_IGNORE_LIMITED_LIKES_BUTTON
        # self.driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.ARROW_RIGHT)

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

        if number_of_photos in (0, 1):
            return

        for _ in range(randint(1, number_of_photos-1)):
            self.driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.SPACE)
            sleep(0.5)

    def close(self):
        logging.info('Closing the bot...')
        self.driver.quit()
