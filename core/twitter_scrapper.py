import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException,WebDriverException
import pickle
import os
import time
from time import sleep
import json
from .constans.twitter_constants import (
    TWITTER_BASE_URL,
    TWITTER_LOGIN_URL
)

class TwitterScrapper:
    options = Options()
    path = os.path.abspath('core\drivers\chromedriver.exe')
    connected = False
    cookies = None
    wait = None
    username = None
    status = None
    def __init__(self,headless = False):
        self.options.set_capability('goog:loggingPrefs', { 'performance':'ALL' })
        self.options.headless = headless
        self.status = '<span class="badge badge-danger">Disconnected</span>'
    
    def run(self):
        service = ChromeService(executable_path=self.path)
        self.driver = webdriver.Chrome(options=self.options,service=service)
        self.driver.get(TWITTER_BASE_URL)
        if os.path.exists(os.path.abspath("core\drivers\cookie\cookies_twitter.pkl")):
             os.unlink(os.path.abspath("core\drivers\cookie\cookies_twitter.pkl"))
        self.wait = WebDriverWait(self.driver,20)

    def connect(self,username,password):
        self.status = '<span class="badge badge-warning">Connecting To Twitter...</span>'
        self.run()
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH,'//a[@href="/login"]')))
        except NoSuchElementException:
            self.driver.get(TWITTER_BASE_URL)
            self.status = '<span class="badge badge-success">Connected</span>'
            return '<span class="badge badge-success">Connected</span>'
        finally:
            if os.path.exists(os.path.abspath("core\drivers\cookie\cookies_twitter.pkl")) == False:
                return self.login(username, password)
            else:
                self.driver.refresh()
                self.connected = True
                self.status = '<span class="badge badge-success">Connected</span>'
                return '<span class="badge badge-success">Connected</span>'
    def login(self,username,password):
        self.driver.get(TWITTER_LOGIN_URL)
        try:
            wait = self.wait.until(EC.visibility_of_element_located((By.XPATH,'//input[@autocomplete="username"]')))
            if wait:
                p = self.driver.find_element(By.XPATH,'//input[@autocomplete="username"]')
                p.send_keys(username)
                p.send_keys(Keys.RETURN)
        except NoSuchElementException:
            self.status = '<span class="badge badge-warning">"TimeOut,Can"t Connected"</span>'
            return '<span class="badge badge-warning">"TimeOut,Can"t Connected"</span>'
        try:
            waits = WebDriverWait(self.driver,5)
            wait = waits.until(EC.visibility_of_element_located((By.XPATH,'//data-testid[@href="ocfEnterTextTextInput"]')))
            if wait:
                p = self.driver.find_element(By.XPATH,'//data-testid[@href="ocfEnterTextTextInput"]')
                p.send_keys(username)
                p.send_keys(Keys.RETURN)
        except NoSuchElementException:
            pass
        except TimeoutException:
            pass
        try:
            wait = self.wait.until(EC.visibility_of_element_located((By.XPATH,'//input[@autocomplete="current-password"]')))
            if wait:
                p = self.driver.find_element(By.XPATH,'//input[@autocomplete="current-password"]')
                p.send_keys(password)
                p.send_keys(Keys.RETURN)
        except NoSuchElementException:
            self.status = '<span class="badge badge-warning">"TimeOut,Can"t Connected"</span>'
            return '<span class="badge badge-warning">"TimeOut,Can"t Connected"</span>'
        try:
            waits = WebDriverWait(self.driver,10)
            wait = waits.until(EC.visibility_of_element_located((By.XPATH,'//a[@href="/home"]')))
            if wait:
                p = self.driver.find_element(By.XPATH,'//div[@class="css-1dbjc4n r-1adg3ll r-bztko3"]')
                username = str(p.get_attribute('data-testid'))
                self.username = username.replace("UserAvatar-Container-", "")
                self.cookies = self.driver.get_cookies()
                self.connected = True
                pickle.dump(self.driver.get_cookies(),open(os.path.abspath("core\drivers\cookie\cookies_twitter.pkl"),"wb"))
                self.driver.get(TWITTER_BASE_URL+self.username)
                self.status = '<span class="badge badge-success">Connected As '+self.username+'</span>'
                return '<span class="badge badge-success">Connected As '+self.username+'</span>'
        except NoSuchElementException:
            self.driver.quit()
            self.status = '<span class="badge badge-success">Can"t Connect, Please Check Your Username Or Password</span>'
            return '<span class="badge badge-success">Can"t Connect, Please Check Your Username Or Password</span>'
        except TimeoutException:
            self.driver.quit()
            self.status = '<span class="badge badge-success">TimeOut,Cant Connected</span>'
            return "TimeOut,Can't Connected" 
    def close(self):
        self.status = '<span class="badge badge-danger">Disconnecting...</span>'
        if self.driver == None:
            self.status = '<span class="badge badge-danger">Disconnected</span>'
            return '<span class="badge badge-danger">Disconnected</span>'
        os.unlink(os.path.abspath("core\drivers\cookie\cookies_twitter.pkl"))
        self.connected = False
        self.username = None
        self.posts = []
        self.driver.quit()
        self.status = '<span class="badge badge-danger">Disconnected</span>'
        return '<span class="badge badge-danger">Disconnected</span>'
    def getPosts(self):
        self.driver.get(TWITTER_BASE_URL+self.username)
        sleep(5)
        logs_raw = self.driver.get_log("performance")
        logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
        for log in filter(self.log_filter, logs):
            request_id = log["params"]["requestId"]
            resp_url = log["params"]["response"]["url"]
            if "/UserTweets?variables=" in resp_url:
                try:
                    data =  self.driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': log["params"]["requestId"]})
                    self.posts = json.loads(data['body'])
                    return json.loads(data["body"])
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