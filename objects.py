
class JECommand:
    def parse_command(self, ln):
        cmd = ln.split(" ")[0]
        args = " ".join(ln.split(" ")[1:])

        match cmd:
            case "quit":
                exit()
            
            case "say":
                player = self.get_entity(self.player)
                self.log(f"{player['tag']} says: {args}")

            case "get":
                a = args.split(" ")

                if len(a) != 2:
                    return self.log("Invalid cmd length")

                ent = self.get_entity(a[0])
                val = ent[a[1]]
                self.log(f"{ent['tag']}.{a[1]} = {val} ({type(val)})")

            case "set":
                a = args.split(" ")

                if len(a) != 3:
                    return self.log("Invalid cmd length")

                ent = self.get_entity(a[0])
                val = a[2]
                if type(val) == str and val.isdigit(): val = int(val)
                if type(val) == str and val.lower() == "true": val = True
                if type(val) == str and val.lower() == "false": val = False
                ent[a[1]] = val

                self.log(f"{ent['tag']}.{a[1]} = {val} ({type(val)})")

            case "bg":
                a = args.split(" ")
                if len(a) == 3:
                    print("bg [", a, "]")
                    a = [int(element) for element in a]
                    self.set_bg(a)
                    self.log("bg changed.")
                else:
                    self.log("Invalid colour code.")
class JEState:
    def get_zone(self, tag):
        if type(tag) == dict: return tag
        for zone in self.zones:
            if zone["tag"] == tag: return zone

    def get_entity(self, tag):
        if type(tag) == dict: return tag
        for entity in self.entities:
            if entity["tag"] == tag: return entity


    def _entity(self, **args):
        o = {
            "tag": "", 
            "name": "DEFAULT_NAME", 
            "description": "DEFAULT_DESCRIPTION", 
            "contains": [], 
            "location": "",
            "type": "actor",
            "events": {},
            "sprite": None,
            "direction": "d",
            "solid": True,
            "hidden": False,
            "health": 100,
            "health_max": 100,
            "invincible": False,
            "energy": 100,
            "energy_max": 100,
            "alliance": "generic",
            "alliances": {
                "generic": 0
            }
        }
        o.update(**args)
        self.entities.append(o)
        return o

    def set_hostility(self, ent, alliance, value):
        ent = self.get_entity(ent)
        ent["alliances"][alliance]= value

    def get_hostility(self, e1, e2) -> int:
        e1a = e1["alliances"]
        #e2a = e2["alliances"]

        return e1a.get(e2['alliance'], 0)

    def is_hostile(self, e1, e2):
        return self.get_hostility(e1, e2) == -1

    def is_friendly(self, e1, e2):
        return self.get_hostility(e1, e2) == 1

    def _zone(self, **args):
        o = {
            "tag": "", 
            "name": "DEFAULT_NAME", 
            "description": "DEFAULT_DESCRIPTION", 
            "contains": [], 
            "type": "zone",
            "events": {},
            "map": [
                #{"loc": [0,0], "tiles": []}
            ]
        }



        o.update(**args)
        self.zones.append(o)
        return o
# 
# Base class of all in-world objects
class TObject:
    pass

class Zone(TObject):
    def __init__(self):
        self.contains = [] # entities inside this zone
        
# Entity objects, characters, NPC's, decorations, etc'
class Entity(TObject):
    def __init__(self, ID):
        self.ID = ID
        self.x = 0 # X position on screen
        self.y = 0 # Y position on screen
        self.grid_x = 0 # X slot on the grid
        self.grid_y = 0 # Y slot on grid
        self.sprite = None # Display image
        self.hidden = False # Wether it's being rendered'
        self.zone = None # Zone the entity is inside
        self.contains = [] # Character or containers inventory
    
    def move_pos(self, x, y):
        self.x = x
        self.y = y
        #@todo math here to make x/y screen map to the grid

# The Player!
class Player(Entity):
    pass
