
"""
Tools for managing and manipulating tables on disk.

 Most users will need TableTools and not TableManagementTools.
"""


#
# Copyright (c) 2016-2020 Deephaven Data Labs and Patent Pending
#

##############################################################################
#               This code is auto generated. DO NOT EDIT FILE!
# Run generatePythonIntegrationStaticMethods or
# "./gradlew :Generators:generatePythonIntegrationStaticMethods" to generate
##############################################################################


import sys
import jpy
import wrapt
from ..conversion_utils import _isJavaType, _isStr

_java_type_ = None  # None until the first _defineSymbols() call
_java_file_type_ = None
_iris_config_ = None
_storage_format_ = None
_compression_codec_ = None


def _defineSymbols():
    """
    Defines appropriate java symbol, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global _java_type_, _java_file_type_, _iris_config_, _storage_format_, _compression_codec_
    if _java_type_ is None:
        # This will raise an exception if the desired object is not the classpath
        _java_type_ = jpy.get_type("com.illumon.iris.db.tables.utils.TableManagementTools")
        _java_file_type_ = jpy.get_type("java.io.File")
        _iris_config_ = jpy.get_type("com.fishlib.configuration.Configuration")
        _storage_format_ = jpy.get_type("com.illumon.iris.db.tables.databases.Database$StorageFormat")
        _compression_codec_ = jpy.get_type("org.apache.parquet.hadoop.metadata.CompressionCodecName")


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


@_passThrough
def getFileObject(input):
    """
    Helper function for easily creating a java file object from a path string
    :param input: path string, or list of path strings
    :return: java File object, or java array of File objects
    """

    if _isJavaType(input):
        return input
    elif _isStr(input):
        return _java_file_type_(input)
    elif isinstance(input, list):
        # NB: map() returns an iterator in python 3, so list comprehension is appropriate here
        return jpy.array("java.io.File", [_java_file_type_(el) for el in input])
    else:
        raise ValueError("Method accepts only a java type, string, or list of strings as input. "
                         "Got {}".format(type(input)))


@_passThrough
def getWorkspaceRoot():
    """
    Helper function for extracting the root directory for the workspace configuration
    """

    return _iris_config_.getInstance().getWorkspacePath()


def _custom_addColumns(*args):
    return _java_type_.addColumns(args[0], getFileObject(args[1]), *args[2:])


def _custom_addGroupingMetadata(*args):
    if len(args) == 1:
        return _java_type_.addGroupingMetadata(getFileObject(args[0]))
    else:
        return _java_type_.addGroupingMetadata(getFileObject(args[0]), *args[1:])


def _custom_deleteTable(path):
    return _java_type_.deleteTable(getFileObject(path))


def _custom_dropColumns(*args):
    return _java_type_.dropColumns(args[0], getFileObject(args[1]), *args[2:])


def _custom_getAllDbDirs(tableName, rootDir, levelsDepth):
    return [el.getAbsolutePath() for el in _java_type_.getAllDbDirs(tableName, getFileObject(rootDir), levelsDepth).toArray()]


def _custom_readTable(*args):
    if len(args) == 1:
        return _java_type_.readTable(getFileObject(args[0]))
    else:
        return _java_type_.readTable(getFileObject(args[0]), *args[1:])


def _custom_renameColumns(*args):
    return _java_type_.renameColumns(args[0], getFileObject(args[1]), *args[2:])


def _custom_updateColumns(currentDefinition, rootDir, levels, *updates):
    return _java_type_.updateColumns(currentDefinition, getFileObject(rootDir), levels, *updates)


def _custom_writeDeephavenTables(sources, tableDefinition, destinations):
    return _java_type_.writeDeephavenTables(sources, tableDefinition, getFileObject(destinations))


def _custom_writeParquetTables(sources, tableDefinition, codecName, destinations, groupingColumns):
    if _isStr(codecName):
        return _java_type_.writeParquetTables(sources, tableDefinition, getattr(_compression_codec_, codecName),
                                              getFileObject(destinations), groupingColumns)
    else:
        return _java_type_.writeParquetTables(sources, tableDefinition, codecName,
                                              getFileObject(destinations), groupingColumns)


def _custom_writeTable(*args):
    if len(args) == 2:
        return _java_type_.writeTable(args[0], getFileObject(args[1]))
    elif len(args) == 3:
        if _isStr(args[2]):
            return _java_type_.writeTable(args[0], getFileObject(args[1]), getattr(_storage_format_, args[2]))
        else:
            return _java_type_.writeTable(args[0], getFileObject(args[1]), args[2])


def _custom_writeTables(sources, tableDefinition, destinations):
    return _java_type_.writeTables(sources, tableDefinition, getFileObject(destinations))


# Define all of our functionality, if currently possible
try:
    _defineSymbols()
except Exception as e:
    pass

@_passThrough
def addColumns(*args):
    """
    Adds new columns to a table definition and persists the result in path.  If there is an exception, the current definition
     is persisted.
    
    *Overload 1*  
      :param currentDefinition: (com.illumon.iris.db.tables.TableDefinition) - initial table definition.
      :param rootDir: (java.io.File) - root directory where tables are found.
      :param levels: (int) - levels below rootDir where table directories are found.
      :param columnsToAdd: (java.lang.String...) - columns to add.
      :return: (com.illumon.iris.db.tables.TableDefinition) new table definition.
      
    *Overload 2*  
      :param currentDefinition: (com.illumon.iris.db.tables.TableDefinition) - initial table definition.  If null, the definition from the table loaded from path is used.
      :param path: (java.io.File) - path of the table containing the columns to add.
      :param columnsToAdd: (java.lang.String...) - columns to add.
      :return: (com.illumon.iris.db.tables.TableDefinition) new table definition if successful; otherwise null.
    """
    
    return _custom_addColumns(*args)


@_passThrough
def addGroupingMetadata(*args):
    """
    Add grouping metadata to a table on disk.
    
    *Overload 1*  
      :param tableDirectory: (java.io.File) - table directory
      
    *Overload 2*  
      :param tableDirectory: (java.io.File) - table directory
      :param tableDefinition: (com.illumon.iris.db.tables.TableDefinition) - table definition
    """
    
    return _custom_addGroupingMetadata(*args)


@_passThrough
def appendToTable(tableToAppend, destDir):
    """
    Appends to an existing table on disk, or writes a new table if the target table does not exist.
    
    :param tableToAppend: (com.illumon.iris.db.tables.Table) - table to append
    :param destDir: (java.lang.String) - destination
    """
    
    return _java_type_.appendToTable(tableToAppend, destDir)


@_passThrough
def appendToTables(definitionToAppend, tablesToAppend, destinationDirectoryNames):
    """
    Appends to existing tables on disk, or writes a new table if the target table does not exist.
    
    :param definitionToAppend: (com.illumon.iris.db.tables.TableDefinition) - table definition
    :param tablesToAppend: (com.illumon.iris.db.tables.Table[]) - tables to append
    :param destinationDirectoryNames: (java.lang.String[]) - destination directories
    """
    
    return _java_type_.appendToTables(definitionToAppend, tablesToAppend, destinationDirectoryNames)


@_passThrough
def deleteTable(path):
    """
    Deletes a table on disk.
    
    :param path: (java.io.File) - path to delete
    """
    
    return _custom_deleteTable(path)


@_passThrough
def dropColumns(*args):
    """
    Removes columns from a table definition and persists the result in path, potentially updating multiple persisted tables.
    
    *Overload 1*  
      :param currentDefinition: (com.illumon.iris.db.tables.TableDefinition) - initial table definition.
      :param rootDir: (java.io.File) - root directory where tables are found.
      :param levels: (int) - levels below rootDir where table directories are found.
      :param columnsToRemove: (java.lang.String...) - columns to remove.
      :return: (com.illumon.iris.db.tables.TableDefinition) new table definition if successful; otherwise null.
      
    *Overload 2*  
      :param currentDefinition: (com.illumon.iris.db.tables.TableDefinition) - initial table definition.
      :param path: (java.io.File) - path of the table receiving the definition.
      :param columnsToRemove: (java.lang.String...) - columns to remove.
      :return: (com.illumon.iris.db.tables.TableDefinition) new table definition.
    """
    
    return _custom_dropColumns(*args)


@_passThrough
def flushColumnData():
    """
    Flush all previously written column data to disk.
    """
    
    return _java_type_.flushColumnData()


@_passThrough
def getAllDbDirs(tableName, rootDir, levelsDepth):
    """
    Gets all subtable directories.
    
    :param tableName: (java.lang.String) - table name
    :param rootDir: (java.io.File) - root directory where tables are found
    :param levelsDepth: (int) - levels below rootDir where table directories are found
    :return: (java.util.List<java.io.File>) all subtable directories for tableName
    """
    
    return _custom_getAllDbDirs(tableName, rootDir, levelsDepth)


@_passThrough
def readTable(*args):
    """
    Reads in a table from disk.
    
    *Overload 1*  
      :param path: (java.io.File) - table location
      :param tableDefinition: (com.illumon.iris.db.tables.TableDefinition) - table definition
      :return: (com.illumon.iris.db.tables.Table) table
      
    *Overload 2*  
      :param path: (java.io.File) - table location
      :return: (com.illumon.iris.db.tables.Table) table
    """
    
    return _custom_readTable(*args)


@_passThrough
def renameColumns(*args):
    """
    Renames columns in a table definition and persists the result in path, potentially updating multiple persisted tables.
    
    *Overload 1*  
      :param currentDefinition: (com.illumon.iris.db.tables.TableDefinition) - initial table definition.
      :param rootDir: (java.io.File) - root directory where tables are found.
      :param levels: (int) - levels below rootDir where table directories are found.
      :param columnsToRename: (java.lang.String...) - columns to rename.
      :return: (com.illumon.iris.db.tables.TableDefinition) new table definition.
      
    *Overload 2*  
      :param currentDefinition: (com.illumon.iris.db.tables.TableDefinition) - initial table definition.
      :param path: (java.io.File) - path of the table receiving the definition.
      :param columnsToRename: (java.lang.String...) - columns to rename.
      :return: (com.illumon.iris.db.tables.TableDefinition) new table definition.
      
    *Overload 3*  
      :param currentDefinition: (com.illumon.iris.db.tables.TableDefinition) - initial table definition.
      :param path: (java.io.File) - path of the table receiving the definition.
      :param columnsToRename: (com.illumon.iris.db.tables.select.MatchPair...) - columns to rename.
      :return: (com.illumon.iris.db.tables.TableDefinition) new table definition.
    """
    
    return _custom_renameColumns(*args)


@_passThrough
def updateColumns(currentDefinition, rootDir, levels, *updates):
    """
    Updates columns in a table definition and persists the result in path, potentially updating multiple persisted tables.
    
    :param currentDefinition: (com.illumon.iris.db.tables.TableDefinition) - initial table definition.
    :param rootDir: (java.io.File) - root directory where tables are found.
    :param levels: (int) - levels below rootDir where table directories are found.
    :param updates: (java.lang.String...) - columns to update.
    :return: (com.illumon.iris.db.tables.TableDefinition) new table definition.
    """
    
    return _custom_updateColumns(currentDefinition, rootDir, levels, *updates)


@_passThrough
def writeDeephavenTables(sources, tableDefinition, destinations):
    """
    Write out tables to disk in the Deephaven format.
    
    :param sources: (com.illumon.iris.db.tables.Table[]) - source tables
    :param tableDefinition: (com.illumon.iris.db.tables.TableDefinition) - table definition
    :param destinations: (java.io.File[]) - destinations
    """
    
    return _custom_writeDeephavenTables(sources, tableDefinition, destinations)


@_passThrough
def writeParquetTables(sources, tableDefinition, codecName, destinations, groupingColumns):
    """
    Writes tables to disk in parquet format under a given destinations.  If you specify grouping columns, there
     must already be grouping information for those columns in the sources.  This can be accomplished with
     .by(<grouping columns>).ungroup() or .sort(<grouping column>).
    
    :param sources: (com.illumon.iris.db.tables.Table[]) - The tables to write
    :param tableDefinition: (com.illumon.iris.db.tables.TableDefinition) - The common schema for all the tables to write
    :param codecName: (org.apache.parquet.hadoop.metadata.CompressionCodecName) - Compression codec to use.  The only supported codecs are
                            CompressionCodecName.SNAPPY and CompressionCodecName.UNCOMPRESSED.
    :param destinations: (java.io.File[]) - The destinations path
    :param groupingColumns: (java.lang.String[]) - List of columns the tables are grouped by (the write operation will store the grouping info)
    """
    
    return _custom_writeParquetTables(sources, tableDefinition, codecName, destinations, groupingColumns)


@_passThrough
def writeTable(*args):
    """
    Write out a table to disk.
    
    *Overload 1*  
      :param sourceTable: (com.illumon.iris.db.tables.Table) - source table
      :param destDir: (java.lang.String) - destination
      
    *Overload 2*  
      :param sourceTable: (com.illumon.iris.db.tables.Table) - source table
      :param destDir: (java.lang.String) - destination
      :param storageFormat: (com.illumon.iris.db.tables.databases.Database.StorageFormat) - Format used for storage
      
    *Overload 3*  
      :param sourceTable: (com.illumon.iris.db.tables.Table) - source table
      :param definition: (com.illumon.iris.db.tables.TableDefinition) - table definition
      :param destDir: (java.io.File) - destination
      :param storageFormat: (com.illumon.iris.db.tables.databases.Database.StorageFormat) - Format used for storage
      
    *Overload 4*  
      :param sourceTable: (com.illumon.iris.db.tables.Table) - source table
      :param destDir: (java.io.File) - destination
      
    *Overload 5*  
      :param sourceTable: (com.illumon.iris.db.tables.Table) - source table
      :param destDir: (java.io.File) - destination
      :param storageFormat: (com.illumon.iris.db.tables.databases.Database.StorageFormat) - Format used for storage
    """
    
    return _custom_writeTable(*args)


@_passThrough
def writeTables(*args):
    """
    Write out tables to disk.
    
    *Overload 1*  
      :param sources: (com.illumon.iris.db.tables.Table[]) - source tables
      :param tableDefinition: (com.illumon.iris.db.tables.TableDefinition) - table definition
      :param destinations: (java.io.File[]) - destinations
      
    *Overload 2*  
      :param sources: (com.illumon.iris.db.tables.Table[]) - source tables
      :param tableDefinition: (com.illumon.iris.db.tables.TableDefinition) - table definition
      :param destinations: (java.io.File[]) - destinations
      :param storageFormat: (com.illumon.iris.db.tables.databases.Database.StorageFormat) - Format used for storage
    """
    
    return _custom_writeTables(*args)
