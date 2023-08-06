"""
result.py
~~~~~~~~~
This module provides a ``EzPyZ.Result`` object which contains the results of any test conducted.
"""

class Result:
    """
    A ``Result`` object. A ``Result`` object will be returned when any test is conducted. This class
    is NOT intended for exernal use!
    """
    def __init__(self, category, data):
        """
        Initializes the ``Result`` object.

        :param type:        String. The type of test conducted.
        :type category:     ``str``
        :param category:    Dictionary. The data from the conducted test.
        :type data:         ``Dict[str, Any]``
        :return:            Nothing.
        :rtype:             ``NoneType``
        """
        # Validate input.
        valid = [
            "t-test"
        ]
        if category not in valid:
            raise ValueError(category + " is not a valid category.")
        

    def t_test_result(self, data):
        """
        Parses results for a t-test and stores them in the object.

        :param data:    The data from the conducted t-test.
        :type data:     ``Dict[str, Any]``
        :return:        Nothing.
        :rtype:         ``NoneType``
        """
        pass
