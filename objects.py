 
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
        self.sprite = None # Display image
        self.hidden = False # Wether it's being rendered'
        self.zone = None # Zone the entity is inside
        self.contains = [] # Character or containers inventory
    
    def move_pos(self, x, y):
        self.x = x
        self.y = y

# The Player!
class Player(Entity):
    pass
