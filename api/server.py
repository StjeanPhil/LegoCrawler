import sys, os, json, subprocess
from flask import Flask, jsonify, request
import sqlite3

# Get the directory path of the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the project root directory to the Python path
sys.path.append(project_root)
# the sys.path.append() method adds the project root directory to the Python path, allowing the import of the scripts from the scripts folder


app = Flask(__name__)


#*** WATCHLIST API ***
@app.route('/getwatchlist',methods=['GET'])
def getwatchlist():
    
    conn = sqlite3.connect('LegoLogs.db') #Opening DB
    cursor = conn.cursor()    
    data=cursor.execute('''SELECT * FROM watchlist''').fetchall() #Getting watchlist
    conn.close() #closing DB
    data=json.dumps(data)#Formating data

    print("Sending watchlist")
    return data

@app.route('/insertwatchlist',methods=['POST'])
def insertwatchlist():
    try:
        data=request.json
        print(request.json)
        conn = sqlite3.connect('LegoLogs.db') #Opening DB
        cursor = conn.cursor()  
        cursor.execute('''INSERT INTO watchlist (set_num,target_price) VALUES (?,?)''',(data['set_num'],data['price']))
        conn.commit()
        conn.close()
        return jsonify({'result': "Success"})
    except Exception as e:
        conn.close()
        print(e)
        return jsonify({'result': "Error"})

@app.route('/deletewatchlist',methods=['POST'])
def deletewatchlist():
    try:
        data=request.json
        print(request.json)
        conn = sqlite3.connect('LegoLogs.db') #Opening DB
        cursor = conn.cursor()  
        cursor.execute('''DELETE FROM watchlist WHERE set_num=?''',(data['set_num'],))
        conn.commit()
        conn.close()
        return jsonify({'result': "Success"})
    except Exception as e:
        conn.close()
        print(e)
        return jsonify({'result': "Error"})
@app.route('/updatewatchlist',methods=['POST'])
def updatewatchlist():
    try:
        data=request.json
        print(request.json)
        conn = sqlite3.connect('LegoLogs.db') #Opening DB
        cursor = conn.cursor()  
        cursor.execute('''UPDATE watchlist SET target_price=? WHERE set_num=?''',(data['price'],data['set_num']))
        conn.commit()
        conn.close()
        return jsonify({'result': "Success"})
    except Exception as e:
        conn.close()
        print(e)
        return jsonify({'result': "Error"})

#*** HITLIST API ***
@app.route('/gethitlist',methods=['GET'])
def gethitlist():
    conn = sqlite3.connect('LegoLogs.db') #Opening DB
    cursor = conn.cursor()    
    data=cursor.execute('''SELECT * FROM hitlist''').fetchall() #Getting watchlist
    conn.close() #closing DB
    data=json.dumps(data)#Formating data

    print("Sending hitlist")
    return data


#*** Call CRAWL ***
@app.route('/crawl',methods=['GET'])
def crawl():
    data=[]
    try:
        data=subprocess.run(["python","bot/MainCrawl.py"])

        return jsonify(data)
    except subprocess.CalledProcessError as e:
        print(e)
        return []

app.run(debug=True)

#https://dev.to/din0saur5/integrating-vite-with-flask-for-production-28af