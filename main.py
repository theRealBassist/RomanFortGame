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
    dt = 0

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    seed = random.randint(0,256)

    terrain = Generate(WORLD_X, WORLD_Y, random.randint(0,256))
    grid = Grid(screen)
    grid.drawTiles(terrain.tileMap)
    map = grid.currentImage

    pygame.display.flip()
    pygame.display.set_caption("Roman Fort Game")

    cameraGroup = CameraGroup()
    player = Roman("Player", (1000, 1000))
    cameraGroup.add(player)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        cameraGroup.customDraw(grid.currentImage, player)
        cameraGroup.update(grid, dt)

        pygame.display.update()

        dt = clock.tick(60) / 1000

    pygame.quit()




