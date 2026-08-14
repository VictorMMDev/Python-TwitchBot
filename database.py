import sqlite3
import datetime


def initialisedb():
    # Create a connection to the database (or create it if it doesn't exist)
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()  # Create a cursor object
    cursor.execute(""" CREATE TABLE IF NOT EXISTS tokens
        (id TEXT PRIMARY KEY,
        tokenaccess TEXT NOT NULL,
        tokenrefresh TEXT NOT NULL,
        date TEXT NOT NULL)""" )

    cursor.execute(""" CREATE TABLE IF NOT EXISTS pointrewards
        (twitchid TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        image TEXT,
        sound TEXT,
        video TEXT,
        duration REAL NOT NULL,
        x INT NOT NULL,
        y INT NOT NULL,
        width INT NOT NULL,
        height INT NOT NULL,
        enabled INTEGER NOT NULL)""" )

    cursor.execute(""" CREATE TABLE IF NOT EXISTS chatandcommands
        (name TEXT PRIMARY KEY,
        response TEXT NOT NULL,
        chatorcommand INTEGER NOT NULL,
        enabled INTEGER NOT NULL)""" )

    
    conn.commit()
    conn.close()

def loadtokens(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()  # Create a cursor object
    cursor.execute(""" SELECT tokenaccess, tokenrefresh
        FROM tokens
        WHERE id = ?
        """, (id,))
    tokens = cursor.fetchone()

    conn.close()
    return tokens

def inserttokens(id,tokenaccess,tokenrefresh):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()  # Create a cursor object
    cursor.execute(""" INSERT INTO tokens
        (id, tokenaccess, tokenrefresh, date)
        VALUES (?, ?, ?, ?)
        """, (id, tokenaccess, tokenrefresh, datetime.datetime.now()))
    conn.commit()
    conn.close()


def updatetokens(id,tokenaccess,tokenrefresh):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()  # Create a cursor object

    cursor.execute(""" UPDATE tokens
        SET tokenaccess = ?, tokenrefresh = ?, date = ?
        WHERE id = ?
        """, (tokenaccess, tokenrefresh, datetime.datetime.now(), id ))

    conn.commit()
    conn.close()



def loadpointsreward(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()  # Create a cursor object
    cursor.execute(""" SELECT image, sound, video, duration, x, y, width, height, name
        FROM pointrewards
        WHERE twitchid = ? AND enabled = 1
        """, (id,))
    media = cursor.fetchone()

    conn.close()
    return media



def chatorcommands(name):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()  # Create a cursor object
    cursor.execute(""" SELECT response, chatorcommand
        FROM chatandcommands
        WHERE name = ? AND enabled = 1
        """, (name,))
    response = cursor.fetchone()
    
    conn.close()
    return response



def randommedia():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()  # Create a cursor object
    cursor.execute(""" SELECT image, sound, video, duration, x, y, width, height
        FROM pointrewards
        WHERE enabled = 1
        ORDER BY RANDOM()
        LIMIT 1
        """)
    media = cursor.fetchone()

    conn.close()
    return media