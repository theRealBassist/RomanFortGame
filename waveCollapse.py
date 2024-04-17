import pygame
from config import *



class World:
    def __init__(self, sizeX, sizeY):
        self.cols, self.rows = sizeX, sizeY
        self.tileRows = []

    
    def test(self):
        validNeighbors = dict()
        filename = "sand_grassB_grassBL_grassBR"
        splitFilename = filename.split("_")
        mainType = splitFilename[0]
        definedPositions = []
        for requirement in splitFilename:
            if requirement == splitFilename[0]:
                continue
            
            tile = "".join(character for character in requirement if not character.isUpper())
            position = "".join(character for character in requirement if character.isUpper())
            definedPositions.append(position)
            invertPosition = ""
            for character in position:
                invertPosition += TILE_RELATIONSHIPS[character]
            
            validNeighbors[invertPosition] = tile



class Tile:

    def __init__(self, x, y):
        self.possibilities = list(tileRules.keys())
        self.entropy = len(self.possibilities)
        self.neighbours = dict()


    def addNeighbour(self, direction, tile):
        self.neighbours[direction] = tile


    def getNeighbour(self, direction):
        return self.neighbours[direction]


    def getDirections(self):
        return list(self.neighbours.keys())


    def getPossibilities(self):
        return self.possibilities


    def collapse(self):
        weights = [tileWeights[possibility] for possibility in self.possibilities]
        self.possibilities = random.choices(self.possibilities, weights=weights, k=1)
        self.entropy = 0


    def constrain(self, neighbourPossibilities, direction):
        reduced = False

        if self.entropy > 0:
            connectors = []
            for neighbourPossibility in neighbourPossibilities:
                connectors.append(tileRules[neighbourPossibility][direction])

            # check opposite side
            if direction == NORTH: opposite = SOUTH
            if direction == EAST:  opposite = WEST
            if direction == SOUTH: opposite = NORTH
            if direction == WEST:  opposite = EAST

            for possibility in self.possibilities.copy():
                if tileRules[possibility][opposite] not in connectors:
                    self.possibilities.remove(possibility)
                    reduced = True

            self.entropy = len(self.possibilities)

        return reduced

