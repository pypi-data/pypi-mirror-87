"""
read_files.py
~~~~~~~~~~~~~
This modules provides functions which aid in reading data from files.
"""

# Standard library.
from typing import Any, Dict, List, Union
# Related third-party library.
from pandas import DataFrame, read_excel, read_csv
from xlrd import open_workbook, XLRDError

def is_excel(filename):
    """
    Returns ``True`` if the file provided in ``filename`` is a valid Excel file, and ``False``
    otherwise.

    :param filename:    The qualified name of the file to be checked.
    :type filename:     ``str``
    :return:            Boolean. Whether ``filename`` is a valid Excel file.
    :rtype:             ``bool``

    Usage::

        >>> import EzPyZ as ez
        >>> ez.tools.read_files.is_excel("bmi_data.xlsx")
        True

    """
    try:
        open_workbook(filename)
        return True
    except XLRDError:
        return False
    except Exception as e:
        print(e)
        return False

def read_file(filename: str, return_pandas_df=False):
    """
    Reads the provided Excel or CSV data file. Returns a pandas ``DataFrame`` object if
    ``return_pandas_df`` is ``True``, or a dictionary where the keys are column titles and the
    values are lists of associated values (in order) otherwise.

    :param filename:            The qualified path to the data file to read.
    :type filename:             ``str``
    :param return_pandas_df:    (optional) Boolean. Whether the data should be returned as a
                                ``pandas.DataFrame``. Defaults to ``False``.
    :return:                    A formatted version of the data in ``filename``.
    :rtype:                     ``pandas.DataFrame`` or ``Dict[str, List[Any]]]``

    Usage::

        >>> import EzPyZ as ez
        >>> data = ez.tools.read_file("bmi_data.csv")

    """
    # Reading file.
    if is_excel(filename):
        # File is an Excel file.
        df = read_excel(filename)
    else:
        # File is a CSV file.
        df = read_csv(filename)

    # Returning value based on whether ``return_pandas_df`` is ``True`` or ``False``
    if return_pandas_df:
        return df
    return {i: list(df[i]) for i in list(df.columns)}
