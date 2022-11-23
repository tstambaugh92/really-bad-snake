#Cutscene class
#Really Bad Snake
#Version 1 of this, I suspect I'll animate sprites in the future

#The idea is that the cutscene can be written in a json file
#so that I can reuse the same logical code to process that file
#This is overkill for snake, but will be useful in the future

import config
import json
import pygame

class Cutscene():
#A cutscene file is a JSON file
#Template is found in template.json to explain
#Each "type" for a step has a function below
#draw_order is unsued this moment, planned to hold layers
#
#skip_key can be changed to skip the cutscene.
#  If you skip the cutscene, whatever is currently on the screen is left
#  Redraw your previous screen from before the cutscene, or load a premade
#  post cutscene surface
#
#canvas is a drawing area to apply multiple images
#  to a surface in multiple steps, but display it to the main
#  window all at once. This is useful for multiline text
#
#save_screen is a surface to 'screen cap' the screen
#  if you want to restore it latter
#
#TO DO: Add ability to keep multiple saved_screens and cavases
    def __init__(self, cs_file_str, game_window):
        if config.DEBUG:
            print("Loading " + cs_file_str)
        with open(cs_file_str, "r") as cs_file:
            self.cs = json.load(cs_file)
        self.game_window = game_window
        self.drawOrder = []
        self.canvas = pygame.surface.Surface((200,200))
        self.saved_screen = pygame.surface.Surface((800,600))
        self.skip_key = pygame.K_SPACE
        self.scene_clock = pygame.time.Clock()
        self.loadImage(self.cs["images"])
        self.loadFonts(self.cs["fonts"])
        self.loadSound(self.cs["sounds"])
        self.loadMusic(self.cs["music"])
        if config.DEBUG:
            print(cs_file_str + " loaded")
        return
    
    ##Loading assets section
    def loadImage(self, image_list):
        if config.DEBUG:
            print("Loading images")
        self.images = {}
        for img in image_list:
            self.images[img] = pygame.image.load(config.BASEDIR + "/img/" + image_list[img]).convert()
        if config.DEBUG:
            print("Finished loading images")
        return
    
    def loadMusic(self, music_list):
        if config.DEBUG:
            print("Loading music")
        self.music = {}
        for curr_song in music_list:
            song = music_list[curr_song]
            self.music[curr_song] = pygame.mixer.Sound(config.BASEDIR + "/audio/" + song)
        if config.DEBUG:
            print("Finished loading music")
        return
    
    def loadFonts(self, font_list):
        if config.DEBUG:
            print("Loading fonts")
        self.fonts = {}
        for curr_font in font_list:
            font = font_list[curr_font]
            self.fonts[curr_font] = pygame.font.Font(config.BASEDIR + '/misc/' + font["file"],font["size"])
        if config.DEBUG:
            print("Finished loading fonts")
        return
    
    def loadSound(self, sound_list):
        if config.DEBUG:
            print("Loading sounds")
        self.sounds = {}
        for curr_sound in sound_list:
            sound = sound_list[curr_sound]
            self.sounds[curr_sound] = pygame.mixer.Sound(config.BASEDIR + "/audio/" + sound)
        if config.DEBUG:
            print("Finished loading sound")
        return
    
    #Run through all the steps and play them
    def play(self):
        if config.DEBUG:
            print("Playing " + self.cs["name"])
        skip = False
        pygame.mixer.stop()
        for step_num in range(1, len(self.cs["steps"]) + 1):
            if config.DEBUG:
                print("  Playing step " + str(step_num))
            step = self.cs["steps"][str(step_num)]
            step_type = step["type"]
            if step_type == "clearScreen":
                skip = self.clearScreen(step["data"])
            elif step_type == "delay":
                skip = self.delay(step["data"])
            elif step_type == "displayCenterImage":
                skip = self.displayCenterImage(step["data"])
            elif step_type == "fadeCanvasIn":
                skip = self.fadeCanvasIn(step["data"])
            elif step_type == "fadeCenterImageIn":
                skip = self.fadeCenterImageIn(step["data"])
            elif step_type == "fadeTextIn":
                skip = self.fadeTextIn(step["data"])
            elif step_type == "newCanvas":
                skip = self.newCanvas(step["data"])
            elif step_type == "playMusic":
                skip = self.playMusic(step["data"])
            elif step_type == "playRestOfMusic":
                skip = self.playRestOfMusic(step["data"])
            elif step_type == "playRestOfSound":
                skip = self.playRestOfSound(step["data"])
            elif step_type == "playSound":
                skip = self.playSound(step["data"])
            elif step_type == "resizeImage":
                skip = self.resizeImage(step["data"])
            elif step_type == "restoreScreen":
                skip = self.restoreScreen(step["data"])
            elif step_type == "saveScreen":
                skip = self.saveScreen(step["data"])
            elif step_type == "textOnCanvas":
                skip = self.textOnCanvas(step["data"])
            if skip:
                break
        
        pygame.mixer.stop()
        if config.DEBUG:
            print("Done playing cutscene " + self.cs["name"])
            print(" ")
        return
    
    #Reusable logic for steps
    def wannaSkip(self):
        #Checks if the SKIP key was pressed
        #Returns True if it has, False otherwise
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == self.skip_key:
                    return True
        return False
    

    def centerSurfaceAt(self, surf, pos):
        #This will return (x,y) coordinates for where to blit
        #surf(surface) so that its center is at pos(int,int)
        rect = surf.get_rect()
        return (pos[0] - int(rect.w / 2), pos[1] - int(rect.h / 2))
    
    #Functions for the logic of each type of step. Will Document this
    #Better because I'd like to reuse it. 
    def clearScreen(self, step):
        #clearScreen - fills the main screen
        #STEP keys:
        #key - data type - desc
        #color - #RRGGBB string - The color of the blank screen
        #save - bool - if the board is redrawn, should it be blank
        if config.DEBUG:
            print("    Start clear screen")
        self.game_window.fill(step["color"])
        pygame.display.update()
        if step["save"]:
            self.drawOrder = []
        if config.DEBUG:
            print("    Finish clear screen")
        return self.wannaSkip()

    def delay(self, step):
        #delay - pauses any action for a time. 
        #        no changes to the screen state will happen
        #STEP keys:
        #key - data type - desc
        #time - int - milisections to delay
        if config.DEBUG:
            print("    Starting delay.")
        for i in range(0, step["time"]):
            if self.wannaSkip():
                return True
            pygame.time.delay(1)
        if config.DEBUG: 
            print("    Finished delay")
        return False
    
    def displayCenterImage(self, step):
        #displayCenterImage - centers an image on a position
        #                     to the game_window at full alpha
        #STEP keys:
        #key - data type - desc
        #img - img nickname - The key for the image in self.images
        #pos - [int, int] - Location for the center of the image
        #save - bool - If the board is redrawn from scratch, should this be included
        if config.DEBUG:
            print("    Displaying image " + step["img"])
        img = self.images[step["img"]]
        pos = self.centerSurfaceAt(img, step["pos"])
        self.game_window.blit(img,pos)
        pygame.display.update()
        if config.DEBUG:
            print("    Finish displaying image " + step["img"])
        return self.wannaSkip()
    
    def fadeCanvasIn(self, step):
        if config.DEBUG:
            print("    Starting to fade in canvas")
        canvas = self.canvas
        fps = round(256 / (step["time"] / 1000))
        old_h = self.game_window.get_height()
        old_w = self.game_window.get_width()
        old_surf = pygame.surface.Surface((800,600))
        old_surf.blit(self.game_window, (0,0))

        pos = self.centerSurfaceAt(canvas, step["pos"])
        for alpha in range(0,255):
            canvas.set_alpha(alpha)
            self.game_window.fill((0,0,0))
            self.game_window.blit(old_surf,(0,0))
            self.game_window.blit(canvas, pos)
            pygame.display.update()
            self.scene_clock.tick(fps)
            if self.wannaSkip():
                return True
        if config.DEBUG:
            print("    Finished fading in canvas")
        return self.wannaSkip()

    def fadeCenterImageIn(self, step):
        #fadeCenterImageIn - Fade an image in from 0 alpha to full alpha
        #STEP keys:
        #key - data type - desc
        #img - img nickname - The key for the image in self.images
        #pos - [int, int] - Location for the center of the image
        #save - bool - If the board is redrawn from scratch, should this be included
        #time - int - Miliseconds for how long it takes to fade in        
        if config.DEBUG:
            print("    Fading in image")
        old_surf = pygame.surface.Surface((800,600))
        old_surf.blit(self.game_window, (0,0))
        delta = round(step["time"] / 256)
        img = self.images[step["img"]]
        pos = self.centerSurfaceAt(img, step["pos"])
        for alpha in range(0, 256):
            img.set_alpha(alpha)
            self.game_window.fill((0,0,0))
            self.game_window.blit(old_surf, (0,0))
            self.game_window.blit(img, pos)
            pygame.display.update()
            pygame.time.delay(delta)
            if self.wannaSkip():
                return True
        if config.DEBUG:
            print("    Done fading in image")
        return False
    
    def fadeCenterImageOut(self, step):
        #fadeCenterImageOut - Fade an image out from full alpha to 0 alpha
        #STEP keys:
        #key - data type - desc
        #img - img nickname - The key for the image in self.images
        #pos - [int, int] - Location for the center of the image
        #save - bool - If the board is redrawn from scratch, should this be included
        #time - int - Miliseconds for how long it takes to fade out  
        if config.DEBUG:
            print("    Fading out image")
        old_surf = pygame.surface.Surface((800,600))
        old_surf.blit(self.game_window, (0,0))
        delta = round(step["time"] / 256)
        img = self.images[step["img"]]
        pos = self.centerSurfaceAt(img, step["pos"])
        for alpha in range(255,-1,-1):
            img.set_alpha(alpha)
            self.game_window.blit(old_surf, (0,0))
            self.game_window.blit(img, pos)
            pygame.display.update()
            pygame.time.delay(delta)
            if self.wannaSkip():
                return True
        if config.DEBUG:
            print("    Done fading out image")
        return False

    def fadeTextIn(self, step):
        #fadeTextIn - Fade an image in from 0 alpha to full alpha
        #STEP keys:
        #key - data type - desc
        #text - text nickname - The key for the text in self.cs["text"]
        #font - font nickname - The key for the font in self.fonts
        #pos - [int, int] - Location for the center of the text
        #save - bool - If the board is redrawn from scratch, should this be included
        #time - int - Miliseconds for how long it takes to fade in  
        if config.DEBUG:
            print("    Fading in text")
        old_surf = pygame.surface.Surface((800,600))
        old_surf.blit(self.game_window, (0,0))
        delta = round(step["time"] / 256)
        font = self.fonts[step["font"]]
        text_surf = font.render(self.cs["text"][step["text"]], True, tuple(step["color"]))
        pos = self.centerSurfaceAt(text_surf, step["pos"])
        for alpha in range(0, 256):
            text_surf.set_alpha(alpha)
            self.game_window.fill(0)
            self.game_window.blit(old_surf, (0,0))
            self.game_window.blit(text_surf, pos)
            pygame.display.update()
            pygame.time.delay(delta)
            if self.wannaSkip():
                return True
        if config.DEBUG:
            print("    Done fading in text")
        return False
    
    def fadeTextOut(self, step):
        #fadeTextOut - Fade an image in from 0 alpha to full alpha
        #STEP keys:
        #key - data type - desc
        #text - text nickname - The key for the text in self.cs["text"]
        #font - font nickname - The key for the font in self.fonts
        #pos - [int, int] - Location for the center of the text
        #save - bool - If the board is redrawn from scratch, should this be included
        #time - int - Miliseconds for how long it takes to fade out 
        if config.DEBUG:
            print("    Fading out text")
        old_surf = pygame.surface.Surface((800,600))
        old_surf.blit(self.game_window, (0,0))
        delta = round(step["time"] / 256)
        font = self.fonts[step["font"]]
        text_surf = font.render(self.cs["text"][step["text"]], True, tuple(step["color"]))
        pos = self.centerSurfaceAt(text_surf, step["pos"])
        for alpha in range(255, -1,-1):
            text_surf.set_alpha(alpha)
            self.game_window.blit(old_surf, (0,0))
            self.game_window.blit(text_surf, pos)
            pygame.display.update()
            pygame.time.delay(delta)
            if self.wannaSkip():
                return True
        if config.DEBUG:
            print("    Done fading out text")
        return False
    
    def newCanvas(self, step):
        #I stopped the detailed comments here because Christ Hawk help me
        #this is an awful system. This did help me figure out a better way
        #to do some of this though, so cool.
        if config.DEBUG:
            print("    Making new canvas")
        self.canvas = pygame.surface.Surface(step["size"],pygame.SRCALPHA)
        self.canvas.fill(step["color"])
        if config.DEBUG:
            print("    Finished making new canvas")
        return self.wannaSkip()
    
    def playMusic(self, step):
        if config.DEBUG:
            print("    Playing music")
        chn = pygame.mixer.Channel(step["channel"])
        chn.play(self.music[step["name"]])
        if config.DEBUG:
            print("    Done playing music")
        return self.wannaSkip()
    
    def playRestOfMusic(self, step):
        if config.DEBUG:
            print("    Playing the rest of the music")
        chn = pygame.mixer.Channel(step["channel"])
        while chn.get_busy():
            if self.wannaSkip():
                return True
        if config.DEBUG:
            print("    Done playing the rest of the music")
        return False
    
    def playRestOfSound(self, step):
        if config.DEBUG:
            print("    Playing the rest of sound")
        chn = pygame.mixer.Channel(step["channel"])
        while chn.get_busy():
            if self.wannaSkip():
                return True
        if config.DEBUG:
            print("    Done playing the rest sound")
        return False
    
    def playSound(self, step):
        if config.DEBUG:
            print("    Start playing " + step["sound"])
        chn = pygame.mixer.Channel(step["channel"])
        chn.play(self.sounds[step["sound"]])
        if config.DEBUG:
            print("    Now playing " + step["sound"])
        return self.wannaSkip()
    
    def resizeImage(self, step):
        if config.DEBUG:
            print("    Starting to resize image")
        img = self.images[step["img"]]
        img = pygame.transform.scale(img, step["size"])
        self.images[step["img"]] = img
        if config.DEBUG:
            print("    Finished resizing image")
        return self.wannaSkip()
 
    def restoreScreen(self, step):
        if config.DEBUG:
            print("    Starting restore screen")
        self.game_window.blit(self.saved_screen,(0,0))
        if config.DEBUG:
            print("    Finished restore screen")
        return self.wannaSkip()
    
    def saveScreen(self, step):
        if config.DEBUG:
            print("    Starting save screen")
        self.saved_screen.blit(self.game_window,(0,0))
        if config.DEBUG:
            print("    Finished save screen")
        return self.wannaSkip()
    
    def textOnCanvas(self, step):
        if config.DEBUG:
            print("    Start text on canvas")
        text_surface = self.fonts[step["font"]].render(self.cs["text"][step["text"]], True, tuple(step["color"]))
        pos = self.centerSurfaceAt(text_surface, step["pos"])
        self.canvas.blit(text_surface,pos)
        if config.DEBUG:
            print("    Finished text on canvas")
        return self.wannaSkip()
    
