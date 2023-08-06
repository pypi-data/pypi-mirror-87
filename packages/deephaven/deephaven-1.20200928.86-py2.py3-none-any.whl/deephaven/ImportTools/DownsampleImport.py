
"""
Easy to use wrapper for downsampling data.
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
        _java_type_ = jpy.get_type("com.illumon.iris.importers.util.DownsampleImport")
        _builder_type_ = jpy.get_type("com.illumon.iris.importers.util.DownsampleImport$Builder")


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
def builder(db, namespace, table, timestampColumn, period, *keyColumns):
    """
    Creates a new DownsampleImportBuilder object. Method calls on this object can then be used to configure
     the import and run it.
    
    :param db: (com.illumon.iris.db.tables.databases.Database) - database.
    :param namespace: (java.lang.String) - namespace into which data will be imported.
    :param table: (java.lang.String) - name of the table into which data will be imported.
    :param timestampColumn: (java.lang.String) - timestamp column.
    :param period: (java.lang.String) - downsample period.
    :param keyColumns: (java.lang.String...) - key columns.
    :return: (com.illumon.iris.importers.util.DownsampleImportBuilder) A new DownsampleImportBuilder object.
    """
    
    return DownsampleImportBuilder(db, namespace, table, timestampColumn, period, *keyColumns)


class DownsampleImportBuilder(object):
    def __init__(self, *args, **kwargs):
        """
        Either *args or **kwargs should be provided for successful construction.
        - *args, when provided, should take the form (db, namespace, table, timestampColumn, period, *keyColumns)
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

    def addAggregate(self, aggType, column):
        """
        Adds a combo aggregate method.
        
        :param aggType: com.illumon.iris.db.v2.by.AggType
        :param column: java.lang.String
        :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.addAggregate(aggType, column))

    def addAggregates(self, *aggregates):
        """
        Adds combo aggregate methods.
        
        :param aggregates: com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy...
        :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.addAggregates(*aggregates))

    def addArrayColumns(self, *columns):
        """
        Adds columns to compute array values for bins.
        
        :param columns: java.lang.String...
        :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.addArrayColumns(*columns))

    def addAvgColumns(self, *columns):
        """
        Adds columns to compute the average values for bins.
        
        :param columns: java.lang.String...
        :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.addAvgColumns(*columns))

    def addFirstColumns(self, *columns):
        """
        Adds columns to compute the first values for bins.
        
        :param columns: java.lang.String...
        :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.addFirstColumns(*columns))

    def addLastColumns(self, *columns):
        """
        Adds columns to compute the last values for bins.
        
        :param columns: java.lang.String...
        :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.addLastColumns(*columns))

    def addMaxColumns(self, *columns):
        """
        Adds columns to compute the max values for bins.
        
        :param columns: java.lang.String...
        :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.addMaxColumns(*columns))

    def addMinColumns(self, *columns):
        """
        Adds columns to compute the min values for bins.
        
        :param columns: java.lang.String...
        :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.addMinColumns(*columns))

    def addStdColumns(self, *columns):
        """
        Adds columns to compute the standard deviation values for bins.
        
        :param columns: java.lang.String...
        :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.addStdColumns(*columns))

    def addSumColumns(self, *columns):
        """
        Adds columns to compute the sum values for bins.
        
        :param columns: java.lang.String...
        :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.addSumColumns(*columns))

    def addVarColumns(self, *columns):
        """
        Adds columns to compute the variance values for bins.
        
        :param columns: java.lang.String...
        :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.addVarColumns(*columns))

    def build(self):
        """
        Builds the importer.
        
        :return: (com.illumon.iris.importers.util.DownsampleImport) importer.
        """
        
        return self._builder.build()

    def setAJStrategy(self, ajStrategy):
        """
        Sets the as-of-join strategy.
        
        *Overload 1*  
          :param ajStrategy: java.lang.String
          :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
          
        *Overload 2*  
          :param ajStrategy: com.illumon.iris.db.tables.Table.JoinStrategy
          :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.setAJStrategy(ajStrategy))

    def setAllBins(self, allBins):
        """
        Sets whether data will be output for all bins, even if there are no samples.
        
        :param allBins: boolean
        :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.setAllBins(allBins))

    def setByStrategy(self, byStrategy):
        """
        Sets the by strategy.
        
        *Overload 1*  
          :param byStrategy: com.illumon.iris.db.tables.Table.ByStrategy
          :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
          
        *Overload 2*  
          :param byStrategy: java.lang.String
          :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.setByStrategy(byStrategy))

    def setCalendar(self, calendar):
        """
        Sets the calendar.
        
        :param calendar: java.lang.String
        :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.setCalendar(calendar))

    def setDestinationDirectory(self, destinationDirectory):
        """
        Sets the destination directory.
        
        :param destinationDirectory: (java.io.File) - destination directory.
        :return: (ImportBuilder.T) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.setDestinationDirectory(destinationDirectory))

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
        
        return DownsampleImportBuilder(builder=self._builder.setDestinationPartitions(destinationPartitions))

    def setLogger(self, logger):
        """
        Sets the logger.
        
        :param logger: com.fishlib.io.logger.Logger
        :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.setLogger(logger))

    def setMaintainStateColumns(self, *maintainStateColumns):
        """
        Adds columns to keep via as-of-join.
        
        :param maintainStateColumns: java.lang.String...
        :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.setMaintainStateColumns(*maintainStateColumns))

    def setNaturalJoinStrategy(self, naturalJoinStrategy):
        """
        Sets the natural join strategy.
        
        *Overload 1*  
          :param naturalJoinStrategy: com.illumon.iris.db.tables.Table.JoinStrategy
          :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
          
        *Overload 2*  
          :param naturalJoinStrategy: java.lang.String
          :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.setNaturalJoinStrategy(naturalJoinStrategy))

    def setNumThreads(self, numThreads):
        """
        Sets the number of threads.
        
        :param numThreads: int
        :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.setNumThreads(numThreads))

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
        
        return DownsampleImportBuilder(builder=self._builder.setOutputMode(outputMode))

    def setPartitionColumn(self, partitionColumn):
        """
        Sets the partition column.
        
        :param partitionColumn: java.lang.String
        :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.setPartitionColumn(partitionColumn))

    def setSchemaService(self, schemaService):
        """
        Sets the schema service.
        
        :param schemaService: (com.illumon.iris.db.schema.SchemaService) - schema service.
        :return: (ImportBuilder.T) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.setSchemaService(schemaService))

    def setSourceName(self, sourceName):
        """
        Sets the source name.
        
        :param sourceName: (java.lang.String) - source name.
        :return: (ImportBuilder.T) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.setSourceName(sourceName))

    def setSourceTable(self, sourceTable):
        """
        Sets the source table.
        
        :param sourceTable: com.illumon.iris.db.tables.Table
        :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.setSourceTable(sourceTable))

    def setStrict(self, strict):
        """
        Sets strict checking.
        
        :param strict: (boolean) - strict.
        :return: (ImportBuilder.T) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.setStrict(strict))

    def setTimeBinMode(self, timeBinMode):
        """
        Sets the time bin mode.
        
        *Overload 1*  
          :param timeBinMode: com.illumon.iris.downsampling.Downsampler.TimeBinMode
          :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
          
        *Overload 2*  
          :param timeBinMode: java.lang.String
          :return: (com.illumon.iris.importers.util.DownsampleImport.Builder) this builder.
        """
        
        return DownsampleImportBuilder(builder=self._builder.setTimeBinMode(timeBinMode))
