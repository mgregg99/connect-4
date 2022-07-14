import random
from flask import Flask, render_template
import json

app = Flask(__name__)
newGame = True
keys = []
#            0  1  2  3  4  5  6
gameboard =[[0, 0, 0, 0, 0, 0, 0], # 0
            [0, 0, 0, 0, 0, 0, 0], # 1
            [0, 0, 0, 0, 0, 0, 0], # 2
            [0, 0, 0, 0, 0, 0, 0], # 3
            [0, 0, 0, 0, 0, 0, 0], # 4
            [0, 0, 0, 0, 0, 0, 0]] # 5
game1 = []

newGame = True

def boardToString(board):
    string = ""
    for row in board:
        for col in row:
            string += str(col)
    return string

@app.route('/')
@app.route('/about')
def about():
    return render_template('info.html')

@app.route('/game')
def game():
    wait = 'true'
    if len(keys) == 2:
        wait = 'false'
    if game1 == False:
        game1 = gameboard
        
    return json.dumps({'wait': wait, 'board': boardToString(game1)})

@app.route("/connect")
def connect():
    if len(keys)  < 2:
        key = str(random.random())
        keys.append(key)
        if len(keys) == 1:
            return json.dumps({"key": key, "con": 'game', "color": 'red'})
        elif len(keys) == 2:
            return json.dumps({"key": key, "con": 'game', "color": 'yellow'})
    else:
        return "full"

@app.route("/clear")
def clear():
    keys.clear()
    return 'done'

@app.route("/test")
def test():
    return "test"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)