"""
Function to handle maps
"""
import json
import pygame
import math
from spriteFunctions import *

def loadMap(system):
  mapData = json.loads( open("./maps/map" + str(system['currentMap']) + ".json" ).read() )

  # clear out the sprites
  system = createSprite("robot", system)
  system = createSprite("goal", system)

  if system['grassTexture']:
    grassTexture = pygame.image.load(system['grassTexture'])

  system['commandq']              = []
  system['mapTileImage']          = pygame.image.load(mapData['tilesets'][0]['image']).convert_alpha()
  system['mapWidth']              = mapData['layers'][0]['width']
  system['mapHeight']             = mapData['layers'][0]['height']
  system['tileWidth']             = mapData['tilewidth']
  system['tileHeight']            = mapData['tileheight']
  system['sprite_robot']['x']     = int(mapData['properties']['robotStartLocationX']) * 100
  system['sprite_robot']['xdest'] = int(mapData['properties']['robotStartLocationX']) * 100
  system['sprite_robot']['y']     = int(mapData['properties']['robotStartLocationY']) * 100
  system['sprite_robot']['ydest'] = int(mapData['properties']['robotStartLocationY']) * 100
  system['sprite_goal']['x']      = int(mapData['properties']['finishLocationX']) * 100
  system['sprite_goal']['xdest']  = int(mapData['properties']['finishLocationX']) * 100
  system['sprite_goal']['y']      = int(mapData['properties']['finishLocationY']) * 100
  system['sprite_goal']['ydest']  = int(mapData['properties']['finishLocationY']) * 100
  system['mapImage']              = pygame.Surface( (system['mapWidth'] * system['tileWidth'],\
                                                     system['mapHeight'] * system['tileHeight']))

  x = 0
  y = 0
  tileData = {}

  for tile in mapData['layers'][0]['data']:
    t = int(mapData['tilesets'][0]['imageheight'] / mapData['tilesets'][0]['tileheight'])
    tilex = int((tile-1) % t ) * system['tileWidth']
    tiley = int((tile-1) / t ) * system['tileHeight']
    tileData["%s,%s" % (x,y)] = mapData['tilesets'][0]['tileproperties'][str(tile)]

    if system['grassTexture']:
      system['mapImage'].blit(grassTexture, (x * system['tileWidth'], y* system['tileHeight'] ))

    system['mapImage'].blit( system['mapTileImage'].subsurface( \
      (tilex,tiley, system['tileWidth'], \
       system['tileHeight'])), (x * system['tileWidth'], y * system['tileHeight']))

    x += 1
    if x >= system['mapWidth']:
      x = 0
      y += 1


  # function to tell us if the current x,y is a crash point
  system['crashFunction'] = lambda x,y: tileData["%s,%s" % ( int(math.ceil(x/100)) ,int(math.ceil(y/100)) )]['crash'] == "true"

  return system
