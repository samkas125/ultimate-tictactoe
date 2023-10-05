<h1 align="center">Ultimate Tic-Tac-Toe</h1> 

### What is Ultimate Tic-Tac-Toe?

Ultimate Tic-Tac-Toe is an expanded form of Tic-Tac-Toe that is played on a 9x9 board. It consists of a 3x3 grid of large squares, that each individually have a 3x3 grid of small cells within them. In this way, the game of Tic-Tac-Toe is played both on individual boxes, as well as on the overall board. You can view the full rules [here](https://mathwithbaddrawings.com/2013/06/16/ultimate-tic-tac-toe/).

This is a python project that allows a user to play Ultimate Tic-Tac-Toe against another player or against a reinforcement learning agent. After trying various reinforcement learning approaches such as Deep Q-Networks and Proximal Policy Optimization, the [Monte Carlo Tree Search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search) algorithm was used alongside the AlphaZero approach for reinforcement learning. The implementation of AlphaZero was adapted from [`AlphaZeroFromScratch`](https://github.com/foersterrobert/AlphaZeroFromScratch).

### AlphaZero

AlphaZero is a game engine developed by DeepMind (subsidiary of Google) to master the ancient Chinese game of [Go](https://en.wikipedia.org/wiki/Go_(game)). Due to it having a generalized approach and not requiring domain specific knowledge, it can be easily applied to other two player complete-information board games (like chess and shogi).

It makes use of `policy` and `value` neural networks to evaluate the best moves in each position (policy) and the relative advantage each of the players has (value). These neural networks are used in accordance with the MCTS search algorithm, where board positions are represented as nodes of a tree.

### MCTS + Neural Networks in AlphaZero

The MCTS algorithm is slightly modified in AlphaZero to consider the information provided by the `value` and `policy` networks in its expansion and backpropagation phases. Specifically, nodes with higher policies are preferred in expansion, and the simulation phase is replaced with the `value` of the leaf node. 

<p align="center" width="100%">
    <img src="https://github.com/samkas125/ultimate-tictactoe/assets/101554474/3b0017da-5b1c-479c-8229-310fee38357a"> 
</p>


### How to run
- Run `pvp.py` to play against another local player.
- Run `pvAlphaZero.py` to play against RL agent.

### Dependencies: `requirements.txt`
- PyGame
- PyTorch
- MatPlotLib
- numpy
- tqdm

### Screenshots

<p align="center" width="100%">
    <img src="https://user-images.githubusercontent.com/101554474/235619968-23c7c257-96b3-4d11-812c-2207f2936b0f.png"> 
</p>

<p align="center" width="100%">
    <img src="https://github.com/samkas125/ultimate-tictactoe/assets/101554474/462efaf6-8a97-46f6-917e-0bacacf32f02"> 
</p>





