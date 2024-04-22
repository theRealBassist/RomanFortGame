import pygame
from config import *
import logging

from entity import Entity

class CameraGroup(pygame.sprite.Group):
    def __init__(self, surface: pygame.Surface) -> None:
        super().__init__()

        self.displaySurface = pygame.display.get_surface()

        self.offset = pygame.math.Vector2()
        self.halfWidth = self.displaySurface.get_size()[0] // 2
        self.halfHeight = self.displaySurface.get_size()[1] // 2

        self.cameraBorders = {"left": 200, "right": 200, "top": 100, "bottom": 100}
        left = self.cameraBorders["left"]
        top = self.cameraBorders["top"]
        width = WINDOW_WIDTH - (self.cameraBorders["left"] - self.cameraBorders["right"])
        height = WINDOW_HEIGHT - (self.cameraBorders["top"] - self.cameraBorders["bottom"])
        self.cameraRect = pygame.Rect(left, top, width, height)
        self.zoomScale = 1
        self.internalSurfSize = (2500,2500)
        self.internalSurf = pygame.Surface(self.internalSurfSize, pygame.SRCALPHA)
        self.internalRect = self.internalSurf.get_rect(center = (self.halfWidth, self.halfHeight))
        self.internalSurfSizeVector = pygame.math.Vector2(self.internalSurfSize)
        self.internalSurfOffset = pygame.math.Vector2()
        self.internalSurfOffset.x = self.internalSurfSize[0] // 2 - self.halfWidth
        self.internalSurfOffset.y = self.internalSurfSize[1] // 2 - self.halfHeight

        self.keyBoardSpeed = 5

        self.groundSurface = surface
        self.groundRect = self.groundSurface.get_rect(topleft = (0,0))

    def centerTargetCamera(self, target: Entity) -> None:
        if target.rect.centerx > self.halfWidth and target.rect.centerx < WORLD_WIDTH - self.halfWidth:
            self.offset.x = target.rect.centerx - self.halfWidth
        if target.rect.centery > self.halfHeight and target.rect.centery < WORLD_HEIGHT - self.halfHeight:
            self.offset.y = target.rect.centery - self.halfHeight

    def boxTargetCamera(self, target: Entity) -> None:
        if target.rect.centerx > self.halfWidth and target.rect.centerx < WORLD_WIDTH - self.halfWidth:
            if target.rect.left < self.cameraRect.left:
                self.cameraRect.left = target.rect.left
            if target.rect.right > self.cameraRect.right:
                self.cameraRect.right = target.rect.right
        if target.rect.centery > self.halfHeight and target.rect.centery < WORLD_HEIGHT - self.halfHeight:
            if target.rect.top < self.cameraRect.top:
                self.cameraRect.top = target.rect.top
            if target.rect.bottom > self.cameraRect.bottom:
                self.cameraRect.bottom = target.rect.bottom

        self.offset.x = self.cameraRect.left - self.cameraBorders["left"]
        self.offset.y = self.cameraRect.top - self.cameraBorders["top"]

    def keyboardControl(self) -> None:
        keys = pygame.key.get_pressed()

        #if self.offset.x - self.cameraBorders["left"] > 0:
        if keys[pygame.K_a]: 
            self.cameraRect.x -= self.keyBoardSpeed
        #if self.offset.x + self.cameraBorders["right"] < WORLD_WIDTH:
        if keys[pygame.K_d]: 
            self.cameraRect.x += self.keyBoardSpeed
        #if self.offset.y - self.cameraBorders["top"] > 0:
        if keys[pygame.K_w]: 
            self.cameraRect.y -= self.keyBoardSpeed
        #if self.offset.y + self.cameraBorders["bottom"] < WORLD_HEIGHT:
        if keys[pygame.K_s]: 
            self.cameraRect.y += self.keyBoardSpeed

        self.offset.x = self.cameraRect.left - self.cameraBorders["left"]
        self.offset.y = self.cameraRect.top - self.cameraBorders["top"]
    
    def zoomKeyboardControl(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.zoomScale +=0.1
        if keys[pygame.K_e]:
            self.zoomScale -=0.1

    def scaleSurface(self) -> None:
        self.scaledSurface = pygame.transform.scale(self.internalSurf, self.internalSurfSizeVector * self.zoomScale)
        self.scaledRect = self.scaledSurface.get_rect(center = (self.halfWidth, self.halfHeight))
        self.displaySurface.blit(self.scaledSurface, self.scaledRect)
        logging.debug(f"changedZoom = {self.zoomScale}")
        
    def blitSprites(self) -> None:
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offsetPos = sprite.rect.topleft - self.offset + self.internalSurfOffset
            self.internalSurf.blit(sprite.image, offsetPos)

    def displayFPS(self) -> None:
        if self.fps is not None:
            font = pygame.font.SysFont("Verdana", 20)
            self.displaySurface.blit (font.render((str(int(self.fps))), True, "black"), (10, 10))
   
    def customDraw(self, player: Entity = None, fps: float = None) -> None:
        self.fps = fps

        #self.centerTargetCamera(player)
        #self.boxTargetCamera(player)
        self.keyboardControl()

        self.internalSurf.fill("green")

        groundOffset = self.groundRect.topleft - self.offset  + self.internalSurfOffset
        self.internalSurf.blit(self.groundSurface, groundOffset)

        self.blitSprites()
        self.scaleSurface()
        self.displayFPS()

        
        
        