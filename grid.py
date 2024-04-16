import pygame
from spritesheet import Spritesheet
import math
from config import *

class Grid:
    def __init__(self, screen):
        self.displaySurface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
        self.tileSheet = pygame.image.load(TERRAIN_TILESHEET)
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
            
            # get the terrain types of each tile corner
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
    
    def getCell(self, pos):
        vectorPos = pygame.math.Vector2(pos[0], pos[1])
        minimum = (9999999999, 0)
        for cell in self.cells:
            cellPixelPos = self.cells[cell].getPixelLocation()
            cellVectorPos = pygame.math.Vector2(cellPixelPos[0], cellPixelPos[1])
            distance = vectorPos.distance_to(cellVectorPos)
            if minimum[0] > distance: 
                minimum = (distance, self.cells[cell])
        
        print(f"Minimum distane is {minimum[0]}")
        return minimum[1]

    # def getCellGroup(self):
    #     cells = pygame.sprite.Group()
    #     for cell in self.cells:
    #         cells.add(self.cells[cell])
    #     return cells


class Cell(pygame.sprite.Sprite):
    def __init__(self, size, pos, image, terrainType, impassable):
        self.size = size
        self.terrainType = terrainType
        self.image = image.convert()
        self.rect = self.image.get_rect(center = pos)
        self.impassable = impassable
        pygame.sprite.Sprite.__init__(self)
    
    def getGridLocation(self):
        return (self.rect.center)

    def getPixelLocation(self):
        return ((self.rect.center[0] * TILESIZE, self.rect.center[1] * TILESIZE))
