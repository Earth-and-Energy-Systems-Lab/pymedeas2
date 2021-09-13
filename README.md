# pymedeas models

[![coverage report](https://gitlab.com/gencat_creaf/pymedeas2/badges/master/coverage.svg)](https://gitlab.com/gencat_creaf/pymedeas2/-/commits/master) 

This is the official repo for the models of the European MEDEAS project (www.medeas.eu). Please register to the mailing list in order to receive the most recent news about the project.

The available models are the result of translating the original MEDEAS Vensim models into Python using [PySD](https://github.com/JamesPHoughton/pysd) library. This same library is used to load and run the simulations.

Currently, pymedeas models for World (*pymedeas_w*), EU28 (*pymedeas_eu*) and Austria (*pymedeas_aut*) are available.

Please note that **to run *pymedeas_eu* you will need to import the values of some variables from the results of a simulation run with *pymedeas_w***.

For running *pymedeas_aut*, in addition to the results of *pymedeas_w*, the results of *pymedeas_eu* also have to be loaded.

When executing either the *pymedeas_eu* or *pymedeas_aut* models, you will be prompted with a file explorer to select the results files (in csv) of the other models.

Python 3.7 is required to run the code.

### Installation instructions for (Windows/Linux/MacOS) using conda

0. Clone or download the repo in your computer

1. If not installed yet, [download and install Miniconda or Anaconda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) on your computer.

2. Open a new terminal and create a conda environement for pymedeas using the *yml* file, this will install all the needed dependencies:
    ```
    conda env create -f environment.yml
    ```
3. Congratulations, you can move to the next step! Go to *Running a simulation from terminal* section of this document to verify that everything went well during the previous steps, and to try to run the model.

NOTE: If you already had Anaconda installed on your Mac and then upgraded the OS to Catalina, If you are running MacOS Catalina, make sure your read [this](https://www.anaconda.com/how-to-restore-anaconda-after-macos-catalina-update/)
### Running a simulation from terminal (Windows/Linux/MacOS)

1. Open a terminal and go to the project folder (using the *cd* command)

2. Activate the project virtual environment running the following command:
    ```console
    conda activate pymedeas
    ```

3. At this point, you should be able to run a default simulation with the following command:

    ```console
    python run.py -x BAU -p
    ```
4. By default world model will be run, you can use *-m* option to select another model:

    ```console
    python run.py -m pymedeas_eu -x BAU -p
    ```
    or

    ```console
    python run.py -m pymedeas_aut -x BAU -p
    ```
NOTE: to see all user options and default parameter values, run:

```console
python run.py -h
```
5. After finishing you can deactivate your environment:
    ```console
    conda deactivate
    ```
### Using the plot GUI to plot previous simulation results from terminal (in csv format)

1. Open a terminal and go to the project folder (using the *cd* command)

2. If it's not active yet, activate the project virtual environment running the following command:
    ```console
    conda activate pymedeas
    ```

3. Run the following command:

    ```console
    python plot_tool.py
    ```

4. Simulation results (csv file) can be found either in the pymedeas_w the pymedeas_eu or the pymedeas_at folder. You can load an unlimited number of results files, to compare several simulation results.

5. After finishing you can deactivate your environment:
    ```console
    conda deactivate
    ```
### Model outputs

Simulation results (csv file) can be found either in the respective folder inside the *outputs* folder.

Unless the user provides the desired output file name with the -n option when launching the simulation (e.g. python run.py -n results_my_scenario), the default results naming convention is the following:

results_SCENARIO-NAME_INITIAL-DATE_FINAL-DATE_TIME-STEP.csv

If a results file with the same name already exists, the characters "_old" will be added at the end of the file name. This can happen up to two times. NOTE that if a fourth simulation with the same name is run, the file of the first simulation result will be automatically deleted.
