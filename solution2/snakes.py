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
        self.state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.reward = 0
        self.food = [int(self.width / 2), int(self.height / 2)]
        self.snake = [[4, 10], [4, 9], [4, 8]]
        self.exit_game = False
        self.prevdist = 21
        self.direction = [2, 3, 0]  # left, straight, right

    def step(self, action):
        prevAction = self.action
        self.action = action

        if action == 0:  # left
            self.direction[0] = (self.direction[0] - 1) % 4
            self.direction[1] = (self.direction[1] - 1) % 4
            self.direction[2] = (self.direction[2] - 1) % 4
        elif action == 2:  # right
            self.direction[0] = (self.direction[0] + 1) % 4
            self.direction[1] = (self.direction[1] + 1) % 4
            self.direction[2] = (self.direction[2] + 1) % 4

        done = False
        food_found = False

        if self.direction[1] == 0:  # west
            self.snake.insert(0, [self.snake[0][0], self.snake[0][1] - 1])
        elif self.direction[1] == 1:  # north
            self.snake.insert(0, [self.snake[0][0] - 1, self.snake[0][1]])
        elif self.direction[1] == 2:  # east
            self.snake.insert(0, [self.snake[0][0], self.snake[0][1] + 1])
        elif self.direction[1] == 3:  # south
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
            self.reward = -20
        elif food_found:
            self.reward = 5
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
        # y = self.snake[0][1]
        # x = self.snake[0][0]
        self.state[0] = self.dist_to_edge(self.direction[0])
        self.state[1] = self.dist_to_edge(self.direction[1])
        self.state[2] = self.dist_to_edge(self.direction[2])
        self.state[3] = self.dist_to_apple(self.direction[0])
        self.state[4] = self.dist_to_apple(self.direction[1])
        self.state[5] = self.dist_to_apple(self.direction[2])
        self.state[6] = self.find_nearest(self.direction[0])
        self.state[7] = self.find_nearest(self.direction[1])
        self.state[8] = self.find_nearest(self.direction[2])

    def dist_to_edge(self, dirr):
        y = self.snake[0][1]
        x = self.snake[0][0]
        if dirr == 0:  # west
            return x
        elif dirr == 1:
            return y
        elif dirr == 2:
            return self.width - 1 - x
        else:
            return self.height - 1 - y

    def dist_to_apple(self, dirr):
        y = self.snake[0][1]
        x = self.snake[0][0]
        if dirr == 0:
            return x - self.food[0] if self.food[0] - x >= 0 else 100
        elif dirr == 1:
            return y - self.food[1] if y - self.food[1] >= 0 else 100
        elif dirr == 2:
            return self.food[0] - y if x - self.food[0] >= 0 else 100
        else:
            return self.food[1] - y if self.food[1] - y >= 0 else 100

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
