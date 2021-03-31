# pymedeas models

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
     python run.py -x bau -f 2050 -p
    ```
4. By default world model will be run, you can use *-m* option to select another model:

    ```console
     python run.py -m europe -x bau -f 2050 -p
    ```
    or

    ```console
     python run.py -m austria -x bau -f 2050 -p
    ```
NOTE: to see all user options and default parameter values, run:

```console
  python run.py -h
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

### Model outputs

Simulation results (csv file) can be found either in the pymedeas_w the pymedeas_eu or the pymedeas_at folder.

Unless the user provides the desired output file name with the -n option when launching the simulation (e.g. python run.py -n results_my_scenario), the default results naming convention is the following:

results_SCENARIO-NAME_INITIAL-DATE_FINAL-DATE_TIME-STEP.csv

If a results file with the same name already exists, the characters "_old" will be added at the end of the file name. This can happen up to two times. NOTE that if a fourth simulation with the same name is run, the file of the first simulation result will be automatically deleted.



### Python IDE of choice (PyCharm Community Edition)

If you would like to use a graphical IDE instead of the command line, we recommend you to download **Pycharm Community edition**, which is free and open source. You cand download it for [Windows](https://www.jetbrains.com/pycharm/download/#section=windows), [Linux](https://www.jetbrains.com/pycharm/download/#section=linux) or [macOS](https://www.jetbrains.com/pycharm/download/#section=mac).

After installation, follow these steps to get the model working:

1. Open the folder where you downloaded the model: go to File\Open and select the model folder

2. Make Pycharm use the virtual environment that you created for the current project (if it doesn't already):
 * Go to *File\Settings* (PyCharm\Preferences in macOS) and start typing **project interpreter**.
 * If the environment you created appears in the drop-down list you can skip the next step.
 * If the environment does not show up, you need to tell Pycharm where to find it. Click on the sprocket wheel icon, in the top right corner and click on **Add**. This will open a new window, where you should check the option **Existing environment**, and select the path where your environment was stored:
      * You can get the path to your pymedeas environment by running the following command in a terminal:

        ```console
        conda env list
        ```
      * on Windows it should be something like *C:\Users\user_name\Anaconda\pymedeas*
      * on MacOS: */Users/user_name/Anaconda\pymedeas*
      * on Linux: */home/user_name/Anaconda\pymedeas*
 * Click *Ok* and *Apply*


3. In the main menu, click on *Run/Edit* configurations
  * Click on the plus sign on the top left corner and choose Python
  * Fill in the boxes as follows:
     * *Name*: Run model
     * *Script* path: select the run.py file from the project folder
     * *Parameters* : -s -t 0.03125 -r 1.0 -x bau -p
     * *Python Interpreter*: select the one you added in step 2 from the drop-down menu
  * Click Ok


4. On the top right corner of the screen you should now see a play icon beside the words **Run model**, click on it to run the simulation.

If you would like to be able to run the **plot GUI** to plot results of previous simulations in PyCharm, repeat step 3 changing the parameters to:

   * *Name*: Plot
   * *Script path*: select the plot_tool.py file from the project folder
   * *Parameters* : (leave blank)
   * *Python Interpreter*: select the one you added in step 2 from the drop-down menu