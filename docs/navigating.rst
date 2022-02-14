Using the terminal or Anaconda Prompt Powershell
================================================

In order to install, run the models, and plot the results a command-line interface (CLI) is used. For Linux and MacOS user the Terminal is recommended, while for Windows used the Anaconda Prompt Powershell is recommended (installed together with miniconda or Anaconda).

Navigate to the project folder
------------------------------
You can navigate in the terminal (Linux/MacOS) or Anaconda Powershell Prompt (Windows) using the *cd* command, example in Linux terminal:

.. code-block::

    (base) user@host:~$ cd pymedeas2
    (base) user@host:~/pymedeas2$


or in Anaconda Powershell:

.. code-block::

    (base) PS C:\Users\user> cd pymedeas2
    (base) PS C:\Users\user\pymedeas2>


.. note::
    The current path position is shown in the left side of the command line. If you need to to show the files and folder inside the current position you can use ``ls`` command:

    .. code-block:: console

        (base) user@host:~/pymedeas2$ ls


You need to know where exactly you have downloaded the models directory, and navigate until there. You can use ``cd ..`` to go one folder back.


Activating and deactivating conda environment
---------------------------------------------
Once the conda environment has been installed, you can `activate the conda environment <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment>`_ from any position in the terminal or Anaconda Powershell Prompt, e.g.:

.. code-block:: console

    (base) user@host:~/pymedeas2$ conda activate pymedeas
    (pymedeas) user@host:~/pymedeas2$


.. note::
    When activated you will see that the *(base)* on the left-hand side has become a *(pymedeas)*.

Once finish working, if you want to continue using the CLI you can `deactivate the conda environment <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#deactivating-an-environment>`_, e.g.:

.. code-block:: console

    (pymedeas) user@host:~/pymedeas2$ conda deactivate
    (base) user@host:~/pymedeas2$


Otherwise you can directly close the terminal or Anaconda Powershell Prompt.