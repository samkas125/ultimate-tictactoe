import numpy as np
from additional.game_env import UltimateTicTacToe

win_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), # rows
                    (0, 3, 6), (1, 4, 7), (2, 5, 8), # columns
                    (0, 4, 8), (2, 4, 6)] # diagonals
avg_win_score = 15
UTTT = UltimateTicTacToe()

def net_num_2_row(board):
    net_2_row = 0
    for combination in win_combinations:
        if (board[combination[0]] + board[combination[1]] + board[combination[2]]) == 2:
            net_2_row += 1
        if (board[combination[0]] + board[combination[1]] + board[combination[2]]) == -2:
            net_2_row -= 1

    return net_2_row
        
def evaluate(state):
    score = 0
    completed = UTTT._get_completed(state)
    _completed = [0 if i == 2 else i for i in completed]
    score += 32 * np.sum(_completed)
    score += 16 * net_num_2_row(_completed)
    for i in range(9):
        if completed[i] == 0:
            score += 2 * np.sum(state[i])
            net_2_row = net_num_2_row(state[i])
            score += 1 * net_2_row

    winner = 0 if UTTT.hasWon(completed) == 2 else UTTT.hasWon(completed)
    score += winner * 1000
    return score

    # Attempt to normalize score between 0 and 1
    score = float(score)
    score = (score / avg_win_score + 1)/2

    return max(min(score, 1), 0)

def evaluate_policy(state):
    valid_moves = UTTT.get_valid_moves(state)
    policy = [0 for _ in range(81)]
    for i in range(81):
        if (valid_moves[i] == 0): 
            continue
        state_next = UTTT.get_next_state(state.copy(), i, 1)
        policy[i] = evaluate(state_next)

    if (policy[i] == 0 for i in range(81)):
        policy = valid_moves

    return np.array(policy, dtype=np.float32)


def minimax(state, depth, is_maximizing):
    
    if (depth == 0 or UTTT.hasWon(UTTT._get_completed(state)) != 0):
        return evaluate(state), None

    valid_moves = UTTT.get_valid_moves(state)
    possible_actions = [i for i in range(81) if valid_moves[i] == 1]
    best_action = None

    if is_maximizing:
        best_score = -float('inf')
        for action in possible_actions:
            next_state = UTTT.get_next_state(state.copy(), action, 1)

            score, _ = minimax(next_state, depth - 1, False)
            
            if (score > best_score):
                best_score = score
                best_action = action
        return best_score, best_action
    else:
        best_score = float('inf')
        for action in possible_actions:
            next_state = UTTT.get_next_state(state.copy(), action, -1)

            score, _ = minimax(next_state, depth - 1, True)
            
            if (score < best_score):
                best_score = score
                best_action = action
        return best_score, best_action

def minimax_alphabeta(state, depth, is_maximizing_player, alpha, beta):
    if (depth == 0 or UTTT.hasWon(UTTT._get_completed(state)) != 0):
        return evaluate(state), None

    possible_actions = UTTT.get_valid_moves(state)
    possible_actions = [i for i in range(81) if possible_actions[i] == 1]

    if is_maximizing_player:
        best_score = float('-inf')
        best_action = None
        for action in possible_actions:
            next_state = UTTT.get_next_state(state.copy(), action, 1)
            score, _ = minimax_alphabeta(next_state, depth - 1, False, alpha, beta)
            if score > best_score:
                best_score = score
                best_action = action
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score, best_action
    else:
        best_score = float('inf')
        best_action = None
        for action in possible_actions:
            next_state = UTTT.get_next_state(state.copy(), action, -1)
            score, _ = minimax_alphabeta(next_state, depth - 1, True, alpha, beta)
            if score < best_score:
                best_score = score
                best_action = action
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score, best_action