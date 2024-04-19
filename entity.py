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
        self.isMoving = False
        self.target = 0
        self.followTarget = None
        self.following = False
        self.moveSpeedModifier = 1
    
    def move(self, grid):

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

    def getTargetDirection(self, pos):
        selfPos = pygame.math.Vector2(self.rect.center)
        targetPos = pygame.math.Vector2(pos)
        direction = pygame.math.Vector2(targetPos.x - selfPos.x, targetPos.y - selfPos.y)
        if direction.length() > 0 : 
            return direction.normalize()
        else:
            return direction

    def getTargetDistance(self, pos):
        selfPos = pygame.math.Vector2(self.rect.center)
        targetPos = pygame.math.Vector2(pos)
        
        return selfPos.distance_to(targetPos)

    def checkArrived(self):
        if  self.distance < 10:
                self.isMoving = False
                self.target = 0
                self.notFollowable = []
        if not self.getLOS(self.target):
            self.isMoving = False
            self.target = 0

    def moveTowards(self, pos):
        #todo implement following mechanic
        self.followTarget = self.getFollowTarget()
        self.direction.x, self.direction.y = 0, 0

        self.direction = self.getTargetDirection(pos)
        if self.following: 
            lerp = self.direction.lerp(self.getTargetDirection(self.followTarget.target), 0.5)
            self.direction = lerp
        distance = self.getTargetDistance(pos)

        if  distance < 10:
            self.isMoving = False
            self.target = 0
        if not self.getLOS(self.target):
            self.isMoving = False
            self.target = 0
        
        self.rect.center += self.direction * self.moveSpeed * self.moveSpeedModifier

    def slowDown(self):
        if self.following and self.getTargetDistance(self.followTarget.rect.center) < self.moveSpeed:
            self.moveSpeedModifier -= .1
    
    def getFollowTarget(self):
        if self.following:
            if self.getStillFollowing():
                self.slowDown()
                return self.followTarget
            
        self.moveSpeedModifier = 1
        followCandidate = (45, 0)
        for entity in self.group:
            if self.getTargetDistance(entity.rect.center) > 500: continue
            angle = abs(entity.direction.angle_to(self.direction))
            if angle < followCandidate[0]:
                followCandidate = (angle, entity)
        
        if followCandidate[1] != 0:
            self.following = True
            return followCandidate[1]
        else:
            self.following = False
            return None
        
    def getStillFollowing(self):
        angle = abs(self.followTarget.direction.angle_to(self.direction))
        followTargetDistance = self.followTarget.getTargetDistance(self.target)
        targetDistance = self.getTargetDistance(self.target)
        if angle <= 15 and followTargetDistance < targetDistance:
            return True
        else:
            return False

    def getLOSRecursive(self, pos, targetPos, direction, distance = 9999, x = 1):
        if x > 999 or pos[0] < 0 or pos[1] < 0:
            return False
        if self.grid.getCell(pos).impassable:
            return False
        if distance < 25:
            return True

        pos += direction * x
        x += 1
        distance = pygame.math.Vector2(pos).distance_to(targetPos)
        return self.getLOSRecursive(pos, targetPos, direction, distance, x)
        
    def getLOS(self, pos):
        if self.getTargetDistance(pos) > 1000:
            return False
        targetPos = pygame.math.Vector2(pos)
        direction = self.getTargetDirection(pos)
        
        return self.getLOSRecursive(self.rect.center, targetPos, direction)

    def update(self, grid):

        self.grid = grid
        self.cellCurrent = grid.getCell(self.rect.center)

        if self.target != 0: 
            self.isMoving = True
            self.moveTowards(self.target)
        #self.move(grid)

    def setTarget(self, pos):
        if not self.isMoving:
            self.target = pos

    def setSpriteGroup(self, group):
        self.group = group
        self.group.add(self)

class Roman(Entity):
    def __init__(self, name, pos):
        romanSpriteSheet = Spritesheet("assets/sprites/roman_test/blue/blue.png")
        image = romanSpriteSheet.parseSprite("Walk/Walk_South_0.png").convert()
        Entity.__init__(self, name, image, pos, 3)
        