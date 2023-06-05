from gym.spaces import Box, Discrete
import numpy as np
import gym

class Board:
    def __init__(self):
        self.pointer = -1
        self.current_player = 1
        self.values = [[0 for _ in range(9)] for _ in range(9)]
        self.completed = [0 for _ in range(9)]
        self.valid_moves = {}
        for i in range(81): self.valid_moves[i] = i

    def update(self):
        self.completed = [Board.hasWon(i) for i in self.values]
        self.valid_moves = {}
        temp_valid_moves = []
        for i in range(0, 81):
            board_index = i // 9
            cell_index = i % 9
            if self.isValid(board_index, cell_index):
                temp_valid_moves.append(i)
        for i in range(len(temp_valid_moves)):
            self.valid_moves[i] = temp_valid_moves[i]
    
    def isValid(self, indexBoard, indexCell):
        temp_pointer = self.pointer
        
        if (self.completed[indexBoard] != 0):
            return False
        if self.values[indexBoard][indexCell] != 0:
            return False
        
        if temp_pointer == -1:
            temp_pointer = indexBoard
        
        if (temp_pointer != indexBoard):
            return False

        return True

    def addValue(self, player, indexBoard, indexCell):
        self.values[indexBoard][indexCell] = player
        self.update()
        self.current_player = 3 - self.current_player

        if self.completed[indexCell] != 0:

            self.pointer = -1
        else:
            self.pointer = indexCell

    @staticmethod
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
        
        if not (0 in valueArray):
            return -1

        return 0

class UltimateTicTacToeEnv(gym.Env):
    def __init__(self):
        super(UltimateTicTacToeEnv, self).__init__()

        self.reset()

        self.action_space = Discrete(81)  # 9 boards * 9 squares = 81 actions spaces.

        self.observation_space = Box(low=0, high=2, shape=(83,), dtype=np.int) # 81 squares from the board + pointer + current_player

    def reset(self):
        self.board = Board()
        self.current_player = 1
        return self.get_state()

    def step(self, action):
        reward = 0
        if not (isinstance(action, tuple)):
            action = int(action)
            board = action // 9
            square = action % 9
        else:
            board = action[0]
            square = action[1]
        self.board.update()
        if self.board.isValid(board, square):
            reward += 1
            self.board.addValue(self.current_player, board, square)
            self.board.update()
            if (Board.hasWon(self.board.values[board]) == self.current_player):
                reward += 3
            done, winner = self.check_game_over()
            if done:
                if (winner == self.current_player): reward += 10

            self.current_player = 3 - self.current_player # switching between players
        else:
            reward -= 3
            done = False
            self.current_player = 3 - self.current_player # switching between players

        return self.get_state(), reward, done, {}

    def get_state(self):
   
        state = np.array(self.board.values)
        state = state.flatten()
        state = np.append(state, self.board.pointer)
        state = np.append(state, self.current_player)
        return state

    def check_game_over(self):

        if Board.hasWon(self.board.completed) == 0:
            return False, 0
        
        return True, Board.hasWon(self.board.completed)

    def render(self, mode='human'):
        print(self.board.values)