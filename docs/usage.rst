Usage
=====

.. _running a simulation:

Running a simulation
--------------------

The models can be run from command line.

1. Open a terminal or Anaconda Prompt Powershell, navigate to the project folder, and activate the conda environment (see :doc:`using the terminal or Anaconda Prompt Powershell <../navigating>` for more information).


2. At this point, you should be able to run a default simulation calling the `run.py` file with python:

.. code-block:: console

    (pymedeas) user@host:~/pymedeas2$ python run.py


3. By default the World model will run, but you can use the *-m* option to select a nested model, e.g.:

.. code-block:: console

    (pymedeas) user@host:~/pymedeas2$ python run.py -m pymedeas_eu


.. note::
    To see all user options and default parameter values, run the help flag, e.g.:

    .. code-block:: console

        (pymedeas) user@host:~/pymedeas2$ python run.py --help

    You can add for example modify the final time, the time step, variable values or the output file name, between others.

4. After finishing you can continue launching more simulations, `plotting simulation results`_, or deactivate your environment or directly close the terminal or Anaconda Powershell Prompt:


Model outputs
-------------

Simulation results (csv file) can be found either in the respective folder inside the *outputs* folder.

Unless the user provides the desired output file name with the -n option when launching the simulation (e.g. python run.py -n results_my_scenario), the default results naming convention is the following:

*results_SCENARIO-NAME_INITIAL-DATE_FINAL-DATE_TIME-STEP.csv*

If a results file with the same name already exists, the suffix "_old" will be added at the end of the file name. This can happen up to two times. NOTE that if a fourth simulation with the same name is run, the file of the first simulation result will be automatically deleted.


.. _plotting simulation results:

Plotting simulation results
---------------------------

1. Open a terminal or Anaconda Prompt Powershell, navigate to the project folder, and activate the conda environment (see :doc:`using the terminal or Anaconda Prompt Powershell <../navigating>` for more information).


2. Call the `plot_tool.py` file with python:

.. code-block:: console

    (pymedeas) user@host:~/pymedeas2$ python plot_tool.py


3. Simulation results can be found either in the respective folder inside the *outputs* folder. You can load an unlimited number of results files, to compare several simulation results.


