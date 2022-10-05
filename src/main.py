#Thomas Stambaugh
#Really Bad Snake
import pygame
import random
from config import *

from snake import Snake
from apple import Apple

def main():
    random.seed()
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