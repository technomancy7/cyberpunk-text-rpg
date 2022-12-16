 

class TObject:
    pass

class Entity(TObject):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.sprite = None
        self.hidden = False

class Player(Entity):
    pass
