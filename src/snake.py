#Snake class
#For Very Bad Snake
import pygame
import random
from config import *

class Snake:
    def __init__(self):
        self.body = [[0,0]]
        self.direction = 'E'
        self.is_dead = False
        self.move_delay = START_SPEED
        self.max_move_delay = START_SPEED
        self.eaten = False
        self.cry = pygame.mixer.Sound('../audio/cry.ogg')
        self.gulp = pygame.mixer.Sound('../audio/gulp.ogg')
        self.deaths = []
        self.deaths.append(pygame.mixer.Sound('../audio/death/TinyAccidentDeath.ogg'))
        self.deaths.append(pygame.mixer.Sound('../audio/death/TylerDeath.ogg'))
        self.deaths.append(pygame.mixer.Sound('../audio/death/TomDeath.ogg'))
        self.deaths.append(pygame.mixer.Sound('../audio/death/YesiDeath.ogg'))
        self.deaths.append(pygame.mixer.Sound('../audio/death/SaltDeath.ogg'))
        self.move_queue = []

    def getBody(self):
        return self.body
    
    def getHead(self):
        return self.body[0]
    
    def move(self):
        self.move_delay = self.move_delay - 1
        new_pos = self.getHead().copy()
          
            
        if self.move_delay == 0:
            if len(self.move_queue) > 0:
                direction = self.move_queue.pop(0)
            else:
                direction = 'X'
            if ((direction == 'E' and self.direction != 'W')
            or  (direction == 'W' and self.direction != 'E')
            or  (direction == 'N' and self.direction != 'S')
            or  (direction == 'S' and self.direction != 'N')):
                self.direction = direction
            
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
        self.gulp.play()
        return
    
    def die(self):
        if DEBUG:
            print("Dying")
        self.is_dead = True
        pygame.mixer.music.pause()
        ch1 = pygame.mixer.Channel(1)
        ch2 = pygame.mixer.Channel(2)
        ch1.play(self.cry)
        ch2.play(random.choice(self.deaths))
        while ch1.get_busy() or ch2.get_busy():
            pass
        print("Dontcrash") #Why do I need this to not crash
        pygame.mixer.music.unpause()
        if DEBUG:
            print("Done Dying")
        return
        
    def isHeDead(self):
        return self.is_dead
    
    def addMove(self,move):
        self.move_queue.append(move)
        if DEBUG:
            print("Queued move " + move)
        return