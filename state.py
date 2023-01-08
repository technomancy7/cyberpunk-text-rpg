import json, os, random

class JEState:
    def start_combat(self, *entities):
        #@todo sort the entities array by lowest DT
        #@todo get recoloured bmp font so that enemies and allies can be identified in the list
        self.combat_data['entities'] = entities
        self.combat_data["turns"] = 0
        self.combat_data['active'] = True

        for ent in entities:
            e = self.get_entity(ent)
            #print("combat", e)
            e['dt'] = random.randint(e['skills']["agility"], e['skills']["agility"] + random.randint(1, 10))

    def end_combat(self, *, pause = False):
        self.combat_data["active"] = False
        if not pause:
            for ent in self.combat_data['entities']:
                e = self.get_entity(ent)
                e['dt'] = 0

            self.combat_data["turns"] = 0    
            self.combat_data['entities'] = []

    def global_start_combat(self, **args):
        print("GLOBAL COMBAT START")
        #print(args)
        #@todo pull in both player and targets squad
        self.start_combat(*[self.player, args['target']])
        
    def init_globals(self):
        self.global_functions = {
            "pickup_item": self.pickup_item,
            "teleport": self.teleport,
            "new_turn": self.new_turn,
            "start_combat": self.global_start_combat
        }
        
    def pickup_item(self, **args):
        print(f"pickup {args}")

    def teleport(self, **args):
        exit_point = args['source']['data'].get("exit", {})
        print(f"teleport {exit_point}")
        self.set_zone(self.player, exit_point['map'])
        self.set_pos(self.player, exit_point['pos'][0], exit_point['pos'][1])

    def new_turn(self, **args):
        z = self.active_zone_object
        for ent in z['contains']:
            entobj = self.get_entity(ent)
            self.trigger_event(entobj, "new_turn", **args)
            self.next_step(entobj)

    def next_step(self, ent):
        ent = self.get_entity(ent)
        if len(ent['ai_scripts']['field']) > 0:
            if self.move_entity(ent, ent['ai_scripts']['field'][0]):
                ent['ai_scripts']['field'].append(ent['ai_scripts']['field'][0])
                del ent['ai_scripts']['field'][0]
    
    def set_event(self, obj, event_type, event):
        obj = self.get_entity(obj)
        if obj['events'].get(event_type, None) == None: obj['events'][event_type] = []
        obj['events'][event_type].append(event)

    def trigger_global(self, global_name, **payload):
        if self.global_functions.get(global_name, None):
            self.global_functions[global_name](**payload)

    def trigger_event(self, obj, event_type, **payload):
        obj = self.get_entity(obj)
        if obj['events'].get(event_type, None) == None: return
        for evt in obj['events'][event_type]:
            payload["source"] = obj
            self.trigger_global(evt, **payload)

    def quicksave(self):
        self.save_state("quick")

    def save_state(self, name = "save"):
        data = self.export_state()
        with open(self.app_path+"states/"+name+".json", "w+") as f:   
            json.dump(data, f, indent=4)
            self.log(f"! State saved to {name}.json")

    def export_state(self):
        output = {
            "variables": self.variables,
            "zones": self.zones,
            "entities": self.entities,
            "virtual_fs": self.virtual_fs
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
            self.virtual_fs = data.get("virtal_fs", {})
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
        self.trigger_event(target, "bumped", mover=mover, direction=direction, target=target)
        return self.bark(target, "bump")

    def bark(self, target, group = "ambient"):
        target = self.get_entity(target)
        barks = target.get("barks", {}).get(group, [])
        if len(barks) > 0:
            self.log(f"{target['name']}: {random.choice(barks)}")
            return True
        return False

    def move_entity(self, e, d) -> bool:
        e = self.get_entity(e)

        #@todo finish this
        #@todo once implemented, add a switch to use tank controls

        # special: move toward a target
        # requires a target in entity['data']['target']
        if d == "toward_target":
            pass

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
                        return False
                else:
                    if e["y"] > 0:
                        e["y"] -= 1
                        return True

            if d == "d":
                collisions = self.collisions_at(e["x"], e["y"]+1)
                if len(collisions) > 0:
                    if e == self.player_object and not self.collided(e, collisions[0]): 
                        self.log(f"! You bumped in to {collisions[0]['name']}")
                        return False
                else:
                    if e["y"] < self.field_size:
                        e["y"] += 1
                        return True

            if d == "r":
                collisions = self.collisions_at(e["x"]+1, e["y"])
                if len(collisions) > 0:
                    if e == self.player_object and not self.collided(e, collisions[0]): 
                        self.log(f"! You bumped in to {collisions[0]['name']}")
                        return False
                else:
                    if e["x"] < self.field_size:
                        e["x"] += 1
                        return True

            if d == "l":
                collisions = self.collisions_at(e["x"]-1, e["y"])
                if len(collisions) > 0:
                    if e == self.player_object and not self.collided(e, collisions[0]): 
                        self.log(f"! You bumped in to {collisions[0]['name']}")
                        return False
                else:
                    if e["x"] > 0:
                        e["x"] -= 1
                        return True

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
            self.trigger_global("new_turn")


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

    def get_skill_level(self, obj, skill):
        obj = self.get_entity(obj)
        return obj['skills'][skill]

    def edit_skill_level(self, obj, skill, value:int):
        obj = self.get_entity(obj)
        obj['skills'][skill] = int(value)
        
