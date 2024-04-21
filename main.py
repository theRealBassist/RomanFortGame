import pygame
from entity import Roman
from terrainGeneration import Generate
from grid import Grid, Forest, Cell
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

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

    seed = random.randint(0,256)

    terrain = Generate(WORLD_X, WORLD_Y, random.randint(0,1000))
    
    grid = Grid()
    grid.drawTiles(terrain.tileMap)

    treesMap = Generate(WORLD_X, WORLD_Y, random.randint(0,1000))
    trees = Forest()
    trees.drawTiles(treesMap.tileMap, grid)
    map = grid.currentImage

    pygame.display.set_caption("Roman Fort Game")

    cameraGroup = CameraGroup(grid.displaySurface)
    

    for x, __ in enumerate(range(25)):
        position = (random.randint(100, 1000), random.randint(100, 1000))
        cell = grid.getCell(position)
        nearbyCells = grid.getNearbyCells(cell.getGridLocation())
        anyImpassable = False
        for cell in nearbyCells:
            if cell.impassable:
                anyImpassable = True
                break
        if not anyImpassable:
            entity = Roman(x, position)
            entity.setSpriteGroup(cameraGroup)
    
    cameraGroup.add(trees.cells.values())

    #logging.debug(f"WORLD_X = {WORLD_X}, WORLD_Y = {WORLD_Y}")
    cameraGroup.update(grid)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEWHEEL:
                cameraGroup.zoomScale += event.y * 0.03
                logging.debug(f"Zoom change of {event.y}")
                cameraGroup.changedZoom = True
        fps = clock.get_fps()

        cameraGroup.customDraw(cameraGroup.sprites()[0], fps)
        for entity in cameraGroup:
            if type(entity) is not Cell:
                target = grid.cells[random.randint(0, WORLD_X - 1), random.randint(0, WORLD_Y - 1)].getPixelLocation()
                entity.setTarget(target)

        cameraGroup.update(grid)

        pygame.display.flip()
        clock.tick(60)


    pygame.quit()




