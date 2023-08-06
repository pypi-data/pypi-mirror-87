===============================
uspec-finder
===============================


.. image:: https://img.shields.io/pypi/v/uspec_finder.svg
        :target: https://pypi.python.org/pypi/uspec_finder

.. image:: https://img.shields.io/travis/StuartLittlefair/uspec_finder.svg
        :target: https://travis-ci.org/StuartLittlefair/uspec_finder

.. image:: https://readthedocs.org/projects/hcam-finder/badge/?version=latest
        :target: https://hcam-finder.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/StuartLittlefair/uspec_finder/shield.svg
     :target: https://pyup.io/repos/github/StuartLittlefair/uspec_finder/
     :alt: Updates


Observation planning and finding charts for ULTRASPEC

``uspec_finder`` provides a Python script ``usfinder`` for observation planning with
ULTRASPEC on the Thai National Telescope. It allows you to generate finding charts as
well as specify the instrument setup you require, whilst providing an estimate of
observing cadence, exposure time and S/N estimates.

``uspec_finder`` is written in Python and is based on TKinter. It should be compatible
with Python2 and Python3, but is only tested on Python3.

Installation
------------

The software is written as much as possible to make use of core Python
components. It requires my own `hcam_widgets <https://github.com/HiPERCAM/hcam_widgets>`_ module.
It also relies on the third party libraries `astropy <http://astropy.org/>`_ for astronomical
calculations and catalog lookup, as well as `ginga <https://ginga.readthedocs.io/en/latest/>`_ for
image display. Optionally, you can also use `astroquery <https://astroquery.readthedocs.io>`_ to expand
the range of surveys one can download images from.

Installing using ``pip`` should take care of these dependencies. Simply install with::

 pip install uspec_finder

or if you don't have root access::

 sudo pip install uspec_finder

or::

 pip install --user uspec_finder

* Free software: MIT license
* Documentation: https://uspec-finder.readthedocs.io.



