# temporary_name models
[![coverage report](https://gitlab.com/gencat_creaf/pymedeas2/badges/master/coverage.svg)](https://gitlab.com/gencat_creaf/pymedeas2/-/commits/master)

The models in this repository are loaded and run using the [PySD](https://github.com/JamesPHoughton/pysd) library.

Currently, *temporary_name* models for World (*temporary_name_w*), EU28 (*temporary_name_eu*) and Catalonia (*temporary_name_cat*) are available.

Please note that the three models are nested, hence **to run *temporary_name_cat* the two parent models (*temporary_name_w* and *temporary_name_eu*) need to be run first**. Child models will request the results file/s from the parents at runtime.


Python >= 3.7 is required to run the code (Python 3.11 is recommended).

### Installation instructions using venv

0. Clone or download this repository in your computer

1. Open a terminal and create a conda environement with the following command:
    ```console
    python -m venv pymedeas2
    ```
2. Activate the virtual environment:
    - On windows:
    ```console
    pymedeas2\Scripts\activate
    ```
    - On Linux and Mac:
    ```console
    source pymedeas2/bin/activate
    ```
3. Install dependencies from the *requirements.txt* file:
    ```console
    pip install -r requirements.txt
    ```

4. Now move to *Running a simulation from terminal* section of this document to run your first simulation.

NOTE: to leave the virtual environment run:
    ```console
    deactivate
    ```

### Running a simulation from terminal (Windows/Linux/MacOS)

1. Open a terminal and go to the project folder (using the *cd* command)

2. Activate the project virtual environment as in step 2 of the previous section.

3. At this point, you should be able to run a default simulation with the following command:

    ```console
    python run.py -x NZP -p
    ```
4. By default the World model will run, but you can use the *-m* option to select another model:

    ```console
    python run.py -m pymedeas_eu -x NZP -p
    ```
    or

    ```console
    python run.py -m pymedeas_cat -x NZP -p
    ```
NOTE: to see all user options and default parameter values, run:

```console
python run.py -h
```
5. After finishing you can deactivate your environment:
    ```console
    deactivate
    ```
### Using the plot GUI to plot previous simulation results from terminal (in csv format)

1. Open a terminal and go to the project folder (using the *cd* command)

2. If it's not active yet, activate the project virtual environment as previously shown.

3. Run the following command:

    ```console
    python plot_tool.py
    ```

4. Simulation results can be found either in the pymedeas_w the pymedeas_eu or the pymedeas_at folder. You can load an unlimited number of results files, to compare several simulation results.


### Model outputs

Simulation results can be found either in the respective folder inside the *outputs* folder.

Unless the user provides the desired output file name with the -n option when launching the simulation (e.g. python run.py -n results_my_scenario), the default results naming convention is the following:

results_SCENARIO-NAME_INITIAL-DATE_FINAL-DATE_TIME-STEP.nc

If a results file with the same name already exists, the characters "_old" will be added at the end of the file name. This can happen up to two times. NOTE that if a fourth simulation with the same name is run, the file of the first simulation result will be automatically deleted.

### Exporting results stored in netCDF (.nc) format to csv (or tab)

Unless specified through the CLI, results are stored in netCDF format (.nc extension).


To export the results to csv or tab format, open the jupyter notebook named `deserialize_simulation_results.ipynb` in the pytools folder and follow the instructions.

To open the jupyter notebook run:
```console
jupyter notebook
```