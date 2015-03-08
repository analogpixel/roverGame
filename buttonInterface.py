"""
Interface to the buttons on the pi
"""
import RPi.GPIO as GPIO
from robotCommands import *

def configGPIO(system,config):
  GPIO.cleanup()
  GPIO.setmode(GPIO.BCM)

  for opt in config['C_GPIOCONFIG']:
    GPIO.setup( int(opt['in']) , GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect( int(opt['in']) , GPIO.FALLING,bouncetime=400)

def pollGPIO(system, config):
  for opt in config['C_GPIOCONFIG']:
    if GPIO.event_detected(int(opt['in'])):
      if opt['command'] == "activate":
        system['sprite_robot']['state'] = "moving"
      else:
        system = pushQ(opt['command'], system, config)
  return system
