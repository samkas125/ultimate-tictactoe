import numpy as np

class UltimateTicTacToe:
    
    def __init__(self):
        self.row_count = 11
        self.column_count = 9
        self.action_size = 81

    def __repr__(self):
        return "UTTT"

    def hasWon(self, valueArray):
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

        if (valueArray[0] == -1 and valueArray[1] == -1 and valueArray[2] == -1):
            return -1
        if (valueArray[3] == -1 and valueArray[4] == -1 and valueArray[5] == -1):
            return -1
        if (valueArray[6] == -1 and valueArray[7] == -1 and valueArray[8] == -1):
            return -1
        if (valueArray[0] == -1 and valueArray[3] == -1 and valueArray[6] == -1):
            return -1
        if (valueArray[1] == -1 and valueArray[4] == -1 and valueArray[7] == -1):
            return -1
        if (valueArray[2] == -1 and valueArray[5] == -1 and valueArray[8] == -1):
            return -1
        if (valueArray[0] == -1 and valueArray[4] == -1 and valueArray[8] == -1):
            return -1
        if (valueArray[2] == -1 and valueArray[4] == -1 and valueArray[6] == -1):
            return -1
        
        if (not (0 in valueArray)) and (not (-0 in valueArray)):
            return 2

        return 0
        
    def _get_completed(self, state):
        completed_boards = [self.hasWon(i) for i in state[:9]]
        return completed_boards

    def get_initial_state(self):
        state = np.zeros((11, 9))
        state[9] = -1
        state[10] = self._get_completed(state)
        return state
    
    def get_next_state(self, state, action, player):
        board = action // 9
        cell = action % 9
        state[board, cell] = player
        state[9] = cell if (self._get_completed(state)[cell] == 0) else -1
        state[10] = self._get_completed(state)
        return state
    
    def get_valid_moves(self, state):
        valid_moves = [0 for _ in range(self.action_size)]
        completed = self._get_completed(state)
        for i in range(self.action_size):
            board = i // 9
            cell = i % 9
            if state[board, cell] != 0 or completed[board] != 0:
                continue
            if state[9, 0] == board or state[9, 0] == -1:
                valid_moves[i] = 1

        return np.array(valid_moves).astype(np.uint8)
    
    def check_win(self, state, action):
        if action == None:
            return False
        
        board = action // 9
        cell = action % 9
        player = state[board, cell]
        completed_boards = self._get_completed(state)
        return self.hasWon(completed_boards) == player
    
    def get_value_and_terminated(self, state, action):
        
        if self.check_win(state, action):
            return 1, True
        
        if self.hasWon(self._get_completed(state)) == 2 or np.sum(self.get_valid_moves(state)) == 0:
            return 0, True
        return 0, False
    
    def get_opponent(self, player):
        return -player
    
    def get_opponent_value(self, value):
        return -value
    
    def change_perspective(self, state, player):
        if state.shape == (11, 9):
            pointer = state[9, 0]
            state *= player
            state[9] = pointer
            return state
        else:
            for i in range(len(state)):
                state[i] = self.change_perspective(state[i], player)
            
            return state

    def get_encoded_state(self, state):

            if state.ndim == 3:
                pointers = []
                for i in range(len(state)):
                    pointers.append(state[i, 9, 0])
                
                encoded_state = np.stack(
                    (state == -1, state == 0, state == 1)
                ).astype(np.float32)
                if len(state.shape) == 3:
                    encoded_state = np.swapaxes(encoded_state, 0, 1)
                
                # fix pointer values
                for i in range(len(encoded_state)):
                    for j in range(len(encoded_state[i])):
                        encoded_state[i, j, 9] = pointers[i]

                return encoded_state
            else:
                pointer = state[9, 0]
                encoded_state = np.stack(
                    (state == -1, state == 0, state == 1)
                ).astype(np.float32)
                if len(state.shape) == 3:
                    encoded_state = np.swapaxes(encoded_state, 0, 1)
                for i in range(len(encoded_state)):
                    encoded_state[i, 9] = pointer
                return encoded_state
            

# class UltimateTicTacToe:
    
#     def __init__(self):
#         self.row_count = 10
#         self.column_count = 9
#         self.action_size = 81

#     def __repr__(self):
#         return "UTTT"

#     def hasWon(self, valueArray):
#         if (valueArray[0] == 1 and valueArray[1] == 1 and valueArray[2] == 1):
#             return 1
#         if (valueArray[3] == 1 and valueArray[4] == 1 and valueArray[5] == 1):
#             return 1
#         if (valueArray[6] == 1 and valueArray[7] == 1 and valueArray[8] == 1):
#             return 1
#         if (valueArray[0] == 1 and valueArray[3] == 1 and valueArray[6] == 1):
#             return 1
#         if (valueArray[1] == 1 and valueArray[4] == 1 and valueArray[7] == 1):
#             return 1
#         if (valueArray[2] == 1 and valueArray[5] == 1 and valueArray[8] == 1):
#             return 1
#         if (valueArray[0] == 1 and valueArray[4] == 1 and valueArray[8] == 1):
#             return 1
#         if (valueArray[2] == 1 and valueArray[4] == 1 and valueArray[6] == 1):
#             return 1

#         if (valueArray[0] == -1 and valueArray[1] == -1 and valueArray[2] == -1):
#             return -1
#         if (valueArray[3] == -1 and valueArray[4] == -1 and valueArray[5] == -1):
#             return -1
#         if (valueArray[6] == -1 and valueArray[7] == -1 and valueArray[8] == -1):
#             return -1
#         if (valueArray[0] == -1 and valueArray[3] == -1 and valueArray[6] == -1):
#             return -1
#         if (valueArray[1] == -1 and valueArray[4] == -1 and valueArray[7] == -1):
#             return -1
#         if (valueArray[2] == -1 and valueArray[5] == -1 and valueArray[8] == -1):
#             return -1
#         if (valueArray[0] == -1 and valueArray[4] == -1 and valueArray[8] == -1):
#             return -1
#         if (valueArray[2] == -1 and valueArray[4] == -1 and valueArray[6] == -1):
#             return -1
        
#         if (not (0 in valueArray)) and (not (-0 in valueArray)):
#             return 2

#         return 0
        
#     def _get_completed(self, state):
#         completed_boards = [self.hasWon(i) for i in state[:9]]
#         return completed_boards

#     def get_initial_state(self):
#         state = np.zeros((10, 9))
#         state[9] = -1
#         return state
    
#     def get_next_state(self, state, action, player):
#         board = action // 9
#         cell = action % 9
#         state[board, cell] = player
#         state[9] = cell if (self._get_completed(state)[cell] == 0) else -1
#         return state
    
#     def get_valid_moves(self, state):
#         valid_moves = [0 for _ in range(self.action_size)]
#         completed = self._get_completed(state)
#         for i in range(self.action_size):
#             board = i // 9
#             cell = i % 9
#             if state[board, cell] != 0 or completed[board] != 0:
#                 continue
#             if state[9, 0] == board or state[9, 0] == -1:
#                 valid_moves[i] = 1

#         return np.array(valid_moves).astype(np.uint8)
    
#     def check_win(self, state, action):
#         if action == None:
#             return False
        
#         board = action // 9
#         cell = action % 9
#         player = state[board, cell]
#         completed_boards = self._get_completed(state)
#         return self.hasWon(completed_boards) == player
    
#     def get_value_and_terminated(self, state, action):
        
#         if self.check_win(state, action):
#             return 1, True
        
#         if self.hasWon(self._get_completed(state)) == 2 or np.sum(self.get_valid_moves(state)) == 0:
#             return 0, True
#         return 0, False
    
#     def get_opponent(self, player):
#         return -player
    
#     def get_opponent_value(self, value):
#         return -value
    
#     def change_perspective(self, state, player):
#         if state.shape == (10, 9):
#             pointer = state[9, 0]
#             state *= player
#             state[9] = pointer
#             return state
#         else:
#             for i in range(len(state)):
#                 state[i] = self.change_perspective(state[i], player)
            
#             return state

#     def get_encoded_state(self, state):

#             if state.ndim == 3:
#                 pointers = []
#                 for i in range(len(state)):
#                     pointers.append(state[i, 9, 0])
                
#                 encoded_state = np.stack(
#                     (state == -1, state == 0, state == 1)
#                 ).astype(np.float32)
#                 if len(state.shape) == 3:
#                     encoded_state = np.swapaxes(encoded_state, 0, 1)
                
#                 # fix pointer values
#                 for i in range(len(encoded_state)):
#                     for j in range(len(encoded_state[i])):
#                         encoded_state[i, j, 9] = pointers[i]

#                 return encoded_state
#             else:
#                 pointer = state[9, 0]
#                 encoded_state = np.stack(
#                     (state == -1, state == 0, state == 1)
#                 ).astype(np.float32)
#                 if len(state.shape) == 3:
#                     encoded_state = np.swapaxes(encoded_state, 0, 1)
#                 for i in range(len(encoded_state)):
#                     encoded_state[i, 9] = pointer
#                 return encoded_state