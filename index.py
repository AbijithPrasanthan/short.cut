#!/usr/bin/python3


import sqlite3
import string
import random

dom = 'short.cut/'
length = 8
letters = string.ascii_letters

conn = sqlite3.connect('main.db')
cur = conn.cursor()

def init():
    cur.executescript('CREATE TABLE IF NOT EXISTS url(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,long varchar(200),short varchar(50));')

def create():
    short = ''
    short += dom
    short += ''.join(random.choice(letters) for i in range(length))     
    return short

def main():
    init()
    url = input('Enter the URL: ')
    short = create()
    cur.execute('INSERT OR IGNORE INTO url (long,short) VALUES ( ?, ?) ',( url, short))
    cur.execute('SELECT short FROM url where long = ?',(url,))
    conn.commit()

    cur.execute('INSERT INTO url (long,short) VALUES ( ?, ?) ',( url, short))
    print("Short URL:",cur.fetchone()[0])
if __name__ == "__main__":
    main()    

    #cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) 
    #    VALUES ( ?, ? )''', ( album, artist_id ) )
