from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3 import PPO, DQN
from environment import *

env = UltimateTicTacToeEnv()
env = DummyVecEnv([lambda: env])

# policy_kwargs = dict(
#     net_arch=dict(pi=[83, 256, 256, 256, 81], vf=[83, 256, 256, 256, 81]),)

policy_kwargs = dict(
    net_arch=[83, 256, 256, 256, 256, 81])

# model = PPO("MlpPolicy", env, verbose=1, learning_rate=2.5e-3, n_steps=2048, batch_size=64, 
#             n_epochs=10, gamma=0.99, gae_lambda=0.95, clip_range=0.2, ent_coef=0.005, policy_kwargs=policy_kwargs, device="cuda", action_noise=action_noise, exploration_fraction=0.1, exploration_initial_eps=1.0,)

# model = DQN("MlpPolicy", env, verbose=1, learning_rate=2.5e-3, policy_kwargs=policy_kwargs, device='cuda')
model = DQN("MlpPolicy", env, verbose=1, learning_rate=2.5e-3, policy_kwargs=policy_kwargs, device='cuda', 
            exploration_fraction=0.5, exploration_initial_eps=2.0, exploration_final_eps=0.7)

model.learn(total_timesteps=20_000)

model.save("models/ultimate_tic_tac_toe_dqn_final")
