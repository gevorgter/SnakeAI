from pygame.locals import *
from random import randint
from NeutralNet import DQNAgent

import pygame
import time
import numpy as np

step = 44
boardSize = 20

LEFT = 0
DOWN=1
RIGHT = 2
UP=3

def isCollision(x1, y1, x2, y2):
    if x1 == x2 and y1 == y2:
        return True
    return False


class Apple:
    x = 0
    y = 0
    image = None

    def __init__(self, img):
        self.image = img

    def assignPosition(self, surface, snake):
        #no need to erase previous position since our snake just ate the apple
        #and head of the sneak was blit over the apple's image
        #so just assign a new position and blit it.
        bPickPosition = True
        while bPickPosition:
            self.x = randint(0, boardSize-1)
            self.y = randint(0, boardSize-1)
            bPickPosition = False
            #check if we did not end up on a snake

            for i in range(snake.length):
                if( self.x == snake.x[i] ) and (self.y == snake.y[i]):
                    bPickPosition = True
                    break

        surface.blit(self.image, (self.x*step, self.y*step))


class Player:
    x = [0]
    y = [0]
    directionX = 1 # we moving right initially
    directionY = 0
    length = 3
    image = None

    def resetPlayer(self):
        self.length = 3
        for i in range(0, 2000):
            self.x.append(-100)
            self.y.append(-100)

        # initial positions, no collision.
        self.x[0] = randint(0, boardSize-1)
        self.y[0] = randint(0, boardSize - 1)
        self.x[1] = self.x[0] + 1
        self.y[1] = self.y[0]
        self.x[2] = self.x[0] + 2
        self.y[2] = self.y[0]
        if self.x[2] > boardSize:
            self.x[1] = self.x[0] - 1
            self.x[2] = self.x[0] - 2

    def __init__(self, img):
        self.image = img
        self.resetPlayer()

    #returns 0-all the same, 1 - we ate an apple,  -2 we hit a wall, -3 we hit ourself.
    def step(self, surface, apple):
        bResult = 0
        newX = self.x[0] + self.directionX
        newY = self.y[0] + self.directionY

        if( apple.x == newX) and (apple.y == newY):
            bResult = 1
            self.length = self.length + 1
        else:
            #erase the last tail.
            x = self.x[self.length - 1] * step
            y = self.y[self.length - 1] * step
            rect = Rect(x, y, step, step)
            surface.fill((255, 255, 255), rect)

        #shift the tail
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        #remove head and paint piece of tail instead
        surface.fill((127, 127, 127), Rect(self.x[0] * step, self.y[0] * step, step, step))
        self.x[0] = newX
        self.y[0] = newY
        #paint a new head
        surface.blit(self.image, (self.x[0] * step, self.y[0] * step))

        # check if we went out of the board
        if (newX < 0) or (newX >= boardSize) or (newY < 0) or (newY >= boardSize):
            bResult = -2

        # did snake collide with itself?
        for i in range(1, self.length):
            if isCollision(newX, newY, self.x[i], self.y[i]):
                bResult = -3
                break

        return bResult

    def draw(self,surface):
        surface.blit(self.image, (self.x[0] * step, self.y[0] * step))
        for i in range(1,self.length):
            rect = Rect(self.x[0] * step, self.y[0] * step, step, step)
            surface.fill((127, 127, 127), rect)
        pass


    def setDirection(self, dirNum):
        if dirNum == 0:  #right
            self.directionX = 1
            self.directionY = 0
            return
        if dirNum == 2:  #left
            self.directionX = -1
            self.directionY = 0
            return
        if dirNum == 1:  #down
            self.directionX = 0
            self.directionY = 1
            return
        if dirNum == 3:  #up
            self.directionX = 0
            self.directionY = -1
            return


class Game:
    player = None
    apple = None
    iStep = 0
    MaxAmountOfSteps = 260

    def __init__(self):
        pass

    def initBoard(self, surface):
        rect = Rect(0, 0, step*boardSize, step*boardSize)
        surface.fill((255, 255, 255), rect)

        self.apple = Apple(pygame.image.load("apple.jpg").convert())
        self.player = Player(pygame.image.load("snakeHead.jpg").convert())
        self.apple.assignPosition(surface, self.player)
        self.player.draw(surface)
        self.iStep = 0
        pass

    def step(self, surface):
        bGameEnded = 0
        reward = 0.0

        distanceToApple =  abs(self.apple.x - self.player.x[0]) +abs(self.apple.y - self.player.y[0])
        iResult = self.player.step(surface, self.apple)
        distanceToAppleNew = abs(self.apple.x - self.player.x[0]) +abs(self.apple.y - self.player.y[0])

        if distanceToApple > distanceToAppleNew:
            reward = 1.0
        #if distanceToApple < distanceToAppleNew:
        #    reward = -1.0

        if iResult == 1:
            self.apple.assignPosition(surface, self.player) #we ate apple, assign new position
            print("Snake length: " + str(self.player.length))
            reward = 1.0
            #bGameEnded = 2  # we got ultimate reward but we do not want to reset the game

        if iResult == -2:
            print("we hit the wall")
            reward = -10.0 #we hit ourself
            bGameEnded = 1  # game has ended, reset the game

        if iResult == -3:
            print("we hit ourself")
            reward = -10.0 #we hit the wall
            bGameEnded = 1  # game has ended, reset the game

        return self.getGamesState(), reward, bGameEnded

    def setDirection(self, iDir):
        self.player.setDirection(iDir)

    def getGamesState(self):
        #state is array of 12 integers.
        #First 4 - direction in which apple relative to snake's head
        #Second 4 - distance between snake's head and wall in each direction.
        #Third 4- distance between snake's head and snake's tail in each direction
        #directions go 0 going right, 1 - going down, 2 - going left, 3 - going up
        state = [0]*12
        #First 4
        state[0 + RIGHT] = self.apple.x - self.player.x[0]
        state[0 + DOWN] = self.apple.y - self.player.y[0]
        state[0 + LEFT] = self.player.x[0] - self.apple.x
        state[0 + UP] = self.player.y[0] - self.apple.y

        #if we got negative value then apple is not in that direction. Set value to double board size
        if state[0 + RIGHT] < 0:
            state[0 + RIGHT] = 2*boardSize
        if state[0 + DOWN] < 0:
            state[0 + DOWN] = 2*boardSize
        if state[0 + LEFT] < 0:
            state[0 + LEFT] = 2*boardSize
        if state[0 + UP] < 0:
            state[0 + UP] = 2*boardSize
        #Second 4
        state[4 + RIGHT] = boardSize - self.player.x[0] - 1 #distance 0  when we next to the right wall
        state[4 + DOWN] = boardSize - self.player.y[0] - 1  # distance 0  when we next to the bottom wall
        state[4 + LEFT] = self.player.x[0] #distance 0 when we next to the left wall
        state[4 + UP] = self.player.y[0]  # distance 0 when we next to the top wall
        #Third 4
        #initialize values to something big since we are looking for minimal distance
        state[8 + RIGHT] = 2*boardSize
        state[8 + DOWN] = 2*boardSize
        state[8 + LEFT] = 2*boardSize
        state[8 + UP] = 2*boardSize

        for i in range(1, self.player.length):
            #make sure head and the tail's piece is on the same Y axle
            if self.player.y[i] == self.player.y[0]:
                #check if tail's piece on a left or on a right and set appropriate distance in that direction
                if self.player.x[i] > self.player.x[0]:
                    state[8 + RIGHT] = min(state[8 + RIGHT], self.player.x[i] - self.player.x[0])
                else:
                    state[8 + LEFT] = min(state[8 + LEFT], self.player.x[0] - self.player.x[i])

            #make sure head and the tail's piece is on the same X axle then get the minimum
            if self.player.x[i] == self.player.x[0]:
                # check if tail's piece above or bellow and set appropriate distance in that direction
                if self.player.y[i] > self.player.y[0] :
                    state[8 + DOWN] = min(state[8 + DOWN], self.player.y[i] - self.player.y[0])
                else:
                    state[8 + UP] = min(state[8 + UP], self.player.y[0] - self.player.y[i])

        #we want to normalize state, make it between 0 and 1 but we do not want 0 so we are adding 0.01
        for i in range(12):
            state[i] = (state[i]+0.01)/(boardSize+0.01)

        return state


class App:
    windowWidth = 800
    windowHeight = 600
    game = None

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.game = Game()

    def on_init(self):
        self._display_surf = pygame.display.set_mode((boardSize * step, boardSize * step), pygame.HWSURFACE)
        pygame.display.set_caption('Pygame pythonspot.com example')
        self.game.initBoard(self._display_surf)
        self._running = True

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_execute(self):
        self.on_init()
        state_size = 12
        agent = DQNAgent(state_size, 4)
        batch_size = 32
        state = self.game.getGamesState()
        #we need to reshape state to format keras expects it in.
        state = np.reshape(state, [1, state_size])

        while self._running:
            pygame.event.pump()
            keys = pygame.key.get_pressed()


            #if keys[K_RIGHT]:
            #    self.game.setDirection(0)

            #if keys[K_LEFT]:
            #    self.game.setDirection(2)

            #if keys[K_UP]:
            #    self.game.setDirection(3)

            #if keys[K_DOWN]:
            #    self.game.setDirection(1)

            if keys[K_ESCAPE]:
                agent.save()
                break

            action = agent.act(state)
            self.game.setDirection(action)
            next_state, reward, done = self.game.step(self._display_surf)

            #reward = reward if not done else -10
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state

            if len(agent.memory) > batch_size:
                agent.replay(batch_size)

            if done == 1:
                #we lost, reinitialize board
                self.game.initBoard(self._display_surf)
                state = self.game.getGamesState()
                state = np.reshape(state, [1, state_size])

            pygame.display.flip()

            #time.sleep(50.0 / 1000.0);

if __name__ == "__main__":
    pygame.init()
    theApp = App()
    theApp.on_execute()

    pygame.display.quit()
    pygame.quit()