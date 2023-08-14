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
import time
import pandas as pd
import facebook_scraper as fs

from .constans.facebook_constants import (
    FB_BASE_URL,
    FB_MBASIC_BASE_URL,
    FB_MOBILE_BASE_URL,
    FB_W3_BASE_URL,

    FB_PROFILE_BASE_URL,
    FB_MOBILE_PROFILE_BASE_URL
)


logger = logging.getLogger(__name__)

class FacebookScrapper:

    options = Options()
    driver = None
    path = os.path.abspath('core\drivers\chromedriver.exe')
    wait = None
    cookies = None
    connected = False
    posts = []
    def __init__(self,headless=False):
        self.options.headless = headless
    def run(self):
        service = ChromeService(executable_path=self.path)
        self.driver = webdriver.Chrome(options=self.options,service=service)
        self.driver.get(FB_MOBILE_BASE_URL)
        if os.path.exists(os.path.abspath("core\drivers\cookie\cookies_facebook.pkl")):
             os.unlink(os.path.abspath("core\drivers\cookie\cookies_facebook.pkl"))
        self.wait = WebDriverWait(self.driver,20)
    def close(self):
        os.unlink(os.path.abspath("core\drivers\cookie\cookies_facebook.pkl"))
        self.driver.quit()
        self.connected = False
        self.posts = []
        return "Disconnected"

    def getPath(self):
        return self.path  
    
    def connect(self,email,password):
        self.run()
        try:
            self.wait.until(EC.visibility_of_element_located((By.NAME,'email')))
            self.wait.until(EC.visibility_of_element_located((By.NAME,'pass')))
        except NoSuchElementException:
            driver.get(FB_MOBILE_BASE_URL)
            return "Connected"
        finally:
            if os.path.exists(os.path.abspath("core\drivers\cookie\cookies_facebook.pkl")) == False:
                return self.login(email, password)
            else:
                self.driver.refresh()
                self.connected = True
                return "Connected"
    
    def login(self,email,password):
        p = self.driver.find_element(By.NAME, "email")
        p.send_keys(email)
        p = self.driver.find_element(By.NAME, "pass")
        p.send_keys(password)
        p.send_keys(Keys.RETURN)
        try:
            waits = WebDriverWait(self.driver,3)
            waits.until(EC.visibility_of_element_located((By.XPATH,'//*[@class="storyStream"]')))
        except NoSuchElementException:
            return "Not Connected"
        finally:
            try:
                self.cookies = self.driver.get_cookies()
                self.connected = True
                pickle.dump(self.driver.get_cookies(),open(os.path.abspath("core\drivers\cookie\cookies_facebook.pkl"),"wb"))
                return "Connected"
            finally:
                self.getPostInBackground()
    
    def getPostInBackground(self):
        if len(self.posts) <= 0:
            self.driver.get(FB_MOBILE_PROFILE_BASE_URL)
            previous_height = self.driver.execute_script('return document.body.scrollHeight')
            while True:
                self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                time.sleep(5)
                new_height = self.driver.execute_script('return document.body.scrollHeight')
                if new_height == previous_height:
                    break
                previous_height = new_height
            #Ekstrak data 
            result = ""
            link_feeds = self.driver.find_elements(By.XPATH,'//div[@class="story_body_container"]/div[1]/a') 
            for i in range(len(link_feeds)):            
                try:
                    if(link_feeds[i].get_attribute('href') != None):
                        link = str(link_feeds[i].get_attribute('href'))
                        start = link.index("story.php?story_fbid=") + 21
                        end = link.index("&id=")
                        if "&substory_index=" in link[start:end]:
                            end = link.index("&substory_index=")
                        gen = fs.get_posts(
                            post_urls=[link[start:end]],
                            options={"comments": True, "progress": True}
                        )
                        post = next(gen)
                        self.posts.append(post)
                    else:
                        posts.append('Postingan Tidak Dapat Di Temukan atau dihapus')
                except IndexError:
                    pass
    
    def updateRecentPosts(self):
        if self.connected == False:
            return "Not Connected"
        self.driver.get(FB_MOBILE_PROFILE_BASE_URL)
        previous_height = self.driver.execute_script('return document.body.scrollHeight')
        while True:
            self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(5)
            new_height = self.driver.execute_script('return document.body.scrollHeight')
            if new_height == previous_height:
                break
            previous_height = new_height
        #Ekstrak data 
        result = ""
        link_feeds = self.driver.find_elements(By.XPATH,'//div[@class="story_body_container"]/div[1]/a') 
        for i in range(len(link_feeds)):            
            try:
                if(link_feeds[i].get_attribute('href') != None):
                    link = str(link_feeds[i].get_attribute('href'))
                    start = link.index("story.php?story_fbid=") + 21
                    end = link.index("&id=")
                    if "&substory_index=" in link[start:end]:
                        end = link.index("&substory_index=")
                    gen = fs.get_posts(
                        post_urls=[link[start:end]],
                        options={"comments": True, "progress": True}
                    )
                    post = next(gen)
                    self.posts.append(post)
                else:
                    posts.append('Postingan Tidak Dapat Di Temukan atau dihapus')
            except IndexError:
                pass

    def getPosts(self):
        if self.connected == False:
            return "Not Connected"
        if len(self.posts) > 0:
            return self.posts
        self.driver.get(FB_MOBILE_PROFILE_BASE_URL)
        previous_height = self.driver.execute_script('return document.body.scrollHeight')
        while True:
            self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(5)
            new_height = self.driver.execute_script('return document.body.scrollHeight')
            if new_height == previous_height:
                break
            previous_height = new_height
        #Ekstrak data 
        result = ""
        link_feeds = self.driver.find_elements(By.XPATH,'//div[@class="story_body_container"]/div[1]/a') 
        for i in range(len(link_feeds)):            
            try:
                if(link_feeds[i].get_attribute('href') != None):
                    link = str(link_feeds[i].get_attribute('href'))
                    start = link.index("story.php?story_fbid=") + 21
                    end = link.index("&id=")
                    if "&substory_index=" in link[start:end]:
                        end = link.index("&substory_index=")
                    gen = fs.get_posts(
                        post_urls=[link[start:end]],
                        options={"comments": True, "progress": True}
                    )
                    post = next(gen)
                    self.posts.append(post)
                else:
                    posts.append('Postingan Tidak Dapat Di Temukan atau dihapus')
            except IndexError:
                pass
        # Post
        result = self.posts
        return result

            
        

            

        
            

        
        

        
       
    

        
           
    