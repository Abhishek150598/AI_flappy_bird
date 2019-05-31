# ABSTRACT

The idea of this project is to create a clone of the popular mobile game, Flappy Birds and train an AI bot to play the game. The game is available in 2 modes- human mode and AI mode.

# LANGUAGES/TECHNOLOGIES USED

- Python
- Pygame

# ALGORITHMS USED

## DESIGNING THE GAME

## DESIGNING THE BOT

The bot uses a popular values-based reinforcemt learning algorithm known as Q learning. For every frame in the game loop, we define a state space and an action space.
The state space is given by the following three variables :
- The horizontal distance between bird and pipe (Assuming 10 pixels as 1 unit for faster training)
- The vertical distance between bird and end of top pipe (Assuming 10 pixels as 1 unit for faster training)
- Vertical velocity of the bird

The action space is given by :
- To jump
- To do nothing

For each state-action pair, we assign a Q- value which is initially zero. Based on the bird's performance we assign certain reward/penalty to each state-action pair based on its outcome.
The rewards are :
- +1 for survival
- -1000 for death

After each death, the Q values of each state-action pair encuntered is updated as follows
