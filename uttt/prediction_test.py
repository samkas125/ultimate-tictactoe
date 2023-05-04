from environment import UltimateTicTacToeEnv
from stable_baselines3 import DQN, PPO

model = PPO.load("models/ultimate_tic_tac_toe_dqn_final")

env = UltimateTicTacToeEnv()
state = env.reset()
done = False
while not done:
    action, _ = model.predict(state)
    print(env.action_space)
    print(env.board.valid_moves)
    print(int(action) in list(env.board.valid_moves.values()))
    state, reward, done, info = env.step(action)
    env.render()
