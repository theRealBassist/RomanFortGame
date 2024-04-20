import pygame
from config import *

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
        
    def getCellsOnVectorCollision(self, start, end, ray):
        startVector  = pygame.math.Vector2(start)
        endVector = pygame.math.Vector2(end)
        direction = pygame.math.Vector2(endVector.x - startVector.x, endVector.y - startVector.y)
        length = startVector.distance_to(endVector)
        if direction.length() > 0 : 
            direction = direction.normalize()
        else: 
            return True
        
        for x in range(-1, int(length)):
            position = self.getCell(startVector + (direction * x))
            nearbyCells = self.getNearbyCells(position.getGridLocation())
            for cell in nearbyCells:
                if cell.impassable:
                    if ray.colliderect(cell.rect):
                        return True
        
        return False
    
    def getNearbyCells(self, gridPos):
        x, y = gridPos[0], gridPos[1]
        if x < 1 : x = 1
        if y < 1 : y = 1
        if x >= WORLD_X - 1 : x = WORLD_X - 2
        if y >= WORLD_Y - 1 : y = WORLD_Y - 2
        nearbyCells = []

        nearbyCells.append(self.cells[(x - 1, y - 1)])
        nearbyCells.append(self.cells[(x - 1, y)])
        nearbyCells.append(self.cells[(x - 1, y + 1)])

        nearbyCells.append(self.cells[(x, y - 1)])
        nearbyCells.append(self.cells[(x, y + 1)])

        nearbyCells.append(self.cells[(x + 1, y - 1)])
        nearbyCells.append(self.cells[(x + 1, y)])
        nearbyCells.append(self.cells[(x + 1, y + 1)])
        
        return nearbyCells
    
    def getCell(self, pos):
        gridPos = (round(abs((pos[0] - (TILESIZE / 2))) / TILESIZE), round((abs(pos[1] - (TILESIZE / 2))) / TILESIZE))
        return self.cells[gridPos]



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
