import pygame

class JEScreens:
    def switch_to_fst(self):
        self.buttons = []
        self.current_scene = self.fullscreen_terminal_scene

    def button_move_player(self, d):
        if not self.combat_data["active"]:
            self.move_player(d)

    def switch_to_main_scene(self):
        self.current_scene = self.main_scene
        self.buttons = [
            {
                "pos": [12, 9], 
                "spr": "diamond_dark", 
                "spr_hl": "diamond", 
                "on_click": lambda: self.button_move_player("u")
            }, 
            {
                "pos": [11, 10], 
                "spr": "diamond_dark", 
                "spr_hl": "diamond",
                "on_click": lambda: self.button_move_player("l")
            },
            {
                "pos": [12, 10], 
                "spr": "diamond_dark", 
                "spr_hl": "diamond",
                "on_click": lambda: self.button_move_player("d")
            },
            {
                "pos": [13, 10], 
                "spr": "diamond_dark", 
                "spr_hl": "diamond",
                "on_click": lambda: self.button_move_player("r")
            },
        ]


    def fullscreen_terminal_scene(self):
        # Background colour
        self.screen.fill(self.bg_colour)
        self.shift_bg()

        text_input_size = 25
        ln = self.text_input_ln
        self.write_text(5, self.cfg["winsize"][1]-text_input_size, f"> {ln}", size=text_input_size)

        log_size = text_input_size-5
        loc = self.cfg["winsize"][1]-text_input_size-log_size

        for msg in reversed(self.msg_history):
            colour = (255, 255, 255)

            sym = "*"
            symbols = ["$", "!", "@", "#", "?"]
            for s in symbols:
                if msg.startswith(f"{s} "): 
                    sym = s
                    msg = msg[2:]

            self.write_text(5, loc, f"{sym} {msg}", size=log_size, colour=colour)
            loc -= log_size

            if loc <= 5:
                break

    def main_scene(self):
        player = self.get_entity(self.player)

        # Background colour
        self.screen.fill(self.bg_colour)
        self.shift_bg()
        precise_cursor = pygame.mouse.get_pos()
        cursor = self.screen_to_tile(precise_cursor)

        #self.draw_text(20, 30, "Field/tile display")
        #self.draw_text(400, 30, "Stats/info/controls")

        #self.write(3, 9, "Test BitMap font sentence")
        #self.write(3, 10, "ALLCAPS TEST 0123456789")

        # text log display
        size = 128 # Size of the text log box
        height = self.cfg["winsize"][1]-size
        width = self.cfg["winsize"][0]
        if self.selected_console:
            pygame.draw.rect(self.screen,(255,0,0), (0, height, width, size), 1)
        else:
            pygame.draw.rect(self.screen,(255,255,255), (0, height, width, size), 1)
        text_input_size = 25
        ln = self.text_input_ln
        if len(ln) > 34:
            ln = ln[-34:]

        if self.seconds % 2 == 0 and self.selected_console:
            ln = ln+"_"

        self.write_text(5, self.cfg["winsize"][1]-(text_input_size+3), f"> {ln}", size=text_input_size-2)

        limit = 5
        current = 0
        log_size = text_input_size-5
        loc = self.cfg["winsize"][1]-text_input_size-log_size
        for msg in reversed(self.msg_history_proxy):
            colour = self.ttext1

            if current == limit-3:
                colour = self.ttext2

            if current == limit-2:
                colour = self.ttext3

            if current == limit-1:
                colour = self.ttext4

            sym = "*"
            symbols = ["$", "!", "@", "#", "?", "+", "-"]
            for s in symbols:
                if msg.startswith(f"{s} "): 
                    sym = s
                    msg = msg[2:]
                    
            self.write_text(5, loc, f"{sym} {msg}", size=log_size, colour=colour)
            loc -= log_size
            current += 1
            if current >= limit:
                break


        # field display            
        text_col = 45
        
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

                num_ents = 0
                if not self.combat_data["active"] and self.status_screen == "stats": 
                    self.write_bmp(text_col, 20, f"Entities in this zone:")


                for entity in self.entities:
                    if not entity["hidden"] and entity["sprite"] and entity["location"] == cur_loc["tag"]:
                        if entity["screen_x"] > entity["x"] * self.tile_size:
                            entity["screen_x"] -= self.spr_move_speed
                            entity["spr_moving"] = True

                        elif entity["screen_x"] < entity["x"] * self.tile_size:
                            entity["screen_x"] += self.spr_move_speed
                            entity["spr_moving"] = True

                        elif entity["screen_y"] > entity["y"] * self.tile_size:
                            entity["screen_y"] -= self.spr_move_speed
                            entity["spr_moving"] = True

                        elif entity["screen_y"] < entity["y"] * self.tile_size:
                            entity["screen_y"] += self.spr_move_speed
                            entity["spr_moving"] = True

                        else:
                            entity["spr_moving"] = False
                        self.draw_entity_precise(entity)

                        if(self.status_screen == "stats" and not self.combat_data["active"]):
                            num_ents += 1
                            #l = f"{entity['x']}x{entity['y']}"
                            #l = f"{entity['x']*self.tile_size}x{entity['y']*self.tile_size} / {entity['screen_x']}x{entity['screen_y']}"
                        
                            self.write_bmp(text_col, 20+num_ents, f"{num_ents}: {entity['name']}")

        # Border around the field
        pygame.draw.rect(self.screen, (125,255,255), (0, 0, height, height), 1)

        lbl_s = "stats"
        lbl_i = "inventory"
        lbl_g = "goals"
        if precise_cursor[0] > 370 and precise_cursor[0] < 422:
            if precise_cursor[1] > 8 and precise_cursor[1] < 25:
                lbl_s = lbl_s.upper()

        if precise_cursor[0] > 424 and precise_cursor[0] < 512:
            if precise_cursor[1] > 8 and precise_cursor[1] < 25:
                lbl_i = lbl_i.upper()

        if precise_cursor[0] > 530 and precise_cursor[0] < 582:
            if precise_cursor[1] > 8 and precise_cursor[1] < 25:
                lbl_g = lbl_g.upper()  

        if self.combat_data["active"]:
            i = 7
            for ent in self.combat_data["entities"]:
                ent = self.get_entity(ent)
                self.write_bmp(text_col, i, f"{ent['name']} ({ent['dt']})")
                i += 1

        elif self.status_screen == "stats":
            lbl_s = lbl_s.upper()
            self.write_bmp(text_col, 1, f" [{lbl_s}] [{lbl_i}] [{lbl_g}]")
            self.write_bmp(text_col+10, 2, " -- Stats --")

            # Get health and energy values as percentage
            hp = 100*(player['health']/player['health_max'])
            ep = 100*(player['energy']/player['energy_max'])
            wgt = 100*(player['container_weight']/player['weight_limit'])

            self.write_bmp(text_col, 7, f"Health: {hp}% ({player['health']}/{player['health_max']})")
            self.write_bmp(text_col, 8, f"Energy: {ep}% ({player['energy']}/{player['energy_max']})")
            self.write_bmp(text_col, 9, f"Weight: {wgt} ({player['container_weight']}/{player['weight_limit']})")

            ln = 9

            for skill, level in player['skills'].items():
                ln += 1
                self.write_bmp(text_col, ln, f"* {skill.title()}: {level}")

            if self.variables.get("debug", False):
                self.write_bmp(text_col, 5, f"FPS: {int(self.clock.get_fps())}")
                self.write_bmp(text_col, 6, f"Mouse POS: {precise_cursor}")

        elif self.status_screen == "goals":
            lbl_g = lbl_g.upper()
            self.write_bmp(text_col, 1, f" [{lbl_s}] [{lbl_i}] [{lbl_g}]")
            self.write_bmp(text_col+10, 2, " -- Goals --")
            
            gi = 5
            for goal in self.goals:
                if goal['active']:
                    msg = f"{goal['message']}"
                    if goal['completed']: msg += f" (DONE)"
                    self.write_bmp(text_col, gi, f"* {msg}")
                    gi += 1

        elif self.status_screen == "inventory":
            lbl_i = lbl_i.upper()
            self.write_bmp(text_col, 1, f" [{lbl_s}] [{lbl_i}] [{lbl_g}]")
            self.write_bmp(text_col+8, 2, " -- Inventory --")
            wgt = 100*(player['container_weight']/player['weight_limit'])
            self.write_bmp(text_col, 5, f"Weight: {wgt} ({player['container_weight']}/{player['weight_limit']})")
            i = 7
            for item in player["contains"]:
                en = self.get_entity(item)

                if en['tag'] == self.selected_inventory:
                    self.write_bmp(text_col, i, f"> {i-7}. {en['name']}")
                else:
                    self.write_bmp(text_col, i, f"{i-7}. {en['name']}")
                i += 1
            
            lbli = 7
            for lbl in self.inventory_menu_labels:
                self.write_bmp(text_col+25, lbli, f"{lbl}")
                lbli += 1

            if self.selected_inventory != "":
                desc = self.get_entity(self.selected_inventory)['description']
                start = 183
                #self.write_bmp(text_col, 25, f"{desc}")
                if "<br>" in desc:
                    for item in desc.split("<br>"):
                        self.write_text(360, start, f"{item}", size=12, colour=(255, 255, 255))
                        start += 20
                else:
                    self.write_text(360, start, f"{desc}", size=12, colour=(255, 255, 255))

        for button in self.buttons:
            xy = button["pos"]
            img = button["spr"]
            img_highlight = button["spr_hl"]
            #@todo add option for real screen xy boundary
            if cursor == xy:
                self.draw_arbitrary(xy, img_highlight)
            else:
                self.draw_arbitrary(xy, img)

        if len(self.dialog_stack) > 0:
            def spl(s, *, lim=40):
                out = []
                iters = 0
                while len(s) >= lim:
                    iters += 1
                    newsplit = " ".join(s[0:lim].split(" ")[:-1])
                    s = s[len(newsplit):]
                    out.append(newsplit.strip())

                    if iters > 6:
                        print("EMERGENCY BREAK: Dialog message too big.")
                        break

                out.append(s.strip())
                return out




            tsize = 40
            rect = (40, 200, 550, 200)
            rect_sender = (45, 175, 205, 40)


            pygame.Surface.fill(self.screen, (0,0,0), rect)
            pygame.draw.rect(self.screen, (255,255,255, 100), rect, 3)

            pygame.Surface.fill(self.screen, (0,0,0), rect_sender)
            pygame.draw.rect(self.screen, (255,255,255, 100), rect_sender, 3)

            lines = spl(self.dialog_msg_proxy)
            sender = self.dialog_stack[0][0]

            if sender != "": self.write_text(50, 183, f"{sender}", size=25, colour=(255, 255, 255))

            ind = 225
            for ln in lines:
                self.write_text(50, ind, f"{ln}", size=20, colour=(255, 255, 255))
                ind += 25

            if self.dialog_msg_proxy == self.dialog_stack[0][1]:
                #self.write_text(520, 380, f"[Confirm]", size=10, colour=(255, 255, 255))
                if len(self.dialog_stack) > 1:
                    self.write_text(510, 380, f"[Confirm] >", size=10, colour=(255, 255, 255))
                else:
                    self.write_text(520, 380, f"[Confirm]", size=10, colour=(255, 255, 255))

