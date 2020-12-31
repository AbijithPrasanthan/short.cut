#!/usr/bin/python3
from flask import *
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import string
import random
import re
import os

app = Flask(__name__)
app.secret_key = "abc"  
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

dom = 'https://short-cut-url.herokuapp.com/'
length = 4
letters = string.ascii_letters + '1234567890'
#DATABASE_URL = 'postgres://qtnygtouakwayq:9dc9a298313c8bf7c8554d5f10f1230a03aeaa23e79e647a17730db1f0ce504d@ec2-54-175-243-75.compute-1.amazonaws.com:5432/d4g5dn2frm9iqd'


'''def init():
    conn = sqlite3.connect(DATABASE_URL)
    cur = conn.cursor()
    print("DB initialised !!!!!")
    cur.executescript('CREATE TABLE IF NOT EXISTS url(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,long varchar(200),short varchar(50));')'''

@app.before_first_request
def create_tables():
    db.create_all()


class Urls(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True)
    long = db.Column("long", db.String())
    short = db.Column("short", db.String(10))

    def __init__(self, long, short):
        self.long = long
        self.short = short

def create():
    short = ''
    short += dom
    short += ''.join(random.choice(letters) for i in range(4))     
    return short

def isValid(long):
    regex =  ("((http|https)://)(www.)?"
            + "[a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]"
            + "{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)")
    p = re.compile(regex)
    
    if(long == None):
        return False

    if(re.search(p,long)):
        return True
    else:
        return False

def checkIfNotExists(short_url):
    '''conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    cur.execute('SELECT * from url where short = ?',(short,))
    res = cur.fetchone()'''

    res = Urls.query.filter_by(short=short_url).first()

    if(res):
        return False
    else:
        return True

@app.route('/long',methods=['GET','POST'])
def displayLong():
    if(request.method == 'POST'):
        long_url = request.form['text']
        if(isValid(long)):
            short = Urls.query.filter_by(long=long_url)
            if(short == None):
                short_url = create()
                new_url = Urls(long_url, short_url)
                db.session.add(new_url)
                db.session.commit()

            flash(short)
            return render_template('long.html')
        else:
            return redirect("invalid")

@app.route('/',methods = ['GET','POST'])
def index():
    if(request.method == 'POST'):
        short = request.form['text']
        flash(short)
    return render_template('index.html')

@app.route('/invalid')
def invalid():
    return render_template('indexAlert.html')

@app.route('/<short_url>')
def redirectShort(short_url):
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    long = Urls.query.filter_by(short=(dom + short_url))
    if(long != None):
        return redirect(long)
    else:
        flash('Invalid URL')
        return render_template('long.html')