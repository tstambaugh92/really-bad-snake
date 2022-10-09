#Thomas Stambaugh
#Really Bad Snake
from imp import reload
import pygame
import random
from config import *

from snake import Snake
from apple import Apple
from button import Button
from cutscene import Cutscene


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
                snake.addMove(direction)
                if DEBUG:
                    print("Direction switched: " + direction)

        #game logic
        snake.move()
        if snake.isHeDead() == True:
            if DEBUG:
                print("The Snake is dead")
            game_is_running = False
        elif snake.getHead() == apple.getPos():
            snake.eat()
            score+=1
            pygame.display.set_caption('Very Bad Snake - Score: ' + str(score))
            apple.regrow(snake.getBody())
        
        #graphics
        if game_is_running:
            game_window.blit(blank_board, (0, 0))
            for tile in snake.getBody():
                game_window.blit(snake_piece, (tile[0] * BODY_SIZE, tile[1] * BODY_SIZE))
            game_window.blit(apple_piece, (apple.getX() * BODY_SIZE, apple.getY() * BODY_SIZE))
            pygame.display.update()
        
        #wait
        pygame.time.wait(int(1000/60)) #1/60th of a second, or '60fps'
        
    pygame.event.clear 
    if DEBUG:
        print("Ending playGame()")
    return quit
    
def exitScreen(game_window):
    #load files
    pygame.mixer.music.stop()
    exit_cs = Cutscene("../cutscene/exit.json", game_window)
    exit_cs.play()
    return

def credits(game_window):
    credit_cs = Cutscene("../cutscene/credits.json", game_window)
    credit_cs.play()
    return
    

def main():
    random.seed()
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    pygame.display.set_caption('Very Bad Snake')
    
    #load images
    titlePic = pygame.image.load('../img/title.png')
    deathPic = pygame.image.load('../img/title2.png')
    playButton = Button('../img/play.png', (200,100))
    quitButton = Button('../img/quit.png', (200,100))
    creditsButton = Button('../img/credits.png', (200,50))
    icon = pygame.image.load('../img/icon.png')
    icon = pygame.transform.scale(icon,(32,32))
    pygame.display.set_icon(icon)
    
    #load music
    pygame.mixer.music.load('../audio/midsummers.ogg')
    pygame.mixer.music.play(loops=-1)
    
    #create window and boot title screen
    game_window = pygame.display.set_mode((800, 600))
    playButtonPos = (200,400)
    quitButtonPos = (430,400)
    creditsButtonPos = (430,520)
    quit = False
    reload_title = True
    titleScreen = titlePic
    while quit == False:
        for event in pygame.event.get():
            #button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if playButton.wasItClicked(mousePos):
                    quit = playGame(game_window)
                    titleScreen = deathPic
                    reload_title = True
                if quitButton.wasItClicked(mousePos):
                    quit = True
                if creditsButton.wasItClicked(mousePos):
                    pygame.mixer.music.pause()
                    credits(game_window)
                    pygame.mixer.music.unpause()
                    reload_title = True
            #hot key for starting
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    quit = playGame(game_window)
                    titleScreen = deathPic
                    reload_title = True
            #Windows exit button
            elif event.type == pygame.QUIT:
                quit = True
                
        if reload_title == True and quit == False:
            reload_title = False
            game_window.blit(titleScreen, (0,0))
            playButton.display(game_window, playButtonPos)
            quitButton.display(game_window, quitButtonPos)
            creditsButton.display(game_window, creditsButtonPos)
            pygame.display.update()
            
    exitScreen(game_window)
    return

if __name__ == '__main__':
    main()