import json, os, random

class JEState:
    def pickup_item(self, **args):
        print(f"pickup {args}")

    def teleport(self, **args):
        exit_point = args['source']['data'].get("exit", {})
        print(f"teleport {exit_point}")
        self.set_zone(self.player, exit_point['map'])
        self.set_pos(self.player, exit_point['pos'][0], exit_point['pos'][1])
    def init_events(self):
        self.events = {
            "pickup_item": self.pickup_item,
            "teleport": self.teleport
        }
    
    def set_event(self, obj, event_type, event):
        obj = self.get_entity(obj)
        if obj['events'].get(event_type, None) == None: obj['events'][event_type] = []
        obj['events'][event_type].append(event)

    def trigger_event(self, obj, event_type, **payload):
        obj = self.get_entity(obj)
        if obj['events'].get(event_type, None) == None: return
        for evt in obj['events'][event_type]:
            if self.events.get(evt, None):
                payload["source"] = obj
                self.events[evt](**payload)

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

    def collided(self, mover, target, direction = "u"):
        self.trigger_event(target, "bumped", mover=mover, direction=direction)
        return self.bark(target, "bump")

    def bark(self, target, group = "ambient"):
        target = self.get_entity(target)
        barks = target.get("barks", {}).get(group, [])
        if len(barks) > 0:
            self.log(f"{target['name']}: {random.choice(barks)}")
            return True

    def move_entity(self, e, d):
        e = self.get_entity(e)

        #@todo finish this
        #@todo once implemented, add a switch to use tank controls
        # forward, backward, strafe right, straight left
        # moves in directions relative to direction
        # does not rotate
        if d in ["fw", "bk", "sr", "sl"]:
            pass

        # rotate right, rotate left
        if d in ["rr", "rl"]:
            pass

        # face up, face down, face left, face right
        # turns in direction
        # does not move
        if d in ["fu", "fd", "fl", "fr"]:
            pass

        # up, down, left, right
        # move in directions relative to screen
        # rotates to direction
        if d in ["u", "d", "l", "r"]:
            e["direction"] = d
            if d == "u":
                collisions = self.collisions_at(e["x"], e["y"]-1)
                if len(collisions) > 0:
                    if e == self.player_object and not self.collided(e, collisions[0]): 
                        self.log(f"! You bumped in to {collisions[0]['name']}")
                else:
                    if e["y"] > 0:
                        e["y"] -= 1

            if d == "d":
                collisions = self.collisions_at(e["x"], e["y"]+1)
                if len(collisions) > 0:
                    if e == self.player_object and not self.collided(e, collisions[0]): 
                        self.log(f"! You bumped in to {collisions[0]['name']}")
                else:
                    if e["y"] < self.field_size:
                        e["y"] += 1

            if d == "r":
                collisions = self.collisions_at(e["x"]+1, e["y"])
                if len(collisions) > 0:
                    if e == self.player_object and not self.collided(e, collisions[0]): 
                        self.log(f"! You bumped in to {collisions[0]['name']}")
                else:
                    if e["x"] < self.field_size:
                        e["x"] += 1

            if d == "l":
                collisions = self.collisions_at(e["x"]-1, e["y"])
                if len(collisions) > 0:
                    if e == self.player_object and not self.collided(e, collisions[0]): 
                        self.log(f"! You bumped in to {collisions[0]['name']}")
                else:
                    if e["x"] > 0:
                        e["x"] -= 1

    def collisions_at(self, x, y):
        out = []
        for ent in self.entities:
            if ent["x"] == x and ent["y"] == y and ent["hidden"] == False and ent["solid"] == True:
                out.append(ent)
        return out

    def find_entities_at(self, x, y, properties = []):
        out = []
        for ent in self.entities:
            if ent["location"] == self.active_zone and ent["x"] == x and ent["y"] == y:
                if len(properties) > 0:
                    if any(x in ent['properties'] for x in properties):
                        out.append(ent)
                else:
                    out.append(ent)
        return out

    def move_player(self, d):
        player = self.player_object
        if player != None:
            self.move_entity(player, d)
            ent = self.find_entities_at(player['x'], player["y"])

            if len(ent):
                for item in ent:
                    if self.variables.get("auto_pickup", True) and "inventory" in item['properties']:
                        if item["weight"] + player["container_weight"] < player["weight_limit"]:
                            self.set_container(item, player)
                            self.log(f"! You picked up {item['name']}.")
                            self.trigger_event(item, "pickup_item")

                    self.trigger_event(item, "on_player")

    def set_pos(self, ent, x, y):
        ent = self.get_entity(ent)
        ent['x'] = x
        ent['y'] = y

    def set_zone(self, ent, zone, *, x = None, y = None):
        ent = self.get_entity(ent)
        new_zone = self.get_zone(zone)

        if ent["location"] != "":
            loc = self.get_zone(ent['location'])
            if loc != None:
                loc['contains'].remove(ent['tag'])
        
        ent['location'] = new_zone['tag']
        if ent['tag'] not in new_zone['contains']: new_zone["contains"].append(ent['tag'])
        if type(x) == int: ent["x"] = x
        if type(y) == int: ent["y"] = y

    def set_container(self, ent, zone):
        ent = self.get_entity(ent)
        container = self.get_entity(zone)
        ent["x"] = -1
        ent["y"] = -1
        if ent["location"] != "":
            loc = self.get_zone(ent['location'])
            if loc != None:
                loc['contains'].remove(ent['tag'])
            
            loc2 = self.get_entity(ent['location'])
            if loc2 != None:
                loc2["contains"].remove(ent['tag'])
                loc2["container_weight"] -= ent["weight"]
        
        ent['location'] = container['tag']
        if ent['tag'] not in container['contains']: 
            container["contains"].append(ent['tag'])
            container["container_weight"] += ent["weight"]

        if self.current_scene == self.main_scene and self.status_screen == "inventory" and zone['tag'] == self.player:
            self.update_inventory_mousezones()

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
            "health": 100,
            "health_max": 100,
            "invincible": False,
            "energy": 100,
            "energy_max": 100,
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