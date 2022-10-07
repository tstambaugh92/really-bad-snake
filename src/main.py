#Thomas Stambaugh
#Really Bad Snake
import pygame
import random
from config import *

from snake import Snake
from apple import Apple
from button import Button


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
    blank_board = pygame.Surface((800, 600))
    blank_board.fill(pygame.Color('#000000'))
    game_window.blit(blank_board,(0,0))
    pygame.display.update()
    pygame.mixer.music.stop()
    logo = pygame.image.load('../img/LOGO.png')
    hawkmaster = pygame.image.load('../img/hawkmaster.jpg')
    hawkmaster = pygame.transform.scale(hawkmaster, (300,300))
    hawkmaster.set_alpha(0)
    FLY_WITH_CHRIST = pygame.mixer.Sound('../audio/FlyWithChrist.ogg')
    hawkmasters_endorsement = pygame.mixer.Sound('../audio/MadeThisGame.ogg')
    
    #play sequence
    FLY_WITH_CHRIST.play()
    pygame.time.wait(1000)
    game_window.blit(logo, (0,200))
    pygame.display.update()
    pygame.time.wait(3500)
    for i in range(255,-1,-1):
        logo.set_alpha(i)
        game_window.blit(blank_board,(0,0))
        game_window.blit(logo, (0,200))
        pygame.display.update()
        pygame.time.delay(3)
    pygame.time.delay(400)
    hawkmasters_endorsement.play()
    for i in range(1,256,1):
        hawkmaster.set_alpha(i)
        game_window.blit(blank_board,(0,0))
        game_window.blit(hawkmaster, (250,150)) 
        pygame.display.update()
        pygame.time.delay(3)       
    pygame.time.delay(2700)
    
    
    return

def main():
    random.seed()
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption('Very Bad Snake')
    
    #load images
    titlePic = pygame.image.load('../img/title.png')
    deathPic = pygame.image.load('../img/title2.png')
    playButton = Button('../img/play.png', (200,100))
    quitButton = Button('../img/quit.png', (200,100))
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
                    reload_title = True
                if quitButton.wasItClicked(mousePos):
                    quit = True
            #hot key for quitting
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    quit = playGame(game_window)
                    reload_title = True
            #Windows exit button
            elif event.type == pygame.QUIT:
                quit = True
                
        if reload_title == True and quit == False:
            reload_title = False
            game_window.blit(titleScreen, (0,0))
            playButton.display(game_window, playButtonPos)
            quitButton.display(game_window, quitButtonPos)
            pygame.display.update()
            titleScreen = deathPic
            
    exitScreen(game_window)
    return
    
    

    
if __name__ == '__main__':
    main()