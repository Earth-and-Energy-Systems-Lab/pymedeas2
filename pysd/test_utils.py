""" Utilities for aiding in testing and comparing outputs """

import os.path
import warnings

import numpy as np
import pandas as pd
from chardet.universaldetector import UniversalDetector

import pysd


def runner(model_file):
    """
    Runs translates and runs a model and returns its output and the
    canonical.

    Parameters
    ----------
    model_file: str
        Name of the original model file. Must be '.mdl' or '.xmile'.

    Returns
    -------
    output, canon: tuple of pandas.DataFrame
        pandas.DataFrame of the model output and the canonical output
        read from output.csv or output.tab.

    """
    directory = os.path.dirname(model_file)
    
    # load canonical output
    canon = load_canon(os.path.join(directory,'output'))

    # load model
    if model_file.endswith('.mdl'):
        model = pysd.read_vensim(model_file)
    elif model_file.endswith(".xmile"):
        model = pysd.read_xmile(model_file)
    else:
        raise AttributeError('Modelfile should be *.mdl or *.xmile')
    # run model
    output = model.run(return_columns=canon.columns)

    return output, canon


def load_canon(file_name):
    """
    Load canonical output

    Parameters
    ----------
    file_name: str
        Output file to read. Must be csv or tab. If the file extension
        is not given, it will check for file_name.csv first and for
        file_name.tab after.

    Returns
    -------
    canon: pandas.DataFrame
        A pandas.DataFrame with the canonical output

    """
    filename, file_extension = os.path.splitext(file_name)
    if not file_extension:
        # if extension not given check for csv and tab
        # needed for integration tests
        if os.path.isfile(filename + '.csv'):
            file_extension = '.csv'
        elif os.path.isfile(filename + '.tab'):
            file_extension = '.tab'
        else:
            raise IOError('Canonical output file not found')
        file_name = filename + file_extension
            
    if file_extension == '.csv':
        canon = pd.read_csv(
            file_name,
            encoding=detect_encoding(file_name),
            index_col='Time')
    elif file_extension == '.tab':
        canon = pd.read_table(
            file_name,
            encoding=detect_encoding(file_name),
            index_col='Time')

    if 'Time.1' in canon.columns:
        # Remove DATA type inputs from output
        return canon.drop(
            canon.columns[np.where(canon.columns=='Time.1')[0][0]:],
            axis=1)

    return canon


def assert_frames_close(actual, expected, assertion="raise", 
                        precision=2, **kwargs):
    """
    Compare DataFrame items by column and
    raise AssertionError if any column is not equal.

    Ordering of columns is unimportant, items are compared only by label.
    NaN and infinite values are supported.

    Parameters
    ----------
    actual: pandas.DataFrame
        Actual value from the model output
    expected: pandas.DataFrame
        Expected model output
    assertion: str (optional)
        "raise" if an error should be raised when not able to
        assert that two frames are close. Otherwise, it will
        show a warning message. Default is "raise".
    precision: int (optional)
        Precision to print the numerical values of assertion
        message. Default is 2.
    kwargs:
        Optional rtol and atol values for assert_allclose

    Examples
    --------
    >>> assert_frames_close(pd.DataFrame(100, index=range(5), columns=range(3)),
    ...                   pd.DataFrame(100, index=range(5), columns=range(3)))

    >>> assert_frames_close(pd.DataFrame(100, index=range(5), columns=range(3)),
    ...                   pd.DataFrame(110, index=range(5), columns=range(3)),
    ...                   rtol=.2)

    >>> assert_frames_close(pd.DataFrame(100, index=range(5), columns=range(3)),
    ...                   pd.DataFrame(150, index=range(5), columns=range(3)),
    ...                   rtol=.2)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    AssertionError:
    ...

    References
    ----------
    Derived from: http://nbviewer.jupyter.org/gist/jiffyclub/ac2e7506428d5e1d587b
    """

    assert (isinstance(actual, pd.DataFrame) and
            isinstance(expected, pd.DataFrame)), \
        'Inputs must both be pandas DataFrames.'

    assert set(expected.columns) == set(actual.columns), \
        'test set columns must be equal to those in actual/observed set.'

    assert np.all(np.equal(expected.index.values, actual.index.values)), \
        'test set and actual set must share a common index' \
        'instead found' + expected.index.values + 'vs' + actual.index.values

    for col in expected.columns:
        # if for Vensim outputs where constant values are only
        # in the first row
        if np.isnan(expected[col].values[1:]).all():
            expected[col] = expected[col].values[0]
        try:
            assert_allclose(expected[col].values,
                            actual[col].values,
                            **kwargs)
        except AssertionError as e:
            assertion_details = '\n\n'\
                + 'Column: ' + str(col) + ' is not close.'\
                + '\n\nExpected values:\n\t'\
                + np.array2string(expected[col].values,
                                  precision=precision,
                                  separator=',')\
                + '\n\nActual values:\n\t'\
                + np.array2string(actual[col].values,
                                  precision=precision,
                                  separator=',',
                                  suppress_small=True)\
                + '\n\nDiference:\n\t'\
                + np.array2string(expected[col].values-actual[col].values,
                                  precision=precision,
                                  separator=',',
                                  suppress_small=True)\

            if assertion =="raise":
                raise AssertionError(assertion_details)
            else:
                warnings.warn(assertion_details)


def assert_allclose(x, y, rtol=1.e-5, atol=1.e-5):
    """
    Asserts if elements from two arrays all close
    
    Parameters
    ----------
    x: ndarray
        Expected value.
    y: ndarray
        Actual value.
    rtol: float (optional)
        Relative tolerance on the error. Default is 1.e-5.
    atol: float (optional)
        Absolut tolerance on the error. Default is 1.e-5.

    Returns
    -------
    None
        
    """
    assert np.all(np.less_equal(abs(x - y), atol + rtol * abs(y)))


def detect_encoding(filename):
    """
    Detects the encoding of a file
    
    Parameters
    ----------
    filename: str
        Name of the file to detect the encoding

    Returns
    -------
    encoding: str
        The encoding of the file.

    """
    detector = UniversalDetector()
    for line in open(filename, 'rb').readlines():
        detector.feed(line)
        if detector.done: break
    detector.close()
    return detector.result['encoding']
