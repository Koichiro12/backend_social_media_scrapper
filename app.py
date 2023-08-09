from flask import Flask,request
import requests
from bs4 import BeautifulSoup
from core.facebook_scrapper import FacebookScrapper
from core.instagram_scrapper import InstagramScrapper
app = Flask(__name__)


fb = FacebookScrapper()
ig = InstagramScrapper()

@app.route('/')
def index():
    return "Hallo"


@app.route('/connect/facebook',methods=['POST'])
def loginFacebook():
    email = request.form['email']
    password = request.form['password']
    return fb.connect(email, password)

@app.route('/connect/instagram',methods=['POST'])
def loginInstagram():
    email = request.form['email']
    password = request.form['password']
    return ig.login(email, password)

@app.route('/disconnect/facebook')
def disconnect():
    fb.close()
    return "Closed"

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
    app.run()
    