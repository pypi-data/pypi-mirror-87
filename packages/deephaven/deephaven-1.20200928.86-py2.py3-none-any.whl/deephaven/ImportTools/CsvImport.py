
"""
Tools for programmatically executing CSV batch imports.
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
        _java_type_ = jpy.get_type("com.illumon.iris.importers.util.CsvImport")
        _builder_type_ = jpy.get_type("com.illumon.iris.importers.util.CsvImport$Builder")


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
def builder(namespace, table):
    """
    Creates a new CsvImportBuilder object. Method calls on this object can then be used to configure
     the import and run it.
    
    :param namespace: (java.lang.String) - The String name of the namespace into which data will be imported.
    :param table: (java.lang.String) - The String name of the table into which data will be imported.
    :return: (com.illumon.iris.importers.util.CsvImportBuilder) A new CsvImportBuilder object.
    """
    
    return CsvImportBuilder(namespace, table)


class CsvImportBuilder(object):
    def __init__(self, *args, **kwargs):
        """
        Either *args or **kwargs should be provided for successful construction.
        - *args, when provided, should take the form (namespace, table)
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

    def build(self):
        """
        Creates a CsvImport object using the properties that have been set in the CsvImport.Builder.
        
        :return: (com.illumon.iris.importers.util.CsvImport) A CsvImport object.
        """
        
        return self._builder.build()

    def setColumnNames(self, columnNames):
        """
        Sets a List of column names to be used when a headerless import is run (CsvImport.Builder.noHeader).
        
        :param columnNames: java.util.List<java.lang.String>
        :return: (com.illumon.iris.importers.util.CsvImport.Builder) this builder.
        """
        
        return CsvImportBuilder(builder=self._builder.setColumnNames(columnNames))

    def setConstantColumnValue(self, constantColumnValue):
        """
        Sets the value to use for source columns with a sourceType of CONSTANT.
        
        :param constantColumnValue: java.lang.String
        :return: (com.illumon.iris.importers.util.CsvImport.Builder) this builder.
        """
        
        return CsvImportBuilder(builder=self._builder.setConstantColumnValue(constantColumnValue))

    def setDelimiter(self, delimiter):
        """
        Set the CSV field delimiter character. Default is comma. This can be used to set a different
         character such as pipe (|), semi-colon (;), or any other single character.
        
        :param delimiter: char
        :return: (com.illumon.iris.importers.util.CsvImport.Builder) this builder.
        """
        
        return CsvImportBuilder(builder=self._builder.setDelimiter(delimiter))

    def setDestinationDirectory(self, destinationDirectory):
        """
        Sets the destination directory.
        
        :param destinationDirectory: (java.io.File) - destination directory.
        :return: (ImportBuilder.T) this builder.
        """
        
        return CsvImportBuilder(builder=self._builder.setDestinationDirectory(destinationDirectory))

    def setDestinationPartitions(self, destinationPartitions):
        """
        Sets the destination partitions
        
        *Overload 1*  
          :param destinationPartitions: (java.lang.String) - destination partitions.
          :return: (ImportBuilder.T) this builder.
          
        *Overload 2*  
          :param destinationPartitions: (java.lang.String[]) - destination partitions.
          :return: (ImportBuilder.T) this builder.
        """
        
        return CsvImportBuilder(builder=self._builder.setDestinationPartitions(destinationPartitions))

    def setFileFormat(self, fileFormat):
        """
        Set the file format of the CSV to be imported.
        
        :param fileFormat: java.lang.String
        :return: (com.illumon.iris.importers.util.CsvImport.Builder) this builder.
        """
        
        return CsvImportBuilder(builder=self._builder.setFileFormat(fileFormat))

    def setNoHeader(self, noHeader):
        """
        Sets an indicator that the file does not include a list of columns in it header. When set
         a list of column names must also be provided with CsvImport.Builder.columnNames.
         Default behavior is to expect a column name list in the header.
        
        :param noHeader: boolean
        :return: (com.illumon.iris.importers.util.CsvImport.Builder) this builder.
        """
        
        return CsvImportBuilder(builder=self._builder.setNoHeader(noHeader))

    def setOutputMode(self, outputMode):
        """
        Sets the output mode.
        
        *Overload 1*  
          :param outputMode: (com.illumon.iris.importers.ImportOutputMode) - output mode.
          :return: (ImportBuilder.T) this builder.
          
        *Overload 2*  
          :param outputMode: (java.lang.String) - output mode.
          :return: (ImportBuilder.T) this builder.
        """
        
        return CsvImportBuilder(builder=self._builder.setOutputMode(outputMode))

    def setPartitionColumn(self, partitionColumn):
        """
        Sets the partition column.
        
        :param partitionColumn: (java.lang.String) - partition column.
        :return: (ImportBuilder.T) this builder.
        """
        
        return CsvImportBuilder(builder=self._builder.setPartitionColumn(partitionColumn))

    def setSchemaService(self, schemaService):
        """
        Sets the schema service.
        
        :param schemaService: (com.illumon.iris.db.schema.SchemaService) - schema service.
        :return: (ImportBuilder.T) this builder.
        """
        
        return CsvImportBuilder(builder=self._builder.setSchemaService(schemaService))

    def setSkipFooterLines(self, skipFooterLines):
        """
        Sets the number of lines to be skipped at the end of files being read.
        
        :param skipFooterLines: (int) - An int of the number of lines to skip. Default is 0.
        :return: (com.illumon.iris.importers.util.CsvImport.Builder) this builder.
        """
        
        return CsvImportBuilder(builder=self._builder.setSkipFooterLines(skipFooterLines))

    def setSkipLines(self, skipLines):
        """
        Sets the number of lines to be skipped at the beginning of files being read before expecting the
         first line of column names or data.
        
        :param skipLines: int
        :return: (com.illumon.iris.importers.util.CsvImport.Builder) this builder.
        """
        
        return CsvImportBuilder(builder=self._builder.setSkipLines(skipLines))

    def setSourceDirectory(self, sourceDirectory):
        """
        Sets the source directory.
        
        *Overload 1*  
          :param sourceDirectory: (java.io.File) - source directory
          :return: (FileImportBuilder.T) this builder
          
        *Overload 2*  
          :param sourceDirectory: (java.lang.String) - source directory
          :return: (FileImportBuilder.T) this builder
        """
        
        return CsvImportBuilder(builder=self._builder.setSourceDirectory(sourceDirectory))

    def setSourceFile(self, sourceFile):
        """
        Sets the source file.
        
        :param sourceFile: (java.lang.String) - source file
        :return: (FileImportBuilder.T) this builder
        """
        
        return CsvImportBuilder(builder=self._builder.setSourceFile(sourceFile))

    def setSourceGlob(self, sourceGlob):
        """
        Sets the source glob.
        
        :param sourceGlob: (java.lang.String) - source glob
        :return: (FileImportBuilder.T) this builer
        """
        
        return CsvImportBuilder(builder=self._builder.setSourceGlob(sourceGlob))

    def setSourceName(self, sourceName):
        """
        Sets the source name.
        
        :param sourceName: (java.lang.String) - source name.
        :return: (ImportBuilder.T) this builder.
        """
        
        return CsvImportBuilder(builder=self._builder.setSourceName(sourceName))

    def setStrict(self, strict):
        """
        Sets strict checking.
        
        :param strict: (boolean) - strict.
        :return: (ImportBuilder.T) this builder.
        """
        
        return CsvImportBuilder(builder=self._builder.setStrict(strict))

    def setTrim(self, trim):
        """
        Sets whether to trim white space around values within delimited fields.
        
        :param trim: boolean
        :return: (com.illumon.iris.importers.util.CsvImport.Builder) this builder.
        """
        
        return CsvImportBuilder(builder=self._builder.setTrim(trim))
