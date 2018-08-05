# SnakeAI
Packages used: Keras (with TensorFlow), numpy, pygame

We are using "deep Q-learning" algortm that works for games where result of the move is not clear immediately.
Deep Q-learning requres us to define a game's state. Basically it's a state of the board (game) at the current moment. 
Also we need to define a reward. When AI makes a move the state changes and we evelaute our new state and assign reward if our state became better or not.
I found good explanation of "deep Q-learning" here: https://keon.io/deep-q-learning/

## State.
We need to feed our neutral network some data. We are going to supply 12 numbers.<br>
Snake can move in 4 directions Right, Down, Left, Up.<br>
First 4 are a distances between snake's head and apple in each direction.<br>
Second 4 are distances between snake's head and wall in each direction.<br>
Thrid 4 are distances between snake's head and snake itself (closed piece of tail) in each direction.<br>

Also, we do not want to have 0 (zeroes) in our state. Zeroes are bad since any weight multiply by 0 will be 0. And we do not want big numbers either. So we will normalize out state by adding 0.01 (avoiding 0) and divide distances by boardisze. 
## Reward.
1. By default reward = 0. 
2. If we became closer to apple reward = 1. We will not punish ourself to become further from the apple. I discovered that if we do the snake going to try to cross itself in order to get closer to apple rathen than go around.
3. if we ate the apple reward = 1. (Pretty much same as we just become closer to apple). We might want to increase it but practice showed that it's not needed
4. If we hit ourself reward = -10
5. If we hit the wall reward = -10.

## The Neutral network.
Output of the network will be  One-Hot encoded. So output 4 neuron with each neuron showing Right, Down, Left and Top direction.
The Input will be our State obviously. 12 Neurons.
If we look at our State data we will see that we have 3 independent components. Basically First part (4 neurons) define direction we will go to. And Second and Third part will tell us direction in which we can not move. Hence it looks like our Network hidden layers have to be dividable by 3. So we picked 2 layers. 24 and 12 Neurons. I did experiment with just one hidden layer that had 12 Neurons and result were not bad at all and network was much faster. 


## The code. 
There are 2 source files, couple of .jpg files to make it pretty and weight file if you do not want to train from scracth.
main.py is the game and NeuralNet.py is the network.

## Problems. 
Our network doing very good at getting those apples and not hitting wals.<br>
Problem is that sometimes Snake would try to cross itself when going for an apple. Ideally it should not cross itself untill it boxed itself in. 
My theory is that network gets 15-20 succesfull moves by getting closer to apple and only 1 bad move when it hits itself. So Network learned quickly how to get an apple and more training needed for Network to learn not to cross itself. Another solution might be to start penalizing for getting closer to own body.

