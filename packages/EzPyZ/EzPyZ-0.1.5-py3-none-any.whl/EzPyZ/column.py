"""
column.py
~~~~~~~~~
This module provides an ``EzPyZ.Column`` class which will be used internally to provide certain
functionality.
"""

# Standard library.
from math import isnan
import statistics as st

class Column:
    """
    A ``Column`` object. ``Column`` objects will make up ``EzPyZ.DataFrame`` objects in this module.
    This class is NOT intended for exernal use!
    """
    # ~~~~~ Special methods ~~~~~
    def __init__(self, title, values):
        """
        Constructs a ``Column`` object.

        :param title:   A string containing the title of the column.
        :type title:    ``str``
        :param values:  A list containing the values in the column, in order.
        :type values:   ``List[Any]``
        :return:        Nothing.
        :rtype:         ``NoneType``
        """
        # Validating input.
        if type(title) is not str:
            # ``title`` is of an invalid type.
            raise TypeError(
                "expected ``title`` to be of type str, got "
                + type(title).__name__
            )
        elif type(values) is not list:
            # ``values`` is of an invalid type.
            raise TypeError(
                "expected ``values`` to be of type List[Any], got "
                + type(values).__name__
            )

        self.col_title = title
        self.values = values
        return
    def __repr__(self):
        """
        Returns basic ``Column`` information.

        :return:    Basic ``Column`` information for debugging.
        :rtype:     ``str``

        Usage::

            >>> import EzPyZ as ez
            >>> col = ez.column.Column("height_cm", [134, 168, 149, 201, 177, 168])
            >>> print(repr(col))
            Column(title=height_cm, values=[134, 168, 149, 201, 177, ...])

        """
        if len(self.values) <= 5:
            return 'Column(title={}, values={})'.format(self.col_title, self.values)
        val_str = "["
        for i in self.values[:5]:
            val_str += str(i) + ", "
        val_str += "...]"
        return 'Column(title={}, values={})'.format(self.col_title, val_str)
    def __str__(self):
        """
        Returns the ``Column`` as a string.

        :return:    The ``Column`` as a string.
        :rtype:     ``str``

        Usage::

            >>> import EzPyZ as ez
            >>> col = ez.column.Column("height_cm", [134, 168, 149, 201, 177, 168])
            >>> print(col)
            height_cm
            134
            168
            149
            201
            177
            168

        """
        out_str = self.col_title + "\n"
        for i in self.values:
            out_str += str(i) + "\n"
        return out_str[:-1]

    # ~~~~~ Public methods ~~~~~
    def get_values(self):
        """
        Returns ``self.values``.

        :return:    The values in the column.
        :rtype:     ``List[Any]``

        Usage::

            >>> import EzPyZ as ez
            >>> col = ez.column.Column("height_cm", [134, 168, 149, 201, 177, 168])
            >>> print(col.get_values())
            [134, 168, 149, 201, 177, 168]

        """
        return self.values
    def length(self):
        """
        Returns the length of ``self.values``.

        :return:    The number of values in the column.
        :rtype:     ``int``

        Usage::

            >>> import EzPyZ as ez
            >>> col = ez.column.Column("height_cm", [134, 168, 149, 201, 177, 168])
            >>> print(col.length())
            6

        """
        return len(self.values)
    def mean(self):
        """
        Returns the mean of ``self.values``.

        :return:    The mean of the values in the column.
        :rtype:     ``float``

        Usage::

            >>> import EzPyZ as ez
            >>> col = ez.column.Column("height_cm", [134, 168, 149, 201, 177, 168])
            >>> print(col.mean())
            166.16666666666666

        """
        vals = []
        for i in self.values:
            if type(i) not in (int, float, type(None)):
                raise TypeError("expected values in column "
                                + self.title() +
                                " to be str, float, or NoneType, got "
                                + type(i).__name__
                )
            elif type(i) is not None and not isnan(i):
                vals.append(i)
        return st.mean(vals)
    def median(self):
        """
        Returns the median of ``self.values``.

        :return:    The median of the values in the column.
        :rtype:     ``float``

        Usage::

            >>> import EzPyZ as ez
            >>> col = ez.column.Column("height_cm", [134, 168, 149, 201, 177, 168])
            >>> print(col.median())
            168.0

        """
        vals = []
        for i in self.values:
            if type(i) not in (int, float, type(None)):
                raise TypeError("expected values in column "
                                + self.title() +
                                " to be str, float, or NoneType, got "
                                + type(i).__name__
                )
            elif type(i) is not None and not isnan(i):
                vals.append(i)
        return st.median(self.values)
    def mode(self):
        """
        Returns the mode of ``self.values``.

        :return:    The mode of the values in ``Column``.
        :rtype:     ``float``

        Usage::

            >>> import EzPyZ as ez
            >>> col = ez.column.Column("height_cm", [134, 168, 149, 201, 177, 168])
            >>> print(col.mode())
            168

        """
        vals = []
        for i in self.values:
            if type(i) not in (int, float, type(None)):
                raise TypeError("expected values in column "
                                + self.title() +
                                " to be str, float, or NoneType, got "
                                + type(i).__name__
                )
            elif type(i) is not None and not isnan(i):
                vals.append(i)
        return st.mode(self.values)
    def stdev(self):
        """
        Returns the standard deviation of ``self.values``.

        :return:    The standard deviation of the values in the column.
        :rtype:     ``float``

        Usage::

            >>> import EzPyZ as ez
            >>> col = ez.column.Column("height_cm", [134, 168, 149, 201, 177, 168])
            >>> print(col.stdev())
            23.094732444145496

        """
        vals = []
        for i in self.values:
            if type(i) not in (int, float, type(None)):
                raise TypeError("expected values in column "
                                + self.title() +
                                " to be str, float, or NoneType, got "
                                + type(i).__name__
                )
            elif type(i) is not None and not isnan(i):
                vals.append(i)
        return st.stdev(vals)
    def set_values(self, values):
        """
        Sets ``self.values``.

        :param values:  A list containing the values in the column, in order.
        :type values:   ``List[Any]``
        :return:        Nothing.
        :rtype:         ``NoneType``
        """
        if type(values) is not list:
            # ``values`` is of an invalid type.
            raise TypeError(
                "expected ``values`` to be of type List[Any], got "
                + type(values).__name__
            )
        self.values = values
    def title(self):
        """
        Returns ``self.col_title``

        :return:    The title of the column.
        :rtype:     ``str``

        Usage::

            >>> import EzPyZ as ez
            >>> col = ez.column.Column("height_cm", [134, 168, 149, 201, 177, 168])
            >>> print(col.title())
            height_cm

        """
        return self.col_title
    def variance(self):
        """
        Returns the variance of ``self.values``.

        :return:    The variance of the values in the column.
        :rtype:     ``float``

        Usage::

            >>> import EzPyZ as ez
            >>> col = ez.column.Column("height_cm", [134, 168, 149, 201, 177, 168])
            >>> print(col.variance())
            533.3666666666667

        """
        vals = []
        for i in self.values:
            if type(i) not in (int, float, type(None)):
                raise TypeError("expected values in column "
                                + self.title() +
                                " to be str, float, or NoneType, got "
                                + type(i).__name__
                )
            elif type(i) is not None and not isnan(i):
                vals.append(i)
        return st.variance(vals)