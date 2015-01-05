"""
Interface to the buttons on the pi
"""
import RPi.GPIO as GPIO
      
def configGPIO(config):
  GPIO.cleanup()
  GPIO.setmode(GPIO.BCM)

  for opt in config:
    GPIO.setup( config['in'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(config['in'], GPIO.FALLING)


def pollGPIO(config, robot):
  for opt in config:
    if GPIO.event_detected(opt['in']):
      pushQ(opt['command'])
    
    
