#!/usr/bin/env python
__author__ = "Roger Samsó, Eneko Martin"
__maintainer__ = "Eneko Martin, Roger Samsó"
__status__ = "Development"

from pytools.config import read_model_config
import sys
import time
from datetime import datetime

import re
import pandas as pd
import numpy as np
import xarray as xr
import pathlib

import argparse
from .argparser import parser, config
from .config import Params, ParentModel

# imports for GUI
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from .logger.logger import log

# PySD imports for replaced functions
from pysd.py_backend.utils import xrmerge
from pysd.py_backend.functions import Model

# these imports will not be needed in Python 3.9
from typing import Union, Dict, List
from . import PROJ_FOLDER


def get_initial_user_input(args=None) -> argparse.Namespace:
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
    # TODO review the documentation cause this function has changed

    """
    # this is only used for testing purposes
    if args is None:
        args = sys.argv[1:]

    return parser.parse_args(args)


def update_config_from_user_input(options: argparse.Namespace,
                                  base_path: pathlib.Path =
                                  PROJ_FOLDER) -> Params:

    """
    This function takes user inputs and updates the config class attributes
    accordingly.
    The base_path argument is for testing purposes only
    """
    # update configurations based on user input
    for att in options.__dict__.keys():
        # only if there's a default or the user adds input for that attribute
        if hasattr(config, att) and getattr(options, att):
            setattr(config, att, getattr(options, att))

    # adding the configurations of the specific model selected by the user
    read_model_config(config)

    # TODO make for loop

    if getattr(options, 'export_file'):
        export_file_raw = getattr(options, 'export_file')
        if pathlib.Path(export_file_raw).is_absolute():
            if pathlib.Path(export_file_raw).parent.is_dir():
                config.model_arguments.export = pathlib.Path(
                    export_file_raw).resolve()
            else:
                raise(ValueError, "Invalid pickle export path {}".format(
                    str(pathlib.Path(export_file_raw))))
        else:
            pickle_path = base_path.joinpath(export_file_raw).resolve()
            if pickle_path.parent.is_dir():
                config.model_arguments.export = pickle_path
            else:
                raise("Invalid pickle export path {}".format(
                    str(pathlib.Path(export_file_raw).resolve())))

    config.model_arguments.time_step = getattr(options, 'time_step')
    config.model_arguments.final_time = getattr(options, 'final_time')
    config.model_arguments.return_timestamp = getattr(options,
                                                      'return_timestamp')
    config.model_arguments.results_fname = getattr(options, 'results_fname')

    if getattr(options, 'return_columns'):
        config.model_arguments.return_columns = getattr(options,
                                                        'return_columns')
    if options.new_values['param']:
        config.model_arguments.update_params = options.new_values['param']

    if options.new_values['initial']:
        config.model_arguments.update_initials = options.new_values['initial']

    if options.results_file_path:  # should be a dictionary
        # in models with two parents, if the user provides the results for one
        # they should also provide the resutls for the other.
        parents_names = [dic.name for dic in config.model.parent]
        difference = list(set(parents_names).difference(set(
            options.results_file_path[0])))
        if difference:
            raise ValueError(difference[0] + ". Please provide results "
                             "file paths for " + " and ".join(
                                        parents_names) + " models")
        for mod_name, res_path in options.results_file_path[0].items():
            mod_name, res_path = mod_name.strip(), res_path.strip()
            if mod_name in parents_names:
                idx = parents_names.index(mod_name)
                if pathlib.Path(res_path).is_absolute():
                    if pathlib.Path(res_path).is_file():
                        config.model.parent[idx].results_file_path = \
                            pathlib.Path(res_path).resolve()
                    else:
                        raise FileNotFoundError(str(
                            pathlib.Path(res_path).resolve()) +
                            " is not a valid path for the " +
                            "results file of the " + mod_name +
                            " model")
                else:
                    results_path = base_path.joinpath(res_path).resolve()
                    if results_path.is_file():
                        config.model.parent[idx].results_file_path = \
                            results_path
                    else:
                        raise FileNotFoundError(
                            str(results_path) + " is not a valid path for " +
                            "the results file of the " + mod_name + " model")

            else:
                raise ValueError(
                        "Invalid parent model name when importing parent model"
                        " outputs: " + mod_name + ". Valid names for parent"
                        "models of the " + config.region + " model are: " +
                        ", ".join(parents_names))

    return config


def store_results_csv(result: pd.DataFrame, config: Params) -> pd.DataFrame:
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
    _rename_old_simulation_results(config)

    # storing results to csv file
    result.transpose().to_csv(config.model_arguments.results_fpath)
    log.info('Simulation results file is located in {}'.format(str(
        config.model_arguments.results_fpath)))

    # recording the output variables in a file, in case the user wants to
    # output the same variables in the next simulations
    with open(config.model.out_folder.joinpath('last_output.txt'),
              mode='w') as f:
        f.write('\n'.join(sorted(result.columns)))

    if result.isna().any().any():
        nan_vars = result.columns[result.isna().any()].tolist()
        log.warning(
            "There are NaN's in the timeseries of the following variables\n\n:"
            + " {}\n\n, which might indicate ".format("\n".join(nan_vars)) +
            "convergence issues, try decreasing the time step")

    return result


def _rename_old_simulation_results(config: Params) -> None:
    """
    This function renames old simulation results with the same name but
    adding date and time at the end of the file name

    :return (str) new file path
    """

    file_path = config.model_arguments.results_fpath
    folder = file_path.parent
    fname = file_path.stem
    extension = file_path.suffix

    if file_path.is_file():
        creation_time: str = datetime.fromtimestamp(
            file_path.stat().st_ctime).strftime("%Y%m%d__%H%M%S")
        old_file_new_path = folder.joinpath(fname + "_{}".format(creation_time)
                                            + extension)
        file_path.rename(old_file_new_path)
        log.info(
            'File {} has been renamed as {}'.format(fname + extension,
                                                    old_file_new_path.name))


def select_model_outputs(config: Params, model: Model,
                         select: Union[str, None] = None) -> list:
    """
    Select model outputs. If the simulation was called using silent mode,
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
    selsect: 'all', 'default' or None
        If 'all', select directly all columns. If 'default' select only default
        columns. Else print in stdin the message to select columns.
        Default is None.

    Returns
    -------
    return_columns: list
        List of columns to return by the simulation.

    """
    # avoid variables containing these words
    # TODO this list should not be hardcoded
    avoid_vars = ["historic", "delay", "next", "variation", "leontief",
                  "ia_matrix", "year", "initial", "aux", "policy",
                  "future",
                  ] + config.model.out_default

    # returning cache.step objects
    var_list = sorted([
        model.components._namespace[var_name]
        for var_name in model._default_return_columns(which='step')
        if all([a_var not in model.components._namespace[var_name]
                for a_var in avoid_vars])
        ])

    if config.silent:
        col_ind = 'r'
    elif select == 'all':
        col_ind = '0'
    elif select == 'default':
        return config.model.out_default
    else:
        for num, var_name in enumerate(var_list, 1):
            print('{}: {}'.format(num, var_name))

        print('\n\nDefault output variables:')
        for var_name in config.model.out_default:
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
            with open(config.model.out_folder.joinpath('last_output.txt'),
                      'r', encoding='utf-8') as f:
                return_columns = [x.strip() for x in f.readlines()]
        except FileNotFoundError:
            log.warning("The list of output variables from the last"
                        " simulation. All model outputs will be returned.")
            return_columns = var_list
        else:
            log.info("The number and type of output variables of the current "
                     "simulation will be the same as in the previous one.")
            if config.silent:
                log.info("\nIf you want to change the number of outputs please"
                         " remove the '-s' (silent mode) from the options when"
                         " you run a simulation")

    elif col_ind.lstrip().startswith('+'):
        try:
            with open(config.model.out_folder.joinpath('last_output.txt'),
                      mode='r', encoding='utf-8') as f:
                return_columns_set.update([x.strip() for x in f.readlines()])
        except FileNotFoundError:
            log.warning("There is no previous simulation available, "
                        "taking only the given variables instead")
        return_columns = sorted(list(return_columns_set))

    else:
        return_columns = sorted(list(return_columns_set))

    # adding the default variables to the choice of the user
    return_columns = list(set(return_columns + config.model.out_default))

    with open(config.model.out_folder.joinpath('last_output.txt'),
              mode='w', encoding='utf-8') as f:
        f.write("\n".join(sorted(return_columns)))

    return return_columns


def run(config: Params, model: Model) -> pd.DataFrame:
    """
    Runs the model

    Parameters
    ----------
    config: dict
        Configuration parameters.
    model: pysd.Model
        Model object.
    return_columns: list
        Name of the variables that are to be written in the outputs file.

    Returns
    -------
    stocks: pandas.DataFrame
        Result of the simulation.

    """
    # generating the output file name
    if not config.model_arguments.results_fname:
        config.model_arguments.results_fname = \
            "results_{}_{}_{}_{}.csv".format(
                config.scenario_sheet,
                config.model_arguments.initial_time,
                config.model_arguments.final_time,
                config.model_arguments.time_step
                )

    config.model_arguments.results_fpath = config.model.out_folder.joinpath(
        config.model_arguments.results_fname)

    print(
        "\n\nSimulation parameters:\n"
        "- Model name: {name}\n"
        "- Scenario: {scenario}\n"
        "- Initial time: {initial}\n"
        "- Final time: {final}\n"
        "- Simulation time step: {tstep} years ({tstep_days} days)\n"
        "- Results file path: {fpath}".format(
            name=config.region,
            scenario=config.scenario_sheet.upper(),
            initial=config.model_arguments.initial_time,
            final=config.model_arguments.final_time,
            tstep=config.model_arguments.time_step,
            tstep_days=config.model_arguments.time_step*365,
            fpath=str(config.model_arguments.results_fpath)))

    if config.model.parent:
        for parent in config.model.parent:
            print("- External data file for {}: {}".format(
                parent.name,
                str(parent.results_file_path)))

    if isinstance(config.model_arguments.update_initials, dict):
        print("- Updated initial conditions:\n\t" + "\n\t".join(
            [par + ": " + str(val) for par, val in
             config.model_arguments.update_initials.items()]))

    sim_start_time = time.time()

    stocks = model.run(
        params=config.model_arguments.update_params,
        initial_condition=(config.model_arguments.initial_time,
                           config.model_arguments.update_initials),
        return_columns=config.model_arguments.return_columns,
        return_timestamps=np.arange(
            config.model_arguments.initial_time,
            config.model_arguments.final_time + 0.01,
            float(config.model_arguments.return_timestamp)),
        progress=config.progress,
        final_time=config.model_arguments.final_time,
        time_step=config.model_arguments.time_step,
        flatten_output=True)

    sim_time = time.time() - sim_start_time
    log.info(f"Total simulation time: {(sim_time/60.):.2f} minutes")

    stocks.index.name = 'time'

    return stocks


def user_select_data_file_gui(parent: ParentModel) -> str:
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
    dir_path = parent.default_results_folder

    Tk().withdraw()  # keep the root window from appearing
    return askopenfilename(
        initialdir=dir_path,
        title="Select external data file",
        filetypes=(('.csv files', '*.csv'), ("All files", '*'))
        )


def user_select_data_file_headless(parent: ParentModel) -> pathlib.Path:
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
    dir_path = parent.default_results_folder

    files_list = list(filter(lambda x: x.is_file() and x.suffix == ".csv",
                             dir_path.iterdir()))
    files_list.sort()

    if files_list:  # there are csv files in the folder
        while True:
            val_ = input(
             "\nPlease write the number associated with the results file of"
             + f" {parent.name} model from which you wish to import data:\n\t"
             + "\n\t".join("{}: {}".format(i, j.name)
                           for i, j in enumerate(files_list, 0))
             + "\n\n here ->")
            try:
                val = int(val_)
            except ValueError:
                print('Only integer numbers allowed')
                sys.exit(0)
            if (val >= 0) and (val < len(files_list)):
                return files_list[val]
            else:
                raise ValueError("Please provide a number between 0 and "
                                 "{}".format(len(files_list)-1))
    else:
        raise ValueError('There are no csv files to import data from.\n'
                         'Please run the parent model/s first')


def create_parent_models_data_file_paths(config: Params) -> None:
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

    # if the user passed the file paths from the CLI, they should be here
    paths_from_user_input = all([dic.results_file_path for dic in
                                 config.model.parent])

    if config.silent:
        # no user input asked during execution, hence external files must
        # be provided beforehand
        if not paths_from_user_input:
            # silent mode and file names not provided -> error
            print('If you want to run in silent mode, please provide the name '
                  'of the results file/s from which you want to '
                  'import data. Examples below:\n'
                  '\t-f pymedeas_w: outputs/results_w.csv\n'
                  '\t-f pymedeas_w: outputs/results_w.csv, pymedeas_eu: '
                  'outputs/results_eu.csv\n')
            sys.exit(0)

    else:
        # not silent, user may be asked for input
        if config.headless:
            # no graphical interface can be displayed, only CLI
            if not paths_from_user_input:
                # it won't open a graphical window to select the file
                # but let you chose the file from CLI
                for num, _ in enumerate(config.model.parent):
                    config.model.parent[num].results_file_path = \
                        user_select_data_file_headless(
                            config.model.parent[num])

        else:
            if not paths_from_user_input:
                # the user will be asked for input and can be graphical
                for num, _ in enumerate(config.model.parent):
                    config.model.parent[num].results_file_path = \
                        pathlib.Path(user_select_data_file_gui(
                            config.model.parent[num]))


def load_external_data(config: Params,
                       subscripts: dict,
                       namespace: dict) -> dict:  # TODO subscripts not used
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
    xarrayDict: Dict[str, Dict[str, List]] = {}

    for parent in config.model.parent:
        df = pd.read_csv(parent.results_file_path, index_col=0).T
        df.index = pd.to_numeric(df.index)

        imports = []
        vars_with_subs = []
        for _, vals in parent.input_vars.items():
            vensim_var =\
                list(namespace.keys())[list(namespace.values()).index(
                    vals["name_in_parent"])]
            if vals["subs"]:
                # find all columns with subscripts
                cols_in_df = [(vals["name_in_parent"], col) for col in
                              df.columns if col.startswith(
                                  vals["name_in_parent"]+"[")]
                if not cols_in_df:
                    # try to find cols by vensim name
                    cols_in_df = [(vals["name_in_parent"], col) for col
                                  in df.columns if col.startswith(
                                      vensim_var+"[")]
                if not cols_in_df:
                    raise NameError("Variable {}".format(
                        vals["name_in_parent"]) + " is not in the results file"
                        + " of the {} model".format(parent.name))
                imports += cols_in_df
                # add to the dictionary with the dimensions to merge
                xarrayDict[vals["name_in_parent"]] = {'subs': vals["subs"],
                                                      'cols': []}
                vars_with_subs.append(vals["name_in_parent"])
            else:
                if vals["name_in_parent"] in df.columns:
                    imports.append((vals["name_in_parent"],
                                    vals["name_in_parent"]))
                elif vensim_var in df.columns:
                    imports.append((vals["name_in_parent"], vensim_var))
                else:
                    raise NameError("Variable {} ".format(
                        vals["name_in_parent"]) + "is not in the results file"
                        + " of the {} model".format(parent.name))

        for py_var, df_var in imports:
            if '[' in df_var:
                # Create 0 dims xarrays
                dims = xarrayDict[py_var]['subs']
                coords_ = re.split('\[|\]| , |, | ,|,', df_var)[1:-1]
                coords = {dim: [coord] for (dim, coord) in zip(dims, coords_)}
                df[df_var] = df[df_var].apply(xr.DataArray, args=(coords,
                                                                  dims))
                xarrayDict[py_var]['cols'].append(df_var)
            else:
                dataDict[py_var] = df[df_var]
        for py_var in vars_with_subs:  # only xarrays (inputs with subscripts)
            # merge xarrays to create a pandas.Series of xarray.DataArray
            dataDict[py_var] = df[xarrayDict[py_var]['cols']].apply(
                xrmerge, axis=1)

    return dataDict


def select_scenario_sheet(model: Model, scen_sheet_name: str) -> None:
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

    return None
