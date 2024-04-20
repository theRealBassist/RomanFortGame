import pygame
from spritesheet import Spritesheet
import math
from config import *
import time
import logging

class Entity(pygame.sprite.Sprite):

    def __init__(self, name, sprite, pos, moveSpeed):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.defaultSprite = sprite
        self.image =  sprite
        self.moveSpeed = moveSpeed
        self.direction = None
        self.rect = self.image.get_rect(center = pos) 
        self.gridPos = (round(abs((pos[0] - (TILESIZE / 2))) / TILESIZE), round((abs(pos[1] - (TILESIZE / 2))) / TILESIZE))
        self.isMoving = False
        self.target = None
        self.followTarget = None
        self.following = False

    def getTargetDirection(self, pos):
        selfPos = pygame.math.Vector2(self.getPosition())
        targetPos = pygame.math.Vector2(pos)
        direction = pygame.math.Vector2(targetPos.x - selfPos.x, targetPos.y - selfPos.y)
        if direction.length() > 0 : 
            return direction.normalize()
        else:
            return direction

    def getTargetDistance(self, pos):
        selfPos = pygame.math.Vector2(self.getPosition())
        targetPos = pygame.math.Vector2(pos)
        
        return selfPos.distance_to(targetPos)

    #this is used to find the angle difference between the straight-line path to the current target and the current direction of the followTarget
    def getTargetAngleToCurrentTarget(self, target):
        selfAngleToTarget = self.getTargetDirection(self.target)
        followTargetCurrentDirection = target.direction
        angle = abs(selfAngleToTarget.angle_to(followTargetCurrentDirection))

        return angle

    def checkArrived(self):
        if  self.distance < 10:
                self.isMoving = False
                self.target = None
        if not self.getLOS(self.target):
            self.isMoving = False
            self.target = None

    def stopFollowing(self):
        self.following = False
        self.followTarget = None
        self.image = self.defaultSprite

    def startFollowing(self, target):
        self.following = True
        self.followTarget = target
        self.image = self.attackSprite

    def move(self):
        start = time.perf_counter()
        if not self.target == None:
            logging.debug(f"Entity {self.name} has a target of {self.target}")
            distanceToTarget = self.getTargetDistance(self.target)
            if distanceToTarget < 10: 
                self.isMoving = False 
                self.target = None 
                return
            direction = self.getTargetDirection(self.target) 
            targetLOS = self.getLOS(self.target)
            if not targetLOS: 
                self.isMoving = False
                self.target = None
                return
            if not self.getStillFollowing():
               self.getFollowTarget()
            if self.following and self.direction is not None:
                directionToTarget = self.getTargetDirection(self.followTarget.getPosition())
                distanceToTarget = self.getTargetDistance(self.followTarget.getPosition())
                direction = self.direction.lerp(directionToTarget, .85).normalize()
                targetLOS = self.getLOS(self.followTarget.getPosition())
            
            if targetLOS:
                self.direction = direction                   
            else: 
                self.isMoving = False
                self.target = None
            if self.direction is not None:    
                self.setPosition(self.getPosition() + self.direction * self.moveSpeed)
        end = time.perf_counter()
        logging.debug(f"Move executed in {end - start}")

    
    def getFollowTarget(self):
        if self.getStillFollowing(): 
            self.startFollowing(self.followTarget)
            return

        followCandidate = (35, 0)
        
        for entity in self.group:
            entityPosition = entity.getPosition()
            if self.getTargetDistance(entityPosition) > 100 or self.getTargetDistance(entityPosition) < 2 or entity.direction is None: continue
            angle = self.getTargetAngleToCurrentTarget(entity)
            if angle < followCandidate[0] and angle > 2:
                followCandidate = (angle, entity)
        
        if followCandidate[1] != 0:
            self.startFollowing(followCandidate[1])
        else:
            self.stopFollowing()

    def checkFollowLoopRecursive(self, original, visited = []):
        if self.followTarget is None:
            return False
        if self.followTarget is original or self.followTarget in visited:
            return True
        
        visited.append(self)
        return self.followTarget.checkFollowLoopRecursive(original, visited)

    def getStillFollowing(self):
        if not self.following: 
            return False

        if self.getTargetDistance(self.followTarget.getPosition()) < 10:
            return False

        angle = self.getTargetAngleToCurrentTarget(self.followTarget)
        followTargetDistance = self.followTarget.getTargetDistance(self.target)
        targetDistance = self.getTargetDistance(self.target)

        if angle <= 30 and followTargetDistance < targetDistance:
            self.startFollowing(self.followTarget)
            return True
        else:
            self.stopFollowing()
            return False
        
    #def getLOSRecursive(self):

    
    def getLOS(self, pos):
        if self.getTargetDistance(pos) > 500:
            return False
        
        #need to optimize this 
        
        
        ray = pygame.draw.line(self.grid.displaySurface, "red", self.getPosition(), pos)
        cellsOnVector = self.grid.getCellsOnVectorCollision(self.getPosition(), pos, ray)
        #collision = ray.collideobjects(cellsOnVector, key = lambda r: r.rect)
        if cellsOnVector:
            return False
        if self.cellCurrent.impassable: 
            print("missed me")
        return True

    def update(self, grid):

        self.grid = grid
        self.cellCurrent = grid.getCell(self.getPosition())

        if self.target: 
            #self.direction = self.getTargetDirection(self.target)
            self.isMoving = True
            self.move()

    def setTarget(self, pos):
        if not self.isMoving:
            self.target = pos

    def setSpriteGroup(self, group):
        self.group = group
        self.group.add(self)

    def setPosition(self, position):
        self.rect.center = position
    
    def getPosition(self):
        return self.rect.center

class Roman(Entity):
    def __init__(self, name, pos):
        romanSpriteSheet = Spritesheet("assets/sprites/roman_test/blue/blue.png")
        image = romanSpriteSheet.parseSprite("Walk/Walk_South_0.png").convert()
        self.attackSprite = romanSpriteSheet.parseSprite("Battle Axe & Shield/Attack/AttackSwing_East_0.png").convert()
        Entity.__init__(self, name, image, pos, 3)
        