"""
Function to handle maps
"""
import json
import pygame
import math

def loadMap(filename, grassFile=None):
  """
  filename  : filename of json map data
  tileFile  : filename that contains tile image data
  grassFile : filename of grass if using
  """
  mapData = json.loads( open(filename).read() )

  if grassFile:
    grassTexture = pygame.image.load(grassFile)

  mapTileImage = pygame.image.load(mapData['tilesets'][0]['image']).convert_alpha()
  mapWidth     = mapData['layers'][0]['width'] 
  mapHeight    = mapData['layers'][0]['height'] 
  tileWidth    = mapData['tilewidth']
  tileHeight   = mapData['tileheight']

  mapImage = pygame.Surface( (mapWidth * tileWidth, mapHeight * tileHeight))

  x = 0
  y = 0
  tileData = {}
  
  for tile in mapData['layers'][0]['data']:
    t = int(mapData['tilesets'][0]['imageheight'] / mapData['tilesets'][0]['tileheight'])
    tilex = int((tile-1) % t ) * tileWidth
    tiley = int((tile-1) / t ) * tileHeight
    tileData["%s,%s" % (x,y)] = mapData['tilesets'][0]['tileproperties'][str(tile)]

    if grassFile:
      mapImage.blit(grassTexture, (x * tileWidth, y* tileHeight ))

    mapImage.blit( mapTileImage.subsurface( \
      (tilex,tiley, tileWidth, tileHeight)), (x * tileWidth, y * tileHeight))

    x += 1
    if x >= mapWidth:
      x = 0
      y += 1


  # function to tell us if the current x,y is a crash point
  crashFunction = lambda x,y: tileData["%s,%s" % ( int(math.ceil(x/100)) ,int(math.ceil(y/100)) )]['crash'] == "true"

  return [mapImage, crashFunction, tileWidth, (800,300) ]
