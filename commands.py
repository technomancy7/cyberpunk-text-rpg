class JECommand:
    def parse_command(self, ln):
        cmd = ln.split(" ")[0]
        args_raw = ln.split(" ")[1:]
        args = " ".join(args_raw)

        if cmd == "quit":
                exit()
        
        if cmd == "addgoal":
            if self.variables.get("debug", False) == True:
                self.add_goal(args_raw[0], " ".join(args_raw[1:]))

        if cmd == "completegoal":
            if self.variables.get("debug", False) == True:
                if self.has_goal(args_raw[0]):
                    self.edit_goal(args_raw[0], completed=True)

        if cmd == "uncompletegoal":
            if self.variables.get("debug", False) == True:
                if self.has_goal(args_raw[0]):
                    self.edit_goal(args_raw[0], completed=False)

        if cmd == "activategoal":
            if self.variables.get("debug", False) == True:
                if self.has_goal(args_raw[0]):
                    self.edit_goal(args_raw[0], active=True)

        if cmd == "deactivategoal":
            if self.variables.get("debug", False) == True:
                if self.has_goal(args_raw[0]):
                    self.edit_goal(args_raw[0], active=False)

        if cmd == "setskill":
            if self.variables.get("debug", False) == True:
                skill = args_raw[0]
                if not args_raw[1].isdigit():
                    return self.log("! Invalid option: value must be a number.")
                value = int(args_raw[1])
                self.player_object["skills"][skill] = value

        if cmd == "save":
                save_name = args or "save"
                #self.log(f"! Saving to {save_name}.json")
                self.save_state(save_name)

        if cmd == "load":
                save_name = args or "save"
                #self.log(f"! Loading {save_name}.json")
                self.load_state(save_name)

        if cmd == "walk":
                steps = args_raw
                for step in steps:
                    self.log("You moved "+step)
                    self.move_player(step)

        if cmd == "diag":
                self.push_dialog("Player", f"{args}")

        if cmd == "say":
                player = self.get_entity(self.player)
                self.log(f"{player['tag']} says: {args}")

            #@todo for set and get, if entity not found, switch to variable modifying
            # or, change syntax, set player.health, but if object is world, then its variables
        if cmd == "get":
                #a = args

                if "." not in args:
                    return self.log("Invalid cmd format.")
                target = args.split(".")[0]
                param = args.split(".")[1]
                if target.lower() == "world":
                    self.log(f"world.{param} = {self.variables.get(param, None)}")
                else:
                    ent = self.get_entity(target)
                    val = ent[param]
                    self.log(f"{ent['tag']}.{param} = {val} ({type(val)})")

        if cmd == "set":
                if "." not in args:
                    return self.log("Invalid cmd format.")

                # player.health 1
                target = args.split(".")[0] # player
                param = ".".join(args.split(".")[1:]) # health 1
                val = param.split(" ")[0] # health
                param = " ".join(param.split(" ")[1:]) # 1

                def is_float(s):
                    try:
                        float(s)
                        return True
                    except:
                        return False

                       
                if type(param) == str and param.isdigit(): param = int(param)
                if type(param) == str and is_float(param): param = float(param) 
                if type(param) == str and param.lower() == "true": param = True
                if type(param) == str and param.lower() == "false": param = False

                if target == "world" or target == "self" or target == "$":
                    self.variables[val] = param
                    self.log(f"{target}.{val} = {param} ({type(param)})")
                else:
                    ent = self.get_entity(target)
                    if ent == None:
                        return self.log(f"Entity {target} not found.")
                    ent[val] = param

                    self.log(f"{target}.{val} = {param} ({type(param)})")

        if cmd == "bg":
                a = args_raw
                if len(a) == 3:
                    print("bg [", a, "]")
                    a = [int(element) for element in a]
                    self.set_bg(a)
                    self.log("bg changed.")
                else:
                    self.log("Invalid colour code.")