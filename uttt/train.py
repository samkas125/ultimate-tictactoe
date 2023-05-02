from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3 import PPO
from environment import *

env = UltimateTicTacToeEnv()
env = DummyVecEnv([lambda: env])

policy_kwargs = dict(
    net_arch=[256, 256, 256, 256],
)

model = PPO("MlpPolicy", env, verbose=1, learning_rate=2.5e-3, n_steps=2048, batch_size=64, 
            n_epochs=10, gamma=0.99, gae_lambda=0.95, clip_range=0.2, ent_coef=0.005, policy_kwargs=policy_kwargs)

model.learn(total_timesteps=60_000)

model.save("models/ultimate_tic_tac_toe_ppo_final")
