#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

import jpy
import wrapt


_java_type_ = None  # None until the first _defineSymbols() call
_logger_type_ = None
_log_level_type_ = None


def _defineSymbols():
    """
    Defines appropriate java symbol, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global _java_type_, _logger_type_, _log_level_type_
    if _java_type_ is None:
        # This will raise an exception if the desired object is not the classpath
        _java_type_ = jpy.get_type("com.illumon.iris.controller.PersistentQueryControllerClient")
        _logger_type_ = jpy.get_type("com.fishlib.io.logger.NullLoggerImpl")
        _log_level_type_ = jpy.get_type("com.fishlib.io.log.LogLevel")


# every module method should be decorated with @_passThrough
@wrapt.decorator
def _passThrough(wrapped, instance, args, kwargs):
    """
    For decoration of module methods, to define necessary symbols at runtime

    :param wrapped: the method to be decorated
    :param instance: the object to which the wrapped function was bound when it was called
    :param args: the argument list for `wrapped`
    :param kwargs: the keyword argument dictionary for `wrapped`
    :return: the decorated version of the method
    """

    _defineSymbols()
    return wrapped(*args, **kwargs)


# Define all of our functionality, if currently possible
try:
    _defineSymbols()
except Exception as e:
    pass


class PersistentQueryControllerClient(object):
    """A client for the persistent query controller"""

    def __init__(self, log=None, logLevel='INFO'):
        """
        Creates a connection to the controller client.

        Note:

        * `log` takes precedence over `logLevel`. Default will be `logLevel=INFO` if not provided.

        :param log: None or the desired Java logger object
        :param logLevel: if `log` is None, the desired log level for the java logger constructed for this
        :return: persistent query controller client
        """
        _defineSymbols()
        if log is None:
            if not hasattr(_log_level_type_, logLevel):
                raise ValueError("{} has no level attribute {}".format(_log_level_type_, logLevel))
            # construct the default logger
            log = _logger_type_(getattr(_log_level_type_, logLevel))
        # save the java object which gets returned
        self._PersistentQueryControllerClient = _java_type_.getControllerClient(log)

    @classmethod
    def getControllerClient(cls, log=None, logLevel='INFO'):
        """
        Creates a connection to the controller client.

        Note:

        * `log` takes precedence over `logLevel`. Default will be `logLevel=INFO` if not provided.

        :param log: None or the desired Java logger object
        :param logLevel: if `log` is None, the desired log level for the java logger constructed for this
        :return: persistent query controller client
        """
        return cls(log=log, logLevel=logLevel)

    def getPersistentQueryConfiguration(self, log=None, logLevel='INFO', configSerial=None, owner=None, name=None):
        """
        Gets the configuration for a persistent query.

        Note:

        * `log` takes precedence over `logLevel`. Default will be `logLevel=INFO` if not provided.

        * `configSerial` takes precedence over `owner` & `name`, but one valid choice must be provided.

        :param log: None or the desired Java logger object
        :param logLevel: if `log` is None, the desired log level for the java logger constructed for this
        :param configSerial: the serial number of the persistent query
        :param owner: the owner of the persistent query
        :param name: the name of the persistent query
        :return: the PersistentQueryConfiguration
        """

        if log is None:
            if not hasattr(_log_level_type_, logLevel):
                raise ValueError("{} has no level attribute {}".format(_log_level_type_, logLevel))
            # construct the default logger
            log = _logger_type_(getattr(_log_level_type_, logLevel))

        if configSerial is not None:
            try:
                serial = int(configSerial)
            except Exception:
                raise ValueError("The value for configSerial should be an integer. Received {}".format(configSerial))
            return self._PersistentQueryControllerClient.getPersistentQueryConfiguration(log, serial)
        elif owner is not None and name is not None:
            return self._PersistentQueryControllerClient.getPersistentQueryConfiguration(log, owner, name)
        else:
            raise ValueError("A valid identifier (configSerial), or the owner and name for the "
                             "persistent query client must be supplied")

    def publishTemporaryQueries(self, *args, **kwargs):
        """
        Publishes one or many configurations as temporary persistent queries

        Note:

        * `log` takes precedence over `logLevel`. Default will be `logLevel=INFO` if not provided.

        :param args: the configurations collection
        :param kwargs: can only contain keyword arguments 'log' or 'logLevel'.
            *log* - if present, is the the desired Java logger object.
            *logLevel* - is the desired log level for the constructed java logger.  if `log` is None or not present, [default is 'INFO'].
        """

        if len(args) == 0:
            raise ValueError("You must enter at least one configuration to publish")

        log = kwargs.get('log', None)
        logLevel = kwargs.get('logLevel', 'INFO')
        allowed = ('log', 'LogLevel')

        for key in kwargs.keys():
            if key not in allowed:
                raise ValueError("Unexpected keyword argument {}, must be one of {}".format(key, allowed))

        if log is None:
            if not hasattr(_log_level_type_, logLevel):
                raise ValueError("{} has no level attribute {}".format(_log_level_type_, logLevel))
        # construct the default logger
        log = _logger_type_(getattr(_log_level_type_, logLevel))

        self._PersistentQueryControllerClient.publishTemporaryQueries(log, *args)

    def __getattr__(self, item):
        # return the java object attribute, if it exists
        if hasattr(self._PersistentQueryControllerClient, item):
            return getattr(self._PersistentQueryControllerClient, item)
        raise AttributeError('Attribute {} does not exist for {}'.format(item, type(self._PersistentQueryControllerClient)))
