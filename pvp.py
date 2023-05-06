from pygame.locals import *
import pygame, os
pygame.init()

# Initializing global variables
WIN_SIZE = 600
WINDOW = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
pygame.display.set_caption('Ultimate Tic-Tac-Toe (PvP)')
BOARD_IMG = pygame.image.load(os.path.join('assets', 'board.png'))
BOARD_IMG = pygame.transform.scale(BOARD_IMG, (WIN_SIZE, WIN_SIZE))
Ximg = pygame.image.load(os.path.join('assets', 'cross.png'))
Oimg = pygame.image.load(os.path.join('assets', 'circle.png'))

# Class used for cross image
class Cross:
    def __init__(self, x, y, scale):
        self.image = pygame.transform.scale(Ximg, (Ximg.get_width() * scale, Ximg.get_height() * scale))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
    
    def show(self):
        WINDOW.blit(self.image, (self.rect.x, self.rect.y))

X = Cross(0, 0, (WIN_SIZE/800) * 0.7)

# Class used for circle image
class Circle:
    def __init__(self, x, y, scale):
        self.image = pygame.transform.scale(Oimg, (Oimg.get_width() * scale, Oimg.get_height() * scale))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
    
    def show(self):
        WINDOW.blit(self.image, (self.rect.x, self.rect.y))

O = Circle(0, 0, (WIN_SIZE/800) * 0.7)

# Links each element of a 3x3 grid to a single integer index 
posToIndex = {
(0,0): 0,
(1,0): 1,
(2,0): 2,
(0,1): 3,
(1,1): 4,
(2,1): 5,
(0,2): 6,
(1,2): 7,
(2,2): 8
}

# Links a single integer index to each element of a 3x3 grid
indexToPos = {
0: (0,0),
1: (1,0),
2: (2,0),
3: (0,1),
4: (1,1),
5: (2,1),
6: (0,2),
7: (1,2),
8: (2,2)
}

class Board:
    def __init__(self):
        self.pointer = -1
        self.values = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
        self.completed = [0,0,0,
                          0,0,0,
                          0,0,0]
        self.case = False

    def isValid(self, indexBoard, indexCell):
        if (self.completed[indexBoard] != 0):
            return False
        
        if self.pointer == -1:
            self.pointer = indexBoard
        
        if (self.pointer != indexBoard):
            return False

        if self.values[indexBoard][indexCell] != 0:
            return False

        return True

    def addValue(self, player, indexBoard, indexCell):
        self.values[indexBoard][indexCell] = player
        if self.completed[indexCell] != 0:
            self.pointer = -1
        else:
            self.pointer = indexCell

board = Board()

def locToIndex(rawx, rawy):
    for i in range(1, 10):
        if rawx < (WIN_SIZE/9) * i:
            cell_x = i-1
            board_x = int(cell_x/3)
            cell_x = cell_x - 3 * board_x
            break
    
    for j in range(1, 10):
        if rawy < (WIN_SIZE/9) * j:
            cell_y = j-1
            board_y = int(cell_y/3)
            cell_y = cell_y - 3 * board_y
            break

    return posToIndex[(board_x, board_y)], posToIndex[(cell_x, cell_y)]

def indexToLoc(indexBoard, indexCell):
    (board_x, board_y) = indexToPos[indexBoard]
    (cell_x, cell_y) = indexToPos[indexCell]
    cell_x = cell_x + 3 * board_x 
    cell_y = cell_y + 3 * board_y 

    
    pos_x = ((WIN_SIZE/9) * cell_x) + WIN_SIZE/32
    pos_y = ((WIN_SIZE/9) * cell_y) + WIN_SIZE/32

    return (pos_x, pos_y)

def hasWon(valueArray):
    if (valueArray[0] == 1 and valueArray[1] == 1 and valueArray[2] == 1):
        return 1
    if (valueArray[3] == 1 and valueArray[4] == 1 and valueArray[5] == 1):
        return 1
    if (valueArray[6] == 1 and valueArray[7] == 1 and valueArray[8] == 1):
        return 1
    if (valueArray[0] == 1 and valueArray[3] == 1 and valueArray[6] == 1):
        return 1
    if (valueArray[1] == 1 and valueArray[4] == 1 and valueArray[7] == 1):
        return 1
    if (valueArray[2] == 1 and valueArray[5] == 1 and valueArray[8] == 1):
        return 1
    if (valueArray[0] == 1 and valueArray[4] == 1 and valueArray[8] == 1):
        return 1
    if (valueArray[2] == 1 and valueArray[4] == 1 and valueArray[6] == 1):
        return 1

    if (valueArray[0] == 2 and valueArray[1] == 2 and valueArray[2] == 2):
        return 2
    if (valueArray[3] == 2 and valueArray[4] == 2 and valueArray[5] == 2):
        return 2
    if (valueArray[6] == 2 and valueArray[7] == 2 and valueArray[8] == 2):
        return 2
    if (valueArray[0] == 2 and valueArray[3] == 2 and valueArray[6] == 2):
        return 2
    if (valueArray[1] == 2 and valueArray[4] == 2 and valueArray[7] == 2):
        return 2
    if (valueArray[2] == 2 and valueArray[5] == 2 and valueArray[8] == 2):
        return 2
    if (valueArray[0] == 2 and valueArray[4] == 2 and valueArray[8] == 2):
        return 2
    if (valueArray[2] == 2 and valueArray[4] == 2 and valueArray[6] == 2):
        return 2
    
    return 0


def draw_window(board: Board):
    WINDOW.blit(BOARD_IMG, (0, 0))
    for i in range(9):
        for j in range(9):
            if board.values[i][j] == 0:
                continue
            if board.values[i][j] == 1:
                pos = indexToLoc(i, j)
                X.update(pos)
                X.show()
                continue
            if board.values[i][j] == 2:
                pos = indexToLoc(i, j)
                O.update(pos)
                O.show()
                continue


    pygame.display.update()

def main():
    curr_player = 1
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(10)
        draw_window(board)
            
        if hasWon(board.completed): # Win condition
            print(f'Player {hasWon(board.completed)} has won the game')
            continue

        if not (0 in board.completed):
            print('The game is a draw')
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                boardIndex, cellIndex = locToIndex(x, y)
                if board.isValid(boardIndex, cellIndex):
                    board.addValue(curr_player, boardIndex, cellIndex)
                    board.completed[boardIndex] = hasWon(board.values[boardIndex])
                    # if (hasWon(board.values[boardIndex]) == curr_player):
                    curr_player = 3 - curr_player

    
main()