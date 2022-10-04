#Thomas Stambaugh
#Really Bad Snake
import pygame
import random

BOARD_WIDTH = 40
BOARD_HEIGHT = 30
BODY_SIZE = 20
#Board is X by Y, with 0,0 being the upper left corner. 

class Snake:
    def __init__(self):
        self.body = [[0,0]]
        self.direction = 'E'
        self.is_dead = False
        self.move_delay = 3
        self.max_move_delay = 3
        self.eaten = False
    
    def getBody(self):
        return self.body
    
    def getHead(self):
        return self.body[0]
    
    def move(self, direction = 'X'):
        self.move_delay = self.move_delay - 1
        new_pos = self.getHead().copy()
        
        if direction != 'X':
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


def main():
    random.seed()
    board = [[[0] * BOARD_HEIGHT] * BOARD_WIDTH]
    snake = Snake()
    apple = Apple()
    pygame.init()
    pygame.display.set_caption('Very Bad Snake')
    game_window = pygame.display.set_mode((800, 600))
    game_is_running = True
    
    blank_board = pygame.Surface((800, 600))
    blank_board.fill(pygame.Color('#000000'))
    
    snake_piece = pygame.Surface((BODY_SIZE,BODY_SIZE))
    snake_piece.fill(pygame.Color('#FF0000'))
    
    apple_piece = pygame.Surface((BODY_SIZE,BODY_SIZE))
    apple_piece.fill(pygame.Color('#FFFF00'))
    score = 0
    quit = False
    while game_is_running: #main loop
        #user input
        direction = 'X'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_is_running = False
                quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    direction = 'N'
                elif event.key == pygame.K_s:
                    direction = 'S'
                elif event.key == pygame.K_a:
                    direction = 'W'
                elif event.key == pygame.K_d:
                    direction = 'E'

        #game logic
        snake.move(direction)
        if snake.getHead() == apple.getPos():
            snake.eat()
            score+=1
            pygame.display.set_caption('Very Bad Snake - Score: ' + str(score))
            apple.regrow(snake.getBody())
        if snake.isHeDead() == True:
            game_is_running = False
        
        #graphics
        game_window.blit(blank_board, (0, 0))
        for tile in snake.getBody():
            game_window.blit(snake_piece, (tile[0] * BODY_SIZE, tile[1] * BODY_SIZE))
        game_window.blit(apple_piece, (apple.getX() * BODY_SIZE, apple.getY() * BODY_SIZE))
        pygame.display.update()
        
        #wait
        pygame.time.wait(int(1000/60)) #1/60th of a second, or '60fps'
        
    if quit == False:
        pygame.time.wait(2000)
    
if __name__ == '__main__':
    main()