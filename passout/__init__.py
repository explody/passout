from __future__ import print_function

import os
import yaml

default_path = os.path.expanduser('~/.passout')
default_env = 'development'


class PassOutException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class PassOutNoEnvironmentData(PassOutException):
    def __init__(self, value):
        super().__init__(f"PassOutNoEnvironmentData: {value}")


class PassOutNoServiceFile(PassOutException):
    def __init__(self, value):
        super().__init__(f"PassOutNoServiceFile: {value}")


class PassOutNoService(PassOutException):
    def __init__(self):
        super().__init__(f"PassOutNoService: service not passed to PassOut() and PASSOUT_SVC "
                         f"environment variable not set")


class PassOut(object):
    '''
    The primary passsout class, a minimal class that reads a YAML file and exposes its data
    through a few simple methods.  Arguments may be passed to __init__() or set in the shell
    environment.

    :param svc: The name of the yaml file, minus the extension, e.g. <environment>.yml
    :param env: The name of the service, a top-level key in the svc yaml file
    :param path: The directory path which contains yaml files.

    '''

    def __init__(self, svc=None, env=None, path=None):

        if path is None and 'PASSOUT_PATH' not in os.environ:
            path = default_path
        elif path is None:
            path = os.environ['PASSOUT_PATH']

        if env is None and 'PASSOUT_ENV' not in os.environ:
            env = default_env
        elif env is None:
            env = os.environ['PASSOUT_ENV']

        # There is no default service, raise an exception if we don't have one
        if svc is None and 'PASSOUT_SVC' not in os.environ:
            raise PassOutNoService
        elif svc is None:
            svc = os.environ['PASSOUT_SVC']

        self._svc = svc
        self._env = env
        self._path = path
        self._loadsvc()

    def __getattr__(self, attr):
        if attr in self._svcdata[self._env]:
            return self._svcdata[self._env][attr]
        else:
            raise AttributeError

    def _hasattr(self, attr):
        return attr in self._svcdata[self._env]

    def _loadsvc(self):
        filename = ".".join([self._svc, 'yml'])
        filepath = os.path.join(self._path, filename)
        try:
            pfh = open(filepath, "rb")
        except (IOError, FileNotFoundError):
            raise PassOutNoServiceFile('No file found: ' + filepath)

        svcdata = yaml.load(pfh.read(), Loader=yaml.FullLoader)

        if self._env not in svcdata:
            raise PassOutNoEnvironmentData('No data found for environment: ' + self._env)

        self._svcdata = svcdata

    def get(self, key):
        try:
            return self.__getattr__(key)
        except AttributeError:
            return False

    @property
    def username(self):
        """
        Returns (in order, first found) the value of the 'username' or 'user' key from the
        yaml data.  The latter is only for backwards compatibility.
        :returns: The value of 'username' or 'user' from the loaded yaml
        :rtype: String
        """
        return self.get('username' if self._hasattr('username') else 'user')

    def user(self):
        """
        Compatibility, see username()
        """
        return self.username

    @property
    def password(self):
        """
        Returns (in order, first found) the value of the 'password' or 'pass' key from the
        yaml data.  The latter is only for backwards compatibility.
        :returns: The value of 'password' or 'pass' from the loaded yaml
        :rtype: String
        """
        return self.get('password' if self._hasattr('password') else 'pass')

    def creds(self):
        """
        Compatibility, see password()
        """
        return self.password

    @property
    def env(self):
        """
        Returns the name of the current environment
        :return: Environment name
        :rtype: String
        """
        return self._env

    @env.setter
    def env(self, env):
        """
        Sets the current environment, and loads the relevant chunk of yaml
        :param env: The name of the environment, a top-level key in the svc yaml file
        """
        self._env = env
        self._loadsvc()

    @property
    def svc(self):
        """
        Returns the name of the current service
        :return: Service name
        :rtype: String
        """
        return self._svc

    @svc.setter
    def svc(self, svc):
        """
        Sets the current service, and loads the relevant yaml file. This loads the service
        environment from the new service, as currently set.
        :param svc: The name of the service, corresponding to the yaml filename
        """
        self._svc = svc
        self._loadsvc()

    def dumpsvc(self):
        """
        Returns the entire dictionary of parsed yaml for a service
        :return: Dictionary of service data
        :rtype: Dict
        """
        return self._svcdata[self._env]
