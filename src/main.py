#Thomas Stambaugh
#Really Bad Snake
from json import load
import pygame
import random
import os

import config
from snake import Snake
from apple import Apple
from button import Button
from cutscene import Cutscene

thisFile = ""

def playGame(game_window):
    snake = Snake()
    apple = Apple()
    blank_board = pygame.Surface((800, 600))
    blank_board.fill(pygame.Color('#000000'))
    
    snake_piece = pygame.Surface((config.BODY_SIZE,config.BODY_SIZE))
    snake_piece.fill(pygame.Color('#FF0000'))
    
    apple_piece = pygame.Surface((config.BODY_SIZE,config.BODY_SIZE))
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
                if config.DEBUG:
                    print("Direction switched: " + direction)

        #game logic
        snake.move()
        if snake.isHeDead() == True:
            if config.DEBUG:
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
            for body, pos in snake.getBodyImages():
                game_window.blit(body, (pos[0] * config.BODY_SIZE, pos[1] * config.BODY_SIZE))
            game_window.blit(apple.getImg(), (apple.getX() * config.BODY_SIZE, apple.getY() * config.BODY_SIZE))
            pygame.display.update()
        
        #wait
        pygame.time.wait(int(1000/60)) #1/60th of a second, or '60fps'
        
    pygame.event.clear 
    if config.DEBUG:
        print("Ending playGame()")
    return quit

def settingsScreen(game_window):
    blank_board = pygame.Surface((800, 600))
    blank_board.fill(pygame.Color('#00FF00'))
    game_window.blit(blank_board, (0,0))
    settingsBg = pygame.image.load(config.BASEDIR + '/img/settings.jpg')
    game_window.blit(settingsBg, (0,0))

    return_button_pos = (580,480)
    fullscreen_on_pos = (20, 490)
    fullscreen_off_pos = (130, 490)
    sound_on_pos = (420, 310)
    sound_off_pos = (530, 310)

    return_button = Button(config.BASEDIR + '/img/return.jpg', (200,100))
    return_button.display(game_window, return_button_pos)
    fullscreen_on_button = Button(config.BASEDIR + '/img/on.jpg', (100,100))
    fullscreen_on_button.display(game_window, fullscreen_on_pos)
    fullscreen_off_button = Button(config.BASEDIR + '/img/off.jpg', (100,100))
    fullscreen_off_button.display(game_window, fullscreen_off_pos)
    sound_button_on = Button(config.BASEDIR + '/img/on.jpg', (100,100))
    sound_button_on.display(game_window, sound_on_pos)
    sound_button_off = Button(config.BASEDIR + '/img/off.jpg', (100,100))
    sound_button_off.display(game_window, sound_off_pos)

    pygame.display.update()
    go_back = False
    while go_back == False:
        for event in pygame.event.get():
            #button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if return_button.wasItClicked(mousePos):
                    go_back = True
                elif fullscreen_on_button.wasItClicked(mousePos):
                    if config.FULL_SCREEN == False:
                        config.FULL_SCREEN = True
                        pygame.display.set_mode((800, 600), vsync=1, flags=pygame.FULLSCREEN)
                        pygame.display.update()
                elif fullscreen_off_button.wasItClicked(mousePos):
                    if config.FULL_SCREEN == True:
                        config.FULL_SCREEN = False
                        pygame.display.set_mode((800, 600), vsync=1)
                        pygame.display.update()
                elif sound_button_off.wasItClicked(mousePos):
                    if config.SOUND == True:
                        config.SOUND = False
                        pygame.mixer.music.stop()
                elif sound_button_on.wasItClicked(mousePos):
                    if config.SOUND == False:
                        config.SOUND = True
                        pygame.mixer.music.play(loops=-1)
            #Windows exit button
            elif event.type == pygame.QUIT:
                return True
    
    
    return False
    
def exitScreen(game_window):
    #load files
    pygame.mixer.music.stop()
    exit_cs = Cutscene(config.BASEDIR + "/cutscene/exit.json", game_window)
    exit_cs.play()
    return

def credits(game_window):
    credit_cs = Cutscene(config.BASEDIR + "/cutscene/credits.json", game_window)
    credit_cs.play()
    return

def setDifficulty(setting):
    if config.DEBUG:
        print("Still working on difficulty")
    return

def loadSettings():
    with open(config.BASEDIR + "/misc/config.ini", "r") as config_file:
        for line in config_file:
            line_str = line.replace(" ", "")
            line_str = line_str.replace("\n", "")
            if config.DEBUG:
                print("line:" + line_str)
            index = line_str.find("=")
            if line_str[0:index] == "difficulty":
                config.DIFFICULTY = line_str[index+1]
                setDifficulty(line_str[index+1:])
            elif line_str[0:index] == "gore":
                print("Herp derp: " + line_str[index+1:] + "#")
                if line_str[index+1:] == "True":
                    config.GORE = True
                    print("Herp")
                else:
                    config.GORE = False
                    print("Derp")
            elif line_str[0:index] == "sound":
                if line_str[index+1:] == "True":
                    config.SOUND = True
                else:
                    config.SOUND = False
            elif line_str[0:index] == "fullscreen":
                if line_str[index+1:] == "True":
                    config.FULL_SCREEN = True
                else:
                    config.FULL_SCREEN = False     
        config_file.close()
        if config.DEBUG:
            print("Sound is " + str(config.SOUND))
            print("Gore is " + str(config.GORE))
            print("Full Screen is " + str(config.FULL_SCREEN))
            print("Loaded configuration file")
    return

def main():
    config.BASEDIR = os.path.join( os.path.dirname( __file__ ), '..' )
    print(config.BASEDIR)
    random.seed()
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    pygame.display.set_caption('Very Bad Snake')
    loadSettings()
    
    #load images
    titlePic = pygame.image.load(config.BASEDIR + '/img/title.png')
    deathPic = pygame.image.load(config.BASEDIR + '/img/title2.png')
    playButton = Button(config.BASEDIR + '/img/play.png', (200,100))
    quitButton = Button(config.BASEDIR + '/img/quit.png', (200,100))
    settingsButton = Button(config.BASEDIR + '/img/settings.png', (200,50))
    creditsButton = Button(config.BASEDIR + '/img/credits.png', (200,50))
    icon = pygame.image.load(config.BASEDIR + '/img/icon.png')
    icon = pygame.transform.scale(icon,(32,32))
    pygame.display.set_icon(icon)
    
    #load music
    pygame.mixer.music.load(config.BASEDIR + '/audio/midsummers.ogg')
    pygame.mixer.music.play(loops=-1)
    
    #create window and boot title screen
    if config.FULL_SCREEN:
        fs_option = pygame.FULLSCREEN
    else:
        fs_option = 0
    game_window = pygame.display.set_mode((800, 600), vsync=1, flags=fs_option)
    playButtonPos = (200,400)
    quitButtonPos = (430,400)
    settingsButtonPos = (200,520)
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
                    if config.GORE:
                        titleScreen = deathPic
                    reload_title = True
                if quitButton.wasItClicked(mousePos):
                    quit = True
                if creditsButton.wasItClicked(mousePos):
                    pygame.mixer.music.pause()
                    credits(game_window)
                    pygame.mixer.music.unpause()
                    reload_title = True
                if settingsButton.wasItClicked(mousePos):
                    quit = settingsScreen(game_window)
                    reload_title = True
            #hot key for starting
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    quit = playGame(game_window)
                    if config.GORE:
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
            settingsButton.display(game_window, settingsButtonPos)
            creditsButton.display(game_window, creditsButtonPos)
            pygame.display.update()
            
    exitScreen(game_window)
    return

if __name__ == '__main__':
    main()