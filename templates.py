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
    
    def _damage_calculation(self, name):
        calcs = {
            "instakill": "health: [target.value.health]",
            "drain": "health: [self.strength] + [1:10] >> drain: [damage]",
            "heal": "restore health: [item.healing_power] + [1:10]",
            "recharge": "restore energy: [item.healing_power] + [1:10]",
            "basic_damage": "health: [self.strength] + [self.weapons] + [1:10] - [target.armour]"
        }
        return calcs.get(name, "health: 1")

    def _combat_action(self, **args):
        o = {
            "damage_calculation": "health: [self.strength] >> energy: 0",

            # calculation is evaluated as a pythonic math expression after some tags are replaced
            # multiple calculations can be used and split with >>
            # each calc is run consecutively and the result from the previous calc is saved for use

            # by default, they will damage hp, but this can be changed by prepending the value
            # can be arbitrary, matches the int value of the target
            # if key starts with `restore` then it adds instead of heals

            # a special key `drain` exists, which can only be used after the first calculation
            # if drain is used, then it switches scope to self and applies restore

            # [self.<skill name>] // uses the current level of the skill of the user
            # [target.<skill name>] // skill level of the target is used, defaults 0 when scope is all

            # [self.value.<value>] // uses arbitrary int value from user
            # [target.value.<value>]
            # [item.<value>] // uses arbitrary value from the item used, defaults 0 if unavailable
            # [world.<var name>] // takes a variable from the global vars, must be an int

            # [1:10] // random number between 1 and 10

            # [damage] // raw damage number that the previous calculation

            "function": None, #name of a global function to call on-cast
            "ignore_damage_calculation": False,
            # damage is passed to the damage calculation
            # if ignore_damage_calculation is true, then it does damage as a flat number
            "hp_damage": 0, # base damage done to scope
            "en_damage": 0, # base energy damage done to scope
            "hp_damage_percent": False, # hp damage is done as a percentage of *current* health
            "hp_damage_percent_max": False, # same, but *max* health
            "en_damage_percent": False, # hp damage is done as a percentage of *current* en
            "en_damage_percent_max": False, # same, but *max* en
            "drain_hp": 0, #int, percentage of damage done to HP to recover
            "drain_en": 0, #same, but energy
            "scope": "target", # accepts: target, self, all
            "animation": None, # tbd
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
            "party": [], # list of tags for NPC's considered part of the player party, for battles etc
            "manual_control": False, # does the player input this entities actions in battle
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