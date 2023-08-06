
"""
Tools for reading data from a JDBC source into an in-memory Deephaven table.
"""


#
# Copyright (c) 2016-2020 Deephaven Data Labs and Patent Pending
#

##############################################################################
# This code is auto generated. DO NOT EDIT FILE!
# Run "./gradlew :Generators:generatePythonImportTools" to generate
##############################################################################
"""
This module defines utilities for reading a JDBC query result directly into an in-memory table. The metadata provided
by the JDBC ResultSet is used to generate Deephaven columns of the most appropriate type. The functionality of this
module depends on the jvm having been properly initialized before usage.

Additionally, it provides wrappers for the java enum CaseFormat and java class TimeZone to allow proper construction
of a ReadJdbcOptions object.

>>> newTable1 = JdbcHelpers.readJdbc('com.microsoft.sqlserver.jdbc.SQLServerDriver',
                                     'jdbc:sqlserver://dbserverhost;database=dbname',
                                     'myuser',
                                     'mypassword',
                                     'SELECT * FROM table1')

>>> options = JdbcHelpers.readJdbcOptions()\\
                  .sourceTimeZone('America/New_York')\\
                  .columnNameFormat('LOWER_UNDERSCORE', 'UPPER_CAMEL')
>>> newTable1 = JdbcHelpers.readJdbc('com.microsoft.sqlserver.jdbc.SQLServerDriver',
                                     'jdbc:sqlserver://dbserverhost;database=dbname',
                                     'myuser',
                                     'mypassword',
                                     'SELECT * FROM table1',
                                     options.readJdbcOptions)
"""

import jpy
import wrapt
from ..conversion_utils import _isStr, getJavaClassObject


_java_type_ = None  # None until the first _defineSymbols() call
_readJdbcOptions_type_ = None  # None until the first _defineSymbols() call
CasingStyle = None  #: Enum of string formatting styles for use when standardizing externally supplied column names (com.illumon.iris.utils.CasingStyle)
TimeZone = None     #: Java timezone class (java.util.TimeZone).


def _defineSymbols():
    """
    Defines appropriate java symbol, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global _java_type_, _readJdbcOptions_type_, CasingStyle, TimeZone
    if _java_type_ is None:
        # This will raise an exception if the desired object is not the classpath
        _java_type_ = jpy.get_type("com.illumon.iris.db.tables.utils.JdbcHelpers")
        _readJdbcOptions_type_ = jpy.get_type("com.illumon.iris.db.tables.utils.JdbcHelpers$ReadJdbcOptions")
        CasingStyle = jpy.get_type('com.illumon.iris.console.utils.CasingStyle')
        TimeZone = jpy.get_type('java.util.TimeZone')


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


def _custom_columnNameFormat(self, casingStyle, replacement):
    if _isStr(casingStyle):
        casingStyle = getattr(CasingStyle, casingStyle)
    return JdbcHelpersOptionsBuilder(readJdbcOptions=self._readJdbcOptions.columnNameFormat(casingStyle, replacement))


def _custom_columnTargetType(self, columnName, targetType):
    if _isStr(targetType):
        targetType = getJavaClassObject(targetType)
    return JdbcHelpersOptionsBuilder(readJdbcOptions=self.readJdbcOptions.columnTargetType(columnName, targetType))


def _custom_sourceTimeZone(self, sourceTimeZone):
    if _isStr(sourceTimeZone):
        sourceTimeZone = TimeZone.getTimeZone(sourceTimeZone)
    return JdbcHelpersOptionsBuilder(readJdbcOptions=self.readJdbcOptions.sourceTimeZone(sourceTimeZone))


# Define all of our functionality, if currently possible
try:
    _defineSymbols()
except Exception as e:
    pass


@_passThrough
def readJdbc(*args):
    """
    Return a JDBC query result as an in-memory Deephaven table.
     Standard JDBC-to-Deephaven type mapping applies.
    
    *Overload 1*  
      :param jdbcDriver: (java.lang.String) - JDBC driver to use
      :param jdbcUrl: (java.lang.String) - JDBC URL/connection string
      :param user: (java.lang.String) - JDBC user
      :param password: (java.lang.String) - JDBC password
      :param query: (java.lang.String) - an SQL query
      :return: (com.illumon.iris.db.tables.Table) in memory table with results of the given query
      
    *Overload 2*  
      :param jdbcDriver: (java.lang.String) - JDBC driver to use
      :param jdbcUrl: (java.lang.String) - JDBC URL/connection string
      :param user: (java.lang.String) - JDBC user
      :param password: (java.lang.String) - JDBC password
      :param query: (java.lang.String) - an SQL query
      :param options: (com.illumon.iris.db.tables.utils.JdbcHelpers.ReadJdbcOptions) - options to apply to the read/mapping operation
      :return: (com.illumon.iris.db.tables.Table) in memory table with results of the given query
      
    *Overload 3*  
      :param jdbcDriver: (java.lang.String) - JDBC driver to use
      :param jdbcUrl: (java.lang.String) - JDBC URL/connection string
      :param query: (java.lang.String) - an SQL query
      :return: (com.illumon.iris.db.tables.Table) in memory table with results of the given query
      
    *Overload 4*  
      :param jdbcDriver: (java.lang.String) - JDBC driver to use
      :param jdbcUrl: (java.lang.String) - JDBC URL/connection string
      :param query: (java.lang.String) - an SQL query
      :param options: (com.illumon.iris.db.tables.utils.JdbcHelpers.ReadJdbcOptions) - options to apply to the read/mapping operation
      :return: (com.illumon.iris.db.tables.Table) in memory table with results of the given query
      
    *Overload 5*  
      :param jdbcDriver: (java.lang.String) - JDBC driver to use
      :param jdbcUrl: (java.lang.String) - JDBC URL/connection string
      :param user: (java.lang.String) - JDBC user
      :param password: (java.lang.String) - JDBC password
      :param catalog: (java.lang.String) - the desired JDBC system catalog (specify null for default)
      :param schema: (java.lang.String) - the desired JDBC schema (specify null for default)
      :param query: (java.lang.String) - an SQL query
      :param options: (com.illumon.iris.db.tables.utils.JdbcHelpers.ReadJdbcOptions) - options to apply to the read/mapping operation
      :return: (com.illumon.iris.db.tables.Table) in memory table with results of the given query
      
    *Overload 6*  
      :param resultSet: (java.sql.ResultSet) - an open JDBC ResultSet
      :return: (com.illumon.iris.db.tables.Table) in memory table with results of the given ResultSet
      
    *Overload 7*  
      :param resultSet: (java.sql.ResultSet) - an open JDBC ResultSet
      :param progress: (com.illumon.util.progress.StatusCallback) - status callback
      :return: (com.illumon.iris.db.tables.Table) in memory table with results of the given ResultSet
      
    *Overload 8*  
      :param resultSet: (java.sql.ResultSet) - an open JDBC ResultSet
      :param options: (com.illumon.iris.db.tables.utils.JdbcHelpers.ReadJdbcOptions) - options to apply to the read/mapping operation
      :param progress: (com.illumon.util.progress.StatusCallback) - status callback
      :return: (com.illumon.iris.db.tables.Table) in memory table with results of the given ResultSet
    """
    
    return _java_type_.readJdbc(*args)


@_passThrough
def readJdbcOptions():
    """
    Returns a new options object that the user can use to customize a readJdbc operation.
    
    :return: (com.illumon.iris.db.tables.utils.JdbcHelpers.ReadJdbcOptions) a new ReadJdbcOptions object
    """
    
    return JdbcHelpersOptionsBuilder()


class JdbcHelpersOptionsBuilder(object):
    def __init__(self, *args, **kwargs):
        """
        Either *args or **kwargs should be provided for successful construction.
        - *args, when provided, should take the form ()
        - **kwargs, when provided, should take the form {'readJdbcOptions': *value*}, and is generally 
          meant for internal use
        """
        _defineSymbols()
        readJdbcOptions = kwargs.get('readJdbcOptions', None)
        if readJdbcOptions is not None:
            self._readJdbcOptions = readJdbcOptions
        else:
            self._readJdbcOptions = _java_type_.readJdbcOptions(*args)

    @property
    def readJdbcOptions(self):
        """The java readJdbcOptions object."""
        return self._readJdbcOptions

    def arrayDelimiter(self, arrayDelimiter):
        """
        Specify the delimiter to expect when mapping JDBC String columns to Deephaven arrays. Defaults to ",".
        
        :param arrayDelimiter: (java.lang.String) - the delimiter
        :return: (com.illumon.iris.db.tables.utils.JdbcHelpers.ReadJdbcOptions) customized options object
        """
        
        return JdbcHelpersOptionsBuilder(readJdbcOptions=self._readJdbcOptions.arrayDelimiter(arrayDelimiter))

    def columnNameFormat(self, casingStyle, replacement):
        """
        An option that will convert source JDBC column names to an alternate style using the CasingStyle class.
         The default is to pass through column names as-is with a minimum of normalization. The
         source columns must consistently match the expected source format for the to function appropriately.
         See CasingStyle for more details.
        
        :param casingStyle: (com.illumon.iris.console.utils.CasingStyle) - if not null, CasingStyle to apply to column names - None or null = no change to casing
        :param replacement: (java.lang.String) - character, or empty String, to use for replacments of space or hyphen in source column names
        :return: (com.illumon.iris.db.tables.utils.JdbcHelpers.ReadJdbcOptions) customized options object
        """
        
        return _custom_columnNameFormat(self, casingStyle, replacement)

    def columnTargetType(self, columnName, targetType):
        """
        Specify the target type for the given column. For columns with multiple possible type mappings, this permits
         the user to specify which Deephaven type should be used. Any columns for which a type is not specified will
         receive the default type mapping.
        
        :param columnName: (java.lang.String) - the column name
        :param targetType: (java.lang.Class<?>) - the desired Deephaven column type
        :return: (com.illumon.iris.db.tables.utils.JdbcHelpers.ReadJdbcOptions) customized options object
        """
        
        return _custom_columnTargetType(self, columnName, targetType)

    def maxErrorCount(self, maxErrorCount):
        """
        Specify the maximum number of errors to tolerate in an import. Default is zero.
        
        :param maxErrorCount: (int) - maximum error count
        :return: (com.illumon.iris.db.tables.utils.JdbcHelpers.ReadJdbcOptions) customized options object
        """
        
        return JdbcHelpersOptionsBuilder(readJdbcOptions=self._readJdbcOptions.maxErrorCount(maxErrorCount))

    def maxRows(self, maxRows):
        """
        Maximum number of rows to read, defaults to no limit. A number less than zero means no limit. This is useful
         to read just a sample of a given query into memory, although depending on the JDBC driver used, it may be
         more efficient to apply a "LIMIT" operation in the query itself.
        
        :param maxRows: (long) - maximum number of rows to read
        :return: (com.illumon.iris.db.tables.utils.JdbcHelpers.ReadJdbcOptions) customized options object
        """
        
        return JdbcHelpersOptionsBuilder(readJdbcOptions=self._readJdbcOptions.maxRows(maxRows))

    def sourceTimeZone(self, sourceTimeZone):
        """
        Specify the timezone to use when interpreting date-time/timestamp JDBC values. Defaults to the server
         time-zone, if discoverable. Otherwise, defaults to the local time zone.
        
        :param sourceTimeZone: (java.util.TimeZone) - the source time zone
        :return: (com.illumon.iris.db.tables.utils.JdbcHelpers.ReadJdbcOptions) customized options object
        """
        
        return _custom_sourceTimeZone(self, sourceTimeZone)

    def strict(self, strict):
        """
        Whether to apply strict mode when mapping from JDBC to Deephaven; for example throwing an exception if
         an out-of-range value is encountered instead of truncating. Defaults to true.
        
        :param strict: (boolean) - use strict mode
        :return: (com.illumon.iris.db.tables.utils.JdbcHelpers.ReadJdbcOptions) customized options object
        """
        
        return JdbcHelpersOptionsBuilder(readJdbcOptions=self._readJdbcOptions.strict(strict))
