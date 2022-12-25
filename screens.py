import pygame

class JEScreens:
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
        self.write_text(5, self.cfg["winsize"][1]-text_input_size, f"> {ln}", size=text_input_size)

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
            symbols = ["$", "!", "@", "#", "?"]
            for s in symbols:
                if msg.startswith(f"{s} "): 
                    sym = s
                    msg = msg[2:]
            self.write_text(5, loc, f"{sym} {msg}", size=log_size, colour=colour)
            loc -= log_size
            current += 1
            if current >= limit:
                break

        text_col = 45
        # field display
        
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
                self.write_bmp(text_col, 20, f"Entities in this zone:")

                # = self.variables.get("sprms", 0.5)#0.5
                for entity in self.entities:
                    if not entity["hidden"] and entity["sprite"] and entity["location"] == cur_loc["tag"]:
                        if entity["screen_x"] > entity["x"] * self.tile_size:
                            entity["screen_x"] -= self.spr_move_speed

                        if entity["screen_x"] < entity["x"] * self.tile_size:
                            entity["screen_x"] += self.spr_move_speed
                            
                        if entity["screen_y"] > entity["y"] * self.tile_size:
                            entity["screen_y"] -= self.spr_move_speed

                        if entity["screen_y"] < entity["y"] * self.tile_size:
                            entity["screen_y"] += self.spr_move_speed

                        self.draw_entity_precise(entity)

                        num_ents += 1
                        l = f"{entity['x']}x{entity['y']}"
                        l = f"{entity['x']*self.tile_size}x{entity['y']*self.tile_size} / {entity['screen_x']}x{entity['screen_y']}"
                        #h = f"Hostility: {self.get_hostility(entity, player)}"
                        #h = f"Facing {entity['direction']}"
                        self.write_bmp(text_col, 20+num_ents, f"{num_ents}: {entity['name']} ({l})")

        # Border around the field
        pygame.draw.rect(self.screen, (125,255,255), (0, 0, height, height), 3)

        # Get health and energy values as percentage
        hp = 100*(player['health']/player['health_max'])
        ep = 100*(player['energy']/player['energy_max'])
        self.write_bmp(text_col, 9, f"Health: {hp}% ({player['health']}/{player['health_max']})")
        self.write_bmp(text_col, 10, f"Energy: {ep}% ({player['energy']}/{player['energy_max']})")
        self.write_bmp(text_col, 11, f"Move speed: {self.variables.get('sprms', 0.5)}")
        cursor = self.screen_to_tile(pygame.mouse.get_pos())
        #print(pygame.mouse.get_pressed())
        

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

            self.write_text(50, 183, f"{sender}", size=25, colour=(255, 255, 255))

            ind = 225
            for ln in lines:
                self.write_text(50, ind, f"{ln}", size=20, colour=(255, 255, 255))
                ind += 25

            if self.dialog_msg_proxy == self.dialog_stack[0][1]:
                self.write_text(520, 380, f"[Confirm]", size=10, colour=(255, 255, 255))

