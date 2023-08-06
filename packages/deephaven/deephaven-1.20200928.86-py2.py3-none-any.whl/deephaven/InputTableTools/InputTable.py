
"""
A pseudo-table implementation that provides rudimentary CRUD-like operations on a user table.
"""


#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

##############################################################################
# This code is auto generated. DO NOT EDIT FILE!
# Run "./gradlew :Generators:generatePythonIntegrationStaticMethods" to generate
##############################################################################


import jpy
import wrapt


_java_type_ = None  # None until the first _defineSymbols() call


def _defineSymbols():
    """
    Defines appropriate java symbol, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global _java_type_
    if _java_type_ is None:
        # This will raise an exception if the desired object is not the classpath
        _java_type_ = jpy.get_type("com.illumon.iris.db.util.config.InputTable")


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
def cloneBlankInputTable(db, namespace, tableName, table):
    """
    Creates a new input table from the definition of an existing table.
    
    :param db: (com.illumon.iris.db.tables.databases.Database) - database
    :param namespace: (java.lang.String) - namespace
    :param tableName: (java.lang.String) - table name
    :param table: (com.illumon.iris.db.tables.Table) - input table to clone
    :return: (com.illumon.iris.db.tables.Table) new, cloned, empty input table
    """
    
    return _java_type_.cloneBlankInputTable(db, namespace, tableName, table)


@_passThrough
def getCurrentInputHandler(db, namespace, tableName):
    """
    Gets the current input table handler.
    
    :param db: (com.illumon.iris.db.tables.databases.Database) - database
    :param namespace: (java.lang.String) - namespace
    :param tableName: (java.lang.String) - table name
    :return: (com.illumon.iris.db.util.config.TableInputHandler) current input table handler
    """
    
    return _java_type_.getCurrentInputHandler(db, namespace, tableName)


@_passThrough
def inputTable(db, namespace, tableName):
    """
    Returns an input table.
    
    :param db: (com.illumon.iris.db.tables.databases.Database) - database
    :param namespace: (java.lang.String) - namespace
    :param tableName: (java.lang.String) - table name
    :return: (com.illumon.iris.db.tables.Table) input table
    """
    
    return _java_type_.inputTable(db, namespace, tableName)


@_passThrough
def it(db, namespace, tableName):
    """
    Returns an input table.
    
    :param db: (com.illumon.iris.db.tables.databases.Database) - database
    :param namespace: (java.lang.String) - namespace
    :param tableName: (java.lang.String) - table name
    :return: (com.illumon.iris.db.tables.Table) input table
    """
    
    return _java_type_.it(db, namespace, tableName)


@_passThrough
def newInputTable(*args):
    """
    Creates a new input table.
    
    *Overload 1*  
      :param db: com.illumon.iris.db.tables.databases.Database
      :param namespace: java.lang.String
      :param tableName: java.lang.String
      :param columns: com.illumon.iris.db.util.config.TableInputHandler.ColumnConfig...
      :return: com.illumon.iris.db.util.config.InputTable
      
    *Overload 2*  
      :param db: (com.illumon.iris.db.tables.databases.Database) - database
      :param namespace: (java.lang.String) - namespace
      :param tableName: (java.lang.String) - time table
      :param initialData: (com.illumon.iris.db.tables.Table) - initial data
      :param keys: (java.lang.String...) - keys
      :return: (com.illumon.iris.db.util.config.InputTable) input table
      
    *Overload 3*  
      :param db: (com.illumon.iris.db.tables.databases.Database) - database
      :param namespace: (java.lang.String) - namespace
      :param tableName: (java.lang.String) - time table
      :param initialData: (com.illumon.iris.db.tables.Table) - initial data
      :param removeExisting: (boolean) - remove an existing input table
      :param keys: (java.lang.String...) - keys
      :return: (com.illumon.iris.db.util.config.InputTable) input table
      
    *Overload 4*  
      :param db: (com.illumon.iris.db.tables.databases.Database) - database
      :param namespace: (java.lang.String) - namespace
      :param tableName: (java.lang.String) - time table
      :param tableSchema: (com.illumon.iris.db.tables.TableDefinition) - table schema
      :param keys: (java.lang.String...) - keys
      :return: (com.illumon.iris.db.util.config.InputTable) input table
    """
    
    return _java_type_.newInputTable(*args)
