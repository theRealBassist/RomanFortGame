import pygame
import math
from spritesheet import Spritesheet
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
                        break
                self.displaySurface.blit(image, (x * TILESIZE, y * TILESIZE))
        self.currentImage = self.displaySurface.copy()
    
    def getTileIndexForType(self, tileCorners, terrainType):
        tileIndex = 0
        for power, cornerType in enumerate(tileCorners):
                if cornerType == terrainType:
                    tileIndex += 2 ** power
        return tileIndex
    
    # def getCell(self, x ,y):
    #     cellLocation = (TILESIZE * math.floor(x / TILESIZE), TILESIZE * math.floor(y / TILESIZE))
    #     return self.cells[cellLocation]

    # def getCellGroup(self):
    #     cells = pygame.sprite.Group()
    #     for cell in self.cells:
    #         cells.add(self.cells[cell])
    #     return cells


# class Cell(pygame.sprite.Sprite):
#     def __init__(self, size, x, y, image):
#         self.size = size
#         self.x = x
#         self.y = y
#         self.image = image.convert()
#         self.rect = self.image.get_rect()
#         self.rect.center = (self.x, self.y)
#         pygame.sprite.Sprite.__init__(self)
    
#     def getLocation(self):
#         return (self.x, self.y)
