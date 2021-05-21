"""
pysd.py

Contains all the code that will be directly accessed by the user in normal operation.

History
--------
August 15, 2014: created
June 6 2015: Major updates - version 0.2.5
Jan 2016: Rework to handle subscripts
May 2016: Updates to handle grammar refactoring
Sept 2016: Major refactor, putting most internal code into the Model and Macro objects
"""

import sys

if sys.version_info[:2] < (3, 7):
    raise RuntimeError(
        "\n\n"
        + "Your Python version is not longer supported by PySD.\n"
        + "The current version needs to run at least Python 3.7."
        + " You are running:\n\tPython " + sys.version + "."
        + "\nPlease update your Python version or use the last "
        + " supported version:\n\t"
        + "https://github.com/JamesPHoughton/pysd/releases/tag/LastPy2")

def load(py_model_file, initialize=True, missing_values="warning"):
    """
    Load a python-converted model file.

    Parameters
    ----------
    py_model_file : <string>
        Filename of a model which has already been converted into a
        python format.
    initialize: bool (optional)
        If False, the model will not be initialize when it is loaded.
        Default is True
    missing_values : <string> (optional)
        What to do with missing values in external objects.
        If "warning" (default) shows a warning message and
        interpolates the values. If "raise" raises an error.
        If "ignore" interpolates the values without showing anything.

    Examples
    --------
    >>> model = load('../tests/test-models/samples/teacup/teacup.py')

    """
    from .py_backend import functions
    return functions.Model(py_model_file, initialize, missing_values)
