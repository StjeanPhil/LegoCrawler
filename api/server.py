import sys, os, json, subprocess
from flask import Flask, jsonify, request

# Get the directory path of the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the project root directory to the Python path
sys.path.append(project_root)
# the sys.path.append() method adds the project root directory to the Python path, allowing the import of the scripts from the scripts folder

from bot.scripts.testscript import test as testy

app = Flask(__name__)

#@app.route('/')
#def index():
#    return render_template('./index.html')

@app.route('/test',methods=['POST'])
def test():
    print("TEST FUNCTION")
    testy()
    return jsonify({'result': "HELLO"})

#*** WATCHLIST API ***
@app.route('/getwatchlist',methods=['GET'])
def getwatchlist():
    data=[]
    with open('data/watchlist.json',"r") as file:
        print("Sending Watchlist")
        data = json.load(file)
    return data

@app.route('/postwatchlist',methods=['POST'])
def postwatchlist():
    data=request.json
    print(request.json)
    with open('data/watchlist.json',"w") as file:
        json.dump(data,file)
    return jsonify({'result': "thanks"})

#*** HITLIST API ***
@app.route('/gethitlist',methods=['GET'])
def gethitlist():
    data=[]
    with open('data/hitlist.json',"r") as file:
        print("Sending hitlist")
        data = json.load(file)
    return data
#*** Call CRAWL ***
@app.route('/crawl',methods=['GET'])
def crawl():
    data=[]
    try:
        subprocess.run(["python","bot/MainCrawl.py"])
        with open('data/hitlist.json',"r") as file:
            print("Sending Hitlist")
            data = json.load(file)
        return data
    except subprocess.CalledProcessError as e:
        print(e)
        return []

app.run(debug=True)

#https://dev.to/din0saur5/integrating-vite-with-flask-for-production-28af