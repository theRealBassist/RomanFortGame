import pygame
from spritesheet import Spritesheet
from entity import Entity, Roman
from terrainGeneration import Generate
from grid import Grid
from camera import CameraGroup
from config import *
import random

if __name__ == "__main__":

    pygame.init()
    clock = pygame.time.Clock()
    running = True

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    seed = random.randint(0,256)

    terrain = Generate(WORLD_X, WORLD_Y, random.randint(0,256))
    grid = Grid()
    grid.drawTiles(terrain.tileMap)
    map = grid.currentImage

    pygame.display.set_caption("Roman Fort Game")

    cameraGroup = CameraGroup()

    for x, __ in enumerate(range(25)):
        entity = Roman(x, (random.randint(WORLD_WIDTH // 2 - 150, WORLD_WIDTH // 2 + 150), random.randint(WORLD_HEIGHT // 2 -150, WORLD_HEIGHT // 2 + 150)))
        entity.setSpriteGroup(cameraGroup)

    cameraGroup.update(grid)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        

        
        cameraGroup.customDraw(grid.currentImage, cameraGroup.sprites()[0])
        
        cameraGroup.update(grid)

        for entity in cameraGroup:
            target = grid.cells[(random.randint(0, 125), random.randint(0,125))].getPixelLocation()
            entity.setTarget(target)



        pygame.display.flip()
        print(clock.get_fps())
        clock.tick(60)


    pygame.quit()




