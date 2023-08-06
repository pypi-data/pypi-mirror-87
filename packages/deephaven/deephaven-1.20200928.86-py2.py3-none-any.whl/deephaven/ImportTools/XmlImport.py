
"""
Tools for programmatically executing XML batch imports.
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
        _java_type_ = jpy.get_type("com.illumon.iris.importers.util.XmlImport")
        _builder_type_ = jpy.get_type("com.illumon.iris.importers.util.XmlImport$Builder")


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
    Creates a new XmlImportBuilder object. Method calls on this object can then be used to configure
     the import and run it.
    
    :param namespace: (java.lang.String) - The String name of the namespace into which data will be imported.
    :param table: (java.lang.String) - The String name of the table into which data will be imported.
    :return: (com.illumon.iris.importers.util.XmlImportBuilder) new XmlImportBuilder object.
    """
    
    return XmlImportBuilder(namespace, table)


class XmlImportBuilder(object):
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
        Creates an XmlImport object using the properties that have been set in the XmlImport.Builder.
        
        :return: (com.illumon.iris.importers.util.XmlImport) A XmlImport object.
        """
        
        return self._builder.build()

    def setConstantColumnValue(self, constantColumnValue):
        """
        Sets the value to use for source columns with a sourceType of CONSTANT.
        
        :param constantColumnValue: java.lang.String
        :return: (com.illumon.iris.importers.util.XmlImport.Builder) this builder.
        """
        
        return XmlImportBuilder(builder=self._builder.setConstantColumnValue(constantColumnValue))

    def setDelimiter(self, delimiter):
        """
        Set the delimiter character used for array data elements. Default is comma.
         This can be used to set a different character such as pipe (|), semi-colon (;),
         or any other single character.
        
        :param delimiter: char
        :return: (com.illumon.iris.importers.util.XmlImport.Builder) this builder.
        """
        
        return XmlImportBuilder(builder=self._builder.setDelimiter(delimiter))

    def setDestinationDirectory(self, destinationDirectory):
        """
        Sets the destination directory.
        
        :param destinationDirectory: (java.io.File) - destination directory.
        :return: (ImportBuilder.T) this builder.
        """
        
        return XmlImportBuilder(builder=self._builder.setDestinationDirectory(destinationDirectory))

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
        
        return XmlImportBuilder(builder=self._builder.setDestinationPartitions(destinationPartitions))

    def setElementType(self, elementType):
        """
        Sets the name or path of the element that will contain data elements.
        
        :param elementType: java.lang.String
        :return: (com.illumon.iris.importers.util.XmlImport.Builder) this builder.
        """
        
        return XmlImportBuilder(builder=self._builder.setElementType(elementType))

    def setMaxDepth(self, maxDepth):
        """
        Sets a value indicating, starting from Start Depth, how many levels of element paths to traverse and
         concatenate to provide a list that can be selected under Element Name.
        
        :param maxDepth: int
        :return: (com.illumon.iris.importers.util.XmlImport.Builder) this builder.
        """
        
        return XmlImportBuilder(builder=self._builder.setMaxDepth(maxDepth))

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
        
        return XmlImportBuilder(builder=self._builder.setOutputMode(outputMode))

    def setPartitionColumn(self, partitionColumn):
        """
        Sets the partition column.
        
        :param partitionColumn: (java.lang.String) - partition column.
        :return: (ImportBuilder.T) this builder.
        """
        
        return XmlImportBuilder(builder=self._builder.setPartitionColumn(partitionColumn))

    def setPositionValues(self, positionValues):
        """
        Set whether field values within the document will be found by name or by position.
         E.g., a value called Price might be contained in an element named Price, or an attribute named Price.
         When this option is included, field names (column names) will be taken from the table schema, and the
         data values will be parsed into them by matching the position of the value with the position of column
         in the schema.
        
        :param positionValues: boolean
        :return: (com.illumon.iris.importers.util.XmlImport.Builder) this builder.
        """
        
        return XmlImportBuilder(builder=self._builder.setPositionValues(positionValues))

    def setSchemaService(self, schemaService):
        """
        Sets the schema service.
        
        :param schemaService: (com.illumon.iris.db.schema.SchemaService) - schema service.
        :return: (ImportBuilder.T) this builder.
        """
        
        return XmlImportBuilder(builder=self._builder.setSchemaService(schemaService))

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
        
        return XmlImportBuilder(builder=self._builder.setSourceDirectory(sourceDirectory))

    def setSourceFile(self, sourceFile):
        """
        Sets the source file.
        
        :param sourceFile: (java.lang.String) - source file
        :return: (FileImportBuilder.T) this builder
        """
        
        return XmlImportBuilder(builder=self._builder.setSourceFile(sourceFile))

    def setSourceGlob(self, sourceGlob):
        """
        Sets the source glob.
        
        :param sourceGlob: (java.lang.String) - source glob
        :return: (FileImportBuilder.T) this builer
        """
        
        return XmlImportBuilder(builder=self._builder.setSourceGlob(sourceGlob))

    def setSourceName(self, sourceName):
        """
        Sets the source name.
        
        :param sourceName: (java.lang.String) - source name.
        :return: (ImportBuilder.T) this builder.
        """
        
        return XmlImportBuilder(builder=self._builder.setSourceName(sourceName))

    def setStartDepth(self, startDepth):
        """
        Set the value, under the element indicated by Start Index, indication how many levels of first children
         to traverse to find an element that contains data to import.
        
        :param startDepth: int
        :return: (com.illumon.iris.importers.util.XmlImport.Builder) this builder.
        """
        
        return XmlImportBuilder(builder=self._builder.setStartDepth(startDepth))

    def setStartIndex(self, startIndex):
        """
        Set the value starting from the root of the document, of the index (1 being the first top-level element
         in the document after the root) of the element under which data can be found.
        
        :param startIndex: int
        :return: (com.illumon.iris.importers.util.XmlImport.Builder) this builder.
        """
        
        return XmlImportBuilder(builder=self._builder.setStartIndex(startIndex))

    def setStrict(self, strict):
        """
        Sets strict checking.
        
        :param strict: (boolean) - strict.
        :return: (ImportBuilder.T) this builder.
        """
        
        return XmlImportBuilder(builder=self._builder.setStrict(strict))

    def setUseAttributeValues(self, useAttributeValues):
        """
        Sets whether field values will be taken from attribute values. E.g., 
        
        :param useAttributeValues: boolean
        :return: (com.illumon.iris.importers.util.XmlImport.Builder) this builder.
        """
        
        return XmlImportBuilder(builder=self._builder.setUseAttributeValues(useAttributeValues))

    def setUseElementValues(self, useElementValues):
        """
        Sets whether field values will be taken from element values. E.g., 10.25>
        
        :param useElementValues: boolean
        :return: (com.illumon.iris.importers.util.XmlImport.Builder) this builder.
        """
        
        return XmlImportBuilder(builder=self._builder.setUseElementValues(useElementValues))
