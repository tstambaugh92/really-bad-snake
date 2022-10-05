#Snake class
#For Very Bad Snake
from config import *
class Snake:
    def __init__(self):
        self.body = [[0,0]]
        self.direction = 'E'
        self.is_dead = False
        self.move_delay = 5
        self.max_move_delay = 5
        self.eaten = False
    
    def getBody(self):
        return self.body
    
    def getHead(self):
        return self.body[0]
    
    def move(self, direction = 'X'):
        self.move_delay = self.move_delay - 1
        new_pos = self.getHead().copy()
        
        if ((direction == 'E' and self.direction != 'W')
            or (direction == 'W' and self.direction != 'E')
            or (direction == 'N' and self.direction != 'S')
            or (direction == 'S' and self.direction != 'N')):
            self.direction = direction
            
            
        if self.move_delay == 0:
            if self.direction == 'W':
                new_pos[0] = new_pos[0] - 1
            elif self.direction == 'E':
                new_pos[0] = new_pos[0] + 1
            elif self.direction == 'S':
                new_pos[1] = new_pos[1] + 1
            elif self.direction == 'N':
                new_pos[1] = new_pos[1] - 1
            
            #collision detection with walls and self
            if new_pos[0] in [-1,BOARD_WIDTH] or new_pos[1] in [-1,BOARD_HEIGHT]:
                self.die()
            elif new_pos in self.getBody():
                self.die()
            else:
                self.body.insert(0,new_pos)
                
            #expand if an apple was eaten
            if self.eaten:
                self.eaten = False
                if ((len(self.getBody()) - 1) % SCORE_SPEEDUP == 0 
                    and self.max_move_delay > 1):
                    #Speed up every SCORE_SPEEDUP points
                    self.max_move_delay -=1
            else:
                self.body.pop()
                
            #reset move delay
            self.move_delay = self.max_move_delay
        return

    def eat(self):
        self.eaten = True
        return
    
    def die(self):
        self.is_dead = True
        
    def isHeDead(self):
        return self.is_dead