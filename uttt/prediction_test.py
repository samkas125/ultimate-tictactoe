from environment import UltimateTicTacToeEnv
from stable_baselines3 import DQN, PPO

model = PPO.load("models/ultimate_tic_tac_toe_ppo_final")

env = UltimateTicTacToeEnv()
state = env.reset()
done = False
moves = 0
while not done:
    action, _ = model.predict(state)
    print(env.action_space)
    print(env.board.valid_moves)
    print(int(action) in list(env.board.valid_moves.values()))
    board = action // 9
    square = action % 9
    state, reward, done, info = env.step(action)
    env.render()
    moves += 1
    print(moves)
