class JECommand:
    def parse_command(self, ln):
        cmd = ln.split(" ")[0]
        args_raw = ln.split(" ")[1:]
        args = " ".join(args_raw)

        match cmd:
            case "quit":
                exit()
            
            case "save":
                save_name = args or "save"
                #self.log(f"! Saving to {save_name}.json")
                self.save_state(save_name)

            case "load":
                save_name = args or "save"
                #self.log(f"! Loading {save_name}.json")
                self.load_state(save_name)

            case "walk":
                steps = args_raw
                for step in steps:
                    self.log("You moved "+step)
                    self.move_player(step)

            case "say":
                player = self.get_entity(self.player)
                self.log(f"{player['tag']} says: {args}")

            #@todo for set and get, if entity not found, switch to variable modifying
            # or, change syntax, set player.health, but if object is world, then its variables
            case "get":
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

            case "set":
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

            case "bg":
                a = args_raw
                if len(a) == 3:
                    print("bg [", a, "]")
                    a = [int(element) for element in a]
                    self.set_bg(a)
                    self.log("bg changed.")
                else:
                    self.log("Invalid colour code.")
