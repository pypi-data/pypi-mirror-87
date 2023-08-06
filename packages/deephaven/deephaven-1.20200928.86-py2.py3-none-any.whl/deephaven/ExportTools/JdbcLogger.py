
"""
A utility that logs Deephaven table snapshots and/or incremental updates to a JDBC table. It is expected that the
 target table is "compatible" with the source: JDBC metadata is interrogated to ensure the types of the source table
 columns match those of the corresponding target columns. Column names may be mapped, but any additional
 conversion must be performed in Deephaven prior to logging.
This logger may be used in two "modes". The default reproduces the content of the source table via a combination of
 SQL INSERT, UPDATE and DELETE statements (batched when possible). In "log mode", each incremental update to the
 source table is logged as an INSERT to the target table, along with (optional) information about which row was
 affected and the relevant operation (Added/Removed/Modified).
In addition, a number of different transaction modes may be used:
 
* When "RowByRow" is specified, each logged row/operation is individually committed.
* When "Atomic" is specified, each update to the source table is logged as an atomic operation - i.e. if an update affecting 100 rows is received by the table listener, these are committed as a unit.

 The following modes only apply when logging snapshots:
 
* When "Start" or "None" is specified, SQL operations are executed in the current transaction, but no commit is executed.
* When "End" is specified, the final row of the snapshot is followed by a single commit operation.

 The "Atomic" mode is recommended in most cases for optimal performance.
"""


#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

##############################################################################
# This code is auto generated. DO NOT EDIT FILE!
# Run "./gradlew :Generators:generatePythonImportTools" to generate
##############################################################################


import jpy
import wrapt


_java_type_ = None  # None until the first _defineSymbols() call
_builder_type_ = None  # None until the first _defineSymbols() call


def _defineSymbols():
    """
    Defines appropriate java symbol, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global _java_type_, _builder_type_
    if _java_type_ is None:
        # This will raise an exception if the desired object is not the classpath
        _java_type_ = jpy.get_type("com.illumon.iris.export.jdbc.JdbcLogger")
        _builder_type_ = jpy.get_type("com.illumon.iris.export.jdbc.JdbcLogger$Builder")


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
def builder(*args):
    """
    Creates a JdbcLogger JdbcLogger.Builder.
    
    *Overload 1*  
      :param logger: (com.fishlib.io.logger.Logger) - logger to use when initializing
      :param jdbcDriver: (java.lang.String) - JDBC driver class name
      :param jdbcUrl: (java.lang.String) - JDBC connection URL
      :param catalog: (java.lang.String) - JDBC database catalog
      :param schema: (java.lang.String) - JDBC database schema
      :param tableName: (java.lang.String) - JDBC database table name
      :return: (com.illumon.iris.export.jdbc.JdbcLogger.Builder) JdbcLogger builder.
      
    *Overload 2*  
      :param logger: (com.fishlib.io.logger.Logger) - logger to use when initializing
      :param jdbcDriver: (java.lang.String) - JDBC driver class name
      :param jdbcUrl: (java.lang.String) - JDBC connection URL
      :param schema: (java.lang.String) - JDBC database schema
      :param tableName: (java.lang.String) - JDBC database table name
      :return: (com.illumon.iris.export.jdbc.JdbcLogger.Builder) JdbcLogger builder.
      
    *Overload 3*  
      :param logger: (com.fishlib.io.logger.Logger) - logger to use when initializing
      :param jdbcDriver: (java.lang.String) - JDBC driver class name
      :param jdbcUrl: (java.lang.String) - JDBC connection URL
      :param tableName: (java.lang.String) - JDBC database table name
      :return: (com.illumon.iris.export.jdbc.JdbcLogger.Builder) JdbcLogger builder.
    """
    
    return JdbcLoggerBuilder(*args)


class JdbcLoggerBuilder(object):
    def __init__(self, *args, **kwargs):
        """
        Either *args or **kwargs should be provided for successful construction.
        - *args, when provided, should take the form (*args)
        - **kwargs, when provided, should take the form {'builder': *value*}, and is generally 
          meant for internal use
        """
        _defineSymbols()
        builder = kwargs.get('builder', None)
        if builder is not None:
            self._builder = builder
        else:
            self._builder = _java_type_.builder(*args)

    @property
    def builder(self):
        """The java builder object."""
        return self._builder

    def batchSize(self, batchSize):
        """
        Specify the batch size when writing to the JDBC data source. For efficiency, the JDBC logger "batches" SQL
         statements when possible. Each Deephaven table update results in at least one commit, regardless of the
         batch size, so this represents a maximum. The default batch size is 500 rows.
        
         Batching is only effective when the TableLoggerBase.Flags setting is not "RowByRow", since that
         effectively requires a commit for every row. When logging with updates, the "Atomic" setting is recommended,
         which requires only one commit for each Deephaven table update (which can affect any number of rows). When
         logging snapshots only, any setting other than "RowByRow" will take advantage of batching.
        
        :param batchSize: (int) - maximum batch size (legal range is 1 to 100,000)
        :return: (com.illumon.iris.export.jdbc.JdbcLogger.Builder) this builder
        """
        
        return JdbcLoggerBuilder(builder=self._builder.batchSize(batchSize))

    def build(self):
        """
        Creates a JdbcLogger with configuration specified by arguments to the builder.
        
        :return: (com.illumon.iris.export.jdbc.JdbcLogger) a new JdbcLogger
        """
        
        return self._builder.build()

    def calendar(self, calendar):
        """
        Specify the Calendar to use when logging to JDBC date/datetime/timestamp columns. This can affect the way
         DateTime values are logged when the target column does not directly store an offset/timezone.
         See PreparedStatement.setDate(int, Date, Calendar) and
         PreparedStatement.setTimestamp(int, Timestamp, Calendar) (int, Date, Calendar)} for details.
        
        :param calendar: (java.util.Calendar) - Calendar to use for logging
        :return: (com.illumon.iris.export.jdbc.JdbcLogger.Builder) this builder
        """
        
        return JdbcLoggerBuilder(builder=self._builder.calendar(calendar))

    def dataColumn(self, *args):
        """
        Add a data column for logging.
        
        *Overload 1*  
          :param targetColumn: (java.lang.String) - column name, with the same name in the source and target.
          :return: (com.illumon.iris.export.jdbc.JdbcLogger.Builder) this builder
          
        *Overload 2*  
          :param targetColumn: (java.lang.String) - column name in the JDBC table
          :param sourceColumn: (java.lang.String) - column name in the source Deephaven table
          :return: (com.illumon.iris.export.jdbc.JdbcLogger.Builder) this builder
        """
        
        return JdbcLoggerBuilder(builder=self._builder.dataColumn(*args))

    def jdbcPassword(self, jdbcPassword):
        """
        Specify the JDBC database password. Only necessary if not specified as part of the JDBC URL.
        
        :param jdbcPassword: (java.lang.String) - JDBC database password
        :return: (com.illumon.iris.export.jdbc.JdbcLogger.Builder) this builder
        """
        
        return JdbcLoggerBuilder(builder=self._builder.jdbcPassword(jdbcPassword))

    def jdbcUser(self, jdbcUser):
        """
        Specify the JDBC database user. Only necessary if not specified as part of the JDBC URL.
        
        :param jdbcUser: (java.lang.String) - JDBC database user name
        :return: (com.illumon.iris.export.jdbc.JdbcLogger.Builder) this builder
        """
        
        return JdbcLoggerBuilder(builder=self._builder.jdbcUser(jdbcUser))

    def keyColumns(self, *keyColumns):
        """
        Specify the set of columns that represent the primary key when logging to JDBC. This set of column(s) will be
         used in order to generate the WHERE clause in UPDATE and DELETE operations, when not in "log mode". If in log
         mode, key columns are unnecessary, since every source table update will simply be logged as an INSERT to the
         JDBC target.
        
         The key columns should be either composed of a subset of the data columns (as they are named in the SQL
         table), or the rowIndex column. Each set of unique values in these columns should represent a unique row in
         order for logging to work properly. If present, a rowIndex column always provides this feature.
        
        :param keyColumns: (java.lang.String...) - an array of columns to use as the composite primary key
        :return: (com.illumon.iris.export.jdbc.JdbcLogger.Builder) this builder
        """
        
        return JdbcLoggerBuilder(builder=self._builder.keyColumns(*keyColumns))

    def logMode(self, logMode):
        """
        Set log mode indicator. If not specified, this defaults to false.
        
         When in log mode, each update to the source Deephaven table will result in an INSERT into the target table
         (i.e. the target will be an append-only log of every update to the source).
        
         Otherwise, each operation is replicated in the target using the appropriate INSERT/UPDATE/DELETE operation,
         using the specified row key columns to uniquely identify rows.
        
        :param logMode: (boolean) - if true, run in log mode
        :return: (com.illumon.iris.export.jdbc.JdbcLogger.Builder) this builder
        """
        
        return JdbcLoggerBuilder(builder=self._builder.logMode(logMode))

    def operationColumn(self, operationColumn):
        """
        Specify the JDBC column that will receive the operation that resulted in that row. This is most useful in
         "log mode", in order to differentiate between Added/ModifiedOld/ModifiedNew/Removed operations in the source
         table. A PreparedStatement.setString(int, java.lang.String) will be used to set this value, so the target column
         should be a VARCHAR with length 11 or more.
        
        :param operationColumn: (java.lang.String) - JDBC column that will receive the operation (must be compatible with a string value)
        :return: (com.illumon.iris.export.jdbc.JdbcLogger.Builder) this builder
        """
        
        return JdbcLoggerBuilder(builder=self._builder.operationColumn(operationColumn))

    def rowIndexColumn(self, rowIndexColumn):
        """
        Specify the JDBC column that will receive the rowIndex of the source table row that resulted in a given
         JDBC row. A PreparedStatement.setLong(int, long) will be used to set this value, so the target column
         should be an SQL BIGINT or equivalent.
        
        :param rowIndexColumn: (java.lang.String) - JDBC column that will receive the operation (must be compatible with 64 bit integer)
        :return: (com.illumon.iris.export.jdbc.JdbcLogger.Builder) this builder
        """
        
        return JdbcLoggerBuilder(builder=self._builder.rowIndexColumn(rowIndexColumn))
