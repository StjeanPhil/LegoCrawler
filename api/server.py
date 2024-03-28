import sys, os,json
from flask import Flask, jsonify, request

#this is to add the project root directory to the python path to allow the import of the scripts from the scripts folder
# Get the directory path of the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the project root directory to the Python path
sys.path.append(project_root)

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


app.run(debug=True)