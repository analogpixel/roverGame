"""
Commands to control the robot
"""
import math

def calcWin(system):
  if system['sprite_robot']['state'] == "moving" and \
     system['sprite_robot']['x'] == system['sprite_goal']['x'] and \
     system['sprite_robot']['y'] == system['sprite_goal']['y']:
    system['sprite_robot']['state'] = 'win'
  return system

def calcCrash(system):
  if system['sprite_robot']['state'] == "moving" and \
     system['crashFunction']( system['sprite_robot']['x'], \
                              system['sprite_robot']['y']):
    system['sprite_robot']['state'] = 'lose'
  return system

def turnCounterClockwise(system):
  """
  subtract 90deg from r; return object
  """
  system['sprite_robot']['rdest'] = system['sprite_robot']['r'] - 90
  return system

def turnClockwise(system):
  """
  add 90deg to the r; return object
  """
  system['sprite_robot']['rdest'] = system['sprite_robot']['r'] + 90
  return system

def moveForward(system):
  """
  calculate what forward is based on r, and then return
  the object with the x,y updated based on that
  """
  xinc =  int(math.cos((system['sprite_robot']['r'] - 90) * (math.pi/180)))
  yinc = int(math.sin((system['sprite_robot']['r'] - 90) * (math.pi/180)))
  system['sprite_robot']['xdest'] += 100 * xinc
  system['sprite_robot']['ydest'] += 100 * yinc
  return system

def pushQ(command, system):
  """
  Add a command which is also a callable function to the q
  return the data
  """
  if "commandq" in system:
    system['commandq'].append(command)
  else:
    system['commandq'] = [command]

  return system

def getNextCommand(system):
  """
  pop off a command which is also a function name
  run that function with the data and return the result
  """
  if "commandq" in system and len(system["commandq"]) > 0:
    system["currentCommand"] = system["commandq"].pop(0)
    system = globals()[system['currentCommand']](system)

  return system

def updateRobot(system):
  """
  if the robot is done moving and has more commands then pop off the next command
  """
  if not "currentCommand" in system:
    return getNextCommand(system)

  # if we aren't moving and there is no data in the q then the game is over
  # otherwise get and exectute the next command
  if system['sprite_robot']['xdest'] == system['sprite_robot']['x'] and \
     system['sprite_robot']['ydest'] == system['sprite_robot']['y'] and \
     system['sprite_robot']['rdest'] == system['sprite_robot']['r']:
    if  len(system['commandq']) == 0:
      system['sprite_robot']['state'] = 'lose'
      system['lose_message'] = "Robot lost"
    else:
      system = getNextCommand(system)

  return system
