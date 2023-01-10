#!/usr/bin/env python3

import json

import importlib
import os
import sys, random
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

app_path = os.path.dirname(os.path.realpath(__file__))+"/"
print(app_path)
sys.path.append(app_path)


from sys import platform
print(f"Platform is... {platform}")

if platform == "linux" or platform == "linux2":
    sys.path.append(app_path+"py-linux/libraries/")
    print("Local library path defined: ", app_path+"py-linux/libraries/")
elif platform == "darwin":
    print("Testing local libraries on OSX not supported yet. Trying global instead.")
elif platform == "win32":
    sys.path.append(app_path+"winpy32/libraries/")
    print("Local library path defined: ", app_path+"winpy32/libraries/")
elif platform == "win64":
    sys.path.append(app_path+"winpy64/libraries/")
    print("Local library path defined: ", app_path+"winpy64/libraries/")

try:
    import pygame
except:
    if platform == "linux" or platform == "linux2":
        sys.path.append(app_path+"py-linux/libraries/")
        os.system(f"bash {app_path}/install_linux.sh")
        os.system(f"bash {app_path}/run_linux.sh")
        quit()
    elif platform == "darwin":
        print("Importing pygame failed and automatic fixing isn't supported on OSX yet.")
    elif platform == "win32":
        print("Importing pygame failed and automatic fixing isn't supported on win32 yet.")
    else:
        print(f"Importing pygame failed and automatic fixing isn't supported on {platform} yet.")

#import pygame.base

# Import engine modules
import state, screens, commands, gui, templates, etos, engineio

world_name = "coreworld" #@todo command line argument to swap out world
world = importlib.import_module("worlds."+world_name)
#import coreworld as world

class Main(state.JEState, screens.JEScreens, commands.JECommand, gui.JEGUI, templates.JETemplates, 
            world.World, etos.EternalTerminal, engineio.JEIO):
    def __init__(self, *, autobuild_world = False):
        # initialize the pygame module
        pygame.init()
        pygame.font.init()

        # Location the current script file is located in
        # Acts as home for any files related to this project
        self.app_path = os.path.dirname(os.path.realpath(__file__))+"/"

        # Variable for the current "scene", which handles the current screen rendering
        self.buttons = []
        self.mouse_zones = []

        self.current_scene = None
        #self.switch_to_main_scene()
        self.switch_to_fst()
        self.cfg = {}
        self.selected_console = False
        #self.status_screen = "stats"
        self.switch_status_scene("stats")

        # fonts
        self.font_file = "term.ttf"
        self.bitmap_font = pygame.image.load(f'{self.app_path}img/system/font.bmp')
        
        # sprite index
        self.sprites = {
            "player": pygame.image.load(f"{self.app_path}img/char/hero.png"),
            "circle": pygame.image.load(f"{self.app_path}img/char/save.png"),
            "wood": pygame.image.load(f"{self.app_path}img/tiles/wood.png"),
            "diamond": pygame.image.load(f"{self.app_path}img/system/diamond.png"),
            "diamond_dark": pygame.image.load(f"{self.app_path}img/system/diamond_dark.png"),
        }

        # global values
        self.spr_move_speed     = 4
        self.tile_size          = 32
        self.field_size         = 10
        self.bg_colour          = [0, 0, 0]
        self._proxy_bg_colour   = [0, 0, 0]
        self.bg_shift_speed     = 0.2
        self.input_disabled     = False

        self.ttext1 = [255, 255, 255]
        self.ttext2 = [205, 205, 205]
        self.ttext3 = [175, 175, 175]
        self.ttext4 = [125, 125, 125]

        self.rebind_keyname = ""
        self.unbinding = ""
        self.appending_bind = False
        self.print_key = False

        # load system config
        with open(f"{self.app_path}config.json", "r+") as f:
            self.cfg = json.load(f)
            
        # load and set the logo and set title name
        #logo = pygame.image.load("logo32x32.png")
        #pygame.display.set_icon(logo)
        pygame.display.set_caption("WIP")

        # create a surface on screen
        self.screen = pygame.display.set_mode(self.cfg["winsize"], pygame.SCALED|pygame.RESIZABLE)

        self.init_commands()

        # define a variable to control the main loop
        self.running = True


        # State values
        self.refresh_state()
        
        self.combat_data = {
            "entities": [], #list of entities participating in the current combat scene
            "turns": 0, #current number of turns
            "active": False, #is combat currently active, can be turned off to pause a battle
        }

        self.selected_inventory = ""
        self.inventory_menu_labels = []

        self.init_globals()

        # Global deltatime
        self.dt         = 0.0
        self.raw_ticks  = 0
        self.seconds    = 0
        self.clock      = pygame.time.Clock()
        self.ticks      = {}

        # containers for the text input system
        self.text_buffer        = []
        self.text_input_ln      = ""
        self.text_input_history = []
        self.text_input_pointer = 0
        self.msg_history        = []
        self.msg_history_proxy  = []
        self.log_size_limit     = 45

        # Dialog box
        self.dialog_box         = None
        self.dialog_stack       = []
        self.dialog_msg_proxy   = ""

        self.goals = []
    
        self.mouse_zones.append({"top_left": 370,      "top_right": 422,
                        "bottom_left": 8, "bottom_right": 25,
                        "group": "status_ui",
                        "button": 1,                "payload": {"status": "stats"},
                        "callback": self.core_mz_callback})


        self.mouse_zones.append({"top_left": 424,      "top_right": 512,
                        "bottom_left": 8, "bottom_right": 25,
                        "group": "status_ui",
                        "button": 1,                "payload": {"status": "inventory"},
                        "callback": self.core_mz_callback})

        self.mouse_zones.append({"top_left": 530,      "top_right": 582,
                        "bottom_left": 8, "bottom_right": 25,
                        "group": "status_ui",
                        "button": 1,                "payload": {"status": "goals"},
                        "callback": self.core_mz_callback})                

        self.terminal_prompt = None
        # build the default world
        if(autobuild_world): self.build_world()

    def save_config(self):
        with open(f"{self.app_path}config.json", "w+") as f:
            json.dump(self.cfg, f, indent=4)

    def wait_for_reply(self, fn):
        self.terminal_prompt = fn

    
    def refresh_state(self):
        self.variables  = {}
        self.entities   = []
        self.zones      = []
        self.virtual_fs = []
        self.variables.update(self.cfg.get("auto", {}))

    def add_goal(self, tag, message, **opts):
        if not self.has_goal(tag):
            #@todo in goals list, sort by tier
            goal = {"tag": tag, "message": message, "completed": False, "active": True, "stage": 0, "tier": 0}
            goal.update(**opts)
            self.goals.append(goal)
            self.log("New goal added.")
            self.log(" = = = = =")
            self.log(f"{message}")
            self.log(" = = = = =")

    def edit_goal(self, tag, **opt):
        g = self.get_goal(tag)
        if g != None:
            g.update(**opt)

    def get_goal(self, tag):
        for goal in self.goals:
            if goal['tag'] == tag:
                return goal
        return None

    def has_goal(self, tag):
        for goal in self.goals:
            if goal['tag'] == tag:
                return True
        return False

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
        return not self.input_disabled

    def write_text(self, x, y, text, *, fontfile = "", sysfont = "", size = 30, colour=(255, 255, 255)):
        # pick a font you have and set its size
        myfont = None

        if sysfont: # if specified a system font
            myfont = pygame.font.SysFont(sysfont, size)

        elif fontfile: # else if specified a font file
            myfont = pygame.font.Font(self.app_path+"font/"+fontfile, size)

        else: # else default to internal
            myfont = pygame.font.Font(self.app_path+"font/"+self.font_file, size)

        # apply it to text on a label
        label = myfont.render(text, 1, colour)

        # put the label object on the screen at point
        self.screen.blit(label, (x, y))

    @property
    def active_zone(self):
        return self.player_object['location']

    @property
    def active_zone_object(self):
        return self.get_zone(self.active_zone)
        
    @property
    def player_object(self):
        if self._player == None:
            self._player = self.get_entity(self.player)

        return self._player

    @property
    def player(self):
        return self.variables.get("focus", None)

    @player.setter
    def player(self, new_player):
        self.variables["focus"] = new_player
        self._player = self.get_entity(new_player)
        print("player updated...", new_player)

    def global_timer(self):
        # called every second (roughly)
        pass

    def global_tick(self, dt):
        # add deltatime (delay between last frame in milliseconds) to overall counter
        self.dt         += dt
        self.raw_ticks  += 1

        if self.raw_ticks % 1 == 0:
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

    def new_generic_event(self, name):    
        self.global_functions[name] = pygame.USEREVENT+len(self.global_functions.keys())

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

                if event.type == self.global_functions.get("intro"):
                    self.intro_scene()
            
            
            self.current_scene()

            self.global_tick((self.clock.tick(self.variables.get("fps_limit", 60))/1000)%60)

            # Updates the display
            pygame.display.flip()

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    runtime = Main()
    runtime.build_world()
    runtime.loop()
