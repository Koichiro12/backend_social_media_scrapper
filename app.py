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
    return '<span class="badge badge-success">Connected</span>'

@app.route('/connect/instagram',methods=['POST'])
def loginInstagram():
    if ig.connected == False:
        username = request.form['username']
        password = request.form['password']
        return ig.connect(username, password)
    return '<span class="badge badge-success">Connected</span>'
@app.route('/connect/twitter',methods=['POST'])
def loginTwitter():
    if twitter.connected == False:
        username = request.form['username']
        password = request.form['password']
        return twitter.connect(username, password)
    return '<span class="badge badge-success">Connected</span>'


@app.route('/disconnect/facebook')
def disconnect():
    if fb.connected == True:
        return fb.close()
    return '<span class="badge badge-danger">Disconnected</span>'
 
@app.route('/disconnect/instagram')
def disconnectInstagram():
    if ig.connected == True:
        return ig.close()
    return '<span class="badge badge-danger">Disconnected</span>'
@app.route('/disconnect/twitter')
def disconnectTwitter():
    if twitter.connected == True:
        return twitter.close()
    return '<span class="badge badge-danger">Disconnected</span>'

@app.route('/getPosts/facebook')
def getFacebookPosts():
    return fb.getPosts()
   
@app.route('/getPosts/instagram')
def getInstagramPosts():
    return ig.getPosts()


@app.route('/getPosts/twitter')
def getTwitterPosts():
    return twitter.getPosts()

@app.route('/getStatus/facebook')
def getFacebookStatus():
    if fb.connected == True:
        return '<span class="badge badge-success">Connected</span>'
    return '<span class="badge badge-danger">Disconnected</span>'
   
@app.route('/getStatus/instagram')
def getInstagramStatus():
    if ig.connected == True:
        return '<span class="badge badge-success">Connected</span>'
    return '<span class="badge badge-danger">Disconnected</span>'

@app.route('/getStatus/twitter')
def getTwitterStatus():
    if twitter.connected == True:
        return '<span class="badge badge-success">Connected</span>'
    return '<span class="badge badge-danger">Disconnected</span>'



if __name__ == '__main__':
    try:
        app.run()
    finally:
        cleanup()
    