"""
Interface to the buttons on the pi
"""
import RPi.GPIO as GPIO
from robotCommands import *

def configGPIO(config):
  GPIO.cleanup()
  GPIO.setmode(GPIO.BCM)

  for opt in config:
    GPIO.setup( int(opt['in']) , GPIO.IN, pull_up_down=GPIO.PUD_UP,bouncetime=400)
    GPIO.add_event_detect( int(opt['in']) , GPIO.FALLING)

def pollGPIO(config, robot):
  for opt in config:
    if GPIO.event_detected(int(opt['in'])):
      if opt['command'] == "activate":
        robot = activate(robot)
      else:
        robot = pushQ(robot, opt['command'])
  return robot
    
