from flask import Flask,request
import requests
from bs4 import BeautifulSoup
from core.facebook_scrapper import FacebookScrapper
from core.instagram_scrapper import InstagramScrapper
from core.twitter_scrapper import TwitterScrapper
app = Flask(__name__)


fb = FacebookScrapper()
ig = InstagramScrapper()
twitter = TwitterScrapper()
def cleanup():
    fb.close()
    ig.close()
    twitter.close()


@app.route('/')
def index():
    return "Hallo"


@app.route('/connect/facebook',methods=['POST'])
def loginFacebook():
    if fb.connected == False:
        email = request.form['email']
        password = request.form['password']
        return fb.connect(email, password)
    return "Already Connected"

@app.route('/connect/instagram',methods=['POST'])
def loginInstagram():
    if ig.connected == False:
        username = request.form['username']
        password = request.form['password']
        return ig.connect(username, password)
    return "Already Connected"

@app.route('/disconnect/facebook')
def disconnect():
    if fb.connected == True:
        return fb.close()
    return "Already Disconnected"
 
@app.route('/disconnect/instagram')
def disconnectInstagram():
    if ig.connected == True:
        return ig.close()
    return "Already Disconnected"
 
@app.route('/getPosts/facebook')
def getFacebookPosts():
    return fb.getPosts()
   
@app.route('/getPosts/instagram')
def getInstagramPosts():
    return ig.getPosts()

@app.route('/getPosts/twitter')
def getTwitterPosts():
    return ig.getPosts()

@app.route('/search/<keyword>',methods=['POST'])
def search(keyword):
    return "Search :"+keyword

if __name__ == '__main__':
    try:
        app.run()
    finally:
        cleanup()
    