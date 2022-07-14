import requests
import time



def local_game():
    #            0  1  2  3  4  5  6
    gameboard =[[0, 0, 0, 0, 0, 0, 0], # 0
                [0, 0, 0, 0, 0, 0, 0], # 1
                [0, 0, 0, 0, 0, 0, 0], # 2
                [0, 0, 0, 0, 0, 0, 0], # 3
                [0, 0, 0, 0, 0, 0, 0], # 4
                [0, 0, 0, 0, 0, 0, 0]] # 5


    def print_board(board):
        for row in board:
            colout = ''
            for col in row:
                if col == 0:
                    colout += '⚫'
                elif col == 1:
                    colout += '🔴'
                elif col == 2:
                    colout += '🟡'
            print(colout)

    def place_piece(color):
        # use the number insted of the color
        if color == 'red':
            color = 1
        elif color == 'yellow':
            color = 2


        check = True
        while check: 
            col = int(input('Enter a column: '))
            col = col - 1

            if col > 6 or col < -1:
                print('Invalid column')
            elif gameboard[0][col] != 0:
                print('Column is full')
            else:
                check = False
            # check if the column is full  



        row = 5
        while row >= 0:
            if gameboard[row][col] == 0:
                gameboard[row][col] = color
                break
            row -= 1

    def check_win():
        # check rows
        for row in gameboard:
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
            for row in gameboard:
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
            if gameboard[y][x] == 0:
                inDiag = 0
                color = 0
            elif gameboard[y][x] == 1:
                if color == 0 or color == 1:
                    inDiag += 1
                    color = 1
                else:
                    inDiag = 1
                    color = 1
            elif gameboard[y][x] == 2:
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
            print(x, y)
            if gameboard[y][x] == 0:
                inDiag = 0
                color = 0
            elif gameboard[y][x] == 1:
                if color == 0 or color == 1:
                    inDiag += 1
                    color = 1
                else:
                    inDiag = 1
                    color = 1
            elif gameboard[y][x] == 2:
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

    #gameloop
    game = True
    player = 'red'

    while game:
        if player == 'red':
            print('🔴 Red player turn\n')
            print_board(gameboard)
            place_piece(player)
            if check_win() == 1:
                print('🔴 Red player wins')
                game = False
                break
            player = 'yellow'


        if player == 'yellow':
            print('🟡 Yellow player turn\n')
            print_board(gameboard)
            place_piece(player)
            if check_win() == 2:
                print('🟡 Yellow player wins')
                game = False
                break
            player = 'red'


    print_board(gameboard)

def multiplayer_game():
    port = 3001

    def print_board(gameString):
        emote = ''
        for letter in gameString:
            
            if letter == '0':
                emote += '⚫'
            elif letter == '1':
                emote += '🔴'
            elif letter == '2':
                emote += '🟡'
            if len(emote) == 7:
                print(emote)
                emote = ''
        


    host = input('Enter the hostname or ip: ')

    # check if the host is valid
    r = requests.get('http://' + host + ':' + str(port) + '/test')
    if r.status_code == 200:
        print('Host is valid')
    else:
        print('Host is invalid')
        return
    
    print('Connecting to host...')
    r = requests.get('http://' + host + ':' + str(port) + '/connect')
    response = r.json()
    try:
        if response['full'] == 'full':
            print('Host is full')
            return
    except:
        a=1
    # read the json response
    
    time.sleep(1)
    key = response['key']
    gamePath = response['con']
    color = response['color']
    dot = ''

    print('Connected to host\n')
    if color == 'red':
        print('You are red 🔴')
        dot = '🔴'
    elif color == 'yellow':
        print('You are yellow 🟡')
        dot = '🟡'

    print('waiting for other player to connect...')
    waiting = True
    while waiting:
        r = requests.get('http://' + host + ':' + str(port) + '/' + gamePath)
        response = r.json()
        if response['wait'] == 'true':
            print('...')
            time.sleep(3)
        else:
            waiting = False
    print('Other player connected')
    print('Starting game...')
    
    game = True
    while game:

        if response['winner'] == 'red':
            print('🔴 Red player wins')
            print_board(response['board'])
            break
        elif response['winner'] == 'yellow':
            print('🟡 Yellow player wins')
            print_board(response['board'])
            break

        if response['turn'] == color:
            print('Your turn ' + dot)
            print_board(response['board'])
            re = input ('Enter the coloumn number: ')
            r = requests.post('http://' + host + ':' + str(port) + '/' + gamePath + '/post', data={'key': key, 'col': re})
            time.sleep(1)
        else:
            print('Other player\'s turn ')
            notTurn = True
            while notTurn:
                time.sleep(4)
                r = requests.get('http://' + host + ':' + str(port) + '/' + gamePath)
                response = r.json()
                if response['turn'] == color:
                    notTurn = False
        r = requests.get('http://' + host + ':' + str(port) + '/' + gamePath)
        response = r.json()









# bootloop
game = True
while game:
    userIn = input('Do you want to play a local or multiplayer? (y/n)\n 1. Local\n 2. Multiplayer\n')
    if userIn == '1':
        local_game()
        game = False
    elif userIn == '2':
        multiplayer_game()
        game = False