# temporary_name models
[![coverage report](https://gitlab.com/gencat_creaf/pymedeas2/badges/master/coverage.svg)](https://gitlab.com/gencat_creaf/pymedeas2/-/commits/master)

The models in this repository are loaded and run using the [PySD](https://github.com/JamesPHoughton/pysd) library.


Please note that the three models are nested, hence **to run *pymedeas_cat* the two parent models (*pymedeas_w* and *temporary_name_eu*) need to be run first**. Child models will request the results file/s from the parents at runtime.


### Installation instructions for (Windows/Linux/MacOS) using venv

0. Clone or download this repository to your computer.

1. If not installed yet, [download and install Python](https://www.python.org/downloads/) on your computer.

2. Open a terminal (Command Prompt on Windows, Terminal on MacOS/Linux) and navigate to the project folder.

3. Create a virtual environment using Python's `venv` module with the following command:

   - On Windows:
     ```
     python -m venv myenv
     ```

   - On MacOS/Linux:
     ```
     python3 -m venv myenv
     ```

4. Activate the virtual environment:

   - On Windows:
     ```
     myenv\Scripts\activate
     ```

   - On MacOS/Linux:
     ```
     source myenv/bin/activate
     ```

5. Install the required dependencies from the `requirements.txt` file using pip:
    ```
    pip install -r requirements.txt
    ```

6. Now move on to the *Running a simulation from terminal* section of this document to run your first simulation.

### Running a simulation from terminal (Windows/Linux/MacOS)

1. Open a terminal and navigate to the project folder (using the `cd` command).

2. Activate the project virtual environment by running the appropriate command mentioned in step 4 above.

3. At this point, you should be able to run a default simulation with the following command:
    ```
    python run.py -x BAU -p
    ```

4. By default, the World model will run, but you can use the `-m` option to select another model:
    ```
    python run.py -m pymedeas_eu -x BAU -p
    ```
    or
    ```
    python run.py -m pymedeas_cat -x BAU -p
    ```

5. To see all user options and default parameter values, run:
    ```
    python run.py -h
    ```

6. After finishing, you can deactivate your environment:
    ```
    deactivate
    ```

### Using the plot GUI to plot previous simulation results from terminal (in csv format)

1. Open a terminal and go to the project folder (using the *cd* command)

2. If it's not active yet, ctivate the project virtual environment by running the appropriate command mentioned in step 4 of the *Installation instructions* section.

3. Run the following command:

    ```console
    python plot_tool.py
    ```

4. Simulation results can be found either in the pymedeas_w, the pymedeas_eu or the pymedeas_cat folders. You can load an unlimited number of results files, to compare several simulation results.

5. After finishing you can deactivate your environment:
    ```
    deactivate
    ```
### Model outputs

Simulation results (nc file) can be found either in the respective folder inside the *outputs* folder.

Unless the user provides the desired output file name with the -n option when launching the simulation (e.g. python run.py -n results_my_scenario.nc), the default results naming convention is the following:

results_SCENARIO-NAME_INITIAL-DATE_FINAL-DATE_TIME-STEP.nc

If a results file with the same name already exists, the characters "_old" will be added at the end of the file name. This can happen up to two times. NOTE that if a fourth simulation with the same name is run, the file of the first simulation result will be automatically deleted.