import random
import numpy as np
import os
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam


class DQNAgent:

    def __init__(self, state_size, action_size):
        self.fileName = "C:\\Projects\\SnakeAI\\snake.h5"
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        self.model = Sequential()
        self.model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        self.model.add(Dense(12, activation='relu'))
        self.model.add(Dense(self.action_size, activation='softmax'))
        self.model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        self.load()
        pass

    def load(self):

        if os.path.exists(self.fileName):
            self.model.load_weights(self.fileName)
            self.epsilon = 0.0001

        for layer in self.model.layers:
            h = layer.get_weights()
            #print(h)

    def save(self):
        for layer in self.model.layers:
            h = layer.get_weights()
            #print(h)

        self.model.save_weights(self.fileName)

    def remember(self, state, action, reward, next_state, done):
            self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            print("Random move, epsilot:" + str(self.epsilon))
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if done == 0:
                tmp = self.model.predict(next_state)
                target = reward + self.gamma * np.amax(tmp[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay