import logging
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pickle
import os
import time
from .constans.instagram_constants import (
   IG_BASE_URL
)

logger = logging.getLogger(__name__)

class InstagramScrapper:


    options = Options()
    driver = None
    path = os.path.abspath('core\drivers\chromedriver.exe')
    wait = None
    cookies = None
    connected = False
    username = None

    def __init__(self,headless=False):
        self.options.headless = headless               

    def run(self):  
        service = ChromeService(executable_path=self.path)
        self.driver = webdriver.Chrome(options=self.options,service=service)
        self.driver.get(IG_BASE_URL)
        if os.path.exists(os.path.abspath("core\drivers\cookie\cookies_instagram.pkl")):
             os.unlink(os.path.abspath("core\drivers\cookie\cookies_instagram.pkl"))
        self.wait = WebDriverWait(self.driver,20)
    
    def connect(self,username,password):
        self.run()
        try:
            self.wait.until(EC.visibility_of_element_located((By.NAME,'username')))
            self.wait.until(EC.visibility_of_element_located((By.NAME,'password')))
        except NoSuchElementException:
            self.driver.get(IG_BASE_URL)
            return "Connected"
        finally:
            if os.path.exists(os.path.abspath("core\drivers\cookie\cookies_instagram.pkl")) == False:
                return self.login(username, password)
            else:
                self.driver.refresh()
                self.connected = True
                return "Connected"
    
    def login(self,username,password):
        p = self.driver.find_element(By.NAME, "username")
        p.send_keys(username)
        p = self.driver.find_element(By.NAME, "password")
        p.send_keys(password)
        p.send_keys(Keys.RETURN)
        try:
            waits = WebDriverWait(self.driver,30)
            wait = waits.until(EC.visibility_of_element_located((By.XPATH,'//a[@href="/?next=%2F"]')))
            if wait:
                p = self.driver.find_element(By.XPATH,'//img[@class="xpdipgo x6umtig x1b1mbwd xaqea5y xav7gou xk390pu x5yr21d xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x11njtxf xh8yej3"]')
                username = str(p.get_attribute('alt'))
                self.username = username.replace("'s profile picture", "")
                self.cookies = self.driver.get_cookies()
                self.connected = True
                pickle.dump(self.driver.get_cookies(),open(os.path.abspath("core\drivers\cookie\cookies_instagram.pkl"),"wb"))
                return "Connected As "+self.username
        except NoSuchElementException:
            self.driver.quit()
            return "Can't Connect, Please Check Your Username Or Password"
        except TimeoutException:
            self.driver.quit()
            return "TimeOut,Can't Connected" 
            
    def getPosts(self):
        if self.connected == False:
            return "Not Connected"
        result = []
        result_posts = []
        self.driver.get(IG_BASE_URL+self.username+'/')
        previous_height = self.driver.execute_script('return document.body.scrollHeight')
        while True:
            self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(10)
            posts = self.driver.find_elements(By.TAG_NAME,'a')
            for post in posts:
                link_post = post.get_attribute('href')
                if '/p/' in link_post and link_post not in result_posts:
                    result_posts.append(link_post)
            new_height = self.driver.execute_script('return document.body.scrollHeight')
            if new_height == previous_height:
                break
            previous_height = new_height
        return result
    def close(self):
        if self.driver == None:
            return "Already Disconnected"
        os.unlink(os.path.abspath("core\drivers\cookie\cookies_instagram.pkl"))
        self.connected = False
        self.username = None
        self.driver.quit()
        return "Disconnected"
    