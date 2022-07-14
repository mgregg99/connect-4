import random
from flask import Flask, render_template
import json
import os

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

player = 'red'

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
        f = open('game/game1.txt', 'w')
        f.write(boardToString(gameboard))
        f.close()
    
    game1 = []
    try:
        f = open('game/game1.txt', 'r')
        game1 = f.read()
        f.close()
    except:
        a = 1

    return json.dumps({'wait': wait, 'board': game1, 'turn': player})

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
    os.remove("game/game1.txt")
    return 'cleared'

@app.route("/test")
def test():
    return "test"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)