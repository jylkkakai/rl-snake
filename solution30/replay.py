import numpy as np
import time
from tensorflow.keras.models import load_model
from snakes import Snakes
from game_window import GameWindow

with open("best_game.txt", "r") as file:
    actions = eval(file.readline())

width = 30
height = 30
snakes = Snakes(width, height)
max_score = 0
exit = False
game_screen = GameWindow(width, height)



while not exit:
    snakes.restart(0, max_score)
    state = snakes.step(0)
    state = np.asarray(state[0])
    state = np.reshape(state, [1, 12])
    done = False
    score = 0
    for i in range(0, len(actions)):
        snakes.replay_game(actions[i][0], actions[i][1])
        score = snakes.get_score()
        if score > max_score:
            max_score = score

        exit = game_screen.draw_screen([snakes.get_snake(), snakes.get_food(), 0, score, max_score])
        time.sleep(0.01)
        if exit:
            break
