from flask import Flask,request
import requests
from bs4 import BeautifulSoup
from core.facebook_scrapper import FacebookScrapper
from core.instagram_scrapper import InstagramScrapper
from core.twitter_scrapper import TwitterScrapper
import threading
app = Flask(__name__)

fb = FacebookScrapper()
ig = InstagramScrapper()
twitter = TwitterScrapper()


def cleanup():
    fb.close()
    ig.close()
    twitter.close()

def thread_scrapper(scraper,credentials):
    return scraper.connect(credentials['username'], credentials['password'])

def thread_disconnect_scrapper(scraper,credentials):
    return scraper.close()


@app.route('/')
def index():
    return "Hallo"


@app.route('/connect/facebook',methods=['POST'])
def loginFacebook():
    if fb.connected == False:
        credentials = {
            "username":request.form['email'],
            "password":request.form['password']
        }
        thread = threading.Thread(target=thread_scrapper,args=(fb,credentials))
        thread.start()
        return fb.status
    return fb.status

@app.route('/connect/instagram',methods=['POST'])
def loginInstagram():
    if ig.connected == False:
        credentials = {
            "username":request.form['username'],
            "password":request.form['password']
        }
        thread = threading.Thread(target=thread_scrapper,args=(ig,credentials))
        thread.start()
        return ig.status
    return ig.status
@app.route('/connect/twitter',methods=['POST'])
def loginTwitter():
    if twitter.connected == False:
        credentials = {
            "username":request.form['username'],
            "password":request.form['password']
        }
        thread = threading.Thread(target=thread_scrapper,args=(twitter,credentials))
        thread.start()
        return twitter.status
    return twitter.status


@app.route('/disconnect/facebook')
def disconnect():
    if fb.connected == True:
        thread = threading.Thread(target=thread_disconnect_scrapper,args=(fb,True))
        thread.start()
        return fb.status
    return fb.status
 
@app.route('/disconnect/instagram')
def disconnectInstagram():
    if ig.connected == True:
        thread = threading.Thread(target=thread_disconnect_scrapper,args=(ig,True))
        thread.start()
        return ig.status
    return ig.status
@app.route('/disconnect/twitter')
def disconnectTwitter():
    if twitter.connected == True:
        thread = threading.Thread(target=thread_disconnect_scrapper,args=(twitter,True))
        thread.start()
        return twitter.status
    return twitter.status

@app.route('/getPosts/facebook')
def getFacebookPosts():
    if len(fb.posts) > 0:
        return fb.posts
    return fb.getPosts()
   
@app.route('/getPosts/instagram')
def getInstagramPosts():
    if len(ig.posts) > 0:
        return ig.posts
    return ig.getPosts()

@app.route('/getPosts/twitter')
def getTwitterPosts():
    if len(twitter.posts) > 0:
        return twitter.posts
    return twitter.getPosts()

@app.route('/getStatus/facebook')
def getFacebookStatus():
    return fb.status
   
@app.route('/getStatus/instagram')
def getInstagramStatus():
    return ig.status

@app.route('/getStatus/twitter')
def getTwitterStatus():
    return twitter.status

@app.route('/search')
def search():
    return

if __name__ == '__main__':
    try:
        app.run()
    finally:
        cleanup()
    