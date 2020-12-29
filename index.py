#!/usr/bin/python3

from flask import *
import sqlite3
import string
import random

app = Flask(__name__)
app.secret_key = "abc"  


dom = 'short.cut/'
length = 8
letters = string.ascii_letters



def init():
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    cur.executescript('CREATE TABLE IF NOT EXISTS url(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,long varchar(200),short varchar(50));')

def create():
    short = ''
    short += dom
    short += ''.join(random.choice(letters) for i in range(length))     
    return short

@app.route('/long',methods=['GET','POST'])
def displayLong():
    conn = sqlite3.connect('main.db')

    if(request.method == 'POST'):

        cur = conn.cursor()

        long = request.form['text']
        short = create()
        cur.execute('INSERT OR IGNORE INTO url (long,short) VALUES ( ?, ?) ',(long, short))
        flash(short)

        conn.commit()
    return render_template('long.html')

@app.route('/',methods = ['GET','POST'])
def index():
    if(request.method == 'POST'):
        short = request.form['text']
        flash(short)
    return render_template('index.html')

def main():
    init()
    app.run(host="0.0.0.0", port='5200',debug=True)

if __name__ == "__main__":
    main()    

