import pygame
from spritesheet import Spritesheet
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
        # Todo: Instead of just saying you can't go in the grid square, check for collisions

        keys = pygame.key.get_pressed()

        self.direction.y = 0
        if keys[pygame.K_UP]:
            cellNorth = grid.cells[self.cellCurrent.rect.center[0], self.cellCurrent.rect.center[1] - 1]
            if not cellNorth.impassable: 
                self.direction.y = -1
            elif not self.rect.colliderect(cellNorth.rect) and not self.cellCurrent.impassable:
                print("no collision") 
                self.direction.y = -1
            else: 
                print("collision")
        elif keys[pygame.K_DOWN]:
            cellSouth = grid.cells[self.cellCurrent.rect.center[0], self.cellCurrent.rect.center[1] + 1]
            if not cellSouth.impassable : self.direction.y = 1
            elif not self.rect.colliderect(cellSouth.rect): self.direction.y = 1
        else:
            self.direction.y = 0

        self.direction.x = 0
        if keys[pygame.K_LEFT]:
            cellWest = grid.cells[self.cellCurrent.rect.center[0] - 1, self.cellCurrent.rect.center[1]]
            if not cellWest.impassable : self.direction.x = -1
            elif not self.rect.colliderect(cellWest.rect): self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            cellEast = grid.cells[self.cellCurrent.rect.center[0] + 1, self.cellCurrent.rect.center[1]]
            if not cellEast.impassable : self.direction.x = 1
            elif not self.rect.colliderect(cellEast.rect): self.direction.x = 1
        else:
            self.direction.x = 0

    def update(self, grid, dt):

        self.gridPos = (int(self.rect.center[0] / TILESIZE), int(self.rect.center[1] / TILESIZE))
        self.cellCurrent = grid.getCell(self.rect.center, self.gridPos)

        self.move(grid)
        self.rect.center += self.direction * self.moveSpeed * dt

class Roman(Entity):
    def __init__(self, name, pos):
        romanSpriteSheet = Spritesheet("assets/sprites/roman_test/blue/blue.png")
        image = romanSpriteSheet.parseSprite("Walk/Walk_South_0.png").convert()
        Entity.__init__(self, name, image, pos, 90)
        