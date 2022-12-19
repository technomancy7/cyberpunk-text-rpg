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
        
        #self.draw_text(20, 30, "Field/tile display")
        #self.draw_text(400, 30, "Stats/info/controls")

        #self.write(3, 9, "Test BitMap font sentence")
        #self.write(3, 10, "ALLCAPS TEST 0123456789")

        # text log display
        size = 128 # Size of the text log box
        height = self.cfg["winsize"][1]-size
        width = self.cfg["winsize"][0]
        if self.selected_console:
            pygame.draw.rect(self.screen,(255,0,0), (0, height, width, size), 3)
        else:
            pygame.draw.rect(self.screen,(255,255,255), (0, height, width, size), 3)
        text_input_size = 25
        ln = self.text_input_ln
        self.draw_text(5, self.cfg["winsize"][1]-text_input_size, f"> {ln}", size=text_input_size)

        limit = 5
        current = 0
        log_size = text_input_size-5
        loc = self.cfg["winsize"][1]-text_input_size-log_size
        for msg in reversed(self.msg_history):
            colour = (255, 255, 255)
            if current == limit-3:
                colour = (255, 255, 255, 5) #(255, 255, 255, 150)

            if current == limit-2:
                colour = (255, 255, 255, 200)

            if current == limit:
                colour = (255, 255, 255, 255)

            #print(msg, colour)
            self.draw_text(5, loc, f"* {msg}", size=log_size, colour=colour)
            loc -= log_size
            current += 1
            if current >= limit:
                break


        # field display
        player = self.get_entity(self.player)
        #print("player", player)
        if player == None: 
            print("ERROR: PLAYER NOT FOUND")
        else:
            cur_loc = self.get_zone(player["location"])
            if cur_loc == None:
                print("ERROR: PLAYER NOT IN VALID ZONE")
            else:
                for tile in cur_loc["map"]:
                    xy = tile[0]
                    tiles = tile[1]
                    for spr in tiles:
                        self.draw_arbitrary(xy, spr)

                self.draw_entity(player)
                for entity in self.entities:
                    if not entity["hidden"] and entity["sprite"] and entity["location"] == cur_loc["tag"]:
                        self.draw_entity(entity)

        pygame.draw.rect(self.screen, (125,255,255), (0, 0, height, height), 3)

class Main(objects.JEState, JEScreens, objects.JECommand):
    def draw_arbitrary(self, xy, spr):
        real_x = xy[0] * self.tile_size
        real_y = xy[1] * self.tile_size
        spr = self.sprites.get(spr, None)
        if spr == None:
            print("ERROR: SPRITE FOR ARBITRARY CALL MISSING")
        else:
            self.screen.blit(spr, (real_x, real_y))

    def draw_entity(self, entity):
        real_x = entity["x"] * self.tile_size
        real_y = entity["y"] * self.tile_size
        spr = self.sprites.get(entity["sprite"], None)
        if spr == None:
            print("ERROR: SPRITE FOR", entity["tag"], "MISSING")
        else:
            self.screen.blit(spr, (real_x, real_y))

    def write(self, x, y, text):
        length = range(len(text))
        
        for i in length:
            ch = text[i]

            # don't blit if it's a space
            if ch == ' ':
                x += 1
                continue
            
            # character sheet starts at '!'
            id = ord(ch) - 33
            self.sprite_draw(self.bitmap_font, x * 8, y * 8, 8, 8, id)
            x += 1

    def sprite_draw(self, image, x, y, width, height, id):
        source_x = (id % 8) * width
        source_y = (id // 8) * height
        self.screen.blit(image, (x, y), (source_x, source_y, width, height))

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
            myfont = pygame.font.Font(self.font_file, size)

        # apply it to text on a label
        label = myfont.render(text, 1, colour)

        # put the label object on the screen at point
        self.screen.blit(label, (x, y))
        
    def set_bg(self, colour, speed = None):
        if speed: self.bg_shift_speed = speed
        self._proxy_bg_colour = colour

    def shift_bg(self, speed = None):
        if speed: self.bg_shift_speed = speed
        
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

    def build_world(self):
        # Build the default world
        # @todo saving/loading state
        self.variables = {}
        self.entities = []
        self.zones = []
        
        self.player = "player"
        
        self.entities.append(self._entity(tag="player", sprite="player", x=2, y=2, location="the_bar"))
        self.entities.append(self._entity(tag="savepoint", sprite="circle", x=6, y=6, location="the_bar"))

        self.zones.append(self._zone(name="The Bar", tag="the_bar", contains=["player"]))

        for x in range(11):
            for y in range(11):
                self.zones[0]["map"].append([[x, y], ["wood"]])

    def __init__(self):
        # Variable for the current "scene", which handles the current screen rendering
        self.current_scene = self.main_scene
        self.selected_console = False
        self.font_file = "font/term.ttf"
        self.bitmap_font = pygame.image.load('img/system/font.bmp')
        self.cfg = {}
        self.sprites = {
            "player": pygame.image.load("img/char/hero.png"),
            "circle": pygame.image.load("img/char/save.png"),
            "wood": pygame.image.load("img/tiles/wood.png"),
        }

        self.tile_size = 32
        self.bg_colour = [0, 0, 0]
        self._proxy_bg_colour = [0, 0, 0]
        self.bg_shift_speed = 0.2

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

        self.build_world()
        # text
        self.text_buffer = []
        self.text_input_ln = ""
        self.msg_history = []

    def refresh_text_input(self):
        self.text_input_ln = "".join(self.text_buffer)

    def handle_key_down(self, event):
        #print("\n\n", event.unicode, event.key, event)
        if self.can_input():
            if event.key == 9:
                self.selected_console = not self.selected_console

            if self.selected_console:
                if event.key == 13:
                    current_cmd = self.text_input_ln
                    self.text_buffer.clear()
                    self.refresh_text_input()
                    self.msg_history.append(current_cmd)
                    self.parse_command(current_cmd)

                if(event.unicode):
                    if event.key != 13 and event.key != 9 and event.key != 8:
                        self.text_buffer.append(event.unicode)
                        self.refresh_text_input()

                if event.key == 8:
                    self.text_buffer.pop()
                    self.refresh_text_input()

            else:
                if event.unicode == "w" or event.scancode == 82:
                    self.move_player("u")
                        
                if event.unicode == "s" or event.scancode == 81:
                    self.move_player("d")

                if event.unicode == "a" or event.scancode == 80:
                    self.move_player("l")

                if event.unicode == "d" or event.scancode == 79:
                    self.move_player("r")

    def move_entity(self, e, d):
        e["direction"] = d
        if d == "u":
            if e["y"] > 0:
                e["y"] -= 1

        if d == "d":
            if e["y"] < 10:
                e["y"] += 1

        if d == "r":
            if e["x"] < 10:
                e["x"] += 1

        if d == "l":
            if e["x"] > 0:
                e["x"] -= 1

    def move_player(self, d):
        player = self.get_entity(self.player)
        if player != None:
            self.move_entity(player, d)

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
