import math
from random import randint


class Snakes:
    def __init__(self, width, height, episode, max_score):
        self.width = width
        self.height = height
        self.game_no = episode
        self.max_score = max_score
        self.score = 0
        self.action = 0
        self.state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.reward = 0
        self.food = [int(self.width / 2), int(self.height / 2)]
        self.snake = [[4, 10], [4, 9], [4, 8]]
        self.exit_game = False
        self.prevdist = 21

    def step(self, action):
        # prevAction = self.action
        self.action = action

        done = False
        food_found = False

        # if (
        #     (self.action == 0 and prevAction == 1)
        #     or (self.action == 1 and prevAction == 0)
        #     or (self.action == 2 and prevAction == 3)
        #     or (self.action == 3 and prevAction == 2)
        # ):
        #     self.action = prevAction

        if self.action == 0:  # right
            self.snake.insert(0, [self.snake[0][0], self.snake[0][1] + 1])
        elif self.action == 1:  # left
            self.snake.insert(0, [self.snake[0][0], self.snake[0][1] - 1])
        elif self.action == 2:  # up
            self.snake.insert(0, [self.snake[0][0] - 1, self.snake[0][1]])
        elif self.action == 3:  # down
            self.snake.insert(0, [self.snake[0][0] + 1, self.snake[0][1]])
        else:
            self.exit_game = True

        if (
            self.snake[0][0] == 0
            or self.snake[0][0] == self.width - 1
            or self.snake[0][1] == 0
            or self.snake[0][1] == self.height - 1
            or self.snake[0] in self.snake[1:]
        ):
            # print(self.snake[0])
            done = True
        else:
            if self.snake[0] == self.food:
                self.food = [randint(1, self.width - 2), randint(1, self.height - 2)]
                while self.food in self.snake:
                    self.food = [
                        randint(1, self.width - 2),
                        randint(1, self.height - 2),
                    ]
                self.score += 1
                food_found = True
            else:
                last = self.snake.pop()

            # self.print_screen()
            # print(self.snake[0])

        self.get_state()
        self.get_reward(done, food_found)

        return [self.state, self.reward, done]

    def get_snake(self):
        return self.snake

    def get_score(self):
        return self.score

    def get_food(self):
        return self.food

    def get_reward(self, done, food_found):
        reward = 0
        if done:
            self.reward = -10
        elif food_found:
            self.reward = 10
        else:
            x = self.snake[0][0] - self.food[0]
            y = self.snake[0][1] - self.food[1]
            dist = math.sqrt(pow(x, 2) + pow(y, 2))
            diff = self.prevdist - dist
            self.prevdist = dist
            # print(diff)
            if diff > 0:
                reward = 1
            self.reward = reward

    def get_state(self):
        y = self.snake[0][1]
        x = self.snake[0][0]
        self.state[0] = y
        self.state[1] = self.width - 1 - x
        self.state[2] = self.height - 1 - y
        self.state[3] = x
        self.state[4] = y - self.food[1] if y - self.food[1] >= 0 else 100
        self.state[5] = self.food[0] - x if self.food[0] - x >= 0 else 100
        self.state[6] = self.food[1] - y if self.food[1] - y >= 0 else 100
        self.state[7] = x - self.food[0] if x - self.food[0] >= 0 else 100
        self.state[8] = self.find_nearest(0)
        self.state[9] = self.find_nearest(1)
        self.state[10] = self.find_nearest(2)
        self.state[11] = self.find_nearest(3)

    def find_nearest(self, dirr):
        head = self.snake[0]
        body = self.snake[1:]
        if dirr == 0:
            for i in range(head[1], 0, -1):
                if [head[0], i] in body:
                    return head[1] - i
            return 100
        if dirr == 1:
            for i in range(head[0], self.width - 1):
                if [i, head[1]] in body:
                    return i - head[0]
            return 100
        if dirr == 2:
            for i in range(head[1], self.height - 1):
                if [head[0], i] in body:
                    return i - head[1]
            return 100
        if dirr == 3:
            for i in range(head[0], 0, -1):
                if [i, head[1]] in body:
                    return head[0] - i
            return 100
