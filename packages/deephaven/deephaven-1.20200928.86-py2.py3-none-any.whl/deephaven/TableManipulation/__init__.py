#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

"""
Functionality to display and modify tables.
"""

import jpy
from ._PersistentQueryControllerClient import PersistentQueryControllerClient

__all__ = ['ColumnRenderersBuilder', 'DistinctFormatter', 'DownsampledWhereFilter', 'LayoutHintBuilder',
           'PersistentQueryTableHelper', 'PersistentQueryControllerClient', 'PivotWidgetBuilder',
           'SmartKey', 'SortPair', 'TotalsTableBuilder', 'WindowCheck']

# None until the first successful _defineSymbols() call
ColumnRenderersBuilder = None   #: Class to build and parse the directive for Table.COLUMN_RENDERERS_ATTRIBUTE (com.illumon.iris.db.v2.ColumnRenderersBuilder).
DistinctFormatter = None        #: Class to create distinct and unique coloration for each unique input value (com.illumon.iris.db.util.DBColorUtil$DistinctFormatter).
DownsampledWhereFilter = None   #: Class to downsample time series data by calculating the bin intervals for values, and then using upperBin and lastBy to select the last row for each bin (com.illumon.iris.db.v2.select.DownsampledWhereFilter).
LayoutHintBuilder = None        #: Builder class for use in assembling layout hints suitable for use with {@link com.illumon.iris.db.tables.Table#layoutHints(LayoutHintBuilder)} or {@link com.illumon.iris.db.tables.Table#layoutHints(String)} (com.illumon.iris.db.tables.utils.LayoutHintBuilder).
PivotWidgetBuilder = None       #: Helper class to build a Pivot Widget and set all of its options (com.illumon.iris.console.utils.PivotWidgetBuilder).
SmartKey = None                 #: A datastructure key class, where more than one value can be used as the key (com.fishlib.datastructures.util.SmartKey).
TotalsTableBuilder = None       #: Class to define the default aggregations and display for a totals table (com.illumon.iris.db.v2.TotalsTableBuilder).
SortPair = None                 #: Class representing a column to sort by and its direction (com.illumon.iris.db.tables.SortPair).


def _defineSymbols():
    """
    Defines appropriate java symbols, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global ColumnRenderersBuilder, DistinctFormatter, DownsampledWhereFilter, LayoutHintBuilder, \
        PivotWidgetBuilder, SmartKey, TotalsTableBuilder, SortPair

    if ColumnRenderersBuilder is None:
        # This will raise an exception if the desired object is not the classpath
        ColumnRenderersBuilder = jpy.get_type('com.illumon.iris.db.v2.ColumnRenderersBuilder')
        DistinctFormatter = jpy.get_type('com.illumon.iris.db.util.DBColorUtil$DistinctFormatter')
        DownsampledWhereFilter = jpy.get_type('com.illumon.iris.db.v2.select.DownsampledWhereFilter')
        LayoutHintBuilder = jpy.get_type('com.illumon.iris.db.tables.utils.LayoutHintBuilder')
        PivotWidgetBuilder = jpy.get_type('com.illumon.iris.console.utils.PivotWidgetBuilder')
        SmartKey = jpy.get_type('com.fishlib.datastructures.util.SmartKey')
        TotalsTableBuilder = jpy.get_type('com.illumon.iris.db.v2.TotalsTableBuilder')
        SortPair = jpy.get_type("com.illumon.iris.db.tables.SortPair")


# Define all of our functionality, if currently possible
try:
    _defineSymbols()
except Exception as e:
    pass
