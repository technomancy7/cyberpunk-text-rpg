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
        for msg in reversed(self.msg_history):
            colour = (255, 255, 255)
            if current == limit-3:
                colour = (255, 255, 255, 5) #(255, 255, 255, 150)

            if current == limit-2:
                colour = (255, 255, 255, 200)

            if current == limit:
                colour = (255, 255, 255, 255)

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
                #self.draw_entity(player)
                #print([ent['tag'] for ent in self.entities])
                for entity in self.entities:
                    if not entity["hidden"] and entity["sprite"] and entity["location"] == cur_loc["tag"]:
                        self.draw_entity(entity)

                        num_ents += 1
                        l = f"{entity['x']}x{entity['y']}"
                        #h = f"Hostility: {self.get_hostility(entity, player)}"
                        h = f"Facing {entity['direction']}"
                        self.write_bmp(text_col, 20+num_ents, f"{num_ents}: {entity['name']} {h} ({l})")

        # Border around the field
        pygame.draw.rect(self.screen, (125,255,255), (0, 0, height, height), 3)

        # Get health and energy values as percentage
        hp = 100*(player['health']/player['health_max'])
        ep = 100*(player['energy']/player['energy_max'])
        self.write_bmp(text_col, 9, f"Health: {hp}% ({player['health']}/{player['health_max']})")
        self.write_bmp(text_col, 10, f"Energy: {ep}% ({player['energy']}/{player['energy_max']})")
        
        cursor = self.screen_to_tile(pygame.mouse.get_pos())
        #print(pygame.mouse.get_pressed())
        

        for button in self.buttons:
            xy = button["pos"]
            img = button["spr"]
            img_highlight = button["spr_hl"]

            if cursor == xy:
                self.draw_arbitrary(xy, img_highlight)
            else:
                self.draw_arbitrary(xy, img)
        """
        self.draw_arbitrary([11, 10], "diamond_dark")
        self.draw_arbitrary([12, 10], "diamond_dark")
        self.draw_arbitrary([13, 10], "diamond_dark")

        up_arrow = [12, 9]
        self.draw_arbitrary(up_arrow, "diamond_dark")

        """
