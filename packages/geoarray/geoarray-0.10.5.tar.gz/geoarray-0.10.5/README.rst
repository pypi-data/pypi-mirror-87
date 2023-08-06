========
geoarray
========


Fast Python interface for geodata - either on disk or in memory.

The geoarray package facilitates reading and writing of all GDAL compatible image file formats
and provides functions for geospatial processing.


* Free software: GNU General Public License v3 or later (GPLv3+)
* Documentation: https://danschef.gitext-pages.gfz-potsdam.de/geoarray/doc/


Status
------

.. .. image:: https://img.shields.io/travis/danschef/geoarray.svg
        :target: https://travis-ci.org/danschef/geoarray

.. .. image:: https://readthedocs.org/projects/geoarray/badge/?version=latest
        :target: https://geoarray.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. .. image:: https://pyup.io/repos/github/danschef/geoarray/shield.svg
     :target: https://pyup.io/repos/github/danschef/geoarray/
     :alt: Updates

.. image:: https://gitext.gfz-potsdam.de/danschef/geoarray/badges/master/pipeline.svg
        :target: https://gitext.gfz-potsdam.de/danschef/geoarray/commits/master
.. image:: https://gitext.gfz-potsdam.de/danschef/geoarray/badges/master/coverage.svg
        :target: https://danschef.gitext-pages.gfz-potsdam.de/geoarray/coverage/
.. image:: https://img.shields.io/pypi/v/geoarray.svg
        :target: https://pypi.python.org/pypi/geoarray
.. image:: https://img.shields.io/conda/vn/conda-forge/geoarray.svg
        :target: https://anaconda.org/conda-forge/geoarray
.. image:: https://img.shields.io/pypi/l/geoarray.svg
        :target: https://gitext.gfz-potsdam.de/danschef/geoarray/blob/master/LICENSE
.. image:: https://img.shields.io/pypi/pyversions/geoarray.svg
        :target: https://img.shields.io/pypi/pyversions/geoarray.svg
.. image:: https://img.shields.io/pypi/dm/geoarray.svg
        :target: https://pypi.python.org/pypi/geoarray


See also the latest coverage_ report and the nosetests_ HTML report.


Features and usage
------------------

* There is an example notebook that shows how to use geoarray: here_.


Installation
------------

Using Anaconda or Miniconda (recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using conda_ (latest version recommended), geoarray is installed as follows:


1. Create virtual environment for geoarray (optional but recommended):

   .. code-block:: bash

    $ conda create -c conda-forge --name geoarray python=3
    $ conda activate geoarray


2. Then install geoarray itself:

   .. code-block:: bash

    $ conda install -c conda-forge geoarray


This is the preferred method to install geoarray, as it always installs the most recent stable release and
automatically resolves all the dependencies.


Using pip (not recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is also a `pip`_ installer for geoarray. However, please note that geoarray depends on some
open source packages that may cause problems when installed with pip. Therefore, we strongly recommend
to resolve the following dependencies before the pip installer is run:

    * cartopy
    * gdal >=2.1.0
    * geopandas
    * holoviews  # optional, in case you want to use interactive plotting
    * matplotlib
    * numpy
    * pandas
    * pyproj >2.2.0
    * scikit-image
    * shapely

Then, the pip installer can be run by:

   .. code-block:: bash

    $ pip install geoarray

If you don't have `pip`_ installed, this `Python installation guide`_ can guide you through the process.


History / Changelog
-------------------

You can find the protocol of recent changes in the geoarray package
`here <https://gitext.gfz-potsdam.de/danschef/geoarray/-/blob/master/HISTORY.rst>`__.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _coverage: https://danschef.gitext-pages.gfz-potsdam.de/geoarray/coverage/
.. _nosetests: https://danschef.gitext-pages.gfz-potsdam.de/geoarray/nosetests_reports/nosetests.html
.. _conda: https://conda.io/docs/
.. _here: examples/notebooks/features_and_usage.ipynb
.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
