from environment import Board, UltimateTicTacToeEnv
from stable_baselines3 import PPO, DQN
from pygame.locals import *
from gym import spaces
import numpy as np
import pygame, os
import gym

pygame.init()

# Initializing global variables
model = PPO.load("models/ultimate_tic_tac_toe_ppo_final")

WIN_SIZE = 600
WINDOW = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
pygame.display.set_caption('Ultimate Tic-Tac-Toe')
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

# class Board:
#     def __init__(self):
#         self.pointer = -1
#         self.values = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
#                        [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
#                        [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
#         self.completed = [0,0,0,
#                           0,0,0,
#                           0,0,0]
#         self.valid_moves = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 14, 15: 15, 
#                             16: 16, 17: 17, 18: 18, 19: 19, 20: 20, 21: 21, 22: 22, 23: 23, 24: 24, 25: 25, 26: 26, 27: 27, 28: 28, 
#                             29: 29, 30: 30, 31: 31, 32: 32, 33: 33, 34: 34, 35: 35, 36: 36, 37: 37, 38: 38, 39: 39, 40: 40, 41: 41, 
#                             42: 42, 43: 43, 44: 44, 45: 45, 46: 46, 47: 47, 48: 48, 49: 49, 50: 50, 51: 51, 52: 52, 53: 53, 54: 54, 
#                             55: 55, 56: 56, 57: 57, 58: 58, 59: 59, 60: 60, 61: 61, 62: 62, 63: 63, 64: 64, 65: 65, 66: 66, 67: 67, 
#                             68: 68, 69: 69, 70: 70, 71: 71, 72: 72, 73: 73, 74: 74, 75: 75, 76: 76, 77: 77, 78: 78, 79: 79, 80: 80}

#     def update(self):
#         self.completed = [hasWon(i) for i in self.values]
#         self.valid_moves = {}
#         temp_valid_moves = []
#         for i in range(0, 81):
#             board_index = i // 9
#             cell_index = i % 9
#             if self.isValid(board_index, cell_index):
#                 temp_valid_moves.append(i)
#         for i in range(len(temp_valid_moves)):
#             self.valid_moves[i] = temp_valid_moves[i]
    
#     def isValid(self, indexBoard, indexCell):
#         temp_pointer = self.pointer
        
#         if (self.completed[indexBoard] != 0):
#             return False
#         if self.values[indexBoard][indexCell] != 0:
#             return False
        
#         if temp_pointer == -1:
#             temp_pointer = indexBoard
        
#         if (temp_pointer != indexBoard):
#             return False

#         return True

#     def addValue(self, player, indexBoard, indexCell):
#         # self.completed = [hasWon(i) for i in self.values]
#         self.values[indexBoard][indexCell] = player
#         if self.completed[indexCell] != 0:
#             self.pointer = -1
#         else:
#             self.pointer = indexCell

# class UltimateTicTacToeEnv(gym.Env):
#     def __init__(self):
#         super(UltimateTicTacToeEnv, self).__init__()

#         self.reset()

#         self.action_space = spaces.Discrete(len(list(self.board.valid_moves.values())))  # 9 boards * 9 squares = 81 actions
#         self.observation_space = spaces.Box(low=0, high=2, shape=(9, 9), dtype=int)

#     def reset(self):
#         self.board = Board()
#         self.current_player = 1
#         return self.get_state()

#     def step(self, action):
#         # Convert the action to board and square coordinates
#         if isinstance(action, np.ndarray):
#             board = action // 9
#             square = action % 9
#         else:
#             board = action[0]
#             square = action[1]

#         self.board.update()
#         if self.board.isValid(board, square):
#             self.board.addValue(self.current_player, board, square)
#             self.board.update()
#             self.action_space = spaces.Discrete(len(list(self.board.valid_moves.values())))

#             done, winner = self.check_game_over(board, square)
#             if done:
#                 reward = 1 if winner == self.current_player else 0
#             else:
#                 reward = 0

#             self.current_player = 3 - self.current_player
#         else:
#             reward = -1
#             done = False

#         return self.get_state(), reward, done, {}

#     def get_state(self):
#         return np.array(self.board.values)

#     def check_game_over(self, board, square):

#         if not (0 in self.board.completed):
#             return True, 0

#         if hasWon(self.board.completed) == 0:
#             return False, 0
#         return True, hasWon(self.board.completed)

#     def render(self, mode='human'):
#         print(self.board.values)

env = UltimateTicTacToeEnv()

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
    clock = pygame.time.Clock()
    run = True
    repeat=0
    while run:
        clock.tick(100)
        draw_window(env.board)
        
        if hasWon(env.board.completed) == -1:
            print('The game is a draw')
            continue

        if hasWon(env.board.completed) != 0: # Win condition
            print(f'Player {hasWon(env.board.completed)} has won the game')
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if env.current_player == 1:
                if repeat: print(repeat)
                repeat = 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    boardIndex, cellIndex = locToIndex(x, y)
                    env.step((boardIndex, cellIndex))
                    
            if env.current_player == 2:
                if (repeat >= 50):
                    env.step(env.action_space.sample())
                action, _ = model.predict(env.get_state())
                state, reward, done, info = env.step(action)
                repeat += 1
            

    
main()