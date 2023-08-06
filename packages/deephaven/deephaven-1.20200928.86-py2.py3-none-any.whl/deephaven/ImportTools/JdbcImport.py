
"""
Tools for programmatically executing JDBC batch imports.
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
        _java_type_ = jpy.get_type("com.illumon.iris.importers.util.JdbcImport")
        _builder_type_ = jpy.get_type("com.illumon.iris.importers.util.JdbcImport$Builder")


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
    Creates a new JdbcImportBuilder object. Method calls on this object can then be used to configure
     the import and run it.
    
    :param namespace: (java.lang.String) - The String name of the namespace into which data will be imported.
    :param table: (java.lang.String) - The String name of the table into which data will be imported.
    :return: (com.illumon.iris.importers.util.JdbcImportBuilder) A new JdbcImportBuilder object.
    """
    
    return JdbcImportBuilder(namespace, table)


@_passThrough
def getServerTimeZone(driver, connectionUrl, user, password):
    """
    Utility method to retrieve database server timezone. Used by default for interpreting dates and times on import.
    
    :param driver: (java.lang.String) - A String of the fully qualified class name of the JDBC driver to use.
    :param connectionUrl: (java.lang.String) - A String connection URL whose formatting is specified by the driver being used.
    :param user: java.lang.String
    :param password: java.lang.String
    :return: (java.util.TimeZone) A TimeZone
    """
    
    return _java_type_.getServerTimeZone(driver, connectionUrl, user, password)


class JdbcImportBuilder(object):
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
        Creates a JdbcImport object using the properties that have been set in the JdbcImport.Builder.
        
        :return: (com.illumon.iris.importers.util.JdbcImport) A JdbcImport object.
        """
        
        return self._builder.build()

    def setConnectionUrl(self, connectionUrl):
        """
        Sets a String of the URL to use when connecting to the JDBC data source.
        
        :param connectionUrl: java.lang.String
        :return: (com.illumon.iris.importers.util.JdbcImport.Builder) this builder.
        """
        
        return JdbcImportBuilder(builder=self._builder.setConnectionUrl(connectionUrl))

    def setDestinationDirectory(self, destinationDirectory):
        """
        Sets the destination directory.
        
        :param destinationDirectory: (java.io.File) - destination directory.
        :return: (ImportBuilder.T) this builder.
        """
        
        return JdbcImportBuilder(builder=self._builder.setDestinationDirectory(destinationDirectory))

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
        
        return JdbcImportBuilder(builder=self._builder.setDestinationPartitions(destinationPartitions))

    def setDriver(self, driver):
        """
        Sets a String of the driver to use when connecting to the JDBC data source.
        
        :param driver: java.lang.String
        :return: (com.illumon.iris.importers.util.JdbcImport.Builder) this builder.
        """
        
        return JdbcImportBuilder(builder=self._builder.setDriver(driver))

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
        
        return JdbcImportBuilder(builder=self._builder.setOutputMode(outputMode))

    def setPartitionColumn(self, partitionColumn):
        """
        Sets the partition column.
        
        :param partitionColumn: (java.lang.String) - partition column.
        :return: (ImportBuilder.T) this builder.
        """
        
        return JdbcImportBuilder(builder=self._builder.setPartitionColumn(partitionColumn))

    def setPassword(self, password):
        """
        Sets a String of the password to use when connecting to the JDBC data source.
        
        :param password: java.lang.String
        :return: (com.illumon.iris.importers.util.JdbcImport.Builder) this builder.
        """
        
        return JdbcImportBuilder(builder=self._builder.setPassword(password))

    def setQuery(self, query):
        """
        Sets a String of the query to execute against the JDBC data source.
        
        :param query: java.lang.String
        :return: (com.illumon.iris.importers.util.JdbcImport.Builder) this builder.
        """
        
        return JdbcImportBuilder(builder=self._builder.setQuery(query))

    def setSchemaService(self, schemaService):
        """
        Sets the schema service.
        
        :param schemaService: (com.illumon.iris.db.schema.SchemaService) - schema service.
        :return: (ImportBuilder.T) this builder.
        """
        
        return JdbcImportBuilder(builder=self._builder.setSchemaService(schemaService))

    def setSourceName(self, sourceName):
        """
        Sets the source name.
        
        :param sourceName: (java.lang.String) - source name.
        :return: (ImportBuilder.T) this builder.
        """
        
        return JdbcImportBuilder(builder=self._builder.setSourceName(sourceName))

    def setSourceTimeZone(self, *args):
        """
        Sets the time zone to use when interpreting date/time values from the source.
        
        *Overload 1*  
          :param sourceTimeZone: java.util.TimeZone
          :return: (com.illumon.iris.importers.util.JdbcImport.Builder) this builder.
          
        *Overload 2*  
          :param sourceTimeZoneID: java.lang.String
          :return: (com.illumon.iris.importers.util.JdbcImport.Builder) this builder.
        """
        
        return JdbcImportBuilder(builder=self._builder.setSourceTimeZone(*args))

    def setStrict(self, strict):
        """
        Sets strict checking.
        
        :param strict: (boolean) - strict.
        :return: (ImportBuilder.T) this builder.
        """
        
        return JdbcImportBuilder(builder=self._builder.setStrict(strict))

    def setUser(self, user):
        """
        Sets a String of the user name to use when connecting to the JDBC data source.
        
        :param user: java.lang.String
        :return: (com.illumon.iris.importers.util.JdbcImport.Builder) this builder.
        """
        
        return JdbcImportBuilder(builder=self._builder.setUser(user))
