import pygame
from pygame import Rect
import time

class GameScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.white = (255,255,255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.grey = (155, 155, 155)
        self.block = 10

        pygame.init()
        self.screen = pygame.display.set_mode((self.width*self.block, (self.height+2)*self.block))
        self.screen.fill(self.black)
        pygame.display.set_caption('Snake')
        pygame.draw.rect(self.screen, self.grey, (0, self.height*self.block, self.width*self.block, self.block*2)) 
        pygame.display.update()



    def draw_screen(self, state):
        exit = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #self.quit()
                exit = True
        self.screen.fill(self.black)
        for block in state[0]:
            pygame.draw.rect(self.screen, self.white, (block[0]*self.block, block[1]*self.block, self.block, self.block))
        
        pygame.draw.rect(self.screen, self.red, (state[1][0]*self.block, state[1][1]*self.block, self.block, self.block))
        
        self.add_text('Epoch: ' + str(state[2]), (5, self.height*self.block+5))
        self.add_text('Score: ' + str(state[3]), (110, self.height*self.block+5))
        self.add_text('Max score: ' + str(state[4]), (180, self.height*self.block+5))
        pygame.display.update()
        return exit

    def add_text(self, input, pos):
        font=pygame.font.Font(None,20)
        scrtext=font.render(str(input), 1,(255,255,255))
        self.screen.blit(scrtext, pos)

    

    def quit(self):
        pygame.display.quit()
        pygame.quit()
        exit()

