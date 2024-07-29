
# Table of contents
- [Table of contents](#table-of-contents)
- [pymedeas2](#pymedeas2)
- [1. Installing and running the models:](#1-installing-and-running-the-models)
  - [1.1 Instructions for running the code with Python (Windows/Linux/MacOS)](#11-instructions-for-running-the-code-with-python-windowslinuxmacos)
  - [Running a simulation from terminal (Windows/Linux/MacOS)](#running-a-simulation-from-terminal-windowslinuxmacos)
  - [2. Instructions for running the code in a Docker container](#2-instructions-for-running-the-code-in-a-docker-container)
- [Model outputs](#model-outputs)
    - [Using the plot GUI to plot simulation results](#using-the-plot-gui-to-plot-simulation-results)
    - [Acknowledgements](#acknowledgements)

# pymedeas2

This repository holds the code for the pymedeas2 models, which are the latest iteration of the original pymedeas models, which were the main output of the H2020 MEDEAS project (2016-2019).

The models are available at **3 regional levels (world, region, country)**, and are currently parametrized for World, EU27 and Catalonia.


A default normative decarbonization scenario, called NZP (Net Zero Pathway) is available for each of the three regional levels.


Please note that the three models are nested, hence **to run *pymedeas_cat* the two parent models (*pymedeas_w* and *pymedeas_eu*) need to be run first (and in that same order)**. Child models will request the results file/s from the parents at runtime (unless they are passed with the -f argument using the CLI).


# 1. Installing and running the models:
First clone or download this repository on your computer. Then, there are two ways to run the code, each requiring different procedures:
  1. With the Python of your system (requires that you install python and all project dependencies): see [instructions here](#11-instructions-for-running-the-code-with-python-windowslinuxmacos)
  2. In a docker container (requires that you have Docker installed on your machine): see [instructions here](#2-instructions-for-running-the-code-in-a-docker-container)


## 1.1 Instructions for running the code with Python (Windows/Linux/MacOS)


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

## Running a simulation from terminal (Windows/Linux/MacOS)

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


## 2. Instructions for running the code in a Docker container

1. Install Docker on your system.
2. Get to the project folder (you should see the `Dockerfile` in it) and build the Docker image with:

```bash
docker build -t pymedeas2 .
```

Now you are ready to run a simulation. However, before that, let's see the different configuration options we can change:

```bash
docker run pymedeas2 -h
```

Now, to run a default simulation with the world model, just run:

```bash
docker run pymedeas2
```

Finally, to run a simulation with another model (say, the EU model), run:

```bash
docker run pymedeas2 -m pymedeas_eu
```

# Model outputs

Simulation results (nc file) for each model can be found in the respective folder inside the *outputs* directory.

Unless the user provides the desired output file name with the -n option when launching the simulation (e.g. python run.py -n results_my_scenario.nc), the default results naming convention is the following:

results_SCENARIO-NAME_INITIAL-DATE_FINAL-DATE_TIME-STEP.nc

If a results file with the same name already exists, the characters "_old" will be added at the end of the file name. This can happen up to two times. NOTE that if a fourth simulation with the same name is run, the file of the first simulation result will be automatically deleted.


### Using the plot GUI to plot simulation results

Clone or download the code for the plot tool [from this repository](https://github.com/Earth-and-Energy-Systems-Lab/pymedeas_plots) and follow the instructions given in the README.

### Acknowledgements
The development of the pymedeas models was supported by the European Union through the funding of the MEDEAS project under the Horizon 2020 research and innovation programme (grant agreement No 69128), and by the Government of Catalonia through the contract programme between the Ministries of Territory and Sustainability and Business and Labour and the Centre for Research on Ecology and Forestry Applications (CREAF), approved by Government Agreement on March 16, 2021.