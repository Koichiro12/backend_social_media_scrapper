from flask import Flask,request
import requests
from bs4 import BeautifulSoup
from core.facebook_scrapper import FacebookScrapper

app = Flask(__name__)


fb = FacebookScrapper()
@app.route('/')
def index():
    return "Hallo"


@app.route('/connect/facebook',methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    return fb.connect(email, password)
@app.route('/disconnect/facebook')
def disconnect():
    fb.close()
    return "Closed"

@app.route('/search/<keyword>',methods=['POST'])
def search(keyword):
    return "Search :"+keyword

if __name__ == '__main__':
    app.run()
    