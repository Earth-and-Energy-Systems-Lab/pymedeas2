#!/usr/bin/env python
__author__ = "Roger Samsó, Eneko Martin"
__maintainer__ = "Eneko Martin, Roger Samsó"
__status__ = "Development"

import sys
import time
import shutil
from datetime import datetime
from pathlib import Path
from argparse import Namespace
# these imports will not be needed in Python 3.9
from typing import Union, List

# imports for GUI
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import pandas as pd
import pysd
from tabulate import tabulate

# PySD imports for replaced functions
from pysd.py_backend.model import Model


from . import PROJ_FOLDER
from .logger.logger import log
from .argparser import parser, config
from .config import Params, ParentModel, read_model_config, read_config


def get_initial_user_input(args: Union[List, None] = None) -> Namespace:
    """
    Get user input to create the config object.

    Parameters
    ----------
    args: list or None (optional)
        List of user arguments to run the model. If None the arguments
        will be taken from the taken from the system input. Default is None.

    Returns
    -------
    config: argparse.Namespace
        Configuration data object.

    """
    if args is None:
        args = sys.argv[1:]

    return parser.parse_args(args)


def update_config_from_user_input(options: Namespace,
                                  base_path: Path = PROJ_FOLDER) -> Params:

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
        if Path(export_file_raw).is_absolute():
            if Path(export_file_raw).parent.is_dir():
                config.model_arguments.export = Path(export_file_raw).resolve()
            else:
                raise ValueError("Invalid pickle export path {}".format(
                    str(Path(export_file_raw))))
        else:
            pickle_path = base_path.joinpath(export_file_raw).resolve()
            if pickle_path.parent.is_dir():
                config.model_arguments.export = pickle_path
            else:
                raise ValueError("Invalid pickle export path {}".format(
                    str(Path(export_file_raw).resolve())))

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
                if Path(res_path).is_absolute():
                    if Path(res_path).is_file():
                        config.model.parent[idx].results_file_path = \
                            Path(res_path).resolve()
                    else:
                        raise FileNotFoundError(str(
                            Path(res_path).resolve()) +
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
    log.info("Simulation results file is located in %s" %
             str(config.model_arguments.results_fpath))

    col_empty = []
    for column in result.columns:
        if result[column].isna().all():
            # remove columns with all na values (unexistent dimensions)
            col_empty.append(column)

    for column in col_empty:
        result.drop(column, inplace=True, axis=1)

    # recording the output variables in a file, in case the user wants to
    # output the same variables in the next simulations
    with open(config.model.out_folder.joinpath('last_output.txt'),
              mode='w') as f:
        f.write('\n'.join(sorted(result.columns)))

    if result.isna().any().any():
        nan_vars = result.columns[result.isna().any()].tolist()
        log.warning(
            "There are NaN's in the timeseries of the following variables\n\n:"
            "\t%s\n\n, which might indicate convergence issues, try"
            "decreasing the time step" % '\n'.join(nan_vars))

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
        model.namespace[var_name]
        for var_name in model._default_return_columns(which='step')
        if all(
            [a_var not in model.namespace[var_name] for a_var in avoid_vars]
            )
        ])

    df = model.doc
    df = df[df["Py Name"].isin(var_list)]
    df = df.loc[:, ["Py Name", "Units", "Comment"]]
    df.dropna(inplace=True, how="all")
    df = df.reset_index(drop=True)

    df.fillna({"Comment": "Description not available for this variable"},
              inplace=True)
    df.fillna({"Units": "-"}, inplace=True)

    # Apply the function to the column with long strings
    df["Comment"] = df["Comment"].apply(split_long_strings)

    if select == "all":
        col_ind = "0"
    elif select == "default":
        return config.model.out_default
    elif config.silent:
        col_ind = "r"
    else:
        page_size = 500
        # Print each page of the paginated data
        for page_num, page_df in enumerate(paginate_dataframe(df, page_size), start=1):
            print(f"Page {page_num}:")
            print(tabulate(page_df, headers='keys', tablefmt='pretty'))
            print("\n")  # Add a newline between pages

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
            "results_{}_{}_{}_{}.nc".format(
                config.scenario_sheet,
                int(config.model_arguments.initial_time),
                int(config.model_arguments.final_time),
                config.model_arguments.time_step
                )

    if not config.model_arguments.results_fpath:
        config.model_arguments.results_fpath =\
            config.model.out_folder.joinpath(
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

    if config.model_arguments.update_initials:
        print("- Updated initial conditions:\n\t" + "\n\t".join(
            [par + ": " + str(val) for par, val in
             config.model_arguments.update_initials.items()]))

    sim_start_time = time.time()

    model.run(
        params=config.model_arguments.update_params,
        initial_condition=(config.model_arguments.initial_time,
                           config.model_arguments.update_initials),
        return_columns=config.model_arguments.return_columns,
        progress=config.progress,
        final_time=config.model_arguments.final_time,
        time_step=config.model_arguments.time_step,
        saveper=config.model_arguments.return_timestamp,
        output_file=config.model_arguments.results_fpath)

    sim_time = time.time() - sim_start_time
    log.info(f"Total simulation time: {(sim_time/60.):.2f} minutes")


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


def user_select_data_file_headless(parent: ParentModel) -> Path:
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
             + "\n\t".join(f"{i}: {j.name}"
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
                                 f"{len(files_list)-1}")
    else:
        raise ValueError('There are no csv files to import data from.\n'
                         'Please run the parent model/s first')


def create_parent_models_data_file_paths(config: Params) -> List[Path]:
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
    file_path: list
        List of parent output file paths.

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
                        Path(user_select_data_file_gui(
                            config.model.parent[num]))

    return [parent.results_file_path for parent in config.model.parent]


def load(config: Params, data_files: Union[list, None] = None) -> Model:
    """
    Load PySD model and changes the paths to load excel data.

    Parameters
    ----------
    config: dict
        Configuration parameters.
    data_files: list or None (optional)
        List of parent output file paths. Default is None.

    Returns
    -------
    pysd.Model

    """
    # Copy _subscripts.json
    target = config.model.model_file.parent /\
        f"_subscripts_{config.model.model_file.with_suffix('.json').name}"
    shutil.copy(
        config.model.model_file.parent.parent / config.aggregation /
        config.model.subscripts_file,
        target
        )

    # Load PySD model
    model = pysd.load(
        str(config.model.model_file), initialize=False,
        data_files=data_files)

    if target.exists():
        target.unlink()
        # target.unlink(missing_ok=True) should work but doesn't for some
        # versions of pathlib

    # Modify external elements information
    scen_file =\
        f"../../scenarios/{config.aggregation}/{config.model.scenario_file}"
    input_folder = f"../{config.aggregation}/"
    for element in model._external_elements:
        # Replace only scenario sheets
        element.sheets = [
            config.scenario_sheet if "../../scenarios/scen" in file_name
            else config.model.inputs_sheet if sheet_name != "Global"
            else sheet_name
            for sheet_name, file_name in zip(element.sheets, element.files)
        ]
        # Select he input files from the agrregation
        element.files = [
            scen_file
            if file_name.startswith("../../scenarios/")
            else file_name.replace("../", input_folder)
            for file_name in element.files
        ]

    return model


def load_model(aggregation: str = "14sectors_cat",
               region: str = "pymedeas_w",
               data_files: Union[list, None] = None) -> Model:
    """
    Load PySD model and changes the paths to load excel data.

    Parameters
    ----------
    aggregation: str (optional)
        Aggregation to load the model. Default is '14sectors_cat'.
    region: str (optional)
        Region to load the model.  Default is 'pymedeas_w'.
    data_files: list or None (optional)
        List of parent output file paths. Default is None.

    Returns
    -------
    pysd.Model

    """
    user_config = read_config()
    user_config.aggregation = aggregation
    user_config.region = region
    read_model_config(user_config)
    return load(user_config, data_files)


# Function to paginate the DataFrame
def paginate_dataframe(df, page_size):
    for i in range(0, len(df), page_size):
        yield df.iloc[i:i+page_size]


# Function to split long strings into multiple lines
def split_long_strings(value, max_width=80):
    if len(value) <= max_width:
        return value
    else:
        return '\n'.join([value[i:i+max_width] for i in range(0, len(value), max_width)])
