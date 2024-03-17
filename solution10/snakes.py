#import curses
#from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
import math

class Snakes:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        #self.restart()

    def restart(self, episode, max_score):
        self.game_no = episode
        self.max_score = max_score
        self.score = 0
        self.action = 0
        self.state = [[0 for i in range(30)] for i in range(30)]
        self.reward = 0
        self.food = [int(self.width/2),int(self.height/2)]
        self.snake = [[4, 10], [4, 9], [4,8]]
        #self.food = [randint(2, self.width-3),randint(2, self.height-3)]
        #self.snake = [[randint(2, self.width-3), randint(2, self.height-3)]]
        self.exit_game = False
        self.prevdist = 21
        self.replay = False

    def empty(self):
        temp =  []
        state = []
        for i in range(0, 30):
            for j in range(0, 30):
                temp.append(0)
            state.append(temp)
        return state

    def step(self, action):
        prevAction = self.action
        self.action = action

        done = False
        food_found = False  

        if self.action == 0:# right
                self.snake.insert(0, [self.snake[0][0], self.snake[0][1]+1])
        elif self.action == 1:# left
                self.snake.insert(0, [self.snake[0][0], self.snake[0][1]-1])
        elif self.action == 2:# up
                self.snake.insert(0, [self.snake[0][0]-1, self.snake[0][1]])
        elif self.action == 3:# down
                self.snake.insert(0, [self.snake[0][0]+1, self.snake[0][1]])
        else:
            self.exit_game = True  


        self.state[self.snake[0][0]][self.snake[0][1]] = 5
        for piece in self.snake[1:]:
           self.state[piece[0]][piece[1]] = 1


        if self.snake[0][0] == 0 or self.snake[0][0] == self.width-1 or self.snake[0][1] == 0 or self.snake[0][1] == self.height-1 or self.snake[0] in self.snake[1:]:
            #print(self.snake[0])
            done = True
        else:
            if self.snake[0] == self.food:
                if not self.replay:
                    self.food = [randint(1,self.width-2), randint(1,self.height-2)]
                    while self.food in self.snake:
                        self.food = [randint(1,self.width-2), randint(1,self.height-2)]
                        self.state[self.food[0]][self.food[1]] = 10
                self.score += 1
                food_found = True
            else:
                self.state[self.snake[-1][0]][self.snake[-1][1]] = 0
                last = self.snake.pop()

            #self.print_screen()
            #print(self.snake[0])

        #self.get_state()
        #print(self.state)
        self.get_reward(done, food_found)

        return [self.state, self.reward, done]

    def replay_game(self, action, food):
        self.replay = True
        self.food = food
        self.step(action)

    def get_snake(self):
        return self.snake

    def get_score(self):
        return self.score

    def get_food(self):
        return self.food

    def get_reward(self, done, food_found):
        reward = 0
        if done:
            self.reward =  -10
        elif food_found:
            self.reward = 10
        else:
            x = self.snake[0][0] - self.food[0]
            y = self.snake[0][1] - self.food[1]
            dist = math.sqrt(pow(x, 2) + pow(y, 2))
            diff = self.prevdist - dist
            self.prevdist = dist
            #print(diff)
            if diff > 0:
                reward = 1           
            self.reward = reward

    def get_state(self):
        self.state[self.food[0]][self.food[1]] = 10
        #print(self.snake)
        self.state[self.snake[0][0]][self.snake[0][1]] = 5
        for piece in self.snake[1:]:
           self.state[piece[0]][piece[1]] = 1

    def find_nearest(self, dirr):
        head = self.snake[0]
        body = self.snake[1:]
        if dirr == 0:
            for i in range(head[1], 0, -1):
                if [head[0], i] in body:
                    return head[1] - i
            return 100
        if dirr == 1:
            for i in range(head[0], self.width-1):
                if [i, head[1]] in body:
                    return i - head[0] 
            return 100
        if dirr == 2:
            for i in range(head[1], self.height-1):
                if [head[0], i] in body:
                    return i - head[1]
            return 100
        if dirr == 3:
            for i in range(head[0], 0, -1):
                if [i, head[1]] in body:
                    return head[0] - i
            return 100
                
                 
