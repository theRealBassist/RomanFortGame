import pygame
from spritesheet import Spritesheet
import math
from config import *

class Entity(pygame.sprite.Sprite):

    def __init__(self, name, sprite, pos, moveSpeed):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image =  sprite
        self.moveSpeed = moveSpeed
        self.direction = pygame.math.Vector2()
        self.rect = self.image.get_rect(center = pos) 
        self.gridPos = (int(pos[0] / TILESIZE), int(pos[1] / TILESIZE))
    
    def move(self, grid):
        # Todo: It seems that diagonal movement is causing the ongoing collision issues. 

        keys = pygame.key.get_pressed()

        currentCellGridPos = self.cellCurrent.getGridLocation()
        self.direction.y = 0

        if keys[pygame.K_UP]:
            cellNorth = grid.cells[currentCellGridPos[0], currentCellGridPos[1] - 1]
            if not cellNorth.impassable: self.direction.y = -1
            elif not self.rect.colliderect(cellNorth.rect): self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            cellSouth = grid.cells[currentCellGridPos[0], currentCellGridPos[1] + 1]
            if not cellSouth.impassable : 
                self.direction.y = 1
            elif not self.rect.colliderect(cellSouth.rect): self.direction.y = 1
        else:
            self.direction.y = 0

        self.direction.x = 0
        if keys[pygame.K_LEFT]:
            cellWest = grid.cells[currentCellGridPos[0] - 1, currentCellGridPos[1]]
            if not cellWest.impassable : self.direction.x = -1
            elif not self.rect.colliderect(cellWest.rect): self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            cellEast = grid.cells[currentCellGridPos[0] + 1, currentCellGridPos[1]]
            if not cellEast.impassable : self.direction.x = 1
            elif not self.rect.colliderect(cellEast.rect): self.direction.x = 1
        else:
            self.direction.x = 0

    def moveTowards(self, pos):
        selfPos = self.rect.center
        targetPos = pos

        distance = pygame.math.Vector2(targetPos[0] - selfPos[0], targetPos[1] - selfPos[1]).normalize()
        self.direction = distance
        

    def update(self, grid):

        self.gridPos = (math.ceil(self.rect.center[0] / TILESIZE), math.ceil(self.rect.center[1] / TILESIZE))
        self.cellCurrent = grid.getCell(self.rect.center, self.gridPos)

        self.move(grid)
        self.rect.center = self.rect.center + (self.direction * self.moveSpeed)

class Roman(Entity):
    def __init__(self, name, pos):
        romanSpriteSheet = Spritesheet("assets/sprites/roman_test/blue/blue.png")
        image = romanSpriteSheet.parseSprite("Walk/Walk_South_0.png").convert()
        Entity.__init__(self, name, image, pos, 3)
        