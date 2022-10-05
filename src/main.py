#Thomas Stambaugh
#Really Bad Snake
import pygame
import random
from config import *

from snake import Snake
from apple import Apple


def playGame(game_window):
    snake = Snake()
    apple = Apple()
    blank_board = pygame.Surface((800, 600))
    blank_board.fill(pygame.Color('#000000'))
    
    snake_piece = pygame.Surface((BODY_SIZE,BODY_SIZE))
    snake_piece.fill(pygame.Color('#FF0000'))
    
    apple_piece = pygame.Surface((BODY_SIZE,BODY_SIZE))
    apple_piece.fill(pygame.Color('#FFFF00'))
    
    score = 0
    quit = False
    game_is_running = True
    
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
        if snake.isHeDead() == True:
            game_is_running = False
        elif snake.getHead() == apple.getPos():
            snake.eat()
            score+=1
            pygame.display.set_caption('Very Bad Snake - Score: ' + str(score))
            apple.regrow(snake.getBody())
        
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
    pygame.event.clear
        
    return quit
    

def main():
    random.seed()
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption('Very Bad Snake')
    
    #load images
    titlePic = pygame.image.load('../img/title.png')
    playButton = pygame.image.load('../img/play.png')
    quitButton = pygame.image.load('../img/quit.png')
    
    #load music
    pygame.mixer.music.load('../audio/midsummers.mp3')
    pygame.mixer.music.play(loops=-1)
    
    #create window and boot title screen
    game_window = pygame.display.set_mode((800, 600))
    playButtonPos = (200,400)
    quitButtonPos = (430,400)
    game_window.blit(titlePic, (0,0))
    game_window.blit(playButton, playButtonPos)
    game_window.blit(quitButton, quitButtonPos)
    pygame.display.update()
    pygame.time.wait(2500)
    quit = False
    while quit == False:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if playButtonPos[1] <= mouseY <= playButtonPos[1] + 100:
                    if playButtonPos[0] <= mouseX <= playButtonPos[0] + 200:
                        quit = playGame(game_window)
                        game_window.blit(titlePic, (0,0))
                        game_window.blit(playButton, playButtonPos)
                        game_window.blit(quitButton, quitButtonPos)
                        pygame.display.update()
                    elif quitButtonPos[0] <= mouseX <= quitButtonPos[0] + 200:
                        quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    quit = playGame(game_window)
                    game_window.blit(titlePic, (0,0))
                    game_window.blit(playButton, playButtonPos)
                    game_window.blit(quitButton, quitButtonPos)
                    pygame.display.update()
            elif event.type == pygame.QUIT:
                quit = True
    
    

    
if __name__ == '__main__':
    main()