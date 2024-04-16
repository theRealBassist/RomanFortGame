from perlin_noise import PerlinNoise
from config import *

class Generate:

    def __init__(self, height, width, random_seed):
        self.generateNoiseMap(height, width, random_seed)

        valueList = [item for subList in self.noiseMap for item in subList]
        self.minValue = min(valueList)
        self.maxValue = max(valueList)

        weights = [0, 5, 10, 5, 50, 20, 0] 

        self.tileMap = self.generateTiledMap(weights)

    
    def generateNoiseMap(self, width, height, random_seed):
        self.noiseMap = []

        noise1 = PerlinNoise(octaves=3, seed=random_seed)
        noise2 = PerlinNoise(octaves=6, seed=random_seed)
        noise3 = PerlinNoise(octaves=12, seed=random_seed)
        noise4 = PerlinNoise(octaves=24, seed=random_seed)

        xpix, ypix = (width) + 1, (height) + 1
        for j in range(ypix):
            row = []
            for i in range(xpix):
                noiseValue = noise1([i/xpix, j/ypix])
                noiseValue += 0.5 * noise2([i/xpix, j/ypix])
                noiseValue += 0.25 * noise3([i/xpix, j/ypix])
                noiseValue += 0.125 * noise4([i/xpix, j/ypix])
                row.append(noiseValue)
            self.noiseMap.append(row)
    
    def generateTiledMap(self, weights):
        totalWeight = sum(weights)
        totalRange = self.maxValue - self.minValue

        # calculate maximum height for each terrain type, based on weight values
        maxTerrainHeights = []
        previousHeight = self.minValue
        for terrainType in ALL_TERRAIN_TYPES:
            height = totalRange * (weights[terrainType] / totalWeight) + previousHeight
            maxTerrainHeights.append(height)
            previousHeight = height
        maxTerrainHeights[SNOW] = self.maxValue

        tileMap = []

        for row in self.noiseMap:
            mapRow = []
            for value in row:
                for terrainType in ALL_TERRAIN_TYPES:
                    if value <= maxTerrainHeights[terrainType]:
                        mapRow.append(terrainType)
                        break

            tileMap.append(mapRow)
        return tileMap