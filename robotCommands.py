"""
Commands to control the robot
"""
import math

def activate(data):
  #data['active'] = True
  data['state'] = "moving"
  return data

def deactivate(data):
  #data['active'] = False
  data['state'] = "stopped"
  return data

def turnCounterClockwise(data):
  """
  subtract 90deg from r; return object
  """
  data['rdest'] = data['r'] - 90
  return data

def turnClockwise(data):
  """
  add 90deg to the r; return object
  """
  data['rdest'] = data['r'] + 90
  return data

def moveForward(data):
  """
  calculate what forward is based on r, and then return
  the object with the x,y updated based on that
  """
  xinc =  int(math.cos((data['r'] - 90) * (math.pi/180)))
  yinc = int(math.sin((data['r'] - 90) * (math.pi/180)))
  data['xdest'] += 100 * xinc
  data['ydest'] += 100 * yinc
  return data

def pushQ(data, command):
  """
  Add a command which is also a callable function to the q
  return the data
  """
  if "commandq" in data:
    data['commandq'].append(command)
  else:
    data['commandq'] = [command]

  return data

def getNextCommand(data):
  """
  pop off a command which is also a function name
  run that function with the data and return the result
  """
  if "commandq" in data and len(data["commandq"]) > 0:
    data["currentCommand"] = data["commandq"].pop(0)
    data = globals()[data['currentCommand']](data)

  return data

def updateRobot(data):
  """
  if the robot is done moving and has more commands then pop off the next command
  """
  if not "currentCommand" in data:
    return getNextCommand(data)

  # if we aren't moving and there is no data in the q then the game is over
  # otherwise get and exectute the next command
  if data['xdest'] == data['x'] and data['ydest'] == data['y'] and data['rdest'] == data['r']:
    if  len(data['commandq']) == 0:
      data['state'] = 'lose'
    else:
      data = getNextCommand(data)

  return data
