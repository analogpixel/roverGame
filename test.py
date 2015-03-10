import ConfigParser
import os

# http://martin-thoma.com/configuration-files-in-python/

config = ConfigParser.SafeConfigParser()
if os.path.isfile("run.cfg"):
  config.read('run.cfg')
  for c in config.options('GPIO'):
    d = eval(config.get("GPIO", c))
    
      
