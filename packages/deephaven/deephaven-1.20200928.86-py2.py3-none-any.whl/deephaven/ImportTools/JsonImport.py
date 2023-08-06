
"""
Tools for programmatically executing JSON batch imports.
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
        _java_type_ = jpy.get_type("com.illumon.iris.importers.util.JsonImport")
        _builder_type_ = jpy.get_type("com.illumon.iris.importers.util.JsonImport$Builder")


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
    Creates a new JsonImportBuilder object. Method calls on this object can then be used to configure
     the import and run it.
    
    :param namespace: (java.lang.String) - The String name of the namespace into which data will be imported.
    :param table: (java.lang.String) - The String name of the table into which data will be imported.
    :return: (com.illumon.iris.importers.util.JsonImportBuilder) A new JsonImportBuilder object.
    """
    
    return JsonImportBuilder(namespace, table)


class JsonImportBuilder(object):
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
        Creates a JsonImport object using the properties that have been set in the JsonImport.Builder.
        
        :return: (com.illumon.iris.importers.util.JsonImport) A JsonImport object.
        """
        
        return self._builder.build()

    def setColumnNames(self, columnNames):
        """
        Sets column names.
        
        *Overload 1*  
          :param columnNames: java.lang.String
          :return: (com.illumon.iris.importers.util.JsonImport.Builder) this builder.
          
        *Overload 2*  
          :param columnNames: java.util.List<java.lang.String>
          :return: (com.illumon.iris.importers.util.JsonImport.Builder) this builder.
        """
        
        return JsonImportBuilder(builder=self._builder.setColumnNames(columnNames))

    def setConstantColumnValue(self, constantColumnValue):
        """
        Sets the value to use for source columns with a sourceType of CONSTANT.
        
        :param constantColumnValue: java.lang.String
        :return: (com.illumon.iris.importers.util.JsonImport.Builder) this builder.
        """
        
        return JsonImportBuilder(builder=self._builder.setConstantColumnValue(constantColumnValue))

    def setDestinationDirectory(self, destinationDirectory):
        """
        Sets the destination directory.
        
        :param destinationDirectory: (java.io.File) - destination directory.
        :return: (ImportBuilder.T) this builder.
        """
        
        return JsonImportBuilder(builder=self._builder.setDestinationDirectory(destinationDirectory))

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
        
        return JsonImportBuilder(builder=self._builder.setDestinationPartitions(destinationPartitions))

    def setFieldPathSeparator(self, fieldPathSeparator):
        """
        Sets a String to use as the separator when generating column names from nested JSON data.
        
        :param fieldPathSeparator: java.lang.String
        :return: (com.illumon.iris.importers.util.JsonImport.Builder) this builder.
        """
        
        return JsonImportBuilder(builder=self._builder.setFieldPathSeparator(fieldPathSeparator))

    def setMaxInferItems(self, maxInferItems):
        """
        Sets a limit of the maximum number of JSON objects to examine when inferring which columns are present
         in the file. Inference is necessary because JSON has no internal "schema".
        
        :param maxInferItems: long
        :return: (com.illumon.iris.importers.util.JsonImport.Builder) this builder.
        """
        
        return JsonImportBuilder(builder=self._builder.setMaxInferItems(maxInferItems))

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
        
        return JsonImportBuilder(builder=self._builder.setOutputMode(outputMode))

    def setPartitionColumn(self, partitionColumn):
        """
        Sets the partition column.
        
        :param partitionColumn: (java.lang.String) - partition column.
        :return: (ImportBuilder.T) this builder.
        """
        
        return JsonImportBuilder(builder=self._builder.setPartitionColumn(partitionColumn))

    def setSchemaService(self, schemaService):
        """
        Sets the schema service.
        
        :param schemaService: (com.illumon.iris.db.schema.SchemaService) - schema service.
        :return: (ImportBuilder.T) this builder.
        """
        
        return JsonImportBuilder(builder=self._builder.setSchemaService(schemaService))

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
        
        return JsonImportBuilder(builder=self._builder.setSourceDirectory(sourceDirectory))

    def setSourceFile(self, sourceFile):
        """
        Sets the source file.
        
        :param sourceFile: (java.lang.String) - source file
        :return: (FileImportBuilder.T) this builder
        """
        
        return JsonImportBuilder(builder=self._builder.setSourceFile(sourceFile))

    def setSourceGlob(self, sourceGlob):
        """
        Sets the source glob.
        
        :param sourceGlob: (java.lang.String) - source glob
        :return: (FileImportBuilder.T) this builer
        """
        
        return JsonImportBuilder(builder=self._builder.setSourceGlob(sourceGlob))

    def setSourceName(self, sourceName):
        """
        Sets the source name.
        
        :param sourceName: (java.lang.String) - source name.
        :return: (ImportBuilder.T) this builder.
        """
        
        return JsonImportBuilder(builder=self._builder.setSourceName(sourceName))

    def setStrict(self, strict):
        """
        Sets strict checking.
        
        :param strict: (boolean) - strict.
        :return: (ImportBuilder.T) this builder.
        """
        
        return JsonImportBuilder(builder=self._builder.setStrict(strict))
