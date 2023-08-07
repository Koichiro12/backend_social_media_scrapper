from flask import Flask,request
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route('/')
def index():
    return "Hallo"

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    login_data = {
        'email': username,
        'pass': password
    }

    return login_data

if __name__ == '__main__':
    app.run()