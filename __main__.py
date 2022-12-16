#!/usr/bin/env python

# import the pygame module, so you can use it
import pygame
import json
import objects

# define a main function
def main():
    cfg = {}
    with open("config.json", "r+") as f:
        cfg = json.load(f)
        
    # initialize the pygame module
    pygame.init()
    
    # load and set the logo
    #logo = pygame.image.load("logo32x32.png")
    #pygame.display.set_icon(logo)
    pygame.display.set_caption("minimal program")
    
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode(cfg["winsize"])
    
    # define a variable to control the main loop
    running = True
    
    i = 0
    
    # main loop
    while running:
        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event if of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
    
        # TECHNO: test code to see if display is working
        i += 1
        if i >= 256: i = 0
        screen.fill((i,0,0))
        
        
        pygame.display.flip()
    
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
