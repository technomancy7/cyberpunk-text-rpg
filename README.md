# Code: Elysium

## Running

### Windows
Execute `run_win32.bat`.

### Linux
Execute `install_linux.sh` to install needed libraries.
Execute `run_linux.sh` to launch.



# Dev Notes

## Events

```py
def event_fn(self, **data):
    print(f"Event has been triggered with data {data}")

self.set_event(obj, "event_type", "event_name")
self.events["event_name"] = self.event_fn


# Teleporters
obj['data']['exit'] = {"map": "exit map tag", "pos": [7, 1]}
self.set_event(obj, "on_player", "teleport")
```