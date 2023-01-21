import pygame

class World:
    def build_world(self):
        print("Building coreworld")
        # Build the default world

        # Refresh world state
        self.refresh_state()
        self.init_etos()
        # SETUP PLAYER
        self.player = "player"
        self._entity(tag = "player", sprite = "player", x = 2, y = 2, alliance = "player", 
                        name = "The Player", manual_control = True)

        # ZONE 1: THE BAR
        self._zone(name="The Bar", tag="the_bar")
        self.set_zone("player", "the_bar")

        src_pistol = self._entity(tag="pistol", sprite="circle", name="9mm Pistol", solid=False, 
            properties=["inventory", "combat"], slot = "weapon", weight=1, x=6, y=6,
            description="""A basic old-world pistol, barely<br>functional.""")

        self.set_data(src_pistol, "ammo", 9)


        self.set_zone(self.clone_entity(src_pistol), "the_bar")


        src_ck = self._entity(tag="knife", sprite="circle", name="Knife", solid=False, 
            properties=["inventory", "combat"], slot = "weapon", weight=1, x=6, y=6,
            description="""A basic old-world knife, barely<br>functional.""")

        self.set_container(self.clone_entity(src_ck), self.player)

        src_medkit = self._entity(tag="medkit", sprite="circle", x=6, y=6, name="Medkit", solid=False, 
            properties=["inventory"], weight=1, events={"use": "use_item"},
            description="A set of medical supplies.")

        md = self.clone_entity("medkit")
        self.set_zone(md, "the_bar", x=7, y=6)

        c = self._entity(tag="communicator", sprite="circle", x=3, y=3, name="Communicator", solid=False, 
            properties=["inventory", "quest"], weight=1, events={"use": "use_com"},
            description="A communication device.")
        self.set_zone(c, "the_bar")

        def com_screen(main):
            self.write_bmp(50, 1, f"Communicator v0.1")


        def use_com(**args):
            self.new_status_screen(com_screen)

        self.global_functions["use_com"] = use_com
        
        jy = 3
        jnk = self._entity(tag=f"junk", sprite="circle", x=0, y=jy, name="Junk", solid=False, 
            properties=["inventory"], weight=1, events={"use": "use_item"},
            description="Some junk.")
            
        self.set_zone(jnk, "the_bar")

        for junk in range(0, 5):
            nj = self.clone_entity(jnk)
            jy += 1
            self.set_zone(nj, "the_bar", x=0, y=jy)


        dmmy = self._entity(tag="target_dummy", sprite="circle", x=2, y=6, name="target dummy")
        dmmy["ai_scripts"]["field"] = ["l", "r"]
        self.set_hostility(dmmy, "player", -1)
        dmmy["barks"]["bump"] = ["Hey!", "Watch it!", "This is a very long message that will hopefully be split properly in the message history, idk tho."]
        self.set_zone(dmmy, "the_bar")
        self.set_event(dmmy, "bumped", "start_combat")
        self.set_container(self.clone_entity(src_ck), dmmy)

        ep = self._entity(tag="bar_out_exit", sprite="circle", x=7, y=0, name="Exit to street", solid=False)
        ep['data']['exit'] = {"map": "the_street", "pos": [2, 2]}
        self.set_zone("bar_out_exit", "the_bar")
        self.set_event(ep, "on_player", "teleport")
        

        for x in range(11):
            for y in range(11):
                self.zones[0]["map"].append([[x, y], ["wood"]])

        #self.push_dialog("Intro", "This is an intro! This dialog box is for testing purposes. I wonder if it'll even work, who knows really.")
        #self.push_dialog("Intro", "Now get out there and test stuff!")

        self._zone(name="The Streets", tag="the_street")
        ep2 = self._entity(tag="bar_entr", sprite="circle", x=7, y=0, name="To Bar", solid=False)
        ep2['data']['exit'] = {"map": "the_bar", "pos": [7, 1]}
        self.set_zone("bar_entr", "the_street")
        self.set_event(ep2, "on_player", "teleport")

        self.add_timer("test", lambda s: print("Test timer!!"), 4)

        if self.cfg.get("skip_intro", False) == True:
            self.variables['progress'] = 4
            self.switch_to_main_scene()
            self.add_goal(tag="tutorial", message="Beat up the training dummy.")
        else:
            self.new_generic_event("intro")
            pygame.time.set_timer(self.global_functions["intro"], 1000, 1)
            self.variables["progress"] = 0

    def intro_scene(self):
        if self.variables['progress'] == 0:
            self.log("! DETECTED ETOS [ACTIVATE] SIGNAL")
            pygame.time.set_timer(self.global_functions["intro"], 1000, 1)
            self.variables['progress'] = 1

        elif self.variables['progress'] == 1:
            self.log("! Scanning filesystem...")
            self.log("! Connected to databases [ETOS_SYS, SELF, WORLD, PERCEPTION, INTERFACE]...")
            self.log("! Validating system files...")
            self.log("! Enabling neural input...")
            pygame.time.set_timer(self.global_functions["intro"], 2000, 1)
            self.variables['progress'] = 2

        elif self.variables['progress'] == 2:
            self.log("! ERROR: Profile data was corrupt, factory reset required.")
            self.log("? Would you like to create a new profile, or attempt to load existing?")
            self.log("Valid responses: new, load, quit")
            #pygame.time.set_timer(self.global_functions["intro"], 1000, 1)
            self.wait_for_reply(self.intro_scene_prompt)

        elif self.variables['progress'] == 3:
            self.log("? What is your name?")
            self.variables['progress'] = 4
            self.wait_for_reply(self.intro_scene_prompt)

    def intro_scene_prompt(self, ln):
        if self.variables['progress'] == 2 and ln == "new":
            self.log("Creating new profile...")
            self.variables['progress'] = 3
            pygame.time.set_timer(self.global_functions["intro"], 1000, 1)
            self.wait_for_reply(None)
        
        if self.variables['progress'] == 4:
            self.player_object["name"] = ln
            self.log(f"Name: {self.player_object['name']}")
            self.log(f"Setup complete. (Full setup not yet implemented.)")
            self.log("Activating field screen...")
            self.switch_to_main_scene()
            self.wait_for_reply(None)
            self.add_goal(tag="tutorial", message="Beat up the training dummy.")
