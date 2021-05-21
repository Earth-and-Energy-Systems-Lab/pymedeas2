#!/usr/bin/env python
__author__ = "Oleg Osychenko, Roger Samsó, Eneko Martin"
__maintainer__ = "Eneko Martin"
__status__ = "Development"

import os
import sys
import time

import re
import json
import pandas as pd
import numpy as np
import xarray as xr
import pysd

# imports to read command line
import getopt

# imports for GUI
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from pytools.logger.logger import log

# PySD imports for replaced functions
from pysd.py_backend import functions
from pysd.py_backend.utils import xrmerge


def update_paths(config):
    """
    Updates config dictionary with the paths to the model folder,
    names of the model and inputs files.

    Parameters
    ----------
    config: dict
        Configuration parameters. config['region'] must be defined.

    Returns
    -------
    None
    """
    # load configuration file
    f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                          'models.json'),)
    dict_models = json.load(f)

    if config['region'] not in dict_models:
        raise ValueError(
            "Invalid region name " + config['region']
            + "\nAvailable regions are:\n\t" + ", ".join(
                list(dict_models)))

    cwd = os.getcwd()
    model = dict_models[config['region']]
    config['model_py'] = model['model_py']
    config['folder'] = os.path.join(cwd, model['folder'])
    config['scenario_inputs'] = model['scenario inputs']
    config['historic_inputs'] = model['historic inputs']
    config['out_folder'] = os.path.join(cwd, model['out_folder'])
    config['out_default'] = model['out_default']
    config['parent'] = [
        {'name': par['name'],
         'folder': dict_models[par['name']]['out_folder'],
         'input_vars': par['input_vars']}
        for par in model['parent']]


def get_initial_user_input(config, run_params):
    """
    Ask for user input to update simulation parameters.
    Get user input and updates the config and run_params dictionaries.

    Parameters
    ----------
    config: dict
        Configuration parameters.
    run_params: dict
        Simulation parameters.

    Returns
    -------
    None
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hspbt:f:r:x:u:n:e:m:")

        for opt, arg in opts:
            if opt == '-h':
                print(
                    'Run run.py module followed by any of the following '
                    'options:\n'
                    '-h --> help menu \n'
                    '-m --> model to use\n'
                    '-f --> final year of simulation (default is 2050) \n'
                    '-t --> time step of simulation (in years) (default '
                    'is 0.03125 years) \n'
                    '-r --> time step of simulation result (in years) '
                    '(default is 1 value per year) \n'
                    '-s --> silent mode \n'
                    '-b --> headless mode  (only CLI, no GUI) \n'
                    '-p --> opens the plot gui after simulation \n'
                    '-x --> scenario name (names should be the same as '
                    'the input file tabs) \n'
                    '-n --> name of the results file (default is '
                    'results_{scenario name}_{initial date}_{final date}'
                    '_{time-step}.csv)\n'
                    '-e --> file from which to import external data (only'
                    ' applies for the EU model) \n\n'
                    'Use keyword argunemts to set model parameter values,'
                    ' or use the inputs file (e.g. eroi=5)\n'
                      )

                sys.exit()

            elif opt in ("-s", "--silent"):
                config["silent"] = True
            elif opt in ("-m", "--model", "--region"):
                config["region"] = arg
            elif opt in ("-f", "--final_time"):
                run_params["final_time"] = int(arg)
            elif opt in ("-t", "--time_step"):
                run_params["time_step"] = float(arg)
            elif opt in ("-r", "--return_timestep"):
                config["return_timestep"] = arg
            elif opt in ("-p", "--plot"):
                config["plot"] = True
            elif opt in ("-x", "--scen"):
                config["scenario_sheet"] = arg
            elif opt in ("-e", "--ext"):
                config["extDataFname"] = arg.split(",")
            elif opt in ("-n", "--fname"):
                config["fname"] = arg.split(".")[0]
            elif opt in ("-b"):
                config["headless"] = True
            else:
                pass

        for arg in args:
            par = arg.split('=')
            d = {par[0]: par[1]}
            config["update_params"].update(d)

    except getopt.GetoptError:
        log.error("Wrong parameter definition (run 'python run.py -h'"
                  + "to see the description of available parameters)")
        sys.exit()


def store_results_csv(result, config):
    """
    Stores the final results as csv.

    Parameters
    ----------
    result: pandas.DataFrame
        Output of the simulation
    config: dict
        Configuration parameters.

    Returns
    -------
    results: pandas.DataFrame
        Transposed result file.

    """
    file_path_csv = _results_naming(config, config["fname"], 'csv')

    # storing results to csv file
    result.transpose().to_csv(file_path_csv)
    log.info('Simulation results file is located in {}'.format(file_path_csv))

    with open(os.path.join(config['folder'], 'last_output_conf.txt'),
              'w') as f:
        f.write(';'.join(result.columns))

    if result.isna().any().any():
        nan_vars = result.columns[result.isna().any()].tolist()
        log.warning(
            "There are NaN's in the timeseries of the following variables\n\n:"
            + " {}\n\n, which might indicate convergence issues, try "
            + "decreasing the time step".format("\n".join(nan_vars)))

    return result


def _results_naming(config, base_name, fmt):
    """This function renames old simulation results with the same name but adding
    _old in the end, or old_old if _old also exists

    :return (str) new file path
    """

    folder = config['out_folder']

    new_path = os.path.join(folder, '{}.{}'.format(base_name, fmt))
    old_path = os.path.join(folder, '{}_old.{}'.format(base_name, fmt))
    old_old_path = os.path.join(folder, '{}_old_old.{}'.format(base_name, fmt))

    if os.path.isfile(new_path):
        if os.path.isfile(old_path):
            if os.path.isfile(old_old_path):
                os.remove(old_old_path)
                log.info('File {0}_old_old.{1} has been removed'.format(base_name, fmt))
            os.rename(old_path, old_old_path)
            log.info('File {0}_old.{1} has been moved to {0}_old_old.{1}'.format(base_name, fmt))
        os.rename(new_path, old_path)
        log.info('File {0}.{1} has been moved to {0}_old.{1}'.format(base_name, fmt))

    return new_path


def select_model_outputs(config, model):
    """
    Select model outputs. If the simulation was call using silent mode
    the outputs from the last simulation will be used. Otherwise, the user
    will be asked via terminal the outputs to include.

    Some default outputs will be always returned by the model, see the
    models.json for the list.

    Parameters
    ----------
    config: dict
        Configuration parameters.
    model: pysd.Model
        Model object.

    Returns
    -------
    return_columns: list
        List of columns to return by the simulation.

    """
    # avoid variables containing this words
    avoid_vars = ["historic", "delay", "next", "variation", "leontief",
                  "ia_matrix", "year", "initial", "aux", "policy",
                  "future",
                  ] + config['out_default']

    # returning cache.step objects
    var_list = sorted([
        model.components._namespace[var_name]
        for var_name in model._default_return_columns(run=False)
        if all([a_var not in model.components._namespace[var_name]
                for a_var in avoid_vars])
        ])

    if config['silent']:
        col_ind = 'r'
    else:
        for num, var_name in enumerate(var_list, 1):
            print('{}: {}'.format(num, var_name))

        print('\nDefault saved variables:')
        for var_name in config['out_default']:
            print('\t{}'.format(var_name))

        message =\
            "\n\nPlease select the desired output variables:" \
            "\n - 0 for all model variables" \
            "\n - comma separated numbers from the list above for "\
            "individual variables (e.g.: 1,4,5)" \
            "\n - r for the same variables of the last simulation" \
            "\n - + followed by the variable number to add individual "\
            "variables to the last simulation output (e.g. +5,+19,+21)" \
            "\n\n Write your choice here:"

        while True:
            col_ind = input(message)
            if col_ind.strip() == '':
                continue

            col_ind_split = [x.strip(' \t\n\b+') for x in col_ind.split(',')]

            if any(x in col_ind_split for x in ['r', '0']):
                break

            col_indices = [int(x) - 1 for x in col_ind_split if x.isdigit()]
            col_vars = [x for x in col_ind_split if not x.isdigit()]

            try:
                return_columns_set = set(list(map(var_list.__getitem__,
                                                  col_indices)) + col_vars)
            except IndexError:
                log.warning('\t\tWrong numerical index, try again...')
                continue

            # check if the variable names are correct
            if return_columns_set.issubset(var_list):
                break
            else:
                log.warning('Wrong variable name, try again...')
    col_ind_split = [x.strip(' \t\n\b+') for x in col_ind.split(',')]
    col_indices = [int(x) - 1 for x in col_ind_split if x.isdigit()]
    col_vars = [x for x in col_ind_split if not x.isdigit()]

    return_columns_set = set(list(map(var_list.__getitem__, col_indices))
                             + col_vars)

    if -1 in col_indices:
        return_columns = var_list

    elif 'r' in col_vars:
        try:
            with open(os.path.join(config['folder'], 'last_output_conf.txt'),
                      'r', encoding='utf-8') as f:
                return_columns = sorted([x.strip().split('[')[0]
                                         for x in f.readline().split(";")])
        except FileNotFoundError:
            log.warning("no last configuration, take all vars")
            return_columns = var_list
        else:
            log.info('The number and type of output variables of the current '
                     'simulation will be the same as in the previous one.'
                     '\nIf you want to change the number of outputs please'
                     ' remove the "-s" (silent mode) from the options when'
                     ' you run a simulation')

    elif col_ind.lstrip().startswith('+'):
        try:
            with open(os.path.join(config['folder'], 'last_output_conf.txt'),
                      'r', encoding='utf-8') as f:
                return_columns_set.update([x.strip().split('[')[0]
                                           for x in f.readline().split(";")])
        except FileNotFoundError:
            log.warning("There is no previous simulation available, "
                        "taking only the given variables instead")
        return_columns = sorted(list(return_columns_set))

    else:
        return_columns = sorted(list(return_columns_set))

    # adding the default variables to the choice of the user
    return_columns = list(set(return_columns + config['out_default']))

    with open(os.path.join(config['folder'], 'last_output_conf.txt'),
              'w', encoding='utf-8') as f:
        f.write(";".join(return_columns))

    return return_columns


def update_model_component(model, comp, value):
    """
    Creates a new function to add to the model.components
    method from pysd

    Parameters
    ----------
    model: pysd.Model
        Model object.
    comp: str
        Name of the component that needs to be changed.
    value: pd.series, str
        Value to return by the function.

    Returns
    -------
    None

    """
    if isinstance(value, pd.Series):
        value = series2lookup(value)

    if isinstance(value, str):
        # execution of the new function
        if "lookup" in value:
            exec("def {}(x): return {}".format(comp, value))
        else:
            exec("def {}(): return {}".format(comp, value))

        exec("model.components.{} = {}".format(comp, comp))

    elif isinstance(value, (int, float, xr.DataArray)):
        setattr(model.components, comp, lambda: value)


def load_model(model_py):
    """
    Load model with PySD

    Parameters
    ----------
    model_py: str
        Model to load.

    Returs
    ------
    model: pysd.Model
        Model object.

    """
    return pysd.load(os.path.join(model_py), initialize=False)


def run(config, model, run_params, return_columns):
    """
    Runs the model

    Parameters
    ----------
    config: dict
        Configuration parameters.
    model: pysd.Model
        Model object.
    run_params: dict
        Simulation parameters.
    return_columns: list
        Name of the variables that are to be written in the outputs file.

    Returns
    -------
    stocks: pandas.DataFrame
        Result of the simulation.

    """
    # create default file name for the results file
    # (if the user didn't pass any)
    if not config.get("fname"):
        config["fname"] = 'results_{}_{}_{}_{}'.format(
            config['scenario_sheet'],
            config['run_params']['initial_time'],
            config['run_params']['final_time'],
            config['run_params']['time_step'])

    print(
        "\n\nSimulation parameters:\n"
        "- Model name: {}\n"
        "- Scenario: {}\n"
        "- Initial time: {}\n"
        "- Final time: {}\n"
        "- Time step: {} years ({} days)\n"
        "- Results file name: {}".format(config['region'],
                                         config['scenario_sheet'].upper(),
                                         round(run_params['initial_time']),
                                         round(run_params['final_time']),
                                         run_params['time_step'],
                                         round(run_params['time_step']*365),
                                         os.path.join(config['out_folder'],
                                                      config["fname"] + ".csv")
                                         ))

    if config['parent']:
        print("- External data file: {}\n".format(config['extDataFilePath']))
    else:
        print("\n")

    if return_columns[0] != '':
        return_columns = return_columns
    else:
        return_columns = None

    if not config['return_timestep'] is None:
        return_timestamps = np.arange(run_params['initial_time'],
                                      run_params['final_time'] + 0.01,
                                      float(config['return_timestep']))
    else:
        return_timestamps = None

    print("Starting simulation.")
    sim_start_time = time.time()
    stocks = model.run(
        run_params,
        return_columns=return_columns,
        return_timestamps=return_timestamps,
        progress=config['progress'],
        flatten_output=True)
    sim_time = time.time() - sim_start_time
    log.info(f"Total simulation time: {(sim_time/60.):.2f} minutes")
    stocks.index.name = 'time'

    return stocks


def user_select_data_file_gui(region):
    """
    Creates a GUI from which the use will be able to select the file f
    rom which to import external data for the EU model.

    Parameters
    ----------
    region: str
        Folder of the region to open.

    Returns
    -------
    filename: str
        Name of the selected file.

    """
    defaultDir = os.path.join(os.getcwd(), region)
    Tk().withdraw()  # keep the root window from appearing
    return askopenfilename(
        initialdir=defaultDir,
        title="Select external data file",
        filetypes=(('.csv files', '*.csv'), ("All files", '*'))
        )


def user_select_data_file_headless(region):
    """
    Asks the user to select the csv file name from which to import data
    required to run the EU model in std output. It looks only in the
    pymedeas_w folder.

    Parameters
    ----------
    region: str
        Region folder name.

    Returns
    -------
    filename: str
        Filename of the file to load and extract data from

    """
    files_list = os.listdir(os.path.join(os.getcwd(), region))

    csv_list = [file for file in files_list if file.endswith('.csv')]

    if csv_list:
        val = input(
            "\nPlease write the number associated with the results file of the"
            + f" {region} model from which you  wish to import data:\n\t"
            + "\n\t".join("{}: {}".format(i, j)
                          for i, j in enumerate(csv_list, 0))
            + "\n\n here ->")
        try:
            val = int(val)
        except TypeError:
            raise TypeError('Only integer numbers allowed')

        if (val >= 0) and (val < len(csv_list)):
            return csv_list[val]
        else:
            raise ValueError("Please provide a number between 0 and "
                             "{}".format(len(csv_list)-1))
    else:
        raise ValueError('There are no csv files to import data from.\n'
                         'Please run the parent model/s first')


def create_external_data_files_paths(config):
    """
    This function lists all csv (results) files in the pymedeas_w and/or
    pymedeas_eu folder/s and asks the user to choose one, so that all the
    external data required by the EU or country model can be imported.
    Updates config with the paths.

    Parameters
    ----------
    config: dict
        Configuration parameters.

    Returns
    -------
    None

    """
    file_paths = {}

    if config['silent']:
        # no user input asked during execution, hence external files must
        # be provided beforehand
        if config['extDataFname']:
            # external data files names provided
            from_provided_external_file(config, file_paths)
        else:
            # silent mode and file names not provided -> error
            print('If you want to run in silent mode, please provide the name '
                  'of the results file/s from which you want to '
                  'import data. Examples below:\n'
                  '-e filename.csv (the file must be in the pymedeas_w folder)'
                  '\n-e filename1.csv,filename2.csv (the first file must be '
                  'in the pymedeas_w folder and the second in the '
                  'pymedeas_eu folder)\n')
            sys.exit(0)

    else:
        # not silent, user may be asked for input
        if config['headless']:
            # no graphical interface can be displayed, only CLI
            if config['extDataFname']:
                # external data files names provided
                file_paths = from_provided_external_file(config, file_paths)
            else:
                # it won't open a graphical window to select the file
                # but let you chose the file from CLI
                for parent in config['parent']:
                    file_paths[parent['name']] = os.path.join(
                        os.getcwd(), parent['folder'],
                        user_select_data_file_headless(parent['folder'])
                        )

        else:
            if config['extDataFname']:
                # external data files names provided
                from_provided_external_file(config, file_paths)
            else:
                # the user will be asked for input and can be graphical
                for parent in config['parent']:
                    file_paths[parent['name']] =\
                        user_select_data_file_gui(parent['folder'])

    config['extDataFilePath'] = file_paths


def from_provided_external_file(config, file_paths):
    """
    This creates the file paths of the folders where the external data
    files to be imported are located.

    Parameters
    ----------
    config: dict
        Configuration parameters.
    file_paths: dict
        Dictionary to save the paths to the files where the outputs are.

    Returns
    -------
    None

    """
    if len(config['parent']) != len(config['extDataFname']):
        raise TypeError(
            "Invalid number of results files  provided to run the model,"
            + f" need to provide {len(config['parent'])} files, but "
            + f" {len(config['extDataFname'])} files where provided.\n"
            + "If you gave two or more file names, make sure to not "
            + "leave any blank space between them (e.g. file1.csv,file2.cv).")

    for parent, filename in zip(config['parent'], config['extDataFname']):
        file_paths[parent['name']] =\
            os.path.join(os.getcwd(), parent['folder'], filename)

    # if any of the file paths generated does not exist, kill the execution
    for path in file_paths:
        if not os.path.exists(file_paths.get(path)):
            raise FileNotFoundError(
                'The file {} cannot be found'.format(file_paths.get(path)))


def load_external_data(config, subscript_dict, namespace):
    """
    Load outputs from parent models.

    Parameters
    ----------
    config: dict
        Configuration parameters.

    subscript_dict: dict
        Dictionary describing the possible dimensions of the
        variable's subscripts

    Returns
    -------
    dataDict: dict
        Dictionary with the names of the functions and their return.

    """
    dataDict = {}
    xarrayDict = {}

    for parent in config['parent']:
        df = pd.read_csv(config['extDataFilePath'][parent['name']],
                         index_col=0).T
        df.index = pd.to_numeric(df.index)

        imports = []
        for import_var, subs in parent['input_vars'].items():
            vensim_var =\
                list(namespace.keys())[list(namespace.values()).index(import_var)]
            if subs:
                # find all columns with subscripts
                cols = [(import_var, col) for col in df.columns
                        if col.startswith(import_var+"[")]
                if not cols:
                    # try to find cols by vensim name
                    cols = [(import_var, col) for col in df.columns
                            if col.startswith(vensim_var+"[")]
                if not cols:
                    raise NameError(
                        f"Variable {import_var} is not in the results file"
                        + f" of the {parent['name']} model")
                imports += cols
                # add to the dictionary with the dimensions to merge
                xarrayDict[import_var] = [[], subs]
            else:
                if import_var in df.columns:
                    imports.append((import_var, import_var))
                elif vensim_var in df.columns:
                    imports.append((import_var, vensim_var))
                else:
                    raise NameError(
                        f"Variable {import_var} is not in the results file"
                        + f" of the {parent['name']} model")

        for py_var, df_var in imports:
            if '[' in df_var:
                xarrayDict[py_var][0].append((
                    series2lookup(df[df_var]),
                    re.split('\[|\]| , |, | ,|,', df_var)[1:-1]
                    ))
            else:
                dataDict[py_var] = series2lookup(df[df_var])

    for var, value in xarrayDict.items():
        dataDict[var] = merge_series(value, subscript_dict)

    return dataDict


def series2lookup(serie):
    """
    Transformas a pandas DataFrame to a formatted lookup.

    Parameters
    ----------
    serie: pd.DataFrame
        Series to convert to a lookup.

    Returns
    -------
    str
        Formatted series.

    """
    dates = ", ".join(serie.index.astype(str))
    values = ", ".join(map(str, serie.values.tolist()))
    return "functions.lookup(x, [{}], [{}])".format(dates, values)


def merge_series(series, subscript_dict):
    """
    Merge series of subscripted variables.

    Parameters
    ----------
    series: list
        List of tuuple with the series lookup expression and the
        subscripts list.

    subscript_dict: dict
        Dictionary describing the possible dimensions of the
        variable's subscripts

    Returns
    -------
    str
        Merged series.

    """
    subs = [serie[1] for serie in series[0]]
    values = [serie[0] for serie in series[0]]
    dims = series[1]

    # merge series, similar to what pysd builder does
    for i, subs_i in enumerate(subs):
        coords = pysd.utils.make_coord_dict(subs_i, subscript_dict,
                                            terse=False)
        coords = {new_dim: coords[dim] for new_dim, dim in zip(dims, coords)}
        values[i] = f"xr.DataArray({values[i]}, {coords}, {list(coords)})"
    return 'xrmerge([%s])' % (', '.join(values))


def select_scenario_sheet(model, scen_sheet_name):
    """
    Selects scenario sheet to load

    Parameters
    ----------
    model: pysd.Model
        Model object.
    scen_sheet_name: str
        Name of the scenario sheet.

    Returns
    -------
    None

    """
    for element in model._external_elements:
        # Replace only user scenario
        element.sheets = [scen_sheet_name if sheet == 'User scenario'
                          else sheet
                          for sheet in element.sheets]
