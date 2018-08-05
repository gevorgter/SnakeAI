# SnakeAI
We are using "deep q learning" algortm that works for games where result of the move is not clear immediately.
Deep Q learning requres as to define a game's state. Basically it's a state of the board (game) at the current moment. 
Also we need to define a reward. When AI makes a move the state changes and we evelaute our new state and assign reward if our satate became better or not.

## State
We need to feed our neutral network some data. We are going to supply 12 integer numbers.
Snake can move in 4 directions Right, Down, Left, Up
First 4 are a distances between snake's head and apple in each direction
Second 4 are distances between snake's head and wall in each direction
Thrid 4 are distances between snake's head and snake itself (closed piece of tail) in eacxh direction

##Reward
1. By default reward = 0. 
2. If we became closer to apple reward = 1 if further from apple reward = -1
3. if we are the apple reward = 1. (Pretty much same as we just become closer to apple). We might want to increase it but practice showed that it's not needed
4. If we hit ourself reward = -10
5. If we hit the wall reward = -10.


