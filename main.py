import pygame
from entity import Roman
from terrainGeneration import Generate
from grid import Grid
from camera import CameraGroup
from config import *
import random
import logging

if __name__ == "__main__":
    loggingLevel = logging.DEBUG
    fmt = '[%(levelname)s] %(asctime)s - %(message)s'
    logging.basicConfig(level=loggingLevel, format = fmt)

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

    for x, __ in enumerate(range(100)):
        position = (random.randint(100, 1000), random.randint(100, 1000))
        if not grid.getCell(position).impassable:
            entity = Roman(x, position)
            entity.setSpriteGroup(cameraGroup)

    logging.debug(f"WORLD_X = {WORLD_X}, WORLD_Y = {WORLD_Y}")
    cameraGroup.update(grid)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        fps = clock.get_fps()

        
        cameraGroup.customDraw(grid.currentImage, cameraGroup.sprites()[0], fps)
        
        

        for entity in cameraGroup:
            target = grid.cells[random.randint(0, WORLD_X - 1), random.randint(0, WORLD_Y - 1)].getPixelLocation()
            entity.setTarget(target)

        cameraGroup.update(grid)

        pygame.display.flip()
        clock.tick(60)


    pygame.quit()




