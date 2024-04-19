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

    x = 0
    while x < 75:
        entity = Roman(x, (random.randint(WORLD_WIDTH // 2 - 50, WORLD_WIDTH // 2 + 50), random.randint(WORLD_HEIGHT // 2 -50, WORLD_HEIGHT // 2 + 50)))
        entity.setSpriteGroup(cameraGroup)
        x += 1

    cameraGroup.update(grid)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        cameraGroup.customDraw(grid.currentImage)
        cameraGroup.update(grid)

        for entity in cameraGroup:
            target = grid.cells[(random.randint(25, 75), random.randint(25,75))].getPixelLocation()
            entity.setTarget(target)



        pygame.display.update()
        #print(clock.get_fps())
        clock.tick(60)


    pygame.quit()




