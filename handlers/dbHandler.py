import sqlite3


db_name = "downloaded.db"
'''
Creates a database file is one does not alreadyexist.
'''
def createTable():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS posts (sub_id TEXT NOT NULL UNIQUE, title TEXT, udate TEXT, author TEXT, url TEXT, speed TEXT, PRIMARY KEY (sub_id))')
    c.close()
    conn.close()

'''
Enter submission information into the database.
Duplicates return 0 and entry is skippped, otherwise
it is logged and a 0 is returned.
'''
def dbWrite(perma, title, udate, author, url, speed):
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("INSERT INTO posts (sub_id, title, udate, author, url, speed) VALUES (?, ?, ?, ?, ?, ?)", (perma, title, udate, str(author), url, speed))
        conn.commit()
    except sqlite3.IntegrityError:
        c.close()
        conn.close()
        return 0

    c.close()
    conn.close()
    return 1

def dbUpdate(sub_id, url):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("UPDATE posts SET url = ? WHERE sub_id = ?", (url, sub_id))
    conn.commit()
    c.close()
    conn.close()

def getURL(sub_id, speed):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE sub_id=? AND speed=?", (sub_id, speed))
    rec = c.fetchone()
    if rec != None:
        return(rec[4])
    else:
        return None

createTable()
# dbWrite("1234", "this is a title", "08-10-17-08:00", "peskiusmobius", "", "0.75")
# dbUpdate("1234", "gfy_butt")
# print(getURL("12334", "0.75"))