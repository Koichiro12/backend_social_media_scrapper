import logging
import requests
from time import sleep
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException,WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pickle
import os
import time
import threading
import instaloader
from .constans.instagram_constants import (
   IG_BASE_URL
)

logger = logging.getLogger(__name__)

class InstagramScrapper:


    options = Options()
    d = DesiredCapabilities.CHROME
    driver = None
    path = os.path.abspath('core\drivers\chromedriver.exe')
    wait = None
    cookies = None
    connected = False
    username = None
    posts = []
    profile = None
    loader = None
    status = None
    def __init__(self,headless=False):
        self.d['goog:loggingPrefs'] = { 'performance':'ALL' }
        self.options.set_capability('goog:loggingPrefs', { 'performance':'ALL' })
        self.options.headless = headless
        self.status = '<span class="badge badge-danger">Disconnected</span>'
        self.posts = []
        self.loader = instaloader.Instaloader()
        self.profile = None

    def run(self):  
        service = ChromeService(executable_path=self.path)
        self.driver = webdriver.Chrome(options=self.options,service=service)
        self.driver.get(IG_BASE_URL)
        if os.path.exists(os.path.abspath("core\drivers\cookie\cookies_instagram.pkl")):
             os.unlink(os.path.abspath("core\drivers\cookie\cookies_instagram.pkl"))
        self.wait = WebDriverWait(self.driver,20)
    
    def connect(self,username,password):
        self.status = '<span class="badge badge-warning">Connecting To Instagram...</span>'
        self.run()
        try:
            self.wait.until(EC.visibility_of_element_located((By.NAME,'username')))
            self.wait.until(EC.visibility_of_element_located((By.NAME,'password')))
        except NoSuchElementException:
            self.driver.get(IG_BASE_URL)
            self.status = '<span class="badge badge-success">Connected</span>'
        finally:
            if os.path.exists(os.path.abspath("core\drivers\cookie\cookies_instagram.pkl")) == False:
                self.login(username, password)
            else:
                self.driver.refresh()
                self.connected = True
                self.status = '<span class="badge badge-success">Connected</span>'
               
    
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
                csrf_token = ""
                session_id = ""
                for cookie in self.cookies:
                    if cookie['name'] == 'csrftoken':
                        csrf_token = cookie['value']
                    if cookie['name'] == 'sessionid':
                        session_id = cookie['value']
                self.loader.load_session(self.username,{"sessionid": session_id, "csrftoken": csrf_token})
                self.profile = instaloader.Profile.from_username(self.loader.context,self.username)
                pickle.dump(self.driver.get_cookies(),open(os.path.abspath("core\drivers\cookie\cookies_instagram.pkl"),"wb"))
                thread = threading.Thread(target=self.getPost)
                thread.start()
        except NoSuchElementException:
            self.driver.quit()
            self.status = '<span class="badge badge-success">Cant Connect, Please Check Your Username Or Password</span>'
           
        except TimeoutException:
            self.driver.quit()
            self.status = '<span class="badge badge-success">Timeout</span>'
           
    def getPost(self):
        self.status = '<span class="badge badge-warning">Reading All Posts</span>'
        self.driver.get(IG_BASE_URL+self.username+'/')
        sleep(3)
        previous_height = self.driver.execute_script('return document.body.scrollHeight')
        while True:
            self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(5)
            new_height = self.driver.execute_script('return document.body.scrollHeight')
            if new_height == previous_height:
                break
            previous_height = new_height
        logs_raw = self.driver.get_log("performance")
        logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
        for log in filter(self.log_filter, logs):
            request_id = log["params"]["requestId"]
            resp_url = log["params"]["response"]["url"]
            if "?count=12" in resp_url:
                try:
                    data =  self.driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': log["params"]["requestId"]})
                    json_data = json.loads(data["body"])
                    if 'items' in json_data:
                        for item in json_data['items']:
                            if item not in self.posts:
                                self.posts.append(item)
                except WebDriverException:
                    pass
        self.connected = True
        self.status = '<span class="badge badge-success">Connected As '+self.username+'</span>'

    def getPosts(self):
        if self.connected == False:
            return "Not Connected"
        self.driver.get(IG_BASE_URL+self.username+'/')
        sleep(3)
        logs_raw = self.driver.get_log("performance")
        logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
        for log in filter(self.log_filter, logs):
            request_id = log["params"]["requestId"]
            resp_url = log["params"]["response"]["url"]
            if "/web_profile_info/?username=" in resp_url:
                try:
                    data =  self.driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': log["params"]["requestId"]})
                    json_data = json.loads(data["body"])
                    if 'items' in json_data:
                        for item in json_data['items']:
                            if item not in self.posts:
                                self.posts.append(item)
                    return self.posts
                except WebDriverException:
                    return "Oops,Something Went Wrong!,Please Try again"            
                break
        return "Oops,Something Went Wrong!,Please Try again"       
    @staticmethod
    def log_filter(log_):
        return (
            # is an actual response
            log_["method"] == "Network.responseReceived"
            # and json
            and "json" in log_["params"]["response"]["mimeType"]
        )
    
    def close(self):
        self.status = '<span class="badge badge-danger">Disconnecting...</span>'
        if self.driver == None:
            self.status = '<span class="badge badge-danger">Disconnected</span>'
        if os.path.exists(os.path.abspath("core\drivers\cookie\cookies_instagram.pkl")):
             os.unlink(os.path.abspath("core\drivers\cookie\cookies_instagram.pkl"))
        self.connected = False
        self.username = None
        self.posts = []
        self.driver.quit()
        self.status = '<span class="badge badge-danger">Disconnected</span>'

    def search(self,keywords):
        data_entries = []
        result = []
        if len(self.posts) < 0:
            self.getPosts()
            return data_entries
        data_entries = self.posts
        if keywords is None:
            return data_entries
        for data in data_entries:
             if data['caption'] != None and keywords in data['caption']['text']:
                result.append(data)
        return result