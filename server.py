import random
from crypt import methods
from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

class gameClass:
    keys = []
    redkey = ''
    yellowkey = ''
    player = 'red'
    gameboard = '000000000000000000000000000000000000000000'
    template =  '000000000000000000000000000000000000000000'
    needsClear = False

    def clear(self):
        self.keys = []
        self.redkey = ''
        self.yellowkey = ''
        self.player = 'red'
        self.gameboard = self.template
        self.needsClear = False

    
    def place_piece(self, col):
        # use the number insted of the color
        nextplayer = ''
        if self.player == 'red':
            color = 1
            nextplayer = 'yellow'
        elif self.player == 'yellow':
            color = 2
            nextplayer = 'red'
        board = []
        temp = []
        for letter in self.gameboard:
            temp.append(letter)
            if len(temp) == 7:
                board.append(temp)
                temp = []
        col = col - 1
        if int(col) > 6 or int(col) < -1:
            return'Invalid column'
        elif board[0][col] != '0':
            return 'Column is full'
    
        row = 5
        while row >= 0:
            if board[row][col] == '0':
                board[row][col] = color
                break
            row -= 1
        temp = ''
        for line in board:
            for i in line:
                temp += str(i)
        self.gameboard = temp
        self.player = nextplayer
        return 'success'

    def check_win(self):

        board = []
        temp = []
        for letter in self.gameboard:
            temp.append(int(letter))
            if len(temp) == 7:
                board.append(temp)
                temp = []
        
        # check rows
        for row in board:
            inRow = 0
            color = 0
            for col in row:
                if col == 0:
                    inRow = 0
                    color = 0
                elif col == 1:
                    if color == 0 or color == 1:
                        inRow += 1
                        color = 1
                    else:
                        inRow = 1
                        color = 1
                elif col == 2:
                    if color == 0 or color == 2:
                        inRow += 1
                        color = 2
                    else:
                        inRow = 1
                        color = 2
                if inRow == 4:
                    return color
        # check columns
        x = 0
        while x < 7:
            inCol = 0
            color = 0
            for row in board:
                if row[x] == 0:
                    inCol = 0
                    color = 0
                elif row[x] == 1:
                    if color == 0 or color == 1:
                        inCol += 1
                        color = 1
                    else:
                        inCol = 1
                        color = 1
                elif row[x] == 2:
                    if color == 0 or color == 2:
                        inCol += 1
                        color = 2
                    else:
                        inCol = 1
                        color = 2
                if inCol == 4:
                    return color
            x += 1

        # check diagonals
        inDiag = 0
        color = 0
        start = [0, 0]
        x = 0
        y = 0
        while x < 7 and y < 6:
            if board[y][x] == 0:
                inDiag = 0
                color = 0
            elif board[y][x] == 1:
                if color == 0 or color == 1:
                    inDiag += 1
                    color = 1
                else:
                    inDiag = 1
                    color = 1
            elif board[y][x] == 2:
                if color == 0 or color == 2:
                    inDiag += 1
                    color = 2
                else:
                    inDiag = 1
                    color = 2
            if inDiag == 4:
                return color
            if x == 6 or y <= 0:
                if start[1] == 5:
                    start[0] += 1
                else:
                    start[1] += 1
                    start[0] = 0
                x = start[0]
                y = start[1]
            else:
                x += 1
                y -= 1

        inDiag = 0
        color = 0
        start = [6, 0]
        x = 6
        y = 0

        while x > -1 and y < 6:
            if board[y][x] == 0:
                inDiag = 0
                color = 0
            elif board[y][x] == 1:
                if color == 0 or color == 1:
                    inDiag += 1
                    color = 1
                else:
                    inDiag = 1
                    color = 1
            elif board[y][x] == 2:
                if color == 0 or color == 2:
                    inDiag += 1
                    color = 2
                else:
                    inDiag = 1
                    color = 2
            if inDiag == 4:
                return color


            if x == 0 or y == 0:
                if start[1] == 5:
                    start[0] -= 1
                else:
                    start[1] += 1
                    start[0] = 6
                x = start[0]
                y = start[1]
            else:
                x -= 1
                y -= 1

        

game1 = gameClass()

@app.route('/')
@app.route('/about')
def about():
    return render_template('info.html')

@app.route('/game')
def game():
    global game1
    wait = 'true'
    if len(game1.keys) == 2:
        wait = 'false'

    winner = game1.check_win()
    if winner == 1:
        winner = 'red'
        game1.needsClear = True
    elif winner == 2:
        winner = 'yellow'
        game1.needsClear = True
    return json.dumps({'wait': wait, 'board': game1.gameboard, 'turn': game1.player, 'winner': winner})

@app.route('/game/post', methods=['POST'])
def post():
    if request.method == 'POST':
        col = request.form['col']
        key = request.form['key']
        global player
        if game1.player == 'red' and key == game1.redkey:
            game1.place_piece(int(col))
        if game1.player == 'yellow' and key == game1.yellowkey:
            game1.place_piece(int(col))

    return 'done'


@app.route("/connect")
def connect():
    global game1
    if game1.needsClear:
        game1.clear()
    if len(game1.keys)  < 2:
        
        key = str(random.random())
        game1.keys.append(key)
        if len(game1.keys) == 1: 
            game1.redkey = key
            return json.dumps({"key": key, "con": 'game', "color": 'red'})
        elif len(game1.keys) == 2:
            game1.yellowkey = key
            return json.dumps({"key": key, "con": 'game', "color": 'yellow'})
    else:
        return json.dumps({"full": 'full'})

@app.route("/clear")
def clear():
    global game1
    game1.clear()
    return 'done'

@app.route("/test")
def test():
    return "test"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)