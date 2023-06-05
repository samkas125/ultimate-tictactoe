import matplotlib.pyplot as plt
from game_env import UltimateTicTacToe
import torch
from resnet import *

game = UltimateTicTacToe()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

state = game.get_initial_state()
state = game.get_next_state(state, 0, 1)
state = game.get_next_state(state, 4, -1)



encoded_state = game.get_encoded_state(state)

tensor_state = torch.tensor(encoded_state, device=device).unsqueeze(0)

model = ResNet(game, 9, 128, device=device)
model.load_state_dict(torch.load('../models/model_2_UTTT.pt', map_location=device))
model.eval()

policy, value = model(tensor_state)
value = value.item()
policy = torch.softmax(policy, axis=1).squeeze(0).detach().cpu().numpy()

print(value)

print(state)
print(tensor_state)

plt.bar(range(game.action_size), policy)
plt.show()