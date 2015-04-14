import sys
import ConfigParser
import time
import pygame
import os
from spriteFunctions import *
from mapFunctions import *
from localutil import *
from robotCommands import *

# http://www.pygame.org/docs/tut/newbieguide.html

def exitGame(system):
  if system['CONFIG']['C_USEGPIO']:
    GPIO.cleanup()
  sys.exit()

system = { 'CONFIG': {}, 'grid': False, 'updateMenu': True, 'updateScreen': False }
waitCount = 0

if __name__ == '__main__':

    # read configuration file
    c = ConfigParser.SafeConfigParser()
    if os.path.isfile("run.cfg"):
        c.read('run.cfg')
        system['CONFIG']['C_FULLSCREEN'] = c.getboolean('config', 'fullscreen')
        system['CONFIG']['C_WIDTH']      = c.getint('config', 'width')
        system['CONFIG']['C_HEIGHT']     = c.getint('config', 'height')
        system['CONFIG']['C_NOFRAME']    = c.getboolean('config', 'windowFrameOff')
        system['CONFIG']['C_GRIDON']     = c.getboolean('gameDynamics', 'gridValue')
        system['CONFIG']['C_HWSURF']     = c.getboolean('config', 'useHWSurface')
        system['CONFIG']['C_DBUFFER']    = c.getboolean('config', 'useDoubleBuffer')
        system['CONFIG']['C_USEGPIO']    = c.getboolean('config', 'useGPIO')
        system['CONFIG']['C_FPS']        = c.getint('config','fps')
        system['CONFIG']['C_COLORDEPTH'] = c.getint('config','colorDepth')
        system['CONFIG']['C_MAXMAPS']    = c.getint('config','maxmaps')
        system['CONFIG']['C_TILESIZE']   = 0 # define in loadMap
        system['CONFIG']['C_GPIOCONFIG'] = []

        for xyz in c.options('GPIO'):
          system['CONFIG']['C_GPIOCONFIG'].append( eval( c.get('GPIO',xyz)) )

        pygame.mixer.init()
        system['CONFIG']['C_SOUNDS'] = {}
        for xyz in c.options('sounds'):
          t = eval(c.get('sounds', xyz))
          system['CONFIG']['C_SOUNDS'][xyz] = {}
          system['CONFIG']['C_SOUNDS'][xyz]['sound'] = pygame.mixer.Sound( "resources/wav/%s" %  t['wav'] )
          system['CONFIG']['C_SOUNDS'][xyz]['loop']  = t['loop']
        system['CONFIG']['C_INPUTACTIVE'] = True

    pygame.init()

    flags = 0
    if system['CONFIG']['C_FULLSCREEN']:
      flags = flags | pygame.FULLSCREEN
    if system['CONFIG']['C_NOFRAME']:
      flags = flags | pygame.NOFRAME
    if system['CONFIG']['C_HWSURF']:
      flags = flags | pygame.HWSURFACE
    if system['CONFIG']['C_DBUFFER']:
      flags = flags | pygame.DOUBLEBUF



    system['commandLayout'] = {'turnClockwise':0 ,'turnCounterClockwise': 100 ,'moveForward':200 }
    system['clock']         = pygame.time.Clock()
    #system['screen']        = pygame.display.set_mode((system['CONFIG']['C_WIDTH'], \
                                                    #   system['CONFIG']['C_HEIGHT']), flags,\
                                                    #  system['CONFIG']['C_COLORDEPTH'])
    system['screen'] = pygame.display.set_mode( (0,0), flags)

    system['menuImage']     = pygame.image.load("./resources/menu.png").convert()
    system['commandImage']  = pygame.image.load("./resources/commands.png").convert()

    system['grassTexture']  = "./resources/grassTexture.jpg"
    system['currentMap']    = 0
    system['maxMap']        = system['CONFIG']['C_MAXMAPS']
    system = loadMap(system)
    system['state'] = "menu"
    system['tic'] = 0

    if system['CONFIG']['C_USEGPIO']:
      from buttonInterface import *
      system = configGPIO( system )

    while True:
      system['clock'].tick(system['CONFIG']['C_FPS'])
      system['tic'] += 1

      # there are two phases:
      # phase 1 input your commands
      # phase 2 let the commands run
      # in phase two no input is allowed
      if system['CONFIG']['C_INPUTACTIVE']:
        if system['CONFIG']['C_USEGPIO']:
          system = pollGPIO(system)

        for event in pygame.event.get():
          # game loop
          if system['state'] == "game":
            if event.type  ==  pygame.KEYDOWN:
              if event.key == pygame.K_LEFT:
                system = pushQ("turnCounterClockwise", system)
              if event.key == pygame.K_RIGHT:
                system = pushQ("turnClockwise", system)
              if event.key == pygame.K_UP:
                system = pushQ("moveForward", system)
              if event.key == pygame.K_p:
                system['sprite_robot']['state'] = "moving"
              if event.key == pygame.K_c:
                system = clearQ(system)
              if event.key == pygame.K_n:
                system['sprite_robot']['state'] = "moving"
              if event.key == pygame.K_g:
                system['grid'] = not system['grid']
                system['updateScreen'] = True

          # menu loop
          if system['state'] == "menu":
            if event.type  ==  pygame.KEYDOWN:
              system['updateMenu'] = True
              if event.key == pygame.K_DOWN:
                system['currentMap'] = system['currentMap'] + 1
                if system['currentMap'] > system['maxMap']:
                  system['currentMap'] = 0

              if event.key == pygame.K_UP:
                system['currentMap'] = system['currentMap'] - 1
                if system['currentMap'] < 0:
                  system['currentMap'] = system['maxMap']

              if event.key == pygame.K_n:
                system = loadMap(system)
                system['state'] = "game"
                system['updateScreen'] = True

          if event.type == pygame.QUIT or \
             (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
              exitGame(system)
              sys.exit()


      # if the menu needs to be updated draw it
      # otherwise do nothing
      if system['state'] == "menu":
        if system['updateMenu']:
          system['screen'].blit( system['menuImage'], (0,0) )
          system['updateMenu'] = False
        system = drawMenu(system)

      # wait for the timer to run down before showing the menu
      elif system['state'] == "wait":
        waitCount -= 1
        if waitCount < 0:
          system['state'] = "menu"
          system['updateMenu'] = True

      # if we aren't waiting or in the menu, then update the sprite
      # states
      else:
        system = calcWin(system)
        system = calcCrash(system)

        if system['sprite_robot']['state'] == "moving":
          system = updateRobot(system)
          system = moveSprite(system)

        # if we lose or win, wait 50 frames before going to the menu so we have time to see
        # the little explosion or winning frames
        if system['sprite_robot']['state'] == 'win' or system['sprite_robot']['state'] == 'lose':
          system['state'] = "wait"
          waitCount = 50

      # this is were we draw if this isn't the menu being updated
      if system['state'] != "menu":
        rx = system['sprite_robot']['x']
        ry = system['sprite_robot']['y']
        gx = system['sprite_goal']['x']
        gy = system['sprite_goal']['y']

        # if this is a full refresh then draw then entire screen
        # otherwise just draw around where the objects are changing
        if system['updateScreen']:
          system['updateScreen'] = False
          if system['grid']:
            system['screen'].blit( system['mapImageGrid'], (0,0) )
          else:
            system['screen'].blit( system['mapImage'], (0,0) )
        else:
          if system['grid']:
            system['screen'].blit( system['mapImageGrid'], (rx-30,ry-30), (rx-30,ry-30, 160,160 ))
            system['screen'].blit( system['mapImageGrid'], (gx-10,gy-10), (gx-10,gy-10, 120,120 ))
          else:
            system['screen'].blit( system['mapImage'], (rx-30,ry-30), (rx-30,ry-30, 160,160 ))
            system['screen'].blit( system['mapImage'], (gx-10,gy-10), (gx-10,gy-10, 120,120 ))

        # controlImage is the bar at the bottom that shows the commands
        # it is only rendered when needed as to speed this up on the pi
        system['screen'].blit( system['controlImage'], ( 0 , system['mapHeight'] * 100 - 100) )

        # draw the goal and the robot
        drawSprite("goal", system)
        drawSprite("robot", system)

      # update the robot status
      # need to be able to see state changes here to start and stop sounds
      system = updateState(system)

      # draw all the changes to the screen
      pygame.display.flip()
