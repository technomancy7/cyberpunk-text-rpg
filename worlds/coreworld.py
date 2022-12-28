
class World:
    def build_world(self):
        print("Building coreworld")
        # Build the default world

        # Refresh world state
        self.variables = {}
        self.entities = []
        self.zones = []

        # SETUP PLAYER
        self.player = "player"
        self._entity(tag="player", sprite="player", x=2, y=2, alliance="player", name="The Player")

        # ZONE 1: THE BAR
        self._zone(name="The Bar", tag="the_bar")
        self.set_zone("player", "the_bar")

        f = self._entity(tag="pistol", sprite="circle", name="9mm Pistol", solid=False, 
            properties=["inventory", "equip"], slot = "weapon", weight=1, x=6, y=6)
        self.set_zone("pistol", "the_bar")

        f = self._entity(tag="medkit", sprite="circle", x=6, y=6, name="Medkit", solid=False, 
            properties=["inventory"], weight=1, events={"use": "use_item"})
        self.set_zone("medkit", "the_bar", x=7, y=6)


        f = self._entity(tag="target_dummy", sprite="circle", x=2, y=6, name="target dummy")
        self.set_hostility("target_dummy", "player", -1)
        f["barks"]["bump"] = ["Hey!", "Watch it!", "This is a very long message that will hopefully be split properly in the message history, idk tho."]
        self.set_zone("target_dummy", "the_bar")

        

        for x in range(11):
            for y in range(11):
                self.zones[0]["map"].append([[x, y], ["wood"]])

        self.push_dialog("Intro", "This is an intro! This dialog box is for testing purposes. I wonder if it'll even work, who knows really.")