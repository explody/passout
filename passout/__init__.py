from __future__ import print_function

import os
import pprint
import yaml

default_dir = os.path.expanduser('~/.passout')
default_env = 'development'

if 'PO_ENV' not in os.environ:
  environment = default_env
else:
  environment = os.environ['PO_ENV']

# These exceptions are such total overkill for this tiny thing
class PassOutException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class PassOutNoEnvironmentData(PassOutException):
  def __init__(self, value):
    super(PassOutNoEnvironmentData, self).__init__('PassOutNoEnvironmentData: ' + value)

class PassOutNoServiceFile(PassOutException):
  def __init__(self, value):
    super(PassOutNoServiceFile, self).__init__('PassOutNoServiceFile: ' + value)

class PassOut(object):

  def __init__(self, svc, env=environment):
    self._svc = svc
    self._env = env
    self._loadsvc()

  def _loadsvc(self):
    filename = ".".join([self._svc,'yml'])
    filepath = os.path.join(default_dir,filename)
    try:
      pfh = open(filepath,"rb")
    except IOError:
      raise PassOutNoServiceFile('No file found: ' + filepath)

    svcdata = yaml.load(pfh.read())

    if self._env not in svcdata:
      raise PassOutNoEnvironmentData('No data found for environment: ' + self._env)

    self._svcdata = svcdata

  def get(self, key):
    if key in self._svcdata[self._env]:
      return self._svcdata[self._env][key]
    else:
      return False

  def user(self):
    return self.get('user')

  def creds(self):
    return self.get('pass')

  def getenv(self):
    return self._env

  def setenv(self, env):
    self._env = env
    self._loadsvc()

  def setsvc(self, svc):
    self._svc = svc
    self._loadsvc()

  def reset(self,svc,env):
    self._env = env
    self._svc = svc
    self._loadsvc()

  def printenv(self):
    print(self.getenv())
