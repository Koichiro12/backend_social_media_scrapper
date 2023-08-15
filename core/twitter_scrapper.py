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



class TwitterScrapper:

    
    options = Options()
    connected = False
    cookies = None
    wait = None
    def __init__(self,headless = False):
        self.options.headless = headless
    
    def connect(self,username,password):
        self.connected = True
        return '<span class="badge badge-success">Connected</span>'
    def close(self):
        self.connected = False
        return '<span class="badge badge-danger">Disconnected</span>'
    def getPosts(self):
        self.connected