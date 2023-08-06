.. |travis status| image:: https://img.shields.io/travis/com/EGuthrieWasTaken/EzPyZ/main
.. |pypi version| image:: https://img.shields.io/pypi/v/EzPyZ
.. |license| image:: https://img.shields.io/pypi/l/EzPyZ
.. |pypi status| image:: https://img.shields.io/pypi/status/EzPyZ

.. |code size| image:: https://img.shields.io/github/languages/code-size/EGuthrieWasTaken/EzPyZ
.. |downloads| image:: https://img.shields.io/pypi/dw/EzPyZ
.. |python versions| image:: https://img.shields.io/pypi/pyversions/EzPyZ
.. |pypi format| image:: https://img.shields.io/pypi/format/EzPyZ

.. |readthedocs status| image:: https://readthedocs.org/projects/ezpyz/badge/?version=latest

============================================================
EzPyZ |travis status| |pypi version| |license| |pypi status|
============================================================
Welcome to EzPyZ! This project seeks to provide an easy-to-use statistical library for Python 3. This project was inspired in concept by the `ez <https://github.com/mike-lawrence/ez>`_ library available in R.

**This project is under development, and will likely not work as intended. You have been warned.**

--------------------------------------------------------------------
Installation |code size| |downloads| |python versions| |pypi format|
--------------------------------------------------------------------
This package is installed using pip. Pip should come pre-installed with all versions of Python for which this package is compatible. Nonetheless, if you wish to install pip, you can do so by downloading `get-pip.py <https://pip.pypa.io/en/stable/installing/>`_ and running that python file (Windows/MacOS/Linux/BSD), or you can run the following command in terminal (Linux/BSD):

.. code:: bash

    sudo apt install python3-pip

If you're using brew (most likely for MacOS), you can install pip (along with the rest of Python 3) using brew:

.. code:: bash

    brew install python3

**Note: The creator of this software does not recommend the installation of python or pip using brew, and instead recommends that Python 3.7+ be installed using the installation candidates found on** `python.org <https://www.python.org/downloads/)>`_, **which include pip by default.**

Using Pip to install from PyPi
==============================
Fetching this repository from PyPi is the recommended way to install this package. From your terminal, run the following command:

.. code:: bash

    pip3 install EzPyZ

And that's it! Now you can go right ahead to the quick-start guide!

Install from Source
===================

Not a big fan of pip? Well, you're weird, but weird is OK! I've written a separate script to help make installation from source as easy as possible. To start, download the installation script and run it:

.. code:: bash

    wget https://raw.githubusercontent.com/EGuthrieWasTaken/EzPyZ/main/source_install.py
    python3 source_install.py

After completing, the script will have downloaded the latest tarball release and extracted it into the working directory. Now, all you have to do is switch into the newly-extracted directory and run the install command:

.. code:: bash

    cd EGuthrieWasTaken-EzPyZ-[commit_id]/
    python3 setup.py install

Congratulations, you just installed EzPyZ from source! Feel free to check out the quick-start guide!

-----------------
Quick-Start Guide
-----------------

Now that you have the package installed, getting started with the package should be easy! You can start with importing the package and creating a ``DataFrame``:

.. code:: python3

    import EzPyZ as ez

    # Create new dataframe.
    raw_data = {
        'height (cm)': [134, 168, 149, 201, 177],
        'weight (kg)': [32.2, 64.3, 59.9, 95.4, 104.2]
    }
    df = ez.DataFrame(data=raw_data)

Already have a ``pandas.DataFrame`` object? Great! You can create an ``EzPyZ.DataFrame`` object with an existing ``pandas.DataFrame``:

.. code:: python3

    import EzPyZ as ez
    import pandas as pd

    # Create new dataframe.
    raw_data = {
        'height (cm)': [134, 168, 149, 201, 177],
        'weight (kg)': [32.2, 64.3, 59.9, 95.4, 104.2]
    }
    pandas_df = pd.DataFrame(raw_data)
    df = ez.DataFrame(data=pandas_df)

Of course, most of the time you will not be hard-coding your data directly. Fortunately this package comes with tools to help with that as well! Check it out:

.. code:: python3

    import EzPyZ as ez
    from EzPyZ.tools import read_file

    df = ez.DataFrame(data=read_file("bmi_data.csv")) # A bmi_data.xlsx would also work here.

That should be enough to get you off the ground! To learn more, check out the documentation.

----------------------------------
Documentation |readthedocs status|
----------------------------------
Documentation for this project can be found on `Read the Docs <https://ezpyz.readthedocs.io/en/latest>`_. Otherwise, feel free to browse the source code within the repository! It is (hopefully) well-documented...
