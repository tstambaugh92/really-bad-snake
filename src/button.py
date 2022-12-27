#Button
#For Very Bad Snake
import pygame

from config import DEBUG

class Button():
    def __init__(self, file, size):
        if DEBUG:
            self.filename = file
        self.img = pygame.image.load(file)
        self.img = pygame.transform.scale(self.img, size)
        self.pos_rect = self.img.get_rect()
        if DEBUG:
            print(self.pos_rect)
        return
        
    def display(self, screen, pos):
        screen.blit(self.img, pos)
        self.pos_rect.x = pos[0]
        self.pos_rect.y = pos[1]
        if DEBUG:
            print(self.filename + " at " + str(self.pos_rect))
        return
        
    def wasItClicked(self, pos):
        if self.pos_rect.collidepoint(pos[0], pos[1]):
            if DEBUG:
                print(self.filename + " was clicked")
            return True
        else:
            return False
        