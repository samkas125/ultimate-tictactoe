from environment import *
from train_dqn import DQN_Solver, Network
import torch

saved_params = torch.load("models/agent.pth")
agent = DQN_Solver()
agent.network = Network(saved_params=saved_params['model_state_dict'])

env = UltimateTicTacToeEnv()
state = env.reset()
done = False
moves = 0
while not done:
    moves += 1
    action = agent.choose_action(state)
    print(env.action_space)
    print(env.board.valid_moves)
    print(int(action) in env.board.valid_moves)
    print(moves)
    state, reward, done, info = env.step(action)
    done = False
    env.render()
    if Board.hasWon(env.board.completed) != 0:
        done = True
        print(env.check_game_over()[1]) # winner
