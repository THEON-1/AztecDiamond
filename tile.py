from tuple_addition import tuple_add as tAdd

class Tile:

    def __init__(self, coord_black, coord_white, direction):
        self.coord_black = coord_black
        self.coord_white = coord_white
        self.direction = direction
    
    def shift(self):
        self.coord_black = tAdd(self.coord_black, self.direction)
        self.coord_white = tAdd(self.coord_white, self.direction)
        return (self.coord_black, self.coord_white)
    
    