import pygame
from spritesheet import Spritesheet
import math
from config import *

class Entity(pygame.sprite.Sprite):

    def __init__(self, name, sprite, pos, moveSpeed):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.defaultSprite = sprite
        self.image =  sprite
        self.moveSpeed = moveSpeed
        self.direction = pygame.math.Vector2(1, 1)
        self.rect = self.image.get_rect(center = pos) 
        self.gridPos = (math.ceil(pos[0] / TILESIZE), math.ceil(pos[1] / TILESIZE))
        self.isMoving = False
        self.target = (0, 0)
        self.followTarget = None
        self.following = False

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
                self.target = (0, 0)
        if not self.newLOS(self.target):
            self.isMoving = False
            self.target = (0, 0)

    def moveTowards(self, pos):
        self.followTarget = self.getFollowTarget()
        self.direction.x, self.direction.y = 0, 1

        if self.newLOS(self.target) : self.direction = self.getTargetDirection(pos)
        distance = self.getTargetDistance(pos)
        if self.following: 
            self.image = self.attackSprite
            entityDirection = self.getTargetDirection(self.followTarget.rect.center)
            lerp = self.direction.lerp(entityDirection, 0.75)
            if self.newLOS(self.target) : 
                self.direction = lerp
            else: 
                self.following = False
                self.image = self.defaultSprite
                self.followTarget = None
        else:
            self.image = self.defaultSprite
        
        if  distance < 10:
            self.isMoving = False
            self.target = (0, 0)
        if not self.newLOS(self.target):
        #if not self.newGetLOS(self.rect.center, self.getTargetDirection(self.target)):
            self.isMoving = False
            self.target = (0, 0)
        
        self.rect.center += self.direction * self.moveSpeed
    
    def getFollowTarget(self):
        if self.following:
            if self.getStillFollowing():
                return self.followTarget
            
        followCandidate = (15, 0)
        for entity in self.group:
            if self.getTargetDistance(entity.rect.center) > 100 or self.getTargetDistance(entity.rect.center) < 2: continue
            entityDirection = self.getTargetDirection(entity.rect.center)
            angle = self.direction.angle_to(entityDirection)
            if angle < followCandidate[0] and angle > 2:
                followCandidate = (angle, entity)
        
        if followCandidate[1] != 0:
            self.following = True
            self.image = self.attackSprite
            return followCandidate[1]
        else:
            self.image = self.defaultSprite
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
    
    def newLOSRecursive(self, ray, increment):
        collisionList = []
        collisionList.append(self.grid.collisionList[increment])
        collision = ray.collideobjects(collisionList, key = lambda r: r.rect)
        if collision: return False

        return self.newLOSRecursive(ray, increment + 1)
    
    def newLOS(self, pos):
        if self.getTargetDistance(pos) > 500:
            return False
        
        cellsOnVector = self.grid.getCellsOnVector(self.rect.center, pos)
        
        ray = pygame.draw.line(self.grid.displaySurface, "red", self.rect.center, pos)
        #return self.newLOSRecursive(ray, 0)
        collision = ray.collideobjects(cellsOnVector, key = lambda r: r.rect)
        if collision:
            return False
        return True

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
        self.attackSprite = romanSpriteSheet.parseSprite("Battle Axe & Shield/Attack/AttackSwing_East_0.png").convert()
        Entity.__init__(self, name, image, pos, 3)
        