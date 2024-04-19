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
        self.collisionList = []
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
                        if terrainType >= 5 or terrainType < 3 : 
                            cell = Cell(TILESIZE, (x, y), image, terrainType, True)
                            self.collisionList.append(cell)
                        else:
                            cell = Cell(TILESIZE, (x, y), image, terrainType, False)
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
    
    def getCellsOnVector(self, start, end):
        cellsOnVector = dict()

        startingCell = self.getCell(start)
        endingCell = self.getCell(end)

        for cell in self.getNearbyCells(startingCell.getGridLocation()):
            if cell.impassable: cellsOnVector[cell.rect.center] = cell
        for cell in self.getNearbyCells(endingCell.getGridLocation()):
            if cell.impassable: cellsOnVector[cell.rect.center] = cell

        startVector  = pygame.math.Vector2(start)
        #23, 45
        endVector = pygame.math.Vector2(end)
        #45, 32
        direction = pygame.math.Vector2(endVector.x - startVector.x, endVector.y - startVector.y)
        #45 - 23, 32 - 45
        #22, -13
        length = startVector.distance_to(endVector)
        #
        if direction.length() > 0 : 
            direction = direction.normalize()
        else: 
            return self.getNearbyCells(self.getCell(start))
        
        for x, __ in enumerate(range(int(length)), start=1):
            position = self.getCell(startVector + (direction * x))
            nearbyCells = self.getNearbyCells(position.getGridLocation())
            for cell in nearbyCells:
                if cell.impassable:
                    cellsOnVector[cell.rect.center] = cell
        
        return list(cellsOnVector.values())





    
    def getNearbyCells(self, gridPos):
        x, y = gridPos[0], gridPos[1]
        if x <= 0: x = 1
        if x >= WORLD_X: x = WORLD_X
        if y <= 0: y = 1
        if y >= WORLD_Y: y = WORLD_Y
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
        self.rect = self.image.get_rect(center = (pos[0] * TILESIZE, pos[1] * TILESIZE))
        
    
    def getGridLocation(self):
        return (self.pos)

    def getPixelLocation(self):
        return (self.rect.center)
