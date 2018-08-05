# SnakeAI
We are using "deep q learning" algortm that works for games where result of the move is not clear immediately.

## State
We need to feed our neutral network some data. We are going to supply 12 integer numbers.
Snake can move in 4 directions Right, Down, Left, Up
First 4 are a distances between snake's head and apple in each direction
Second 4 are distances between snake's head and wall in each direction
Thrid 4 are distances between snake's head and snake itself (closed piece of tail) in eacxh direction
