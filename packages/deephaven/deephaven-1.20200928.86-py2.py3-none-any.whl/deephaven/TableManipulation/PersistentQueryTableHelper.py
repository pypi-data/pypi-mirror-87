#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

"""Functionality for interacting with persistent queries."""

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
        _java_type_ = jpy.get_type("com.illumon.iris.controller.utils.PersistentQueryTableHelper")
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


@_passThrough
def getClientForPersistentQuery(timeoutMillis, log=None, logLevel='INFO', configSerial=None, owner=None, name=None):
    """
    Gets the client for persistent query.

    Note:

    * `log` takes precedence over `logLevel`. Default will be `logLevel=INFO` if not provided.

    * `configSerial` takes precedence over `owner` & `name`, but one valid choice must be provided.

    :param timeoutMillis: [positive value required] timeout for helper.
    :param log: None or the desired Java logger object
    :param logLevel: if `log` is None, the desired log level for the java logger constructed for this
    :param configSerial: the serial number of the persistent query client
    :param owner: the owner of the persistent query client
    :param name: the name of the persistent query client
    :return: the HelperPersistentQueryClient
    """

    try:
        timeout = int(timeoutMillis)
    except Exception:
        raise ValueError("A positive, integer value for timeoutMillis is required. Received {}".format(timeoutMillis))

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
        return _java_type_.getClientForPersistentQuery(log, serial, timeout)
    elif owner is not None and name is not None:
        return _java_type_.getClientForPersistentQuery(log, owner, name, timeout)
    else:
        raise ValueError("A valid identifier (configSerial), or the owner and name for the "
                         "persistent query client must be supplied")


@_passThrough
def getPreemptiveTableFromPersistentQuery(tableName, log=None, logLevel='INFO', helper=None, configSerial=None, owner=None, name=None):
    """
    Gets the Table object associated with a Persistent Query.

    Note:

    * If `helper` is provided, then log options are ignored.

    * `log` takes precedence over `logLevel`. Default will be `logLevel=INFO` if not provided.

    * The precedence for persistent query client information: 1.) `helper`, 2.) `configSerial`, 3.) `owner` & `name`,
      one of which must be provided.

    :param tableName: the table name from the persistent query
    :param log: None or the desired Java logger object
    :param logLevel: if `log` is None, the desired log level for the java logger constructed for this
    :param helper: the HelperPersistentQueryClient
    :param configSerial: the serial number of the persistent query client
    :param owner: the owner of the persistent query client
    :param name: the name of the persistent query client
    :return: the Table associated with the persistent query
    """

    if log is None:
        if not hasattr(_log_level_type_, logLevel):
            raise ValueError("{} has no level attribute {}".format(_log_level_type_, logLevel))
        # construct the default logger
        log = _logger_type_(getattr(_log_level_type_, logLevel))

    if helper is not None:
        return _java_type_.getPreemptiveTableFromPersistentQuery(helper, tableName)
    elif configSerial is not None:
        try:
            serial = int(configSerial)
        except Exception:
            raise ValueError("The value for configSerial should be an integer. Received {}".format(configSerial))
        return _java_type_.getPreemptiveTableFromPersistentQuery(log, serial, tableName)
    elif owner is not None and name is not None:
        return _java_type_.getPreemptiveTableFromPersistentQuery(log, owner, name, tableName)
    else:
        raise ValueError("A persistent query client helper (helper), or a valid identifier (configSerial) "
                         "or the owner and name for the persistent query client must be supplied")
