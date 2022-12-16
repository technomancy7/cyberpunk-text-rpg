#!/usr/bin/env python

# import the pygame module, so you can use it
import pygame
import json
import objects


# define a main function
class Main:
    def draw_text(self, x, y, text, *, font = "Comic Sans MS", size = 30, colour=(255, 255, 255)):
        # pick a font you have and set its size
        myfont = pygame.font.SysFont(font, size)
        # apply it to text on a label
        label = myfont.render(text, 1, colour)
        # put the label object on the screen at point x=100, y=100
        self.screen.blit(label, (x, y))

    def main_screen(self):
        # Background colour
        self.screen.fill((0,0,0))
        
        
        size = 200 # Size of the text log box
        height = self.cfg["winsize"][1]-size
        width = self.cfg["winsize"][0]
        pygame.draw.rect(self.screen,(0,255,255), (0, height, width, size), 3)
        

        pygame.draw.rect(self.screen, (125,255,255), (0, 0, 300, height), 3) 
        
        
        self.draw_text(20, 30, "Field/tile display")
        self.draw_text(400, 30, "Stats/info/controls")
        self.draw_text(20, 300, "Text log")
        
    def __init__(self):
        # Variable for the current "scene", which handles the current screen rendering
        self.current_scene = self.main_screen
        
        self.cfg = {}
        with open("config.json", "r+") as f:
            self.cfg = json.load(f)
            
        # initialize the pygame module
        pygame.init()
        pygame.font.init()
        
        # load and set the logo
        #logo = pygame.image.load("logo32x32.png")
        #pygame.display.set_icon(logo)
        pygame.display.set_caption("WIP")

        # create a surface on screen
        self.screen = pygame.display.set_mode(self.cfg["winsize"])

        # define a variable to control the main loop
        self.running = True


        # State values
        self.variables = {}
        self.entities = []
        self.zones = []
        
    def loop(self):

        # main loop
        while self.running:
            # event handling, gets all event from the eventqueue
            for event in pygame.event.get():
                # only do something if the event if of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    self.running = False

            
            
            self.current_scene()
            
            # Updates the display
            pygame.display.flip()

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    runtime = Main()
    runtime.loop()
