import pygame
from spritesheet import Spritesheet
import math
from config import *
from spritesheet import Spritesheet

class Grid:
    def __init__(self):
        self.displaySurface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
        self.tileSheet = pygame.image.load(TERRAIN_TILESHEET)
        #self.spriteSheet = Spritesheet(TERRAIN_TILESHEET) 
        self.cells = dict()
        self.terrainTiles = []
        self.currentImage = self.displaySurface.copy()
        for terrainType in ALL_TERRAIN_TYPES:
            tileTypes = []
            for tilePos in TERRAIN_TILES[terrainType]:
                tileTypes.append(self.tileSheet.subsurface((tilePos[0], tilePos[1], TILESIZE, TILESIZE)))
            self.terrainTiles.append(tileTypes)

    
    def drawTiles(self, terrainTileMap):
        for y, row in enumerate(terrainTileMap):
            for x, row in enumerate(row):
                if x == WORLD_X or y == WORLD_Y:
                    continue
        
                tileCornerTypes = []
                tileCornerTypes.append(terrainTileMap[y + 1][x + 1])
                tileCornerTypes.append(terrainTileMap[y + 1][x])
                tileCornerTypes.append(terrainTileMap[y][x + 1])
                tileCornerTypes.append(terrainTileMap[y][x])

                for terrainType in ALL_TERRAIN_TYPES:
                    if terrainType in tileCornerTypes:
                        tileIndex = self.getTileIndexForType(tileCornerTypes, terrainType)
                        image = self.terrainTiles[terrainType][tileIndex]
                        impassable = False
                        if terrainType >= 5 or terrainType < 3 : impassable = True 
                        cell = Cell(TILESIZE, (x, y), image, terrainType, impassable)
                        self.cells[(x, y)] = cell
                        break
                self.displaySurface.blit(image, (x * TILESIZE, y * TILESIZE))
        self.currentImage = self.displaySurface.copy()
    
    def getTileIndexForType(self, tileCorners, terrainType):
        tileIndex = 0
        for power, cornerType in enumerate(tileCorners):
                if cornerType == terrainType:
                    tileIndex += 2 ** power
        return tileIndex
    
    def getNearbyCells(self, gridPos):
        x = gridPos[0]
        y = gridPos[1]
        nearbyCells = []

        #nearbyCells.append(self.cells[(x - 1, y - 1)])
        nearbyCells.append(self.cells[(x - 1, y)])
        #nearbyCells.append(self.cells[(x - 1, y + 1)])

        nearbyCells.append(self.cells[(x, y - 1)])
        nearbyCells.append(self.cells[(x, y + 1)])

        #nearbyCells.append(self.cells[(x + 1, y - 1)])
        nearbyCells.append(self.cells[(x + 1, y)])
        #nearbyCells.append(self.cells[(x + 1, y + 1)])
        
        return nearbyCells
        

    def getCellRecursive(self, pos, nearbyCells, index, minimum = (9999999999, 0)):
        if index >= len(nearbyCells):
            return minimum[1]
        
        cellPixelPos = nearbyCells[index].getPixelLocation()
        cellVectorPos = pygame.math.Vector2(cellPixelPos[0], cellPixelPos[1])
        distance = pos.distance_to(cellVectorPos)
        if minimum[0] > distance: 
                minimum = (distance, nearbyCells[index])
        return self.getCellRecursive(pos, nearbyCells, index + 1, minimum)

    def getCell(self, pos):
        vectorPos = pygame.math.Vector2(pos)
        gridPos = (math.ceil(pos[0] / TILESIZE), math.ceil(pos[1] / TILESIZE))
        if gridPos[0] < 1 :  gridPos = (gridPos[0] + 1, gridPos[1])
        if gridPos[1] < 1 : gridPos = (gridPos[0], gridPos[1] + 1)
        gridVectorPos = pygame.math.Vector2(self.cells[gridPos].getPixelLocation())

        if vectorPos.distance_to(gridVectorPos) < TILESIZE / 2:
            return self.cells[gridPos]
        nearbyCells = self.getNearbyCells(gridPos)
        nearestCell = self.getCellRecursive(vectorPos, nearbyCells, 0)
        return nearestCell



class Cell(pygame.sprite.Sprite):
    def __init__(self, size, pos, image, terrainType, impassable):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.terrainType = terrainType
        self.image = image.convert()
        self.impassable = impassable
        self.pos = pos
        if self.impassable: self.rect = self.image.get_rect(center = (pos[0] * TILESIZE, pos[1] * TILESIZE))
        
    
    def getGridLocation(self):
        return (self.rect.center[0] / TILESIZE, self.rect.center[1] / TILESIZE)

    def getPixelLocation(self):
        return (self.pos[0] * TILESIZE, self.pos[1] * TILESIZE)
