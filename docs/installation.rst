Installation
============

For installing *pymedeas2* models you need to first clone or download and unzip the `pymedeas2 repository <https://gitlab.com/gencat_creaf/pymedeas2>`_.

Installing using conda
----------------------

1. If not installed yet, `download and install Miniconda or Anaconda <https://conda.io/projects/conda/en/latest/user-guide/install/index.html>`_ on your computer.

2. Open a terminal or Anaconda Prompt Powershell and navigate to the project folder (see :doc:`using the terminal or Anaconda Prompt Powershell <../navigating>` for more information).

3. `Create a conda environement using the provided environment.yml file <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file>`_, e.g.:

.. code-block::

    (base) user@host:~/pymedeas2$ conda env create -f environment.yml


.. note::
   If you already had Anaconda installed on your Mac and then upgraded the OS to Catalina, If you are running MacOS Catalina, make sure your read `this <https://www.anaconda.com/how-to-restore-anaconda-after-macos-catalina-update/>`_


Alternative installation
------------------------
The models can be also run if the needed dependencies (found in the *environment.yml* file) are required. Alternative package manages such as *pip* can be used to install these dependencies.


Required Dependencies
---------------------
*pymedeas2* models need `PySD <https://pysd.readthedocs.io>`_ library for running. It requires at least **Python 3.7** and **PySD 3.0.0**. Moreover **matplotlib** and **dacite** are required.
