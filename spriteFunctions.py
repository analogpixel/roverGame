"""
Function to handle sprites
"""
import os.path
import pygame
from localutil import *
import math

def createSprite(name, pos=(0,0)):
  """
  Create a sprite object
  """
  return {
    "name": name,
    "r": 90,
    "x": pos[0],
    "y": pos[1],
    "xdest": pos[0],
    "ydest": pos[1],
    "rdest": 90,
    "state": "stopped",
    "oldState": "stopped",
    "moveable": True,
    "imageCache": {},
    "active": False,
    "sound": False
  }

def updateState(data):
  # http://www.pygame.org/docs/ref/mixer.html
  if data['oldState'] != data['state']:

    # stop any existing sounds
    if data['sound']:
      data['sound'].stop()

    path = "resources/%s_%s.wav" % (data['name'], data['state'])
    if os.path.exists(path):
      data['sound'] = pygame.mixer.Sound(path)
      data['sound'].play(fade_ms=1000)
    else:
      data['sound'] = False

  data['oldState'] = data['state']
  return data

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    #rot_rect = orig_rect.copy()
    #rot_rect.center = rot_image.get_rect().center
    #rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def drawSprite(data,tic, fps, canvas):
  """
  draw a sprite and return the updated data
  """
  imageFile = "resources/%s_%s.png" % (data['name'], data['state'])

  if not (imageFile in data['imageCache']):
     data['imageCache'][imageFile] =  pygame.image.load(imageFile).convert_alpha()

  frameCount = data['imageCache'][imageFile].get_width() / 100
  currentFrame = int(translate( tic % fps , 0, fps, 0, frameCount))

  s = pygame.Surface((100,100), pygame.SRCALPHA, 16).convert_alpha()
  s.blit(  data['imageCache'][imageFile] , (0,0) , ( currentFrame * 100, 0, 100,100))
  s = rot_center(s , int(data['r']) * -1)

  canvas.blit( s , (data['x'] , data['y'] ) )

  return data


def moveSprite(data):
  state = "stopped"
  for c in ['x','y','r']:
    if not( data[c] == data[c + "dest"]):
      #print c,data[c], data[c + "dest"]
      data[c] += 5 * int( (data[c + "dest"] - data[c]) / abs(data[c + "dest"] - data[c]) )
      state = "moving"

  data['state'] = state
  return data


def drawCommands(data, commandImage, commandLayout, screenHeight, tileSize, screen):
  if not ("commandq" in data):
    return data
  x = 0
  for command in reversed(data['commandq']):
    if command in commandLayout:
      screen.blit( commandImage , (x, screenHeight - tileSize), (commandLayout[command], 0, 100,100))
      x = x + tileSize
  return data


def spriteCrash(a,b):
  return (a['x'] == b['x'] and a['y'] == b['y'])
