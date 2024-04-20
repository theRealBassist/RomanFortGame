import pygame
import json

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.spriteSheet = pygame.image.load(filename).convert_alpha()
        self.metaData = self.filename.replace("png", "json")
        with open(self.metaData) as f:
            self.data = json.load(f)
        f.close

    def getSprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.spriteSheet, (0,0), (x, y, w, h))
        return sprite

    def parseSprite(self, name):
        sprite = self.data["frames"][name]["frame"]
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.getSprite(x, y, w, h)
        return image
    
    def getAnimationFrames(self, name, count):
        animationFrames = dict()
        for frame, _ in enumerate(range(count)):
            animationFrames[frame] = self.parseSprite(f"{name}_{frame}.png").convert_alpha()
        return animationFrames
