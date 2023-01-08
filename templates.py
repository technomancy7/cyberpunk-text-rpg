class JETemplates:
    def _etos_new_file(self, **args):
        o = {
            "name": "", 
            "body": "", 
            "ftype": "file",
            "location": "/"
            #"files": [] # dir types only
        }

        o.update(**args)
        self.virtual_fs.append(o)
        return o

    def _entity(self, **args):
        o = {
            "tag": "", #tag or ID to track tis object
            "x": 0, # tile position
            "y": 0,
            "move_queue": [],
            "spr_moving": False,
            "screen_x": 0, # precise screen position
            "screen_y": 0,
            "name": "DEFAULT_NAME", 
            "description": "DEFAULT_DESCRIPTION", 
            "contains": [], #inventory
            "properties": [], #keyword to relate to perks, augmentations, abilities, etc, this ent has
            "location": "", # zone tag that this ent exists in, or entity tag if is in inventory
            "type": "entity",
            "events": {}, # table of events
            "sprite": None,
            "direction": "d", # u, d, l, r
            "solid": True, # can entities walk through it or not
            "hidden": False, # will it display in the field
            "dt": 0, # for  characters, current delay in combat. for items, delay that is added when used
            "skills": {
                "weapons": 0,
                "perception": 0,
                "strength": 0,
                "armour": 0,
                "hacking": 0,
                "agility": 0,
                "dexterity": 0
            },
            "equipment": { # to define slots fully later
                "head": "",
                "body": "",
                "hands": ""
            },
            "ai_scripts": {
                "field": [],
                "combat": []
            },
            "state": "idle",
            "health": 100,
            "health_max": 100,
            "invincible": False,
            "energy": 100,
            "energy_max": 100,
            "squad": [], #tags allies to bring in to combat with them
            "data": {}, #storage for custom variables
            "weight": 0.5, # physical mass of the entity
            "container_weight": 0, # total weight of all items currently held in container
            "weight_limit": 10, # limit for the total weight this container can carry
            "alliance": "generic", # allianced tag
            "alliances": {
                "generic": 0
            },
            "barks": {},
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