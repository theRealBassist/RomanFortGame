import pygame
from grid import Grid
from spritesheet import Spritesheet
from config import *
import time

class Entity(pygame.sprite.Sprite):

    def __init__(self, name: str, sprite: pygame.Surface, pos: tuple, moveSpeed: int):
        pygame.sprite.Sprite.__init__(self)
        self.surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT), pygame.SRCALPHA)
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
        self.LOSCooldown = 0
        self.followCooldown = 0
        self.animationCounter = 0
        
    def getAnimationDirection(self) -> int:
        x, y = self.direction.x, self.direction.y
        #logging.debug(f"with {x}, {y} direction, ")
        if abs(x) > abs(y) - .15:
            if x < 0:
                return 3
            else:
                return 2
        else:
            if y < 0:
                return 0
            else:
                return 1
    
    def setAnimationFrame(self, animation: dict) -> None:
        if self.animationCounter >= list(animation.keys())[-1]: self.animationCounter = 0
        self.image = animation[self.animationCounter]
        self.animationCounter += 1

    def getTargetDirection(self, pos: tuple) -> pygame.math.Vector2:
        selfPos = pygame.math.Vector2(self.getPosition())
        targetPos = pygame.math.Vector2(pos)
        direction = pygame.math.Vector2(targetPos.x - selfPos.x, targetPos.y - selfPos.y)
        if direction.length() > 0 : 
            return direction.normalize()
        else:
            return direction

    def getTargetDistance(self, pos: tuple) -> float:
        selfPos = pygame.math.Vector2(self.getPosition())
        targetPos = pygame.math.Vector2(pos)
        
        return selfPos.distance_to(targetPos)

    #this is used to find the angle difference between the straight-line path to the current target and the current direction of the followTarget
    def getTargetAngleToCurrentTarget(self, target: pygame.sprite.Sprite) -> float:
        selfAngleToTarget = self.getTargetDirection(self.target)
        followTargetCurrentDirection = target.direction
        angle = abs(selfAngleToTarget.angle_to(followTargetCurrentDirection))

        return angle

    def checkArrived(self) -> bool:
        if  self.distance < 10:
                self.isMoving = False
                self.target = None
        if not self.getLOS(self.target):
            self.isMoving = False
            self.target = None

    def stopFollowing(self) -> None:
        self.followCooldown = 60
        self.following = False
        self.followTarget = None
        self.image = self.defaultSprite

    def startFollowing(self, target: pygame.sprite.Sprite) -> None:
        self.following = True
        self.followTarget = target
        self.image = self.attackSprite

    def move(self) -> None:
        start = time.perf_counter()
        if not self.target == None:
            #logging.debug(f"Entity {self.name} has a target of {self.target}")
            distanceToTarget = self.getTargetDistance(self.target)
            if distanceToTarget < 10: 
                self.isMoving = False 
                self.target = None 
                return
            direction = self.getTargetDirection(self.target) 
            if self.LOSCooldown <= 0: 
                self.LOSCooldown = 7
                targetLOS = self.getLOS(self.target)
            else:
                targetLOS = True
            if not targetLOS: 
                self.isMoving = False
                self.target = None
                return
            if self.followCooldown <= 0:
                if not self.getStillFollowing():
                    self.getFollowTarget()
            else:
                self.followCooldown -= 1
            if self.following and self.direction is not None:
                directionToTarget = self.getTargetDirection(self.followTarget.getPosition())
                distanceToTarget = self.getTargetDistance(self.followTarget.getPosition())
                direction = self.direction.lerp(directionToTarget, .85).normalize()
                modifier = 1
                if distanceToTarget < 2 : modifier = 5
                directionPosition = (direction * modifier) * (self.getTargetDistance(distanceToTarget))
                targetLOS = self.getLOS(directionPosition)
                if not targetLOS:
                    self.stopFollowing()
            
            if targetLOS:
                self.direction = direction                   
            else: 
                self.isMoving = False
                self.target = None
            if self.direction is not None:    
                self.setPosition(self.getPosition() + self.direction * self.moveSpeed)
        self.setAnimationFrame(self.walkAnimations[self.getAnimationDirection()])
        end = time.perf_counter()
        #logging.debug(f"Move executed in {end - start}")
        self.LOSCooldown -= 1

    
    def getFollowTarget(self) -> None:
        if self.getStillFollowing(): 
            self.startFollowing(self.followTarget)
            return

        followCandidate = (35, 0)
        
        for entity in self.group:
            if type(entity) is Entity:
                entityPosition = entity.getPosition()
                if self.getTargetDistance(entityPosition) > 100 or self.getTargetDistance(entityPosition) < 2 or entity.direction is None: continue
                angle = self.getTargetAngleToCurrentTarget(entity)
                if angle < followCandidate[0] and angle > 2:
                    followCandidate = (angle, entity)
        
        if followCandidate[1] != 0:
            self.startFollowing(followCandidate[1])
        else:
            self.stopFollowing()

    def checkFollowLoopRecursive(self, original: pygame.sprite.Sprite, visited = []) -> bool:
        if self.followTarget is None:
            return False
        if self.followTarget is original or self.followTarget in visited:
            return True
        
        visited.append(self)
        return self.followTarget.checkFollowLoopRecursive(original, visited)

    def getStillFollowing(self) -> bool:
        if not self.following: 
            return False

        if self.getTargetDistance(self.followTarget.getPosition()) < 10:
            self.stopFollowing()
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

    def getLOS(self, pos: tuple) -> bool:
        if self.getTargetDistance(pos) > 500:
            self.LOSCooldown = 0
            return False
        ray = pygame.draw.line(self.surface, (0, 0, 0, 255), self.getPosition(), pos, width=1)
        cellsOnVector = self.grid.getCellsOnVectorCollision(self.getPosition(), pos, ray)
        if cellsOnVector:
            self.LOSCooldown = 0
            return False
        return True

    def update(self, grid: Grid) -> None:

        self.grid = grid
        self.cellCurrent = grid.getCell(self.getPosition())

        if self.target: 
            #self.direction = self.getTargetDirection(self.target)
            self.isMoving = True
            self.move()

    def setTarget(self, pos: tuple) -> None:
        if not self.isMoving:
            self.target = pos

    def setSpriteGroup(self, group: pygame.sprite.Group) -> None:
        self.group = group
        self.group.add(self)

    def setPosition(self, position: tuple) -> None:
        self.rect.center = position
    
    def getPosition(self) -> tuple:
        return self.rect.center

class Roman(Entity):
    def __init__(self, name: str, pos: tuple) -> None:
        romanSpriteSheet = Spritesheet("assets/sprites/roman_test/blue/blue.png")
        self.defaultSprite = romanSpriteSheet.parseSprite("Walk/Walk_South_0.png").convert()
        
        walkNorthAnimation = romanSpriteSheet.getAnimationFrames("Walk/Walk_North", 4)
        walkSouthAnimation = romanSpriteSheet.getAnimationFrames("Walk/Walk_South", 4)
        walkEastAnimation = romanSpriteSheet.getAnimationFrames("Walk/Walk_East", 4)
        walkWestAnimation = romanSpriteSheet.getAnimationFrames("Walk/Walk_West", 4)
        self.walkAnimations = [walkNorthAnimation, walkSouthAnimation, walkEastAnimation, walkWestAnimation]
        self.attackSprite = romanSpriteSheet.parseSprite("Battle Axe & Shield/Attack/AttackSwing_East_0.png").convert()
        Entity.__init__(self, name, self.defaultSprite, pos, 3)
        