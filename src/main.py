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
    blank_board = pygame.image.load(config.BASEDIR + '/img/gameboard.png')
    
    snake_piece = pygame.Surface((config.BODY_SIZE,config.BODY_SIZE))
    snake_piece.fill(pygame.Color('#FF0000'))
    
    apple_piece = pygame.Surface((config.BODY_SIZE,config.BODY_SIZE))
    apple_piece.fill(pygame.Color('#FFFF00'))
    
    score = 0
    quit = False
    game_is_running = True
    draw_grid = False
    slow_down = False
    
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
                elif event.key == pygame.K_ESCAPE:
                    game_is_running = False
                    quit = True
                elif config.DEBUG and event.key == pygame.K_m:
                    pauseToDebug(game_window,snake)
                elif config.DEBUG and event.key == pygame.K_n:
                    draw_grid = not draw_grid
                elif config.DEBUG and event.key == pygame.K_b:
                    slow_down = not slow_down

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
            if draw_grid:
                drawGrid(game_window)
            pygame.display.update()

        #Wait for next frame    
        if slow_down:
            pygame.time.wait(300)
        else:
            pygame.time.wait(int(1000/60)) #1/60th of a second, or '60fps'
        
    pygame.event.clear 
    if config.DEBUG:
        print("Ending playGame()")
    return quit

def pauseToDebug(game_window, snake):
    #debug pause
    pygame.event.clear
    print("Snake's full body: ")
    print(snake.getBody())
    print("Snake's body directions:")
    print(snake.getBodyDirections())
    print("Snake's current direction:")
    print(snake.getCurrentDirection())
    debug_pause = True 
    drawGrid(game_window)
    pygame.display.update()
    while debug_pause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    debug_pause = False

def drawGrid(game_window):
    debug_font = pygame.font.Font(None, 12)
    for i in range(config.BOARD_WIDTH):
        for j in range(config.BOARD_HEIGHT):
            coordinates = debug_font.render("(" + str(i) + "," + str(j) + ")", True, (0,0,0))
            coordinates_rect = coordinates.get_rect()
            coordinates_x_pos = config.BODY_SIZE*i + config.BODY_SIZE/2 - coordinates_rect.w/2
            coordinates_y_pos = config.BODY_SIZE*j + config.BODY_SIZE/2 - coordinates_rect.h/2
            game_window.blit(coordinates, (coordinates_x_pos,coordinates_y_pos))
    #vert grid lines
    for i in range(config.BOARD_WIDTH):
        pygame.draw.line(game_window, (255,255,255), (i*config.BODY_SIZE,0),(i*config.BODY_SIZE,config.BOARD_HEIGHT*config.BODY_SIZE))
    #horizontal grid lines
    
    for j in range(config.BOARD_WIDTH):
        pygame.draw.line(game_window, (255,255,255), (0,j*config.BODY_SIZE),(config.BOARD_WIDTH*config.BODY_SIZE,j*config.BODY_SIZE))
    

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
    gore_on_pos = (20, 310)
    gore_off_pos = (130, 310)
    nesting_pos = (50, 130)
    knighthawk_pos = (300 , 130)
    hawkmaster_pos = (550, 130)

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
    gore_button_on = Button(config.BASEDIR + '/img/on.jpg', (100,100))
    gore_button_on.display(game_window, gore_on_pos)
    gore_button_off = Button(config.BASEDIR + '/img/off.jpg', (100,100))
    gore_button_off.display(game_window, gore_off_pos)
    nesting_button = Button(config.BASEDIR + '/img/nesting.png',(200,100))
    nesting_button.display(game_window, nesting_pos)
    knighthawk_button = Button(config.BASEDIR + '/img/knighthawk.png', (200,100))
    knighthawk_button.display(game_window, knighthawk_pos)
    hawkmaster_button = Button(config.BASEDIR + '/img/hawkmaster.png', (200,100))
    hawkmaster_button.display(game_window, hawkmaster_pos)

    highlight_box = pygame.Surface((100,100))
    highlight_box.set_alpha(128)
    highlight_box.fill('#FFFF66')
    highlight_rect = pygame.Surface((200,100))
    highlight_rect.set_alpha(128)
    highlight_rect.fill('#FFFF66')

    base_background = pygame.Surface((800,600))
    base_background.blit(game_window, (0,0))

    go_back = False
    redraw = True
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
                        redraw = True
                elif fullscreen_off_button.wasItClicked(mousePos):
                    if config.FULL_SCREEN == True:
                        config.FULL_SCREEN = False
                        pygame.display.set_mode((800, 600), vsync=1)
                        redraw = True
                elif sound_button_off.wasItClicked(mousePos):
                    if config.SOUND == True:
                        config.SOUND = False
                        redraw = True
                        pygame.mixer.music.stop()
                elif sound_button_on.wasItClicked(mousePos):
                    if config.SOUND == False:
                        config.SOUND = True
                        redraw = True
                        pygame.mixer.music.play(loops=-1)
                elif gore_button_on.wasItClicked(mousePos):
                    if config.GORE == False:
                        config.GORE = True
                        redraw = True
                elif gore_button_off.wasItClicked(mousePos):
                    if config.GORE == True:
                        config.GORE = False
                        redraw = True
                elif nesting_button.wasItClicked(mousePos):
                    if config.DIFFICULTY != 0:
                        setDifficulty(0)
                        redraw = True
                elif knighthawk_button.wasItClicked(mousePos):
                    if config.DIFFICULTY != 1:
                        setDifficulty(1)
                        redraw = True
                elif hawkmaster_button.wasItClicked(mousePos):
                    if config.DIFFICULTY != 2:
                        setDifficulty(2)
                        redraw = True
            #Windows exit button
            elif event.type == pygame.QUIT:
                return True

        if redraw:
            redraw = False
            game_window.fill(pygame.Color('#000000'))
            game_window.blit(base_background,(0,0))
            if config.FULL_SCREEN:
                game_window.blit(highlight_box,fullscreen_on_pos)
            else:
                game_window.blit(highlight_box,fullscreen_off_pos)
            if config.SOUND:
                game_window.blit(highlight_box,sound_on_pos)
            else:
                game_window.blit(highlight_box,sound_off_pos)
            if config.GORE:
                game_window.blit(highlight_box,gore_on_pos)
            else:
                game_window.blit(highlight_box,gore_off_pos)
            if config.DIFFICULTY == 0:
                game_window.blit(highlight_rect, nesting_pos)
            elif config.DIFFICULTY == 1:
                game_window.blit(highlight_rect, knighthawk_pos)
            else:
                game_window.blit(highlight_rect, hawkmaster_pos)
            pygame.display.update()
    
    
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
        print("Difficulty is " + str(setting))
    if setting == 0:
        config.DIFFICULTY = 0
        config.START_SPEED = 8
        config.SCORE_SPEEDUP = 50
    elif setting == 1:
        config.DIFFICULTY = 1
        config.START_SPEED = 7
        config.SCORE_SPEEDUP = 40
    elif setting == 2:
        config.DIFFICULTY = 2
        config.START_SPEED = 6
        config.SCORE_SPEEDUP = 30
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
                setDifficulty(int(line_str[index+1:]))
            elif line_str[0:index] == "gore":
                if line_str[index+1:] == "True":
                    config.GORE = True
                else:
                    config.GORE = False
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
                    if config.GORE == False:
                        titleScreen = titlePic
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