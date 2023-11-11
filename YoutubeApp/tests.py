import time
import unittest
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tools.settings')

django.setup()

from django.test import TestCase
from django.test import LiveServerTestCase

from django.contrib.contenttypes.models import ContentType

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui  import WebDriverWait
import os

# Create your tests here.

class Index(LiveServerTestCase):
    driver:WebDriver = None

    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass


    @classmethod
    def setUpClass(self):

        ContentType.objects.clear_cache()
        super().setUpClass()
        self.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(self):
        self.driver.quit()
        super().tearDownClass()

   


    def test_navbar_items(self):
        #Choose your url to visit
        self.driver.get('http://127.0.0.1:8000/')
        elements = self.driver.find_elements(by=By.CSS_SELECTOR,value="nav a")
        self.assertEqual(len(elements),5)

    def test_youtube_transcript(self):
        self.driver.get('http://127.0.0.1:8000/')
        YoutubeNavTab = self.driver.find_element(by=By.CSS_SELECTOR,value="nav a[href~='/YoutubePage']")
        YoutubeNavTab.click()

        self.assertIn('YoutubePage',self.driver.current_url)

        url = self.driver.find_element(by=By.NAME,value="url")

        url.send_keys("https://www.youtube.com/watch?v=gsKH_VpqIuo")
        submit = self.driver.find_element(by=By.CSS_SELECTOR,value="form button")

        submit.click()

        wait = WebDriverWait(self.driver,15)
        Result:WebElement =wait.until(lambda x:x.find_element(by=By.CSS_SELECTOR,value="details p") )
        
        text = Result.get_attribute('innerText')
        self.assertGreater(len(text),2)

class Login(LiveServerTestCase):
    driver:WebDriver = None
    @classmethod
    def setUpClass(self):

        ContentType.objects.clear_cache()
        super().setUpClass()
        self.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(self):
        self.driver.quit()
        super().tearDownClass()
    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass

    def test_login(self):
        self.driver.get('http://127.0.0.1:8000/accounts/login/')
        wait = WebDriverWait(self.driver,15)
        
        UserName:WebElement =wait.until(lambda x:x.find_element(by=By.NAME,value="login") )

        Password = self.driver.find_element(by=By.NAME,value="password")

        UserName.send_keys("test")
        Password.send_keys("tomato123")
        Submit = self.driver.find_element(by=By.CSS_SELECTOR,value="button[type~='submit']")
        Submit.click()

        self.assertIn('http://127.0.0.1:8000/',self.driver.current_url)

        CurrentlyWatching:WebElement =wait.until(lambda x:x.find_element(by=By.CSS_SELECTOR,value="nav a[href~='/CurrentlyWatching']") )


        self.assertEqual(CurrentlyWatching.is_displayed(),True)

