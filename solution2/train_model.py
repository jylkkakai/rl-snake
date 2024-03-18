# from PIL import ImageGrab
import random
import time

# import cv2 as cv
from collections import deque
from statistics import mean

import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential

# from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import Conv2D, Dense, Dropout, Flatten, MaxPool2D
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam

from screen import GameScreen
from snakes import Snakes

# from random import randint


class DQNAgent:
    def __init__(self, state_size, action_size, prev_epochs, epsilon):
        self.state_size = state_size
        self.action_size = action_size
        self.prev_epochs = prev_epochs
        self.memory = deque(maxlen=100)
        self.gamma = 0.95  # discount rate
        self.epsilon_decay = 0.995
        self.epsilon = epsilon  # exploration rate
        self.epsilon_min = 0.001
        self.learning_rate = 0.001
        self.counter = 0
        self.callbacks = []
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        mse = tf.keras.losses.MeanSquaredError()

        if not self.prev_epochs > 0:
            model = Sequential()
            model.add(Dense(24, activation="relu", input_shape=(self.state_size,)))
            model.add(Dense(24, activation="relu"))
            model.add(Dense(self.action_size, activation="linear"))
            model.compile(loss=mse, optimizer=Adam(learning_rate=self.learning_rate))
            # model.summary()
        else:
            # del model
            model = load_model("model/model-" + str(self.prev_epochs) + ".keras")
            # self.epsilon = 0.05
            self.counter = self.prev_epochs
            self.epsilon = self.epsilon * self.epsilon_decay**self.counter
        model.summary()

        # model_checkpoint = ModelCheckpoint('model/model-{epoch:02d}-{loss:.2f}.hdf5', monitor='loss', save_best_only=True)
        # self.callbacks.append(model_checkpoint)
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        # print(self.epsilon)
        act_values = self.model.predict(state, verbose=0)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)

        for state, action, reward, next_state, done in minibatch:

            target = reward
            if not done:
                target = reward + self.gamma * np.amax(
                    self.model.predict(next_state, verbose=0)[0]
                )

            target_f = self.model.predict(state, verbose=0)
            target_f[0][action] = target
            self.model.fit(
                state, target_f, epochs=1, verbose=0
            )  # , callbacks=self.callbacks)#, callbacks=self.callbacks_list)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        else:
            self.epsilon = 0.5
            self.model.save("model/model-" + str(self.counter) + ".keras")
            self.learnin_rate *= 0.5

        self.counter += 1
        if self.counter % 100 == 0:
            self.model.save("model/model-" + str(self.counter) + ".keras")

    def get_eps(self):
        return self.epsilon

    def get_lr(self):
        return self.learning_rate


def write_log(filename, log):
    with open(filename, "a") as file:
        file.write(log)


#########################################################
#                       MAIN                            #
#########################################################
game = True  # False to disable the game screen rendering
game_screen = None
prev_epochs = 0  # If training is continued from pretrained saved model
epsilon = 0.50  # Initial exploration rate


exit = False
width = 30  # Game screen dimensions
height = 30
episodes = prev_epochs + 10000  # Number of epochs is trained
batch_size = 8
state_size = 9
action_size = 3
max_score = 0
avg_score = 0.0
scores = deque(maxlen=100)
counter = 0
if game:
    game_screen = GameScreen(width, height)
agent = DQNAgent(state_size, action_size, prev_epochs, epsilon)

for e in range(prev_epochs, episodes):
    done = False
    snakes = Snakes(width, height, e, max_score)
    state, reward, done = snakes.step(0)
    state = np.asarray(state)
    state = np.reshape(state, [1, state_size])
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
            exit = game_screen.draw_screen(
                [snakes.get_snake(), snakes.get_food(), e, score, max_score]
            )
            time.sleep(0.05)
            if exit:
                break

        next_state = np.asarray(next_state)
        next_state = np.reshape(next_state, [1, state_size])
        if reward > 1:
            steps = 0
        sum_reward = sum_reward + reward
        agent.remember(state, action, reward, next_state, done)
        state = next_state
        score = snakes.get_score()

        counter = counter + 1
        if done or steps > 200:
            scores.append(score)
            avg_score = mean(scores)
            print(
                "episode: {}/{}, iters: {}, reward_sum: {}, score: {}, avg_score: {:.2f}, eps: {:.5f}, lr: {:.5f}".format(
                    e,
                    episodes,
                    step_counter,
                    sum_reward,
                    score,
                    avg_score,
                    agent.get_eps(),
                    agent.get_lr(),
                )
            )
            break
        steps += 1
        step_counter += 1

    if len(agent.memory) > batch_size:
        agent.replay(batch_size)
    write_log("log.csv", "{};{};{:.5f}\n".format(e + 1, score, avg_score))
    # write_log("log.csv", str(e + 1) + ";" + str(score) + ";" + str(avg_score) + "\n")
    if exit:
        break
print("Max score: {}".format(max_score))
if game:
    game_screen.quit()
    exit()
