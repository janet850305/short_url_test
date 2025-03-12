import sqlite3
import os
DB_FILE = "short_urls.db"

def init_db(): #create sqlite database table
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                short_url TEXT PRIMARY KEY,
                original_url TEXT NOT NULL,
                expiration_date INTEGER NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        print("SQLite already build!")
    else:
        print("SQLite already exist!")
init_db()  
