import pygame, json

class JEIO:
    def handle_mouse_down(self, event):
        #print(event)
        # user clicked event
        if self.current_scene == self.main_scene: # handling main scene
            if event.button == 1: # left mouse click
                if self.proceed_dialog():
                    return

                #@todo add a version that checks boundaries of real screen coordinates
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

            for mz in self.mouse_zones:
                px = event.pos[0]
                py = event.pos[1]
                if px > mz["top_left"] and px < mz['top_right'] and py > mz['bottom_left'] and py < mz['bottom_right']:
                    #print(event.button == mz['button'], event.button, mz['button'])
                    if event.button == mz['button']:
                        #print(f"{event.pos} is inside {mz}")
                        mz['callback'](**mz['payload'])

    def delete_button(self, bid):
        for btn in self.buttons:
            if bid == btn.get('id', None):
                self.buttons.remove(btn)
                return

    def purge_mz(self, grp):
        self.mouse_zones = list(filter(lambda a: a['group'] != grp, self.mouse_zones))

    def mz_callback_inventory(self, **data):
        name = data['item']
        item = self.get_entity(name)
        print(f"Clicked inventory {name}")
        self.purge_mz("inv_item_menu")
        self.inventory_menu_labels = []
        self.selected_inventory = name

        modify_by       = 10
        top_left        = 545
        top_right       = 600
        bottom_left     = 55
        bottom_right    = 65
        
        def use_item(**args):
            evt = args['item']['events']['use']
            if self.global_functions.get(evt, None):
                #print("Pushing use item")
                self.global_functions[evt](item = args['item'])
            else:
                print(f"Event {evt} not registered")

        def null_cb(**args):
            pass

        if "use" in item['events'].keys():
            self.inventory_menu_labels.append("Use")
            self.mouse_zones.append({"top_left": top_left,      "top_right": top_right,
                                    "bottom_left": bottom_left, "bottom_right": bottom_right,
                                    "group": "inventory",
                                    "button": 1,                "payload": {"item": item},
                                    "callback": use_item})
            bottom_left     += modify_by
            bottom_right    += modify_by

        if "equip" in item['properties']: #@todo when equipment is implemented, rewrite this logic
            self.inventory_menu_labels.append("Equip")
            self.mouse_zones.append({"top_left": top_left,      "top_right": top_right,
                                    "bottom_left": bottom_left, "bottom_right": bottom_right,
                                    "group": "inventory",
                                    "button": 1,                "payload": {"item": item},
                                    "callback": null_cb})
            bottom_left     += modify_by
            bottom_right    += modify_by

        if "equipped" in item['properties']: #@todo rewrite to check equipment on player
            self.inventory_menu_labels.append("Unequip")
            self.mouse_zones.append({"top_left": top_left,      "top_right": top_right,
                                    "bottom_left": bottom_left, "bottom_right": bottom_right,
                                    "group": "inventory",
                                    "button": 1,                "payload": {"item": item},
                                    "callback": null_cb})
            bottom_left     += modify_by
            bottom_right    += modify_by

        if "quest" not in item['properties'] and "equipped" not in item['properties']:
            self.inventory_menu_labels.append("Drop")
            self.mouse_zones.append({"top_left": top_left,      "top_right": top_right,
                                    "bottom_left": bottom_left, "bottom_right": bottom_right,
                                    "group": "inventory",
                                    "button": 1,                "payload": {"item": item},
                                    "callback": null_cb})

            bottom_left     += modify_by
            bottom_right    += modify_by

    def update_inventory_mousezones(self):
        # keep track and build the clickable zones of the UI for each item in the inventory
        self.purge_mz("status_screen")
        self.purge_mz("inv_item_menu")
        modify_by       = 8
        top_left        = 385
        top_right       = 520
        bottom_left     = 55
        bottom_right    = 65

        for item in self.player_object["contains"]:
            self.mouse_zones.append({"top_left": top_left, 
                                    "top_right": top_right,
                                    "bottom_left": bottom_left,
                                    "bottom_right": bottom_right,
                                    "group": "status_screen",
                                    "button": 1,
                                    "payload": {"item": item},
                                    "callback": self.mz_callback_inventory})
            #print(item)
            bottom_left     += modify_by
            bottom_right    += modify_by

    def core_mz_callback(self, **args):
        if args.get("status"):
            new_status = args["status"]
            self.switch_status_scene(new_status)

    def get_input(self, code, default_key = None):
        r = self.cfg.get("keybinds", {}).get(code, None)
        if r == None:
            if default_key != None:
                self.cfg["keybinds"][code] = default_key
                self.save_config()
            return default_key
        else:
            return r

    def key_trigger(self, code, key, default_key = None):
        i = self.get_input(code, default_key)
        #print("input get", i)
        if i:
            if type(i) == str:
                #print("code", pygame.key.key_code(i))
                return int(pygame.key.key_code(i)) == key

            if type(i) == list:
                for k in i:
                    #print("code", pygame.key.key_code(k))
                    if int(pygame.key.key_code(k)) == key:
                        return True

        return False
    
    def unbind_key(self, command, key = None):
        i = self.get_input(command)

        if type(i) == str:
            if key == None:
                del self.cfg["keybinds"][command]
                self.save_config()
            else:
                if self.cfg["keybinds"][command] == key:
                    del self.cfg["keybinds"][command]
                    self.save_config()

        if type(i) == list:
            if key in i:
                self.cfg["keybinds"][command].remove(key)
                if len(self.cfg["keybinds"][command]) == 1:
                    self.cfg["keybinds"][command] = self.cfg["keybinds"][command][0]
                self.save_config()


    def bind_key(self, key, command, appending=False):
        i = self.get_input(command)
        print("i", i)
        if type(i) == str or i == None:
            if appending:
                self.cfg["keybinds"][command] = [self.cfg["keybinds"][command], key]
                self.save_config()
            else:
                self.cfg["keybinds"][command] = key
                self.save_config()

        if type(i) == list:
            print("appending key")
            if key not in self.cfg["keybinds"][command]:
                self.cfg["keybinds"][command].append(key)
                self.save_config()

    def handle_key_down(self, event):
        if self.print_key == True:
            self.log(f"Input: {pygame.key.name(event.key)}")
            self.print_key = False
            return

        if self.rebind_keyname != "":
            #k = self.variables.get("rebind_key", "")
            keyname = pygame.key.name(event.key)
            self.log(f"Binding {self.rebind_keyname} to {keyname}")
            self.bind_key(keyname, self.rebind_keyname, self.appending_bind)
            self.rebind_keyname = ""
            self.appending_bind = False
            return

        if self.unbinding != "":
            keyname = pygame.key.name(event.key)
            i = self.unbinding
            if keyname in self.get_input(i):
                print(f"Unbind {keyname} // {i}")
                self.unbind_key(i, keyname)
            else:
                print("Invalid unbind")
            
            self.unbinding = ""
            return
            
        # keyboard input
        if self.can_input(): # if user can press buttons right now
            if len(self.dialog_stack) > 0:
                if self.proceed_dialog():
                    return
                return

            for cmd in self.commands.keys():
                if self.key_trigger(cmd, event.key):
                    print("Executed", cmd)
                    #df = self.variables.get("")
                    self.commands[cmd]("")

            battle = self.combat_data["active"]     
            if self.key_trigger("toggle fullscreen terminal", event.key, "f1") and not battle:
                if self.current_scene == self.main_scene:
                    self.switch_to_fst()
                    return
                
                if self.current_scene == self.fullscreen_terminal_scene:
                    self.switch_to_main_scene()
                    return

            if not battle and self.current_scene == self.main_scene:
                if self.key_trigger("toggle input focus", event.key, "f2"):
                    self.selected_console = not self.selected_console

            if not self.selected_console and self.current_scene == self.main_scene:
                if self.key_trigger("focus input", event.key, "t"):
                    self.selected_console = True
                    return

            if self.selected_console or self.current_scene == self.fullscreen_terminal_scene:
                if self.key_trigger("unfocus input", event.key, "escape"):
                    self.selected_console = False
                    return

                if self.key_trigger("autocomplete", event.key, "tab"):
                    print("autocomplete")
                    ac = self.cfg.get("autocomplete", [])
                    pass #@todo autocomplete here
                
                if event.scancode == 82: #up key
                    if len(self.text_input_history) == 0: return

                    self.text_input_pointer += 1
                    if self.text_input_pointer >= len(self.text_input_history):
                        self.text_input_pointer = len(self.text_input_history)
                    
                    self.text_input_ln = self.text_input_history[-self.text_input_pointer]

                if event.scancode == 81: #down key
                    if len(self.text_input_history) == 0: return
                    self.text_input_pointer -= 1     
                    if self.text_input_pointer <= 0:
                        self.text_input_pointer = 0
                        self.text_input_ln = ""
                    else:
                        self.text_input_ln = self.text_input_history[-self.text_input_pointer]
                    
                if self.key_trigger("send input", event.key, "return"):
                    current_cmd = self.text_input_ln
                    if current_cmd != "":
                        self.text_buffer.clear()
                        self.refresh_text_input()
                        self.log("$ "+current_cmd)
                        self.parse_command(current_cmd)
                        if self.cfg.get("autoclose_prompt", False):
                            self.selected_console = False
                        self.text_input_history.append(current_cmd)

                if(event.unicode):
                    if event.key != 13 and event.key != 9 and event.key != 8:
                        self.text_buffer.append(event.unicode)
                        self.refresh_text_input()

                if self.key_trigger("backspace", event.key, "backspace"):
                    if len(self.text_buffer) == 0: return
                    self.text_buffer.pop()
                    self.refresh_text_input()

            else:
                #player = self.player_object
                if not battle:
                    if self.key_trigger("move up", event.key, ["up", "w"]):
                        self.move_player("u")
                            
                    if self.key_trigger("move down", event.key, ["down", "s"]):
                        self.move_player("d")

                    if self.key_trigger("move left", event.key, ["left", "a"]):
                        self.move_player("l")

                    if self.key_trigger("move right", event.key, ["right", "d"]):
                        self.move_player("r")