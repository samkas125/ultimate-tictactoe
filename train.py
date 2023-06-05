import torch
torch.manual_seed(0)
from additional.game_env import *
from additional.resnet import *
from additional.alphazero import *

game = UltimateTicTacToe()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

model = ResNet(game, 9, 128, device)
model.load_state_dict(torch.load("models/model_9_UTTT.pt", map_location=device))

optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=0.0001)

args = {
    'C': 2,
    'num_searches': 1500,
    'num_iterations': 8,
    'num_selfPlay_iterations': 100,
    'num_parallel_games': 25,
    'num_epochs': 4,
    'batch_size': 128,
    'temperature': 1.0,
    'dirichlet_epsilon': 0.05,
    'dirichlet_alpha': 0.3
}

alphaZero = AlphaZeroParallel(model, optimizer, game, args)
alphaZero.learn()