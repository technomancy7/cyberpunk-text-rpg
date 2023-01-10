class JECommand:
    def get_binding_prompt(self, ln):
        self.log("Command input for: "+ln)
        self.log("? Press the key you wish to bind this command to.")
        self.rebind_keyname = ln
        self.wait_for_reply(None)

    def get_unbinding_prompt(self, ln):
        self.log("Command input for: "+ln)
        self.log("? Press the key you wish to unbind.")
        self.unbind_keyname = ln
        self.wait_for_reply(None)

    def init_commands(self):
        self.commands = {
            "quit": lambda ln: exit()
        }

    #@todo when commands have been moved to the dict
    # have support for binding keys to arbitrary commands
    # method is same, in rebind command, you can use either a key code like currently
    # or a command name
    # and in the keyboard event, it checks if the value is in command keys

    # then add commands for quicksave and quickload
    def parse_command(self, ln):
        if self.terminal_prompt != None:
            self.terminal_prompt(ln)
            return

        cmd = ln.split(" ")[0]
        args_raw = ln.split(" ")[1:]
        if self.commands.get(cmd, None):
            self.commands[cmd](" ".join(args_raw))
        
        if cmd == "rebind" or cmd == "bindkey":
            self.log("? Press the key you wish to bind this command to.")
            self.rebind_keyname = args

        if cmd == "addbind":
            self.log("? Press the key you wish to bind this command to.")
            self.rebind_keyname = args
            self.appending_bind = True

        if cmd == "unbind":
            self.log("? Press the key you wish to unbind.")
            self.unbinding = args
            #self.wait_for_reply(self.get_unbinding_prompt)

        if cmd == "testkey":
            print("Testing key")
            self.print_key = True
            self.log("Press a key to get it's name.")
        
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
            args = " ".join(args_raw)
            save_name = args or "save"
            #self.log(f"! Saving to {save_name}.json")
            self.save_state(save_name)

        if cmd == "load":
            args = " ".join(args_raw)
            save_name = args or "save"
            #self.log(f"! Loading {save_name}.json")
            self.load_state(save_name)

        if cmd == "walk":
            for step in args_raw:
                self.log("You moved "+step)
                self.move_player(step)

        if cmd == "diag":
            self.push_dialog("Player", f"{args}")

        if cmd == "say":
            player = self.get_entity(self.player)
            self.log(f"{player['tag']} says: {args}")

        if cmd == "get":
            args = " ".join(args_raw)
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
            args = " ".join(args_raw)
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
            #@todo parse value for list syntax
            #@todo parse value for dict syntax

            if target == "world" or target == "self" or target == "$":
                if self.variables.get(val, None) != None:
                    if type(self.variables[val]) != type(param):
                        self.log(f"Type mismatch for value.")
                        return

                self.variables[val] = param
                self.log(f"{target}.{val} = {param} ({type(param)})")
            else:
                ent = self.get_entity(target)
                if ent == None:
                    return self.log(f"Entity {target} not found.")

                if ent.get(val, None) != None:
                    if type(ent[val]) != type(param):
                        self.log(f"Type mismatch for value.")
                        return

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