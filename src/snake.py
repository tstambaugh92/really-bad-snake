#Snake class
#For Very Bad Snake
import pygame
import random
import config

class Snake:
    def __init__(self):
        print(config.BASEDIR + " lalala")
        self.body = [[0,0]]
        self.body_direction = ['E']
        self.direction = 'E'
        self.is_dead = False
        self.move_delay = config.START_SPEED
        self.max_move_delay = config.START_SPEED
        self.eaten = False
        self.cry = pygame.mixer.Sound(config.BASEDIR + '/audio/cry.ogg')
        self.gulp = pygame.mixer.Sound(config.BASEDIR + '/audio/gulp.ogg')
        self.deaths = []
        self.deaths.append(pygame.mixer.Sound(config.BASEDIR + '/audio/death/TinyAccidentDeath.ogg'))
        self.deaths.append(pygame.mixer.Sound(config.BASEDIR + '/audio/death/TylerDeath.ogg'))
        self.deaths.append(pygame.mixer.Sound(config.BASEDIR + '/audio/death/TomDeath.ogg'))
        self.deaths.append(pygame.mixer.Sound(config.BASEDIR + '/audio/death/YesiDeath.ogg'))
        self.deaths.append(pygame.mixer.Sound(config.BASEDIR + '/audio/death/SaltDeath.ogg'))
        self.move_queue = []
        self.img = {}
        self.loadBodyImages()

    def getBody(self):
        return self.body
    
    def getBodyImages(self):
        images = []
        last = len(self.body_direction) - 1
        for index in range(0,len(self.body_direction)):
            str = ""
            if index == 0: #head
                str = "head" + self.body_direction[index]
            elif index == last: #tail
                if self.body_direction[index] == self.body_direction[index-1]:
                    str = "tail" + self.body_direction[index]
                else:
                    str = "tail" + self.body_direction[index-1]
            else:  #body
                str = "bodyV"
                if self.body_direction[index - 1] == self.body_direction[index]:
                    if self.body_direction[index] in ['N','S']:
                        str = "bodyV"
                    else:
                        str = "bodyH"
                else:
                    if ((self.body_direction[index] == 'W' and self.body_direction[index-1] == 'N')
                    or  (self.body_direction[index] == 'S' and self.body_direction[index-1] == 'E')):
                        str = "cornerNE"
                    elif ((self.body_direction[index] == 'E' and self.body_direction[index-1] == 'N')
                    or    (self.body_direction[index] == 'S' and self.body_direction[index-1] == 'W')):
                        str = "cornerNW"
                    elif ((self.body_direction[index] == 'N' and self.body_direction[index-1] == 'E')
                    or    (self.body_direction[index] == 'W' and self.body_direction[index-1] == 'S')):
                        str = "cornerSE"
                    elif ((self.body_direction[index] == 'E' and self.body_direction[index-1] == 'S')
                    or    (self.body_direction[index] == 'N' and self.body_direction[index-1] == 'W')):
                        str = "cornerSW"
            images.append(self.img[str])
        return zip(images, self.body)
    
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
            if new_pos[0] in [-1,config.BOARD_WIDTH] or new_pos[1] in [-1,config.BOARD_HEIGHT]:
                self.die()
            elif new_pos in self.getBody():
                self.die()
            else:
                self.body.insert(0,new_pos)
                self.body_direction.insert(0,self.direction)
                
            #expand if an apple was eaten
            if self.eaten:
                self.eaten = False
                if ((len(self.getBody()) - 1) % config.SCORE_SPEEDUP == 0 
                    and self.max_move_delay > 1):
                    #Speed up every config.SCORE_SPEEDUP points
                    self.max_move_delay -=1
            else:
                self.body.pop()
                self.body_direction.pop()
                
            #reset move delay
            self.move_delay = self.max_move_delay
        return

    def eat(self):
        self.eaten = True
        self.gulp.play()
        return
    
    def die(self):
        if config.DEBUG:
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
        if config.DEBUG:
            print("Done Dying")
        return
        
    def isHeDead(self):
        return self.is_dead
    
    def addMove(self,move):
        self.move_queue.append(move)
        if config.DEBUG:
            print("Queued move " + move)
        return
    
    def loadBodyImages(self):
        #head
        self.img["headN"] = pygame.image.load(config.BASEDIR + "/img/snake/headN.png")
        self.img["headS"] = pygame.image.load(config.BASEDIR + "/img/snake/headS.png")
        self.img["headE"] = pygame.image.load(config.BASEDIR + "/img/snake/headE.png")
        self.img["headW"] = pygame.image.load(config.BASEDIR + "/img/snake/headW.png")
        #tail
        self.img["tailN"] = pygame.image.load(config.BASEDIR + "/img/snake/tailN.png")
        self.img["tailS"] = pygame.image.load(config.BASEDIR + "/img/snake/tailS.png")
        self.img["tailE"] = pygame.image.load(config.BASEDIR + "/img/snake/tailE.png")
        self.img["tailW"] = pygame.image.load(config.BASEDIR + "/img/snake/tailW.png")
        #body
        self.img["bodyV"] = pygame.image.load(config.BASEDIR + "/img/snake/bodyV.png")
        self.img["bodyH"] = pygame.image.load(config.BASEDIR + "/img/snake/bodyH.png")
        #corners
        self.img["cornerNW"] = pygame.image.load(config.BASEDIR + "/img/snake/cornerNW.png")
        self.img["cornerNE"] = pygame.image.load(config.BASEDIR + "/img/snake/cornerNE.png")
        self.img["cornerSW"] = pygame.image.load(config.BASEDIR + "/img/snake/cornerSW.png")
        self.img["cornerSE"] = pygame.image.load(config.BASEDIR + "/img/snake/cornerSE.png")
        return