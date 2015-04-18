"""
Interface to the buttons on the pi
"""
import RPi.GPIO as GPIO
from robotCommands import *
from mapFunctions import *

def configGPIO(system):
  GPIO.cleanup()
  GPIO.setmode(GPIO.BCM)

  for opt in system['CONFIG']['C_GPIOCONFIG']:
    GPIO.setup( int(opt['in']) , GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup( int(opt['out']), GPIO.OUT)
    GPIO.add_event_detect( int(opt['in']) , GPIO.FALLING,bouncetime=400)

  return system

def updateLights(system):
  # clear all
  for opt in system['CONFIG']['C_GPIOCONFIG']:
    GPIO.output( int( opt['out'] ), 0)

  # based on the mode setup the lights
  if system['state'] == "game":
    for b in system['CONFIG']['C_GAMEBUTTONS']:
      GPIO.output(int(b), 1)
  if system['state'] == "menu":
    for b in system['CONFIG']['C_MENUBUTTONS']:
      GPIO.output(int(b),1)

  return system

def pollGPIO(system):
  for opt in system['CONFIG']['C_GPIOCONFIG']:
    if GPIO.event_detected(int(opt['in'])):
      system['updateScreen'] = True

      print("Event on %s\n" % opt['in'])

      if opt['command'] == "activate":
        if system['state'] == "game":
          system['sprite_robot']['state'] = "moving"
        if system['state'] == "menu":
          system = loadMap(system)
          system['state'] = "game"


      if opt['command'] == "turnClockwise":
        if system['state'] == "game":
          system = pushQ("turnClockwise", system)
        if system['state'] == "menu":
          system['updateMenu'] = True
          system['currentMap'] = system['currentMap'] + 1
          if system['currentMap'] > system['maxMap']:
            system['currentMap'] = 0
          system = loadMap(system)

      if opt['command'] == "turnCounterClockwise":
        if system['state'] == "game":
          system = pushQ("turnCounterClockwise", system)
        if system['state'] == "menu":
          system['updateMenu'] = True
          system['currentMap'] = system['currentMap'] - 1
          if system['currentMap'] < 0:
            system['currentMap'] = system['maxMap']
          system = loadMap(system)

      if opt['command'] == "moveForward":
        if system['state'] == "game":
          system = pushQ("moveForward", system)

      if opt['command'] == "backspace":
        if system['state'] == "game":
          system = popQ(system)
          system['updateScreen'] = True

        if system['state'] == "game":
          system = pushQ("moveForward", system)

      if opt['command'] == "grid":
        system['grid'] = GPIO.input( int(opt['in']))
        system['grid'] = not system['grid']

        if system['grid']:
          GPIO.output( int(opt['out']), 1)
        else:
          GPIO.output( int(opt['out']), 0)

  return system
