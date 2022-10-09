#Cutscene class
#Really Bad Snake
#Version 1 of this, I suspect I'll animate sprites in the future

#The idea is that the cutscene can be written in a json file
#so that I can reuse the same logical code to process that file
#This is overkill for snake, but will be useful in the future

from config import *
import json
import pygame

class Cutscene():
    
    def __init__(self, cs_file_str, game_window):
        if DEBUG:
            print("Loading " + cs_file_str)
        with open(cs_file_str, "r") as cs_file:
            self.cs = json.load(cs_file)
        self.game_window = game_window
        self.drawOrder = []
        self.step = 0
        self.drawnImgs = []
        self.skip_key = pygame.K_SPACE
        self.clock = pygame.time.Clock()
        self.loadImage(self.cs["images"])
        self.loadFonts(self.cs["fonts"])
        self.loadSound(self.cs["sounds"])
        self.loadMusic(self.cs["music"])
        if DEBUG:
            print(cs_file_str + " loaded")
        return
    
    def loadImage(self, image_list):
        if DEBUG:
            print("Loading images")
        self.images = {}
        for img in image_list:
            self.images[img] = pygame.image.load("../img/" + image_list[img])
        if DEBUG:
            print("Finished loading images")
        return
    
    def loadMusic(self, music_list):
        if DEBUG:
            print("Loading music")
        self.music = {}
        for curr_song in music_list:
            song = music_list[curr_song]
            self.music[curr_song] = pygame.mixer.Sound("../audio/" + song)
        if DEBUG:
            print("Finished loading music")
        return
    
    def loadFonts(self, font_list):
        if DEBUG:
            print("Loading fonts")
        self.fonts = {}
        for curr_font in font_list:
            font = font_list[curr_font]
            self.fonts[curr_font] = pygame.font.Font('../misc/' + font["file"],font["size"])
        if DEBUG:
            print("Finished loading fonts")
        return
    
    def loadSound(self, sound_list):
        if DEBUG:
            print("Loading sounds")
        self.sounds = {}
        for curr_sound in sound_list:
            sound = sound_list[curr_sound]
            self.sounds[curr_sound] = pygame.mixer.Sound("../audio/" + sound)
        if DEBUG:
            print("Finished loading sound")
        return
    
    def play(self):
        if DEBUG:
            print("Playing " + self.cs["name"])
        skip = False
        pygame.mixer.stop()
        for step_num in range(1, len(self.cs["steps"]) + 1):
            if DEBUG:
                print("  Playing step " + str(step_num))
            step = self.cs["steps"][str(step_num)]
            if step["type"] == "playMusic":
                skip = self.playMusic(step["data"])
            elif step["type"] == "playRestOfMusic":
                skip = self.playRestOfMusic(step["data"])
            elif step["type"] == "fadeTextIn":
                skip = self.fadeTextIn(step["data"])
            elif step["type"] == "delay":
                skip = self.delay(step["data"])
            elif step["type"] == "playSound":
                skip = self.playSound(step["data"])
            elif step["type"] == "displayCenterImage":
                skip = self.displayCenterImage(step["data"])
            elif step["type"] == "clearScreen":
                skip = self.clearScreen(step["data"])
            if skip:
                break
        
        pygame.mixer.stop()
        if DEBUG:
            print("Done playing cutscene " + self.cs["name"])
            print(" ")
        return
    
    def wannaSkip(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == self.skip_key:
                    return True
        return False
    
    def centerSurfaceAt(self, text, pos):
        rect = text.get_rect()
        return (pos[0] - rect.w / 2, pos[1] - rect.h / 2)
    
    def playMusic(self, step):
        if DEBUG:
            print("    Playing music")
        chn = pygame.mixer.Channel(step["channel"])
        chn.play(self.music[step["name"]])
        if DEBUG:
            print("    Done playing music")
        return self.wannaSkip()
    
    def playRestOfMusic(self, step):
        if DEBUG:
            print("    Playing the rest of the music")
        chn = pygame.mixer.Channel(step["channel"])
        while chn.get_busy():
            if self.wannaSkip():
                return True
        if DEBUG:
            print("    Done playing the rest of the music")
        return False
    
    def fadeTextIn(self, step):
        if DEBUG:
            print("    Fading in text")
        old_surf = pygame.surface.Surface((800,600))
        old_surf.blit(self.game_window, (0,0))
        delta = round(step["time"] / 256)
        font = self.fonts[step["font"]]
        text_surf = font.render(self.cs["text"][step["text"]], True, tuple(step["color"]))
        pos = self.centerSurfaceAt(text_surf, step["pos"])
        for alpha in range(0, 256):
            text_surf.set_alpha(alpha)
            self.game_window.blit(old_surf, (0,0))
            self.game_window.blit(text_surf, pos)
            pygame.display.update()
            pygame.time.delay(delta)
        if DEBUG:
            print("    Done fading in text")
        return False
    
    def delay(self, step):
        if DEBUG:
            print("    Starting delay.")
        for i in range(0, step["time"]):
            if self.wannaSkip():
                return True
            pygame.time.delay(1)
        if DEBUG: 
            print("    Finished delay")
        return False
    
    def displayCenterImage(self, step):
        if DEBUG:
            print("    Displaying image " + step["img"])
        img = self.images[step["img"]]
        pos = self.centerSurfaceAt(img, step["pos"])
        self.game_window.blit(img,pos)
        pygame.display.update()
        if DEBUG:
            print("    Finish displaying image " + step["img"])
        return self.wannaSkip()
    
    def playSound(self, step):
        if DEBUG:
            print("    Start playing " + step["sound"])
        chn = pygame.mixer.Channel(step["channel"])
        chn.play(self.sounds[step["sound"]])
        if DEBUG:
            print("    Now playing " + step["sound"])
        return self.wannaSkip()
    
    def clearScreen(self, step):
        if DEBUG:
            print("    Start clear screen")
        self.game_window.fill(step["color"])
        pygame.display.update()
        if step["save"]:
            self.drawOrder = []
        if DEBUG:
            print("    Finish clear screen")
        return self.wannaSkip()