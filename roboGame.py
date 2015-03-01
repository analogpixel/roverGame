import sys
import ConfigParser
import time
import pygame
import os
from spriteFunctions import *
from mapFunctions import *
from localutil import *
from robotCommands import *


def exitGame(usegpio):
  if usegpio:
    GPIO.cleanup()
  sys.exit()

def lm(message):
  pass
  #print(message)

play =False

if __name__ == '__main__':

    lm("Loading Config")
    # read configuration file
    config = ConfigParser.SafeConfigParser()
    if os.path.isfile("run.cfg"):
        config.read('run.cfg')
        C_FULLSCREEN = config.getboolean('config', 'fullscreen')
        C_WIDTH      = config.getint('config', 'width')
        C_HEIGHT     = config.getint('config', 'height')
        C_NOFRAME    = config.getboolean('config', 'windowFrameOff')
        C_GRIDON     = config.getboolean('gameDynamics', 'gridValue')
        C_HWSURF     = config.getboolean('config', 'useHWSurface')
        C_DBUFFER    = config.getboolean('config', 'useDoubleBuffer')
        C_USEGPIO    = config.getboolean('config', 'useGPIO')

        C_FPS        = config.getint('config','fps')
        C_COLORDEPTH = config.getint('config','colorDepth')
        C_TILESIZE   = 0 # define in loadMap

        C_GPIOCONFIG = []
        for xyz in config.options('GPIO'):
          C_GPIOCONFIG.append( eval( config.get('GPIO',xyz)) )

        pygame.mixer.init()
        C_SOUNDS = {}
        for xyz in config.options('sounds'):
          t = eval(config.get('sounds', xyz))
          C_SOUNDS[xyz] = {}
          C_SOUNDS[xyz]['sound'] = pygame.mixer.Sound( "resources/wav/%s" %  t['wav'] )
          C_SOUNDS[xyz]['loop']  = t['loop']
        C_INPUTACTIVE = True

    pygame.init()

    flags = 0
    if C_FULLSCREEN:
      flags = flags | pygame.FULLSCREEN
    if C_NOFRAME:
      flags = flags | pygame.NOFRAME
    if C_HWSURF:
      flags = flags | pygame.HWSURFACE
    if C_DBUFFER:
      flags = flags | pygame.DOUBLEBUF

    lm("Config Loaded")

    lm("Loading command image")
    commandImage  = pygame.image.load("./resources/commands.png")
    commandLayout = {'turnClockwise':0 ,'turnCounterClockwise': 100 ,'moveForward':200 }
    lm("Image loaded")

    clock         = pygame.time.Clock()
    screen        = pygame.display.set_mode((C_WIDTH, C_HEIGHT), flags, C_COLORDEPTH)

    lm("Loading Map")
    [mapImage, checkCrash, C_TILESIZE, mapGoal] = loadMap("./maps/map1.json", "./resources/grassTexture.jpg")
    lm("Map Loaded")

    robot = createSprite("robot",(400,400))
    goal  = createSprite("goal",mapGoal)
    tic = 0

    if C_USEGPIO:
      from buttonInterface import *
      lm("Configuring GPIO")
      configGPIO( C_GPIOCONFIG )
      lm("Configured")

    while True:
      clock.tick(C_FPS)
      tic += 1

      # there are two phases:
      # phase 1 input your commands
      # phase 2 let the commands run
      # in phase two no input is allowed
      if C_INPUTACTIVE:
        if C_USEGPIO:
          robot = pollGPIO(C_GPIOCONFIG, robot)

        lm("Polling for keyboard events")
        for event in pygame.event.get():
          if event.type  ==  pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
              robot = pushQ(robot, "turnCounterClockwise")
            if event.key == pygame.K_RIGHT:
              robot = pushQ(robot, "turnClockwise")
            if event.key == pygame.K_UP:
              robot = pushQ(robot,"moveForward")
            if event.key == pygame.K_p:
              robot = activate(robot)
            if event.key == pygame.K_c:
              robot = clearQ()
            if event.key == pygame.K_n:
              robot['state'] = "moving"

          if event.type == pygame.QUIT or \
             (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
              exitGame(C_USEGPIO)
              sys.exit()

      # game loop
      if robot['state'] == "moving" and spriteCrash(robot, goal):
        robot['state'] = 'win'

      if robot['state'] == "moving" and checkCrash( robot['x']   , robot['y'] ):
        robot['state'] = 'lose'

      if robot['state'] == "moving":
        robot = updateRobot(robot)
        robot = updateState(robot, C_SOUNDS)
        robot = moveSprite(robot, C_SOUNDS)

      screen.blit( mapImage, (0,0) )
      goal  = drawSprite(goal, tic, C_FPS, screen)
      robot = drawSprite(robot, tic, C_FPS , screen)
      robot = drawCommands(robot, commandImage, commandLayout, C_HEIGHT, C_TILESIZE, screen)
      pygame.display.flip()



      # if robot['state'] == 'win' or robot['state'] == 'lose':
      #   showMenu()

      lm("Finished")
