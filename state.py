import json, os

class JEState:
    def save_state(self, name = "save"):
        data = self.export_state()
        with open(self.app_path+"states/"+name+".json", "w+") as f:   
            json.dump(data, f, indent=4)
            self.log(f"! State saved to {name}.json")

    def export_state(self):
        output = {
            "variables": self.variables,
            "zones": self.zones,
            "entities": self.entities
        }
        return output

    def import_state(self, name = "save"):
        if not os.path.exists(self.app_path+"states/"+name+".json"):
            self.log(f"! Save file not found {name}")
            return

        with open(self.app_path+"states/"+name+".json", "r") as f:
            return json.load(f)

    def load_state(self, name = "save"):
        data = self.import_state(name)
        if data:
            self.entities = data.get("entities", [])
            self.zones = data.get("zones", [])
            self.variables = data.get("variables", {})
            self.log(f"! State loaded from {name}.json")

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
