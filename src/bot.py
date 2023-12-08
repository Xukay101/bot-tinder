from time import sleep

from selenium import webdriver

from config import settings

class TinderBot:

    def __init__(self): 
        self.driver = webdriver.Chrome()
        self.tinder_url = settings.TINDER_URL

    def start(self):
        self.driver.get(self.tinder_url)
        sleep(10)
