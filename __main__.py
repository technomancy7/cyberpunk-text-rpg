#!/usr/bin/env python

# import the pygame module, so you can use it
import pygame
import json
import state, screens, commands, world
import os
import sys, random

class Main(state.JEState, screens.JEScreens, commands.JECommand, world.ElysiumWorld):
    def screen_to_tile(self, xy):
        real_x = int(xy[0] / self.tile_size)
        real_y = int(xy[1] / self.tile_size)
        return [real_x, real_y]

    def tile_to_screen(self, xy):
        real_x = xy[0] * self.tile_size
        real_y = xy[1] * self.tile_size
        return [real_x, real_y]

    def draw_button(self, xy, spr, spr_highlight):
        pass

    def draw_arbitrary_precise(self, xy, spr):
        real_x = xy[0]
        real_y = xy[1]
        spr = self.sprites.get(spr, None)
        if spr == None:
            print("ERROR: SPRITE FOR ARBITRARY CALL MISSING")
        else:
            self.screen.blit(spr, (real_x, real_y))

    def draw_entity_precise(self, entity):
        real_x = entity["screen_x"]
        real_y = entity["screen_y"]
        spr = self.sprites.get(entity["sprite"], None)
        if spr == None:
            print("ERROR: SPRITE FOR", entity["tag"], "MISSING")
        else:
            self.screen.blit(spr, (real_x, real_y))

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

    def write_bmp(self, x, y, text, *, precise = False):
        length = range(len(text))

        for i in length:
            ch = text[i]

            # don't blit if it's a space
            if ch == ' ':
                x += 1
                continue
            
            # character sheet starts at '!'
            id = ord(ch) - 33
            if not precise:
                self.fbmp(self.bitmap_font, x * 8, y * 8, 8, 8, id)
            else:
                self.fbmp(self.bitmap_font, x, y, 8, 8, id)
            x += 1

    def fbmp(self, image, x, y, width, height, id):
        source_x = (id % 8) * width
        source_y = (id // 8) * height
        self.screen.blit(image, (x, y), (source_x, source_y, width, height))

    def can_input(self) -> bool:
        if self.current_scene == self.main_scene: return True
        if self.current_scene == self.fullscreen_terminal_scene: return True
        return False

    def write_text(self, x, y, text, *, fontfile = "", sysfont = "", size = 30, colour=(255, 255, 255)):
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

    @property
    def player(self):
        return self.variables.get("focus", None)

    @player.setter
    def player(self, new_player):
        self.variables["focus"] = new_player

    def switch_to_fst(self):
        self.buttons = []
        self.current_scene = self.fullscreen_terminal_scene


    def switch_to_main_scene(self):
        self.current_scene = self.main_scene
        self.buttons = [
            {
                "pos": [12, 9], 
                "spr": "diamond_dark", 
                "spr_hl": "diamond", 
                "on_click": lambda: self.move_player("u")
            }, 
            {
                "pos": [11, 10], 
                "spr": "diamond_dark", 
                "spr_hl": "diamond",
                "on_click": lambda: self.move_player("l")
            },
            {
                "pos": [12, 10], 
                "spr": "diamond_dark", 
                "spr_hl": "diamond",
                "on_click": lambda: self.move_player("d")
            },
            {
                "pos": [13, 10], 
                "spr": "diamond_dark", 
                "spr_hl": "diamond",
                "on_click": lambda: self.move_player("r")
            },
        ]

    def __init__(self):
        # initialize the pygame module
        pygame.init()
        pygame.font.init()

        # Location the current script file is located in
        # Acts as home for any files related to this project
        self.app_path = os.path.dirname(os.path.realpath(__file__))+"/"

        # Variable for the current "scene", which handles the current screen rendering
        self.current_scene = None
        self.switch_to_main_scene()
        self.cfg = {}
        self.selected_console = False
        
        # fonts
        self.font_file = "font/term.ttf"
        self.bitmap_font = pygame.image.load(f'{self.app_path}img/system/font.bmp')
        
        # sprite index
        self.sprites = {
            "player": pygame.image.load(f"{self.app_path}img/char/hero.png"),
            "circle": pygame.image.load(f"{self.app_path}img/char/save.png"),
            "wood": pygame.image.load(f"{self.app_path}img/tiles/wood.png"),
            "diamond": pygame.image.load(f"{self.app_path}img/system/diamond.png"),
            "diamond_dark": pygame.image.load(f"{self.app_path}img/system/diamond_dark.png"),
        }

        # consts
        self.spr_move_speed = 0.5
        self.tile_size = 32
        self.field_size = 10
        self.bg_colour = [0, 0, 0]
        self._proxy_bg_colour = [0, 0, 0]
        self.bg_shift_speed = 0.2

        self.ttext1 = [255, 255, 255]
        self.ttext2 = [205, 205, 205]
        self.ttext3 = [175, 175, 175]
        self.ttext4 = [125, 125, 125]

        # load system config
        with open("config.json", "r+") as f:
            self.cfg = json.load(f)
        
        # load and set the logo and set title name
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

        # Global deltatime
        self.dt = 0.0
        self.raw_ticks = 0
        self.seconds = 0
        self.clock = pygame.time.Clock()
        self.ticks = {}

        # containers for the text input system
        self.text_buffer = []
        self.text_input_ln = ""
        self.msg_history = []
        self.msg_history_proxy = []
        self.log_size_limit = 45


        # Dialog box
        self.dialog_box = None
        self.dialog_stack = []
        self.dialog_msg_proxy = ""

        # build the default world
        self.build_world()

    def push_dialog(self, speaker, message):
        self.dialog_stack.append([speaker, message])

    def log(self, txt):
        iters = 0
        # Send a message to the in-game terminal
        print(len(txt), "<", self.log_size_limit, "=", len(txt) <= self.log_size_limit)
        if len(txt) < self.log_size_limit:
            self.msg_history.append(txt)
            self.msg_history_proxy.append("")
        else:
            out = []
            while len(txt) >= self.log_size_limit:
                iters += 1
                newsplit = " ".join(txt[0:self.log_size_limit].split(" ")[:-1])
                txt = txt[len(newsplit):]
                self.msg_history.append(newsplit)
                self.msg_history_proxy.append("")
                if iters > 10:
                    print("EMERGENCY BREAK: Log message too big.")
                    break

            self.msg_history.append(txt)
            self.msg_history_proxy.append("")

    def refresh_text_input(self):
        # Refreshes the string of text used for the terminal input
        self.text_input_ln = "".join(self.text_buffer)

    def proceed_dialog(self):
        if len(self.dialog_stack) > 0:
            if self.dialog_msg_proxy != self.dialog_stack[0][1]:
                self.dialog_msg_proxy = self.dialog_stack[0][1]
            else:
                self.dialog_stack.remove(self.dialog_stack[0])
                self.dialog_msg_proxy = ""   
            return True
        return False

    def handle_mouse_down(self, event):
        # user clicked event
        if self.current_scene == self.main_scene: # handling main scene
            if event.button == 1: # left mouse click
                if self.proceed_dialog():
                    return

                # get mouse position and convert it to "tile" position
                pos = self.screen_to_tile(event.pos)

                # loop over our current list of buttons
                for button in self.buttons:
                    # get this buttons tile position
                    xy = button["pos"]

                    # mouse cursor is in same tile as the button
                    if pos == xy:
                        if button.get("on_click", None): # send to the buttons on_click event if it exists
                            button["on_click"]()


    def handle_key_down(self, event):
        # keyboard input
        if self.can_input(): # if user can press buttons right now
            if len(self.dialog_stack) > 0:
                if self.proceed_dialog():
                    return
                return

            if self.current_scene == self.main_scene and event.scancode == 58:
                self.switch_to_fst()
                return
            
            
            if self.current_scene == self.fullscreen_terminal_scene and event.scancode == 58:
                self.switch_to_main_scene()
                return

            if self.current_scene == self.main_scene and event.key == 9:
                self.selected_console = not self.selected_console

            if self.selected_console or self.current_scene == self.fullscreen_terminal_scene:
                if event.key == 13:
                    current_cmd = self.text_input_ln
                    if current_cmd != "":
                        self.text_buffer.clear()
                        self.refresh_text_input()
                        self.log("$ "+current_cmd)
                        self.parse_command(current_cmd)
                        if self.cfg.get("autoclose_prompt", False):
                            self.selected_console = False

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

    def collided(self, mover, target, direction = "u"):
        return self.bark(target, "bump")

    def bark(self, target, group = "ambient"):
        target = self.get_entity(target)
        barks = target.get("barks", {}).get(group, [])
        if len(barks) > 0:
            self.log(f"{target['name']}: {random.choice(barks)}")
            return True

    def move_entity(self, e, d):
        #@todo finish this
        #@todo once implemented, add a switch to use tank controls
        # forward, backward, strafe right, straight left
        # moves in directions relative to direction
        # does not rotate
        if d in ["fw", "bk", "sr", "sl"]:
            pass

        # rotate right, rotate left
        if d in ["rr", "rl"]:
            pass

        # face up, face down, face left, face right
        # turns in direction
        # does not move
        if d in ["fu", "fd", "fl", "fr"]:
            pass

        # up, down, left, right
        # move in directions relative to screen
        # rotates to direction
        if d in ["u", "d", "l", "r"]:
            e["direction"] = d
            if d == "u":
                collisions = self.collisions_at(e["x"], e["y"]-1)
                if len(collisions) > 0:
                    if not self.collided(e, collisions[0]): 
                        self.log(f"! You bumped in to {collisions[0]['name']}")
                else:
                    if e["y"] > 0:
                        e["y"] -= 1

            if d == "d":
                collisions = self.collisions_at(e["x"], e["y"]+1)
                if len(collisions) > 0:
                    if not self.collided(e, collisions[0]): 
                        self.log(f"! You bumped in to {collisions[0]['name']}")
                else:
                    if e["y"] < self.field_size:
                        e["y"] += 1

            if d == "r":
                collisions = self.collisions_at(e["x"]+1, e["y"])
                if len(collisions) > 0:
                    if not self.collided(e, collisions[0]): 
                        self.log(f"! You bumped in to {collisions[0]['name']}")
                else:
                    if e["x"] < self.field_size:
                        e["x"] += 1

            if d == "l":
                collisions = self.collisions_at(e["x"]-1, e["y"])
                if len(collisions) > 0:
                    if not self.collided(e, collisions[0]): 
                        self.log(f"! You bumped in to {collisions[0]['name']}")
                else:
                    if e["x"] > 0:
                        e["x"] -= 1

    def collisions_at(self, x, y):
        out = []
        for ent in self.entities:
            if ent["x"] == x and ent["y"] == y and ent["hidden"] == False and ent["solid"] == True:
                out.append(ent)
        return out

    def find_entities_at(self, x, y):
        out = []
        for ent in self.entities:
            if ent["x"] == x and ent["y"] == y:
                out.append(ent)
        return out

    def move_player(self, d):
        player = self.get_entity(self.player)
        if player != None:
            self.move_entity(player, d)

    def global_timer(self):
        # called every second (roughly)
        
        # typewriter effect
        pass

    def global_tick(self, dt):
        # add deltatime (delay between last frame in milliseconds) to overall counter
        self.dt += dt
        self.raw_ticks += 1

        if self.raw_ticks % 10 == 0:
            for i, val in enumerate(self.msg_history):
                if self.msg_history_proxy[i] != val:
                    self.msg_history_proxy[i] += val[len(self.msg_history_proxy[i])]

            if len(self.dialog_stack) > 0:
                msg = self.dialog_stack[0][1]
                if self.dialog_msg_proxy != msg:
                    self.dialog_msg_proxy += msg[len(self.dialog_msg_proxy)]

        # if it's been a second since the last run...
        if int(self.dt) != self.seconds:
            self.seconds = int(self.dt)
            self.global_timer()

        for k, v in self.ticks.items():
            v(self.dt, dt)


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

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_down(event)
            
            
            self.current_scene()

            self.global_tick((self.clock.tick()/1000)%60)

            # Updates the display
            pygame.display.flip()

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    runtime = Main()
    runtime.loop()
