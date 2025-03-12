from flask import Flask, request, jsonify, redirect
import uuid
import string
import sqlite3
import os
import time
from datetime import datetime
DB_FILE = "short_urls.db"

#create sqlite database table
def init_db(): 
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


def save_url(short_url, original_url, expiration_date):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(('''INSERT OR IGNORE INTO urls (short_url,original_url,expiration_date) VALUES (?,?,?)'''),(short_url, original_url, expiration_date))
    conn.commit()
    conn.close()

def get_original_url(short_url):
    conn  = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(('''SELECT original_url, expiration_date FROM urls WHERE short_url = ?'''),(short_url,))
    
    result = c.fetchone()
    print(result)
    conn.close()
    return result

app = Flask(__name__)
BASE62_ALPHABET = string.ascii_letters + string.digits
def base62_encode(num):
    if num == 0:
        return BASE62_ALPHABET[0]
    base62 = []
    while num:
        num, rem = divmod(num, 62)
        base62.append(BASE62_ALPHABET[rem])
    
    return ''.join(reversed(base62))

def generate_short_url(original_url):
    unique_id = uuid.uuid5(uuid.NAMESPACE_DNS, original_url).int
    short_url = base62_encode(unique_id)[:32]
    return short_url 

@app.route('/shorten', methods=['POST'])
def short_url():
    try:
        data = request.get_json()
        original_url=data.get("original_url")
        if not original_url:
            return jsonify({"success":False,"reason":"Missing URL"}),400
        
        if len(original_url) > 2048:
            return jsonify({"success":False,"reason":"URL too long"}),400
        
        shorten_url =  generate_short_url(original_url)
        
        #Calculate expiration date  
        expiration_date = int(time.time()) + 30 * 24 * 60 * 60
        
        #Change timestamp to datetime
        exact_expiration_date = datetime.fromtimestamp(expiration_date)

        save_url(shorten_url,original_url,expiration_date)
        return jsonify({"short_url": shorten_url,"success":True,"expiration_date":exact_expiration_date}),400
    
    except sqlite3.Error as e:
        return jsonify({"success":False,"reason":"Database Error", "error": str(e)}),500
    
    except Exception as e:
        return jsonify({"success": False, "reason": "Server error", "error": str(e)}), 500 


@app.route('/<short_url>',methods = ['GET'])
def redirect_to_original(short_url):#redirect to original link
    try:
        result = get_original_url(short_url)
    
        if not result:
            return jsonify({"success":False,"reason":"Short URL not found"}),404
        
        original_url, expiration_date = result

        if time.time() > expiration_date:
            return jsonify({"success":False,"reason":"Short URL already expired"}),410
        
    except sqlite3.Error as e:  #catch sqlite error
        return jsonify({"success": False, "reason": "Database error","error":str(e)}),500
    
    except Exception as e: #catch unknown error
        return jsonify({"success":False, "reason":"Server error", "error":str(e)}),500
    
    return redirect(original_url)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
