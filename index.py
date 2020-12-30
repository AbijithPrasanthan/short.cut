#!/usr/bin/python3
from flask import *
import sqlite3
import string
import random
import re

app = Flask(__name__)
app.secret_key = "abc"  


dom = 'short.cut/'
length = 8
letters = string.ascii_letters + '1234567890'



def init():
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    cur.executescript('CREATE TABLE IF NOT EXISTS url(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,long varchar(200),short varchar(50));')

def create():
    short = ''
    short += dom
    short += ''.join(random.choice(letters) for i in range(length))     
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

@app.route('/long',methods=['GET','POST'])
def displayLong():
    conn = sqlite3.connect('main.db')

    if(request.method == 'POST'):

        cur = conn.cursor()

        long = request.form['text']
        if(isValid(long)):
            cur.execute('SELECT short FROM url where long = ?',(long,))
            fetch_data = cur.fetchone()
            if(not fetch_data):
                short = create()
                cur.execute('INSERT OR IGNORE INTO url (long,short) VALUES ( ?, ?) ',(long, short))
            else:
                short = fetch_data[0]
            flash(short)

        else:
            return redirect("invalid")

        conn.commit()
    return render_template('long.html')

@app.route('/',methods = ['GET','POST'])
def index():
    if(request.method == 'POST'):
        short = request.form['text']
        flash(short)
    return render_template('index.html')

@app.route('/invalid')
def invalid():
    return render_template('indexAlert.html')

def main():
    init()
    app.run(host="0.0.0.0", port='5200',debug=True)
if __name__ == "__main__":
    main()    

