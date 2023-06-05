import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame.locals import *
import pygame
import numpy as np
import torch
from additional.game_env import UltimateTicTacToe
from additional.alphazero import *
from additional.resnet import *
pygame.init()

# AlphaZero variables initialization
game = UltimateTicTacToe()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
args = {
    'C': 2,
    'num_searches': 4000,
    'dirichlet_epsilon': 0.0,
    'dirichlet_alpha': 0.3
}
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = ResNet(game, 9, 128, device)
model.load_state_dict(torch.load("./models/model_9_UTTT.pt", map_location=device))
model.eval()
mcts = MCTS(game, args, model)

# Initializing global variables
WIN_SIZE = 600
SIDE = WIN_SIZE / 3
WINDOW = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
pygame.display.set_caption('Ultimate Tic-Tac-Toe (PvAlphaZero)')
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

def draw_window(state, prev_move):
    WINDOW.blit(BOARD_IMG, (0, 0))
    highlight_squares = []
    completed = game._get_completed(state)

    for i in range(9):
        if completed[i] != 0:
            continue
        for j in range(9):
            if (game.get_valid_moves(state)[i * 9 + j] == 1) and not i in highlight_squares:
                highlight_squares.append(i)
    
    yellow = pygame.Surface((SIDE, SIDE), pygame.SRCALPHA)
    yellow.fill((255, 255, 153, 0.2*255))
    red = pygame.Surface((SIDE, SIDE), pygame.SRCALPHA)
    red.fill((255, 51, 0, 0.2*255))
    blue = pygame.Surface((SIDE, SIDE), pygame.SRCALPHA)
    blue.fill((51, 204, 255, 0.2*255))
    for i in highlight_squares:
        x = (i % 3) * SIDE
        y = (i // 3) * SIDE
        WINDOW.blit(yellow, (x, y))

    for i in range(len(completed)):
        if completed[i] == 1:
            x = (i % 3) * SIDE
            y = (i // 3) * SIDE
            WINDOW.blit(red, (x, y))

        if completed[i] == -1:
            x = (i % 3) * SIDE
            y = (i // 3) * SIDE
            WINDOW.blit(blue, (x, y))

    for i in range(9):
        for j in range(9):
            if state[i, j] == 0:
                continue
            if state[i, j] == 1:
                pos = indexToLoc(i, j)
                X.update(pos)
                X.show()
                continue
            if state[i, j] == -1:
                pos = indexToLoc(i, j)
                O.update(pos)
                O.show()
                continue
    
    if prev_move:
        pos = indexToLoc(prev_move[0], prev_move[1])
        pos = (pos[0] - WIN_SIZE/32, pos[1] - WIN_SIZE/32)
        s = pygame.Surface((SIDE / 3, SIDE / 3), pygame.SRCALPHA)
        if state[prev_move] == 1:
            s.fill((255, 51, 0, 0.2*255))
        else:
            s.fill((51, 204, 255, 0.2*255))
        WINDOW.blit(s, pos)

    pygame.display.update()

def main():
    curr_player = 1
    clock = pygame.time.Clock()
    run = True
    state = game.get_initial_state()
    action_taken = False
    prev_move = False
    while run:
        clock.tick(60)
        draw_window(state, prev_move)
        action_taken = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if curr_player == 1:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x,y = pygame.mouse.get_pos()
                    boardIndex, cellIndex = locToIndex(x, y)
                    action = boardIndex * 9 + cellIndex
                    if game.get_valid_moves(state)[action] == 1:
                        game.get_next_state(state, action, curr_player)
                        prev_move = (action // 9, action % 9)
                        action_taken = True
        
        if curr_player == -1:
            copy = state.copy()
            neutral_state = game.change_perspective(copy, curr_player)
            mcts_probs = mcts.search(neutral_state)
            action = np.argmax(mcts_probs)
            game.get_next_state(state, action, curr_player)
            prev_move = (action // 9, action % 9)
            action_taken = True

        if action_taken:
            value, is_terminal = game.get_value_and_terminated(state, action)
            if is_terminal:
                if value == 1:
                    if curr_player == -1:
                        print(f'AlphaZero won!')
                    if curr_player == 1:
                        print(f'You won!')
                if value == 0:
                    print(f'Draw!')
                state = game.get_initial_state()
                curr_player = -1
                prev_move = False
            curr_player = game.get_opponent(curr_player)
    
main()