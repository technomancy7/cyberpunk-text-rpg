
class JECommand:
    def parse_command(self, ln):
        print(f"Recv {ln}") 

        cmd = ln.split(" ")[0]
        args = " ".join(ln.split(" ")[1:])

        print(cmd)
        print(args)
class JEState:
    def _actor(self, **args):
        o = {
            "id": "", 
            "name": "DEFAULT_NAME", 
            "description": "DEFAULT_DESCRIPTION", 
            "contains": [], 
            "location": "",
            "type": "actor",
            "events": {}
        }
        o.update(**args)
        self.entities.append(o)
        return o

    def _zone(self, **args):
        o = {
            "id": "", 
            "name": "DEFAULT_NAME", 
            "description": "DEFAULT_DESCRIPTION", 
            "contains": [], 
            "type": "zone",
            "exits": {},
            "events": {}
        }

        for d in self._directions():
            o["exits"][d] = {
                "target": "",
                "locked": False,
                "events": {
                    "on_exit": [], 
                    "on_exit_failed": []
                }
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
