from ensta import Host,NewSessionID
import logging
import requests
import pandas as pd
logger = logging.getLogger(__name__)

class InstagramScrapper:


    username = None
    password = None
    profile = None
    host = None
    session_id = None
    def __init__(self):
        if self.session_id != None:
            self.host = Host(session_id)                

    def login(self,username,password):  
        session_id = NewSessionID(username, password)
        self.host = Host(session_id)
        self.username = username
        self.password = password
        if self.host.authenticated():
            self.session_id = session_id
            return "Connected"
        return "Cant'Connect"
    def getPosts(self):
        if self.session_id == None:
            return "Not Connected"
        posts = self.host.posts(self.username)
        result = []
        
        return result
    
    