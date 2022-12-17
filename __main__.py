#!/usr/bin/env python

# import the pygame module, so you can use it
import pygame
import json
import objects

class JEScreens:
    def main_scene(self):
        # Background colour
        self.screen.fill(self.bg_colour)
        self.shift_bg()
        
        
        size = 200 # Size of the text log box
        height = self.cfg["winsize"][1]-size
        width = self.cfg["winsize"][0]
        pygame.draw.rect(self.screen,(0,255,255), (0, height, width, size), 3)
        

        pygame.draw.rect(self.screen, (125,255,255), (0, 0, 300, height), 3) 
        
        
        self.draw_text(20, 30, "Field/tile display")
        self.draw_text(400, 30, "Stats/info/controls")


        # Text log and input
        text_input_size = 25
        ln = self.text_input_ln
        self.draw_text(5, self.cfg["winsize"][1]-text_input_size, f"> {ln}", size=text_input_size)

        limit = 8
        current = 0
        log_size = text_input_size-5
        loc = self.cfg["winsize"][1]-text_input_size-log_size
        for msg in reversed(self.msg_history):
            colour = (255, 255, 255)
            if current == 5:
                colour = (222, 222, 222)

            if current == 6:
                colour = (180, 180, 180)

            if current == 7:
                colour = (150, 150, 150)

            self.draw_text(5, loc, f"* {msg}", size=log_size, colour=colour)
            loc -= log_size
            current += 1
            if current >= limit:
                break

class Main(objects.JEState, JEScreens, objects.JECommand):
    def can_input(self) -> bool:
        if self.current_scene == self.main_scene: return True
        return False

    def draw_text(self, x, y, text, *, fontfile = "", sysfont = "", size = 30, colour=(255, 255, 255)):
        # pick a font you have and set its size
        myfont = None

        if sysfont: # if specified a system font
            myfont = pygame.font.SysFont(sysfont, size)

        elif fontfile: # else if specified a font file
            myfont = pygame.font.Font(fontfile, size)

        else: # else default to internal
            myfont = pygame.font.Font(self.FONT_FILE, size)

        # apply it to text on a label
        label = myfont.render(text, 1, colour)

        # put the label object on the screen at point
        self.screen.blit(label, (x, y))
        
    def set_bg(self, colour, speed = None):
        if speed: self.bf_shift_speed = speed
        self._proxy_bg_colour = colour

    def shift_bg(self):
        if self.bg_colour[0] < self._proxy_bg_colour[0]:
            self.bg_colour[0] += self.bg_shift_speed

        if self.bg_colour[0] > self._proxy_bg_colour[0]:
            self.bg_colour[0] -= self.bg_shift_speed

        if self.bg_colour[1] < self._proxy_bg_colour[1]:
            self.bg_colour[1] += self.bg_shift_speed

        if self.bg_colour[1] > self._proxy_bg_colour[1]:
            self.bg_colour[1] -= self.bg_shift_speed

        if self.bg_colour[2] < self._proxy_bg_colour[2]:
            self.bg_colour[2] += self.bg_shift_speed

        if self.bg_colour[2] > self._proxy_bg_colour[2]:
            self.bg_colour[2] -= self.bg_shift_speed

    def __init__(self):
        # Variable for the current "scene", which handles the current screen rendering
        self.current_scene = self.main_scene
        self.FONT_FILE = "term.ttf"
        self.cfg = {}
        self.bg_colour = (0, 0, 0)
        self._proxy_bg_colour = (0, 0, 0)
        self.bf_shift_speed = 0.2

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

        # text
        self.text_buffer = []
        self.text_input_ln = ""
        self.msg_history = []

    def refresh_text_input(self):
        self.text_input_ln = "".join(self.text_buffer)

    def handle_key_down(self, event):
        if(event.unicode):
            #print(event)
            #print(event.unicode)
            if self.can_input():
                if event.key == 13:
                    #print("Sending")
                    current_cmd = self.text_input_ln
                    self.text_buffer.clear()
                    self.refresh_text_input()
                    self.msg_history.append(current_cmd)
                    self.parse_command(current_cmd)

                if event.key != 13 and event.key != 9 and event.key != 8:
                    #print("Appending")
                    self.text_buffer.append(event.unicode)
                    self.refresh_text_input()

                if event.key == 8:
                    #print("Backspace")
                    #self.text_buffer.remove(self.text_buffer[-1])
                    self.text_buffer.pop()
                    self.refresh_text_input()

    def loop(self):

        # main loop
        while self.running:
            # event handling, gets all event from the eventqueue
            for event in pygame.event.get():
                # only do something if the event if of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    self.handle_key_down(event)

            
            
            self.current_scene()
            
            # Updates the display
            pygame.display.flip()

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    runtime = Main()
    runtime.loop()
