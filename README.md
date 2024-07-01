# pymedeas2
[![coverage report](https://gitlab.com/gencat_creaf/pymedeas2/badges/master/coverage.svg)](https://gitlab.com/gencat_creaf/pymedeas2/-/commits/master)

This repository holds the code for the pymedeas2 models, which are the latest iteration of the original pymedeas models, which were the main output of the H2020 MEDEAS project (2016-2019).

The models are available at **3 regional levels (world, region, country)**, and are currently parametrized for World, EU27 and Catalonia.


A default normative decarbonization scenario, called NZP (Net Zero Pathway) is available for each of the three regional levels.


Please note that the three models are nested, hence **to run *pymedeas_cat* the two parent models (*pymedeas_w* and *pymedeas_eu*) need to be run first (and in that same order)**. Child models will request the results file/s from the parents at runtime (unless they are passed with the -f argument using the CLI).


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
    python run.py
    ```

4. By default, the World model will run under the NZP (Net Zero Pathway) scenario, but you can use the `-m` option to select another model, and the `-x` to use a scenario of your own:
    ```
    python run.py -m pymedeas_eu
    ```
    or
    ```
    python run.py -m pymedeas_cat -x MY_SCENARIO
    ```

5. To see all user options and default parameter values, run:
    ```
    python run.py -h
    ```

6. After finishing, you can deactivate your environment:
    ```
    deactivate
    ```

### Model outputs

Simulation results (nc file) for each model can be found in the respective folder inside the *outputs* directory.

Unless the user provides the desired output file name with the -n option when launching the simulation (e.g. python run.py -n results_my_scenario.nc), the default results naming convention is the following:

results_SCENARIO-NAME_INITIAL-DATE_FINAL-DATE_TIME-STEP.nc

If a results file with the same name already exists, the characters "_old" will be added at the end of the file name. This can happen up to two times. NOTE that if a fourth simulation with the same name is run, the file of the first simulation result will be automatically deleted.


### Using the plot GUI to plot simulation results

Clone or download the code for the plot tool [from this repository](https://github.com/Earth-and-Energy-Systems-Lab/pymedeas_plots) and follow the instructions given in the README.


### Contributions are welcome
We welcome any contributions from the community. In particular