#Apple class
#For Very Bad Snake
from config import *
import random
class Apple:
    def __init__(self):
        self.position = [10,10]
        
    def getX(self):
        return self.position[0]
    
    def getY(self):
        return self.position[1]
    
    def getPos(self):
        return self.position
        
    def regrow(self, snake_body):
        new_pos = [random.randint(0,BOARD_WIDTH - 1),random.randint(0,BOARD_HEIGHT - 1)]
        while new_pos in snake_body:
            new_pos = [random.randint(0,BOARD_WIDTH - 1),random.randint(0,BOARD_HEIGHT - 1)]
        self.position = new_pos
        return