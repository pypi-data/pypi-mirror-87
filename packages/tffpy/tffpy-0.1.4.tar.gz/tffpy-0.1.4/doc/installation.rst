Installation
############

``tffpy`` requires the following packages, which will be automatically
installed with ``tffpy`` using ``pip``:

* `python >= 3.6 <https://wiki.python.org/moin/BeginnersGuide/Download>`_
* `numpy >= 1.13 <http://www.numpy.org>`_
* `scipy <https://www.scipy.org/>`_
* `matplotlib <https://matplotlib.org/>`_
* `pandas <https://pandas.pydata.org/>`_
* `xarray <https://xarray.pydata.org/>`_
* `ltfatpy <http://dev.pages.lis-lab.fr/ltfatpy/>`_
* `skpomade <http://valentin.emiya.pages.lis-lab.fr/skpomade/>`_
* `yafe <http://skmad-suite.pages.lis-lab.fr/yafe/>`_
* `madarrays <https://gitlab.lis-lab.fr/skmad-suite/madarrays>`_

Make sure your Python environment is properly configured. It is recommended to
install ``tffpy`` in a virtual environment.

Release version
---------------

First, make sure you have the latest version of pip (the Python package
manager) installed. If you do not, refer to the `Pip documentation
<https://pip.pypa.io/en/stable/installing/>`_ and install ``pip`` first.

Install the current release with ``pip``::

    pip install tffpy

To upgrade to a newer release use the ``--upgrade`` flag::

    pip install --upgrade tffpy

If you do not have permission to install software systemwide, you can install
into your user directory using the ``--user`` flag::

    pip install --user tffpy

Alternatively, you can manually download ``tffpy`` from its `GitLab project
<https://gitlab.lis-lab.fr/skmad-suite/tff2020>`_  or `PyPI
<https://pypi.python.org/pypi/tffpy>`_.  To install one of these versions,
unpack it and run the following from the top-level source directory using the
Terminal::

    pip install .

Dataset installation
--------------------
Download the data from `this link <https://gitlab.lis-lab.fr/skmad-suite/tff2020/-/archive/master/tff2020-master.zip?path=data>`_.

Then run function :py:func:`tffpy.utils.generate_config` in order to create
a configuration file and modify it to specify the path to your data folder.
The location of the configuration file is given by function
:py:func:`tffpy.utils.get_config_file`.

Development version
-------------------

If you have `Git <https://git-scm.com/>`_ installed on your system, it is also
possible to install the development version of ``tffpy``.

Before installing the development version, you may need to uninstall the
standard version of ``tffpy`` using ``pip``::

    pip uninstall tffpy

Clone the Git repository::

    git clone git@gitlab.lis-lab.fr:skmad-suite/tff2020.git
    cd python

You may also need to install required packages::

    pip install -r requirements/defaults.txt

Then execute ``pip`` with flag ``-e`` to follow the development branch::

    pip install -e .

To update ``tffpy`` at any time, in the same directory do::

    git pull

To run unitary tests, first install required packages::

    pip install -r requirements/dev.txt

and execute ``pytest``::

    pytest

