
"""
Easy to use wrapper for merging data.
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
        _java_type_ = jpy.get_type("com.illumon.iris.importers.util.MergeData")
        _builder_type_ = jpy.get_type("com.illumon.iris.importers.util.MergeData$Builder")


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
def builder(database, namespace, table):
    """
    Creates a new MergeDataBuilder object. Method calls on this object can then be used to configure
     the merge and run it.
    
    :param database: (com.illumon.iris.db.tables.databases.Database) - database.
    :param namespace: (java.lang.String) - namespace into which data will be merged.
    :param table: (java.lang.String) - name of the table into which data will be merged.
    :return: (com.illumon.iris.importers.util.MergeDataBuilder) new MergeDataBuilder.
    """
    
    return MergeDataBuilder(database, namespace, table)


class MergeDataBuilder(object):
    def __init__(self, *args, **kwargs):
        """
        Either *args or **kwargs should be provided for successful construction.
        - *args, when provided, should take the form (database, namespace, table)
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
        Creates a MergeData object using the properties that have been set in the MergeData.Builder.
        
        :return: (com.illumon.iris.importers.util.MergeData) new MergeData object.
        """
        
        return self._builder.build()

    def setAllowEmptyInput(self, allowEmptyInput):
        """
        Sets if empty inputs are allowed.
        
        :param allowEmptyInput: java.lang.Boolean
        :return: (com.illumon.iris.importers.util.MergeData.Builder) this builder.
        """
        
        return MergeDataBuilder(builder=self._builder.setAllowEmptyInput(allowEmptyInput))

    def setCodecName(self, codecName):
        """
        Sets the codec.
        
        :param codecName: java.lang.String
        :return: (com.illumon.iris.importers.util.MergeData.Builder) this builder.
        """
        
        return MergeDataBuilder(builder=self._builder.setCodecName(codecName))

    def setForce(self, force):
        """
        Sets whether to force merge when destinations already have data.
        
        :param force: java.lang.Boolean
        :return: (com.illumon.iris.importers.util.MergeData.Builder) this builder.
        """
        
        return MergeDataBuilder(builder=self._builder.setForce(force))

    def setLowHeapUsage(self, lowHeapUsage):
        """
        Sets how much heap to use.
        
        :param lowHeapUsage: java.lang.Boolean
        :return: (com.illumon.iris.importers.util.MergeData.Builder) this builder.
        """
        
        return MergeDataBuilder(builder=self._builder.setLowHeapUsage(lowHeapUsage))

    def setPartitionColumnFormula(self, partColumnFormula):
        """
        Sets the partition column formula.
        
        :param partColumnFormula: java.lang.String
        :return: (com.illumon.iris.importers.util.MergeData.Builder) this builder.
        """
        
        return MergeDataBuilder(builder=self._builder.setPartitionColumnFormula(partColumnFormula))

    def setPartitionColumnValue(self, partColumnValue):
        """
        Sets the partition column value.  This method adds quotes around a literal partition value to make a formula.
        
        :param partColumnValue: java.lang.String
        :return: (com.illumon.iris.importers.util.MergeData.Builder) this builder.
        """
        
        return MergeDataBuilder(builder=self._builder.setPartitionColumnValue(partColumnValue))

    def setSortColumnFormula(self, sortColumnFormula):
        """
        Sets the sort column formula.
        
        :param sortColumnFormula: java.lang.String
        :return: (com.illumon.iris.importers.util.MergeData.Builder) this builder.
        """
        
        return MergeDataBuilder(builder=self._builder.setSortColumnFormula(sortColumnFormula))

    def setStorageFormat(self, storageFormat):
        """
        Sets the storage format.
        
        :param storageFormat: java.lang.String
        :return: (com.illumon.iris.importers.util.MergeData.Builder) this builder.
        """
        
        return MergeDataBuilder(builder=self._builder.setStorageFormat(storageFormat))

    def setSyncMode(self, syncMode):
        """
        Sets the data synchornization mode.
        
        :param syncMode: java.lang.String
        :return: (com.illumon.iris.importers.util.MergeData.Builder) this builder.
        """
        
        return MergeDataBuilder(builder=self._builder.setSyncMode(syncMode))

    def setThreadPoolSize(self, threadPoolSize):
        """
        Sets the thread pool size.
        
        :param threadPoolSize: int
        :return: (com.illumon.iris.importers.util.MergeData.Builder) this builder.
        """
        
        return MergeDataBuilder(builder=self._builder.setThreadPoolSize(threadPoolSize))
