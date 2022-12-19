
class JECommand:
    def parse_command(self, ln):
        print(f"Recv {ln}") 

        cmd = ln.split(" ")[0]
        args = " ".join(ln.split(" ")[1:])

        print(cmd)
        print(args)

        match cmd:
            case "quit":
                exit()

            case "bg":
                a = args.split(" ")
                if len(a) == 3:
                    print("bg [", a, "]")
                    a = [int(element) for element in a]
                    self.set_bg(a)
                else:
                    print("Invalid")
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
            "hidden": False
        }
        o.update(**args)
        self.entities.append(o)
        return o

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
