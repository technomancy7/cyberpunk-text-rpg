# Code: Elysium

## Running

### Windows
Execute `run_win32.bat`.

### Linux
Execute `install_linux.sh` to install needed libraries.
Execute `run_linux.sh` to launch.



# Dev Notes

## Events
How to do certain things. `self` refers to the Main state object.
```py
# Events
def event_fn(self, **data):
    print(f"Event has been triggered with data {data}")
    self.log(f"Message: {data['message']}")

self.set_event(obj, "event_type", "event_name")
self.events["event_name"] = self.event_fn

self.trigger_event(obj, "event_type", source=obj, message="This event was triggered as a test!")

# Teleporters
obj['data']['exit'] = {"map": "exit map tag", "pos": [7, 1]}
self.set_event(obj, "on_player", "teleport")
```

# AI scripts
Defining behavior of entities
```py
# AI scripts
obj['ai_scripts']['field'] = ["l", "l", "l", "r", "r", "r"]
# object will pace left and right
# @todo each "turn" triggered when player takes an action, run move_entity on entry[0], then move 0 to the end

```

# Custom world support
WIP. Eventually the engine will be able to support custom created worlds using the same python API that generates the main world.