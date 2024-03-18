import time

import numpy as np
from screen import GameScreen

# from random import randint
# import random
from snakes import Snakes

# from tensorflow.keras import Sequential
# from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPool2D, Dropout
# from tensorflow.keras.optimizers import Adam
# from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import load_model

game = True
width = 30
height = 30
model = load_model("model/model-3600.h5")
snakes = Snakes(width, height)
max_score = 0
counter = 0
exit = False
save_game = []
store_game = []

if game:
    game_screen = GameScreen(width, height)

while not exit and counter < 1000:
    snakes.restart(counter, max_score)
    state = snakes.step(0)
    state = np.asarray(state[0])
    state = np.reshape(state, [1, 30, 30])
    done = False
    score = 0
    store_game = []

    while not done and not exit:
        action = model.predict(state)
        food = snakes.get_food()
        state = snakes.step(np.argmax(action))
        done = state[2]
        state = np.asarray(state[0])
        state = np.reshape(state, [1, 30, 30])
        score = snakes.get_score()
        store_game.append([np.argmax(action), food])

        if score > max_score:
            max_score = score
        if game:
            exit = game_screen.draw_screen(
                [snakes.get_snake(), snakes.get_food(), counter, score, max_score]
            )
            time.sleep(0.01)
            if exit:
                break

    counter += 1
    # print("{} {}".format(len(save_game), len(store_game)))
    if len(store_game) > len(save_game):
        print(max_score)
        save_game = store_game
print("Max score: {}".format(max_score))
with open(str(max_score) + ".txt", "w") as file:
    file.write(str(save_game))
if game:
    game_screen.quit()
    exit()

