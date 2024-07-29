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
        List of user arguments to run the model. If None, the arguments
        will be taken from the system input. Default is None.

    Returns
    -------
    config: argparse.Namespace
        Configuration data object.

    """
    if args is None:
        args = sys.argv[1:]

    return parser.parse_args(args)


def update_config_from_user_input(
    options: Namespace, base_path: Path = PROJ_FOLDER
) -> Params:
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

    if getattr(options, "export_file"):
        export_file_raw = getattr(options, "export_file")
        if Path(export_file_raw).is_absolute():
            if Path(export_file_raw).parent.is_dir():
                config.model_arguments.export = Path(export_file_raw).resolve()
            else:
                raise ValueError(
                    "Invalid pickle export path {}".format(str(Path(export_file_raw)))
                )
        else:
            pickle_path = base_path.joinpath(export_file_raw).resolve()
            if pickle_path.parent.is_dir():
                config.model_arguments.export = pickle_path
            else:
                raise ValueError(
                    "Invalid pickle export path {}".format(
                        str(Path(export_file_raw).resolve())
                    )
                )

    config.model_arguments.time_step = getattr(options, "time_step")
    config.model_arguments.final_time = getattr(options, "final_time")
    config.model_arguments.return_timestamp = getattr(options, "return_timestamp")
    config.model_arguments.results_fname = getattr(options, "results_fname")

    if options.new_values["param"]:
        config.model_arguments.update_params = options.new_values["param"]

    if options.new_values["initial"]:
        config.model_arguments.update_initials = options.new_values["initial"]

    if options.results_file_path:  # should be a dictionary
        # in models with two parents, if the user provides the results for one
        # they should also provide the resutls for the other.
        parents_names = [dic.name for dic in config.model.parent]
        difference = list(
            set(parents_names).difference(set(options.results_file_path[0]))
        )
        if difference:
            raise ValueError(
                difference[0] + ". Please provide results "
                "file paths for " + " and ".join(parents_names) + " models"
            )
        for mod_name, res_path in options.results_file_path[0].items():
            mod_name, res_path = mod_name.strip(), res_path.strip()
            if mod_name in parents_names:
                idx = parents_names.index(mod_name)
                if Path(res_path).is_absolute():
                    if Path(res_path).is_file():
                        config.model.parent[idx].results_file_path = Path(
                            res_path
                        ).resolve()
                    else:
                        raise FileNotFoundError(
                            str(Path(res_path).resolve())
                            + " is not a valid path for the "
                            + "results file of the "
                            + mod_name
                            + " model"
                        )
                else:
                    results_path = base_path.joinpath(res_path).resolve()
                    if results_path.is_file():
                        config.model.parent[idx].results_file_path = results_path
                    else:
                        raise FileNotFoundError(
                            str(results_path)
                            + " is not a valid path for "
                            + "the results file of the "
                            + mod_name
                            + " model"
                        )

            else:
                raise ValueError(
                    "Invalid parent model name when importing parent model"
                    " outputs: " + mod_name + ". Valid names for parent"
                    "models of the "
                    + config.region
                    + " model are: "
                    + ", ".join(parents_names)
                )

    return config


def rename_existing_file(file_path: Path):
    """
    Renames an existing file by appending its creation date to the file name before the file extension.

    If the file specified by `file_path` already exists, it will be renamed to include its creation date in the format
    YYYYMMDD before the file extension. For example, a file named 'filename.nc' created on July 1, 2024, will be
    renamed to 'filename_20240701.nc'. If the file does not exist, the function does nothing.

    Parameters:
    ----------
    file_path : Path
        The path to the file that will be checked and potentially renamed.

    Returns:
    -------
    None
    """
    if file_path.exists():
        # Get the creation time of the existing file
        creation_time = datetime.fromtimestamp(file_path.stat().st_ctime)
        # Format the creation time as YYYYMMDD
        creation_time_str = creation_time.strftime("%Y%m%d")
        # Construct the new file name with the creation date
        new_file_name = f"{file_path.stem}_{creation_time_str}{file_path.suffix}"
        new_file_path = file_path.parent / new_file_name
        # Rename the existing file
        file_path.rename(new_file_path)


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
        config.model_arguments.results_fname = "results_{}_{}_{}_{}.nc".format(
            config.scenario_sheet,
            int(config.model_arguments.initial_time),
            int(config.model_arguments.final_time),
            config.model_arguments.time_step,
        )

    if not config.model_arguments.results_fpath:
        config.model_arguments.results_fpath = config.model.out_folder.joinpath(
            config.model_arguments.results_fname
        )

    rename_existing_file(config.model_arguments.results_fpath)

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
            tstep_days=config.model_arguments.time_step * 365,
            fpath=str(config.model_arguments.results_fpath),
        )
    )

    if config.model.parent:
        for parent in config.model.parent:
            print(
                "- External data file for {}: {}".format(
                    parent.name, str(parent.results_file_path)
                )
            )

    if config.model_arguments.update_initials:
        print(
            "- Updated initial conditions:\n\t"
            + "\n\t".join(
                [
                    par + ": " + str(val)
                    for par, val in config.model_arguments.update_initials.items()
                ]
            )
        )

    sim_start_time = time.time()

    model.run(
        params=config.model_arguments.update_params,
        initial_condition=(
            config.model_arguments.initial_time,
            config.model_arguments.update_initials,
        ),
        return_columns="step",
        progress=config.progress,
        final_time=config.model_arguments.final_time,
        time_step=config.model_arguments.time_step,
        saveper=config.model_arguments.return_timestamp,
        output_file=config.model_arguments.results_fpath,
    )

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
        filetypes=((".nc files", "*.nc"), ("All files", "*")),
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

    files_list = list(
        filter(lambda x: x.is_file() and x.suffix == ".nc", dir_path.iterdir())
    )
    files_list.sort()

    if files_list:  # there are nc files in the folder
        while True:
            val_ = input(
                "\nPlease write the number associated with the results file of"
                + f" {parent.name} model from which you wish to import data:\n\t"
                + "\n\t".join(f"{i}: {j.name}" for i, j in enumerate(files_list, 0))
                + "\n\n here ->"
            )
            try:
                val = int(val_)
            except ValueError:
                print("Only integer numbers allowed")
                sys.exit(0)
            if (val >= 0) and (val < len(files_list)):
                return files_list[val]
            else:
                raise ValueError(
                    "Please provide a number between 0 and " f"{len(files_list)-1}"
                )
    else:
        raise ValueError(
            "There are no .nc files to import data from.\n"
            "Please run the parent model/s first"
        )


def create_parent_models_data_file_paths(config: Params) -> List[Path]:
    """
    This function lists all nc (results) files in the pymedeas_w and/or
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
    paths_from_user_input = all([dic.results_file_path for dic in config.model.parent])

    if config.silent:
        # no user input asked during execution, hence external files must
        # be provided beforehand
        if not paths_from_user_input:
            # silent mode and file names not provided -> error
            print(
                "If you want to run in silent mode, please provide the name "
                "of the results file/s from which you want to "
                "import data. Examples below:\n"
                "\t-f pymedeas_w: outputs/results_w.nc\n"
                "\t-f pymedeas_w: outputs/results_w.nc, pymedeas_eu: "
                "outputs/results_eu.nc\n"
            )
            sys.exit(0)

    else:
        # not silent, user may be asked for input
        if config.headless:
            # no graphical interface can be displayed, only CLI
            if not paths_from_user_input:
                # it won't open a graphical window to select the file
                # but let you chose the file from CLI
                for num, _ in enumerate(config.model.parent):
                    config.model.parent[num].results_file_path = (
                        user_select_data_file_headless(config.model.parent[num])
                    )

        else:
            if not paths_from_user_input:
                # the user will be asked for input and can be graphical
                for num, _ in enumerate(config.model.parent):
                    config.model.parent[num].results_file_path = Path(
                        user_select_data_file_gui(config.model.parent[num])
                    )

    return [parent.results_file_path for parent in config.model.parent]


def load(config: Params, data_files: Union[list, None] = None) -> Model:
    """
    Load PySD model and changes the paths to load excel data.
    PySD expects the _subscripts_model_name.json file to be in the same folder
    than the main file of the model (e.g. pymedeas_w.py), so it temporarily
    copies this file in the main folder.

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
    target = (
        config.model.model_file.parent
        / f"_subscripts_{config.model.model_file.with_suffix('.json').name}"
    )
    shutil.copy(
        config.model.model_file.parent.parent
        / config.aggregation
        / config.model.subscripts_file,
        target,
    )

    # Load PySD model
    model = pysd.load(
        str(config.model.model_file), initialize=False, data_files=data_files
    )

    if target.exists():
        target.unlink()
        # target.unlink(missing_ok=True) should work but doesn't for some
        # versions of pathlib

    # Modify external elements information
    scen_file = f"../../scenarios/{config.aggregation}/{config.model.scenario_file}"
    input_folder = f"../{config.aggregation}/"
    for element in model._external_elements:
        # Replace only scenario tabs
        element.tabs = [
            (
                config.scenario_sheet
                if "../../scenarios/scen" in file_name
                else config.model.inputs_sheet if sheet_name != "Global" else sheet_name
            )
            for sheet_name, file_name in zip(element.tabs, element.files)
        ]
        # Select he input files from the agrregation
        element.files = [
            (
                scen_file
                if file_name.startswith("../../scenarios/")
                else file_name.replace("../", input_folder)
            )
            for file_name in element.files
        ]

    return model


def load_model(
    aggregation: str = "14sectors_cat",
    region: str = "pymedeas_w",
    data_files: Union[list, None] = None,
) -> Model:
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
