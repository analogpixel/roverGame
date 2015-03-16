"""
Function to handle sprites
"""
import os.path
import pygame
from localutil import *
import math
import time

def createSprite(name, system):
#def createSprite(name, pos=(0,0)):
  """
  Create a sprite object
  """
  system["sprite_" + name] = {
    "name": name,
    "r": 90,
    "rdest": 90,
    "state": "stopped",
    "oldState": "stopped",
    "moveable": True,
    "imageCache": {},
    "active": False,
    "sound": False
  }

  return system

def updateState(system):
  # http://www.pygame.org/docs/ref/mixer.html
  if system['sprite_robot']['oldState'] != system['sprite_robot']['state']:

    oldState = "%s_%s" % (system['sprite_robot']['name'], system['sprite_robot']['oldState'])
    newState = "%s_%s" % (system['sprite_robot']['name'], system['sprite_robot']['state'])

    # stop any existing sounds
    if oldState in system['CONFIG']['C_SOUNDS']:
      system['CONFIG']['C_SOUNDS'][oldState]['sound'].stop()

    if newState in system['CONFIG']['C_SOUNDS']:
      system['CONFIG']['C_SOUNDS'][newState]['sound'].play(\
                                      loops=system['CONFIG']['C_SOUNDS'][newState]['loop'])
      time.sleep(0.2)

    system['sprite_robot']['oldState'] = system['sprite_robot']['state']
  return system

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    #rot_rect = orig_rect.copy()
    #rot_rect.center = rot_image.get_rect().center
    #rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def drawSprite(name, system):
  """
  draw a sprite and return the updated data
  """
  imageFile = "resources/%s_%s.png" % (name, system['sprite_' + name]['state'])

  if not (imageFile in system['sprite_' + name ]['imageCache']):
     system['sprite_' + name]['imageCache'][imageFile] =  pygame.image.load(imageFile).convert_alpha()

  fps = system['CONFIG']['C_FPS']
  frameCount = system['sprite_' + name]['imageCache'][imageFile].get_width() / 100
  currentFrame = int(translate( system['tic'] % fps , 0, fps, 0, frameCount))

  s = pygame.Surface((100,100), pygame.SRCALPHA, 16).convert_alpha()
  s.blit(  system['sprite_' + name]['imageCache'][imageFile] , (0,0) , ( currentFrame * 100, 0, 100,100))
  s = rot_center(s , int(system['sprite_' + name]['r']) * -1)

  system['screen'].blit( s , (system['sprite_' + name]['x'] , system['sprite_' + name]['y'] ) )

  return system


def moveSprite(system):
  for c in ['x','y','r']:
    if not( system['sprite_robot'][c] == system['sprite_robot'][c + "dest"]):
      system['sprite_robot'][c] += 5 * \
                                   int( (system['sprite_robot'][c + "dest"] - \
                                         system['sprite_robot'][c]) / \
                                        abs(system['sprite_robot'][c + "dest"] - \
                                            system['sprite_robot'][c]) )
  return system


def drawCommands(system):
  if not ("commandq" in system):
    return system
  x = 0

  system['controlImage'].fill( pygame.Color(0,0,0,0) )
  for command in reversed(system['commandq']):
    if command in system['commandLayout']:
      system['controlImage'].blit( system['commandImage'] , (x, 0), (system['commandLayout'][command], 0, 100,100))
      x = x + system['tileHeight']

  return system


def drawMenu(system):
  color = False
  for i in range(0, system['maxMap'] + 1):

    if i == system['currentMap']:
      color = pygame.Color(255,0,0,10)
    else:
      color = pygame.Color(0,0,255, 90)

    #system['screen'].fill(color, (300 ,300 + i  * 40,500,30), special_flags= pygame.BLEND_RGBA_MAX )
    pygame.draw.circle( system['screen'], (55,113,200), (560, 510 + 40 *  system['currentMap']) ,10)
    system = text("Mission " + str( i + 1) ,500, 500 + i * 40, system)

  return system


def text(t,x,y, system):
  if pygame.font:
    font = pygame.font.Font(None, 36)
    text = font.render(t, 1, (10, 10, 10))
    textpos = text.get_rect(centerx=system['screen'].get_width()/2 )
    textpos[1] = y
    system['screen'].blit(text, textpos)
  return system
