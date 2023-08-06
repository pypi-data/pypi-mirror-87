#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

"""Functionality for working with Deephaven InputTables."""

import jpy

__all__ = ['InputTable', 'TableInputHandler', 'LiveInputTableEditor']


LiveInputTableEditor = None  #: UI editor for input tables class (com.illumon.iris.console.utils.LiveInputTableEditor).


def _defineSymbols():
    """
    Defines appropriate java symbol, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global LiveInputTableEditor
    if LiveInputTableEditor is None:
        # This will raise an exception if the desired object is not the classpath
        LiveInputTableEditor = jpy.get_type("com.illumon.iris.console.utils.LiveInputTableEditor")


# Define all of our functionality, if currently possible
try:
    _defineSymbols()
except Exception as e:
    pass

