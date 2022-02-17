Welcome pymedeas2 models documentation!
=======================================

|made-with-sphinx-doc|
|docs|
|pipeline|
|coverage|

.. |made-with-sphinx-doc| image:: https://img.shields.io/badge/Made%20with-Sphinx-1f425f.svg
   :target: https://www.sphinx-doc.org/

.. |docs| image:: https://readthedocs.org/projects/pymedeas2/badge/?version=latest
   :target: https://pymedeas2.readthedocs.io/en/latest/?badge=latest

.. |pipeline| image:: https://gitlab.com/gencat_creaf/pymedeas2/badges/master/pipeline.svg
   :target: https://gitlab.com/gencat_creaf/pymedeas2/

.. |coverage| image:: https://gitlab.com/gencat_creaf/pymedeas2/badges/master/coverage.svg
   :target: https://gitlab.com/gencat_creaf/pymedeas2/




The models in this repository are loaded and run using `PySD <https://github.com/JamesPHoughton/pysd>`_ library.

Currently, *pymedeas2* models for World (*pymedeas2_w*), EU28 (*pymedeas2_eu*) and Catalonia (*pymedeas2_cat*) are available.

Please note that the three models are nested, hence **to run *pymedeas2_cat* the two parent models (*pymedeas2_w* and *pymedeas2_eu*) need to be run first**. Child models will request the results file/s from the parents at runtime.

For contributions see :doc:`development <development/development_index>`.

Requirements
------------
* Python 3.7+
* PySD 2.2.0+
* matplotlib
* dacite

Contents
--------

.. toctree::
   :maxdepth: 2

   installation
   usage
   development/development_index
   navigating
