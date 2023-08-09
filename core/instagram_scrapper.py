from instaloader import *
import logging
import requests
import pandas as pd
logger = logging.getLogger(__name__)

class InstagramScrapper:

    loader = None
    username = "iki.irul"
    password = None
    profile = None
    def __init__(self):
        self.loader = instaloader.Instaloader()

    def login(self,username,password):
        self.loader.login(username,password)
        self.username = username
        self.password = password
        return "Done"
    def getPosts(self):
        posts = Profile.from_username(self.loader.context,self.username).get_posts()
        post_title = []
        post_date = []
        for post in posts:
            print(post.title)
        return post_title
    
    