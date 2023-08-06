
"""
The ComboAggregateFactory combines one or more aggregations into an operator for use with Table.by(AggregationStateFactory).

 The intended use of this class is to call the ComboAggregateFactory.AggCombo(ComboBy...) method with a set of aggregations
 defined by:
 
* ComboAggregateFactory.AggMin(java.lang.String...)
* ComboAggregateFactory.AggMax(java.lang.String...)
* ComboAggregateFactory.AggSum(java.lang.String...)
* ComboAggregateFactory.AggAbsSum(java.lang.String...)
* ComboAggregateFactory.AggVar(java.lang.String...)
* ComboAggregateFactory.AggAvg(java.lang.String...)
* ComboAggregateFactory.AggWAvg(java.lang.String, java.lang.String...)
* ComboAggregateFactory.AggWSum(java.lang.String, java.lang.String...)
* ComboAggregateFactory.AggMed(java.lang.String...)
* ComboAggregateFactory.AggPct(double, java.lang.String...)
* ComboAggregateFactory.AggStd(java.lang.String...)
* ComboAggregateFactory.AggFirst(java.lang.String...)
* ComboAggregateFactory.AggLast(java.lang.String...)
* ComboAggregateFactory.AggCount(java.lang.String)
* ComboAggregateFactory.AggCountDistinct(java.lang.String...)
* ComboAggregateFactory.AggDistinct(java.lang.String...)
* ComboAggregateFactory.AggArray(java.lang.String...)

For example, to produce a table with several aggregations on the LastPrice of a Trades table:
 ohlc=trades.by(AggCombo(AggFirst("Open=LastPrice"), AggLast("Close=LastPrice"), AggMax("High=LastPrice"), AggMin("Low=LastPrice"), AggSum("Volume=Size"), AggWAvg("Size", "VWAP=LastPrice"), "Symbol")
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
        _java_type_ = jpy.get_type("com.illumon.iris.db.v2.by.ComboAggregateFactory")


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
def Agg(*args):
    """
    Create an aggregation.
    
    *Overload 1*  
      :param factory: (com.illumon.iris.db.v2.by.AggregationStateFactoryImpl) - aggregation factory.
      :param matchPairs: (java.lang.String...) - the columns to apply the aggregation to in the form Output=Input, if the Output and Input have
                         the same name, then the column name can be specified.
      :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy) a ComboBy object suitable for passing to ComboAggregateFactory.AggCombo(ComboBy...)
      
    *Overload 2*  
      :param factoryType: (com.illumon.iris.db.v2.by.AggType) - aggregation factory type.
      :param matchPairs: (java.lang.String...) - the columns to apply the aggregation to in the form Output=Input, if the Output and Input have
                         the same name, then the column name can be specified.
      :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy) a ComboBy object suitable for passing to ComboAggregateFactory.AggCombo(ComboBy...)
    """
    
    return _java_type_.Agg(*args)


@_passThrough
def AggAbsSum(*matchPairs):
    """
    Create an absolute sum aggregation, equivalent to Table.absSumBy(String...).
    
    :param matchPairs: (java.lang.String...) - the columns to apply the aggregation to in the form Output=Input, if the Output and Input have
                       the same name, then the column name can be specified.
    :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy) a ComboBy object suitable for passing to ComboAggregateFactory.AggCombo(ComboBy...)
    """
    
    return _java_type_.AggAbsSum(*matchPairs)


@_passThrough
def AggArray(*matchPairs):
    """
    Create an array aggregation, equivalent to Table.by(String...).
    
    :param matchPairs: (java.lang.String...) - the columns to apply the aggregation to in the form Output=Input, if the Output and Input have
                       the same name, then the column name can be specified.
    :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy) a ComboBy object suitable for passing to ComboAggregateFactory.AggCombo(ComboBy...)
    """
    
    return _java_type_.AggArray(*matchPairs)


@_passThrough
def AggAvg(*matchPairs):
    """
    Create an average aggregation, equivalent to Table.avgBy(String...).
    
    :param matchPairs: (java.lang.String...) - the columns to apply the aggregation to in the form Output=Input, if the Output and Input have
                       the same name, then the column name can be specified.
    :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy) a ComboBy object suitable for passing to ComboAggregateFactory.AggCombo(ComboBy...)
    """
    
    return _java_type_.AggAvg(*matchPairs)


@_passThrough
def AggCombo(*aggregations):
    """
    Create a new ComboAggregateFactory suitable for passing to Table.by(AggregationStateFactory, String...).
    
    :param aggregations: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy...) - the aggregations to compute
    :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory) a new table with the specified aggregations.
    """
    
    return _java_type_.AggCombo(*aggregations)


@_passThrough
def AggCount(resultColumn):
    """
    Create an count aggregation, equivalent to Table.countBy(String).
    
    :param resultColumn: (java.lang.String) - the name of the result column containing the count of each group
    :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy) a ComboBy object suitable for passing to ComboAggregateFactory.AggCombo(ComboBy...)
    """
    
    return _java_type_.AggCount(resultColumn)


@_passThrough
def AggCountDistinct(*args):
    """
    Create a distinct count aggregation.
    
     The output column contains the number of distinct values for the input column in that group.
    
    *Overload 1*  
      :param matchPairs: (java.lang.String...) - the columns to apply the aggregation to in the form Output=Input, if the Output and Input have
                         the same name, then the column name can be specified.
      :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy) a ComboBy object suitable for passing to ComboAggregateFactory.AggCombo(ComboBy...).  Null values are not counted.
      
    *Overload 2*  
      :param countNulls: (boolean) - if true null values are counted as a distinct value, otherwise null values are ignored
      :param matchPairs: (java.lang.String...) - the columns to apply the aggregation to in the form Output=Input, if the Output and Input have
                         the same name, then the column name can be specified.
      :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy) a ComboBy object suitable for passing to ComboAggregateFactory.AggCombo(ComboBy...)
    """
    
    return _java_type_.AggCountDistinct(*args)


@_passThrough
def AggDistinct(*args):
    """
    Create a distinct aggregation.
    
     The output column contains a DbArrayBase with the distinct values for
     the input column within the group.
    
    *Overload 1*  
      :param matchPairs: (java.lang.String...) - the columns to apply the aggregation to in the form Output=Input, if the Output and Input have
                         the same name, then the column name can be specified.
      :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy) a ComboBy object suitable for passing to ComboAggregateFactory.AggCombo(ComboBy...).  Null values are ignored.
      
    *Overload 2*  
      :param countNulls: (boolean) - if true, then null values are included in the result, otherwise null values are ignored
      :param matchPairs: (java.lang.String...) - the columns to apply the aggregation to in the form Output=Input, if the Output and Input have
                         the same name, then the column name can be specified.
      :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy) a ComboBy object suitable for passing to ComboAggregateFactory.AggCombo(ComboBy...)
    """
    
    return _java_type_.AggDistinct(*args)


@_passThrough
def AggFirst(*matchPairs):
    """
    Create a first aggregation, equivalent to Table.firstBy(String...).
    
    :param matchPairs: (java.lang.String...) - the columns to apply the aggregation to in the form Output=Input, if the Output and Input have
                       the same name, then the column name can be specified.
    :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy) a ComboBy object suitable for passing to ComboAggregateFactory.AggCombo(ComboBy...)
    """
    
    return _java_type_.AggFirst(*matchPairs)


@_passThrough
def AggFormula(formula, formulaParam, *matchPairs):
    """
    Create a formula aggregation.
    
    :param formula: (java.lang.String) - the formula to apply to each group
    :param formulaParam: (java.lang.String) - the parameter name within the formula
    :param matchPairs: (java.lang.String...) - the columns to apply the aggregation to in the form Output=Input, if the Output and Input have
                       the same name, then the column name can be specified.
    :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy) a ComboBy object suitable for passing to ComboAggregateFactory.AggCombo(ComboBy...)
    """
    
    return _java_type_.AggFormula(formula, formulaParam, *matchPairs)


@_passThrough
def AggLast(*matchPairs):
    """
    Create a last aggregation, equivalent to Table.lastBy(String...).
    
    :param matchPairs: (java.lang.String...) - the columns to apply the aggregation to in the form Output=Input, if the Output and Input have
                       the same name, then the column name can be specified.
    :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy) a ComboBy object suitable for passing to ComboAggregateFactory.AggCombo(ComboBy...)
    """
    
    return _java_type_.AggLast(*matchPairs)


@_passThrough
def AggMax(*matchPairs):
    """
    Create a maximum aggregation, equivalent to Table.maxBy(String...).
    
    :param matchPairs: (java.lang.String...) - the columns to apply the aggregation to in the form Output=Input, if the Output and Input have
                       the same name, then the column name can be specified.
    :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy) a ComboBy object suitable for passing to ComboAggregateFactory.AggCombo(ComboBy...)
    """
    
    return _java_type_.AggMax(*matchPairs)


@_passThrough
def AggMed(*matchPairs):
    """
    Create a median aggregation, equivalent to Table.medianBy(String...).
    
    :param matchPairs: (java.lang.String...) - the columns to apply the aggregation to in the form Output=Input, if the Output and Input have
                       the same name, then the column name can be specified.
    :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy) a ComboBy object suitable for passing to ComboAggregateFactory.AggCombo(ComboBy...)
    """
    
    return _java_type_.AggMed(*matchPairs)


@_passThrough
def AggMin(*matchPairs):
    """
    Create a minimum aggregation, equivalent to Table.minBy(String...).
    
    :param matchPairs: (java.lang.String...) - the columns to apply the aggregation to in the form Output=Input, if the Output and Input have
                       the same name, then the column name can be specified.
    :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy) a ComboBy object suitable for passing to ComboAggregateFactory.AggCombo(ComboBy...)
    """
    
    return _java_type_.AggMin(*matchPairs)


@_passThrough
def AggPct(*args):
    """
    Create a percentile aggregation.
    
    *Overload 1*  
      :param percentile: (double) - the percentile to calculate
      :param matchPairs: (java.lang.String...) - the columns to apply the aggregation to in the form Output=Input, if the Output and Input have
                         the same name, then the column name can be specified.
      :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy) a ComboBy object suitable for passing to ComboAggregateFactory.AggCombo(ComboBy...)
      
    *Overload 2*  
      :param percentile: (double) - the percentile to calculate
      :param averageMedian: (boolean) - if true, then when the upper values and lower values have an equal size; average the highest
                            lower value and lowest upper value to produce the median value for integers, longs, doubles,
                            and floats
      :param matchPairs: (java.lang.String...) - the columns to apply the aggregation to in the form Output=Input, if the Output and Input have
                         the same name, then the column name can be specified.
      :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy) a ComboBy object suitable for passing to ComboAggregateFactory.AggCombo(ComboBy...)
    """
    
    return _java_type_.AggPct(*args)


@_passThrough
def AggStd(*matchPairs):
    """
    Create a standard deviation aggregation, equivalent to Table.stdBy(String...).
    
    :param matchPairs: (java.lang.String...) - the columns to apply the aggregation to in the form Output=Input, if the Output and Input have
                       the same name, then the column name can be specified.
    :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy) a ComboBy object suitable for passing to ComboAggregateFactory.AggCombo(ComboBy...)
    """
    
    return _java_type_.AggStd(*matchPairs)


@_passThrough
def AggSum(*matchPairs):
    """
    Create a summation aggregation, equivalent to Table.sumBy(String...).
    
    :param matchPairs: (java.lang.String...) - the columns to apply the aggregation to in the form Output=Input, if the Output and Input have
                       the same name, then the column name can be specified.
    :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy) a ComboBy object suitable for passing to ComboAggregateFactory.AggCombo(ComboBy...)
    """
    
    return _java_type_.AggSum(*matchPairs)


@_passThrough
def AggVar(*matchPairs):
    """
    Create a variance aggregation, equivalent to Table.varBy(String...).
    
    :param matchPairs: (java.lang.String...) - the columns to apply the aggregation to in the form Output=Input, if the Output and Input have
                       the same name, then the column name can be specified.
    :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy) a ComboBy object suitable for passing to ComboAggregateFactory.AggCombo(ComboBy...)
    """
    
    return _java_type_.AggVar(*matchPairs)


@_passThrough
def AggWAvg(weight, *matchPairs):
    """
    Create a weighted average aggregation, equivalent to Table.wavgBy(String, String...).
    
    :param weight: (java.lang.String) - the name of the column to use as the weight for the average
    :param matchPairs: (java.lang.String...) - the columns to apply the aggregation to in the form Output=Input, if the Output and Input have
                       the same name, then the column name can be specified.
    :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy) a ComboBy object suitable for passing to ComboAggregateFactory.AggCombo(ComboBy...)
    """
    
    return _java_type_.AggWAvg(weight, *matchPairs)


@_passThrough
def AggWSum(weight, *matchPairs):
    """
    Create a weighted sum aggregation, equivalent to Table.wsumBy(String, String...).
    
    :param weight: (java.lang.String) - the name of the column to use as the weight for the sum
    :param matchPairs: (java.lang.String...) - the columns to apply the aggregation to in the form Output=Input, if the Output and Input have
                       the same name, then the column name can be specified.
    :return: (com.illumon.iris.db.v2.by.ComboAggregateFactory.ComboBy) a ComboBy object suitable for passing to ComboAggregateFactory.AggCombo(ComboBy...)
    """
    
    return _java_type_.AggWSum(weight, *matchPairs)
