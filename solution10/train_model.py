
#from PIL import ImageGrab
import numpy as np
import time
#import cv2 as cv
from collections import deque
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPool2D, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import load_model
from random import randint
import random
from snakes import Snakes
from screen import GameScreen

class DQNAgent:
    def __init__(self, state_size, action_size, prev_epochs, epsilon):
        self.state_size = state_size
        self.action_size = action_size
        self.prev_epochs = prev_epochs
        self.memory = deque(maxlen=1000)
        self.gamma = 0.95    # discount rate 
        self.epsilon_decay = 0.999
        self.epsilon = epsilon# exploration rate
        self.epsilon_min = 0.2
        self.learning_rate = 0.001
        self.counter = 0
        self.callbacks = []
        self.model = self._build_model()
        
        #print(self.epsilon)

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        if not self.prev_epochs > 0:
            model = Sequential()
            model.add(Conv2D((16), kernel_size=(8,8), strides=4, padding="same", activation="relu", input_shape=(30, 30, 1)))
            model.add(Conv2D((32), kernel_size=(4,4), strides=2, padding="same", activation="relu"))
            model.add(Conv2D((64), kernel_size=(3,3), strides=1, padding="same", activation="relu"))
            model.add(Flatten())
            model.add(Dense(128, activation="relu"))
            model.add(Dense(self.action_size, activation='linear'))
            model.compile(loss='mse',
                        optimizer=Adam(lr=self.learning_rate))
        else:
            model = load_model('model/model-' + str(self.prev_epochs) + '.h5')
            self.counter = self.prev_epochs
        
        model.summary()
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        #print(self.epsilon)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        
        for state, action, reward, next_state, done in minibatch:
            
            target = reward
            if not done:
                target = reward + self.gamma * \
                       np.amax(self.model.predict(next_state)[0])
                
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)#, callbacks=self.callbacks)#, callbacks=self.callbacks_list)
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        self.counter += 1
        if self.counter%1000 == 0:
            self.model.save("model/model-" + str(self.counter) + ".h5")
        

def write_log(filename, log):
    with open(filename, 'a') as file:
        file.write(log)

#########################################################
#                       MAIN                            #
#########################################################
game = True # False to disable the game screen rendering
game_screen = None
prev_epochs = 0 # If training is continued from pretrained saved model
epsilon = 0.1 # Initial exploration rate


exit = False
width = 30 # Game field dimensions
height = 30
episodes = prev_epochs + 10000 # Number of epochs is trained
batch_size = 32
state_size = (30, 30)
action_size = 4
max_score = 0
counter = 0
if game:
    game_screen = GameScreen(width, height)
agent = DQNAgent(state_size, action_size, prev_epochs, epsilon)
snakes = Snakes(width, height)

for e in range(prev_epochs ,episodes):
    done = False
    snakes.restart(e, max_score)
    state, reward, done = snakes.step(0)
    state = np.asarray(state)
    state = np.reshape(state, [1, 30, 30, 1])
    sum_reward = 0
    steps = 0
    step_counter = 0
    while True or not exit:
        action = agent.act(state)
        next_state, reward, done = snakes.step(action)
        score = snakes.get_score()
        if score > max_score:
            max_score = score
        if game:
            exit = game_screen.draw_screen([snakes.get_snake(), snakes.get_food(), e, score, max_score])
            #time.sleep(0.05)
            if exit:
                break

        next_state = np.asarray(next_state)
        next_state = np.reshape(next_state, [1, 30, 30, 1])
        if reward > 1:
            steps = 0
        sum_reward = sum_reward + reward
        agent.remember(state, action, reward, next_state, done)
        state = next_state
        score = snakes.get_score()

        counter = counter + 1
        if done or steps > 200:
            print("episode: {}/{}, iterations: {}, reward_sum: {}, score: {}".format(e, episodes, step_counter, sum_reward, score))
            break
        steps += 1
        step_counter += 1
    
    if len(agent.memory) > batch_size:
        agent.replay(batch_size)
    write_log('log.csv', str(e+1) + ';' + str(score) + '\n')
    if exit:
        break
print("Max score: {}".format(max_score) )
if game:
    game_screen.quit()
    exit()