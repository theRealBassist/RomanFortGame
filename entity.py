import pygame
from spritesheet import Spritesheet

class Entity(pygame.sprite.Sprite):

    def __init__(self, name, sprite, pos, moveSpeed):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image =  sprite
        self.moveSpeed = moveSpeed
        self.direction = pygame.math.Vector2()
        self.rect = self.image.get_rect(center = pos) 
    
    def move(self):
        # Todo: Implement checking of tile types in front of and under the target.

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def update(self, grid):

        self.cellCurrent = grid.getCell(self.rect.center)
        self.cellNorth = grid.cells[self.cellCurrent.rect.center[0], self.cellCurrent.rect.center[1] - 1]
        self.cellNorthEast = grid.cells[self.cellCurrent.rect.center[0] + 1, self.cellCurrent.rect.center[1] - 1]
        self.cellEast = grid.cells[self.cellCurrent.rect.center[0] + 1, self.cellCurrent.rect.center[1]]
        self.cellSouthEast = grid.cells[self.cellCurrent.rect.center[0] + 1, self.cellCurrent.rect.center[1] + 1]
        self.cellSouth = grid.cells[self.cellCurrent.rect.center[0], self.cellCurrent.rect.center[1] + 1]
        self.cellSouthWest = grid.cells[self.cellCurrent.rect.center[0] -1, self.cellCurrent.rect.center[1] + 1]
        self.cellWest = grid.cells[self.cellCurrent.rect.center[0] - 1, self.cellCurrent.rect.center[1]]
        self.cellNorthWest = grid.cells[self.cellCurrent.rect.center[0] - 1, self.cellCurrent.rect.center[1] - 1]
        print(f"currentCell = {self.cellCurrent.terrainType}, northCell = {self.cellNorth.terrainType}, cellNorthWest = {self.cellNorthWest.terrainType}")
        self.move()
        self.rect.center += self.direction * self.moveSpeed

class Roman(Entity):
    def __init__(self, name, pos):
        romanSpriteSheet = Spritesheet("assets/sprites/roman_test/blue/blue.png")
        image = romanSpriteSheet.parseSprite("Walk/Walk_South_0.png").convert()
        Entity.__init__(self, name, image, pos, 5)
        