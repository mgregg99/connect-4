import pygame, sys
from colors import *
from pygame.locals import *

SCREEN_SIZE = (750, 650)

pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Connect Four')

#            0  1  2  3  4  5  6
gameboard =[[0, 0, 0, 0, 0, 0, 0], # 0
            [0, 0, 0, 0, 0, 0, 0], # 1
            [0, 0, 0, 0, 0, 0, 0], # 2
            [0, 0, 0, 0, 0, 0, 0], # 3
            [0, 0, 0, 0, 0, 0, 0], # 4
            [0, 0, 0, 0, 0, 0, 0]] # 5

class Flash:
    color = None
    r = 0
    g = 0
    b = 0
    decrease = True

    def __init__(self, color):
        if color == 'red':
            r = 255
            self.color = color
        elif color == 'black':
            r = 128
            g = 128
            b = 128
            self.color = color
    
    def get(self):
        return (self.r, self.g, self.b)
    
    def it(self):
        if self.color == 'red':
            if self.decrease:
                self.r -= 12
                if self.r < 50:
                    self.r = 50
                    self.decrease = False
            else:
                self.r += 12
                if self.r > 255:
                    self.r = 255
                    self.decrease = True
        elif self.color == 'black':
            if self.decrease:
                self.r -= 6
                self.g -= 6
                self.b -= 6
                if self.r < 50:
                    self.r = 50
                    self.g = 50
                    self.b = 50
                    self.decrease = False
            else:
                self.r += 6
                self.g += 6
                self.b += 6
                if self.r > 128:
                    self.r = 128
                    self.g = 128
                    self.b = 128
                    self.decrease = True

def draw_mouse_pos(DISPLAYSURF, pos):
    font = pygame.font.Font('freesansbold.ttf', 12)
    text = font.render(str(pos), True, BLACK)
    textRect = text.get_rect()
    textRect.center = (25, 25)
    DISPLAYSURF.blit(text, textRect)

def draw_colunm_numbers(DISPLAYSURF):
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("1", True, BLACK)
    textRect = text.get_rect()
    textRect.center = (100, 25)
    DISPLAYSURF.blit(text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("2", True, BLACK)
    textRect = text.get_rect()
    textRect.center = (200, 25)
    DISPLAYSURF.blit(text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("3", True, BLACK)
    textRect = text.get_rect()
    textRect.center = (300, 25)
    DISPLAYSURF.blit(text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("4", True, BLACK)
    textRect = text.get_rect()
    textRect.center = (400, 25)
    DISPLAYSURF.blit(text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("5", True, BLACK)
    textRect = text.get_rect()
    textRect.center = (500, 25)
    DISPLAYSURF.blit(text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("6", True, BLACK)
    textRect = text.get_rect()
    textRect.center = (600, 25)
    DISPLAYSURF.blit(text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("7", True, BLACK)
    textRect = text.get_rect()
    textRect.center = (700, 25)
    DISPLAYSURF.blit(text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("1", True, BLACK)
    textRect = text.get_rect()
    textRect.center = (25, 100)
    DISPLAYSURF.blit(text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("2", True, BLACK)
    textRect = text.get_rect()
    textRect.center = (25, 200)
    DISPLAYSURF.blit(text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("3", True, BLACK)
    textRect = text.get_rect()
    textRect.center = (25, 300)
    DISPLAYSURF.blit(text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("4", True, BLACK)
    textRect = text.get_rect()
    textRect.center = (25, 400)
    DISPLAYSURF.blit(text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("5", True, BLACK)
    textRect = text.get_rect()
    textRect.center = (25, 500)
    DISPLAYSURF.blit(text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("6", True, BLACK)
    textRect = text.get_rect()
    textRect.center = (25, 600)
    DISPLAYSURF.blit(text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("7", True, BLACK)
    textRect = text.get_rect()
    textRect.center = (25, 700)
    DISPLAYSURF.blit(text, textRect)

def place_piece(color, pos):
    col = (pos[0] + 50) // 100 - 1

    if col > 6 or col < -1:
        re_color = color
    elif gameboard[0][col] != 0:
        return color
    elif pos[0] < 50:
        return color

    # use the number insted of the color
    if color == 'red':
        color = 1
        re_color = 'black'
    elif color == 'black':
        color = 2
        re_color = 'red'

    
            
    # check if the column is full  

    row = 5
    while row >= 0:

        if gameboard[row][col] == 0:
            gameboard[row][col] = color
            break
        row -= 1

    return re_color

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

def draw_turn(turn):
    if turn == 'red':
        pygame.draw.circle(DISPLAYSURF, RED, (25, 25), 20)
    elif turn == 'black':
        pygame.draw.circle(DISPLAYSURF, GRAY, (25, 25), 20)    

def draw_pieces(DISPLAYSURF, gameboard):
    for x in range(0, 7):
        for y in range(0, 6):
            if gameboard[y][x] == 1:
                pygame.draw.circle(DISPLAYSURF, (RED), ((x * 100 + 100), (y * 100 + 100)), 40)
            elif gameboard[y][x] == 2:
                pygame.draw.circle(DISPLAYSURF, (GRAY), ((x * 100 + 100), (y * 100 + 100)), 40)

def draw_board():
    DISPLAYSURF.fill(YELLOW)
    for x in range(0, 7):
        for y in range(0, 6):
            pygame.draw.circle(DISPLAYSURF, (BLACK), ((x * 100 + 100), (y * 100 + 100)), 45)

def draw_win(color):
    if color == 1:
        pygame.draw.circle(DISPLAYSURF, (RED), (375, 325), 100)
    elif color == 2:
        pygame.draw.circle(DISPLAYSURF, (GRAY), (375, 325), 100)

def draw_hover(color, pos, flash):
    col = (pos[0] + 50) // 100 - 1
    if col > 6 or col < -1:
        return
    elif gameboard[0][col] != 0:
        return
    elif pos[0] < 50:
        return

    row = 5
    while row >= 0:
        if gameboard[row][col] == 0:
            if color == 'red':
                pygame.draw.circle(DISPLAYSURF, flash.get(), ((col * 100 + 100), (row * 100 + 100)), 40)
            elif color == 'black':
                pygame.draw.circle(DISPLAYSURF, flash.get(), ((col * 100 + 100), (row * 100 + 100)), 40)
            break
        row -= 1
    flash.it()

pos = (0,0)
turn = 'red'
flash = Flash(turn)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEMOTION:
            pos = (event.pos)

        if event.type == MOUSEBUTTONDOWN:
            pos = (event.pos)
            turn = place_piece(turn, pos)
            flash = Flash(turn)

    win = check_win()

    draw_board()
    draw_colunm_numbers(DISPLAYSURF)
    draw_pieces(DISPLAYSURF, gameboard)
    draw_turn(turn)
    draw_hover(turn, pos, flash)
    if win is not None:
        draw_win(win)
    #draw_mouse_pos(DISPLAYSURF, pos)

    
    pygame.display.update()
    FPSCLOCK.tick(30)