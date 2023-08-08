import logging
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pickle
import os

from .constans.facebook_constants import (
    FB_BASE_URL,
    FB_MBASIC_BASE_URL,
    FB_MOBILE_BASE_URL,
    FB_W3_BASE_URL,

    FB_PROFILE_BASE_URL
)


logger = logging.getLogger(__name__)

class FacebookScrapper:

    options = Options()
    driver = None
    path = os.path.abspath('core\drivers\chromedriver.exe')
    wait = None
    cookies = None
    def __init__(self,headless=False):
        self.options.headless = headless
    def run(self):
        service = ChromeService(executable_path=self.path)
        self.driver = webdriver.Chrome(options=self.options,service=service)
        self.driver.get(FB_BASE_URL)
        if os.path.exists(os.path.abspath("core\drivers\cookie\cookie.pkl")):
            cookies = pickle.load(open(os.path.abspath("core\drivers\cookie\cookie.pkl"),'rb'))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        self.wait = WebDriverWait(self.driver,20)
    def close(self):
        self.driver.quit()

    def getPath(self):
        return self.path  
    
    def connect(self,email,password):
        self.run()
        try:
            self.wait.until(EC.visibility_of_element_located((By.ID,'email')))
            self.wait.until(EC.visibility_of_element_located((By.ID,'pass')))
        except NoSuchElementException:
            driver.get(FB_BASE_URL)
            return "Connected"
        finally:
            if os.path.exists(os.path.abspath("core\drivers\cookie\cookie.pkl")) == False:
                return self.login(email, password)
            else:
                self.driver.refresh()
                return "Connected"
    
    def login(self,email,password):
        p = self.driver.find_element(By.ID, "email")
        p.send_keys(email)
        p = self.driver.find_element(By.ID, "pass")
        p.send_keys(password)
        p.send_keys(Keys.RETURN)
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="mount_0_0_DY"]/div/div[1]/div')))
        except NoSuchElementException:
            driver.get(FB_BASE_URL)
            return "Not Connected"
        finally:
            self.cookies = self.driver.get_cookies()
            pickle.dump(self.driver.get_cookies(),open(os.path.abspath("core\drivers\cookie\cookie.pkl"),"wb"))
            return "Connected"
        
            

        
        

        
       
    

        
           
    