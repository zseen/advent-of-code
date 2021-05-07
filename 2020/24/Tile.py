from Coordinates import Coordinates
from TileColour import TileColour


class Tile:
    def __init__(self, coordinateX: int, coordinateY: int):
        self.coordinates: Coordinates = Coordinates(coordinateX, coordinateY)
        self.colour: TileColour = TileColour.WHITE
