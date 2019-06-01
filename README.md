# ABSTRACT

The idea of this project is to create a clone of the popular mobile game, Flappy Birds and train an AI bot to play the game. The game is available in 2 modes- human mode and AI mode.

![Screenshot](https://github.com/Abhishek150598/AI_flappy_bird/blob/master/screenshot.png)

# LANGUAGES/TECHNOLOGIES USED

- Python
- Pygame

# ALGORITHMS USED

### DESIGNING THE GAME

The bird follows kinematics equation of free fall and each time the spacebar is clicked, an upward force is applied. The pipe gaps are randomly generated (initially 3 random values are generated in a list, when a pipe goes out of display the first random variable gets popped and a new one gets pushed to the list).

### DESIGNING THE BOT

The bot uses a popular values-based reinforcement learning algorithm known as Q learning. For every frame in the game loop, we define a state space and an action space.
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

After each death, the Q values of each state-action pair encuntered is updated as per the given formula

```python
qvalues[state][act] = (1-step_size) * (qvalues[state][act]) + step_size * ( cur_reward + discount*max(qvalues[res_state]) )
```

where:
- step-size = 0.7
- discount = 1
- res_state is the state resulting from that state-action pair
- cur_reward is the current reward assigned to the state-action pair

# PERFORMANCE

The bot has been extremely slow and inconsistent in the beginning, due to my constant experiment with the learning parameters.
However, once I finalised my algorithm it has shown an excellent growth in average score. Here is the score distribution after 1000 iterations.
![Iteration vs score](https://github.com/Abhishek150598/AI_flappy_bird/blob/master/score_plot.png)

# REFERENCES

- https://github.com/chncyhn/flappybird-qlearning-bot
- https://www.youtube.com/watch?v=ujOTNg17LjI&list=PLQVvvaa0QuDdLkP8MrOXLe_rKuf6r80KO
