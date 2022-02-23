#!/usr/bin/env python
__author__ = "Oleg Osychenko, Roger Samsó, Eneko Martin"
__maintainer__ = "Eneko Martin"
__status__ = "Development"

"""
This code allows parametrizing, launching and saving and plotting the
results of the pymedeas models.
"""
from pytools.config import Params
import warnings
import pysd
import argparse
from pathlib import Path
import sys
import shutil
import os  # TODO remove this import and use patlib
from typing import List
from pandas import DataFrame

import plot_tool
from pytools.tools import get_initial_user_input,\
                          update_config_from_user_input, \
                          select_scenario_sheet,\
                          create_parent_models_data_file_paths,\
                          select_model_outputs,\
                          run,\
                          store_results_csv

from pysd.py_backend.statefuls import Model

warnings.filterwarnings("ignore")

# check PySD version
if tuple(int(i) for i in pysd.__version__.split(".")) < (2, 2, 0):
    raise RuntimeError(
        "\n\n"
        + "The current version of pymedeas models needs at least PySD 2.2.0"
        + " You are running:\n\tPySD "
        + pysd.__version__
        + "\nPlease update PySD library with your package manager, "
        + "via PyPI or conda-forge."
    )


def main(config: Params, model: Model) -> None:
    """
    Main function for running the model

    Parameters
    ----------
    config: dict
        Configuration parameters.
    run_params: dict
        Simulation parameters.
    model: pysd.Model
        Model object.

    """
    # select scenario sheet
    select_scenario_sheet(model, config.scenario_sheet)

    if not config.model_arguments.return_columns:
        # list of columns that need to be present in the output file
        config.model_arguments.return_columns = select_model_outputs(config,
                                                                     model)
    elif config.model_arguments.return_columns[0] in ['all', 'default']:
        config.model_arguments.return_columns = select_model_outputs(
            config, model, config.model_arguments.return_columns[0])

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # TODO this only copies the scenario files, we should also copy the parameter and data files

        # this is the path of the temporary dir (/tmp/_MEILiKPxz)
        bundle_dir = Path(__file__).parent
        # this is the path from which the pymedeas was called
        curr_dir = Path.cwd()
        if not Path(curr_dir, "scenarios").is_dir():
            print("Please run the executable from its main directory")
            sys.exit(1)

        for file_name in Path(curr_dir, "scenarios").iterdir():
            destination = Path(bundle_dir, "scenarios").joinpath(file_name.name)
            # copy scenario files
            if file_name.is_file():
                shutil.copy(file_name, destination)

    # run the simulation
    stock: DataFrame = run(config, model)

    result_df: DataFrame = store_results_csv(stock, config)

    # running the plot tool
    if config.plot:
        if not config.headless:
            plot_tool.main(config, result_df,
                           f"Current ({config.scenario_sheet})")
        else:
            print(
                '\nWe prevented the plot GUI from popping up, since'
                ' you are in headless mode. To prevent this message'
                ' from showing up again, please either remove the '
                '-p (or --plot) or -b (or --headless) from the simulation '
                'options.\n')


if __name__ == "__main__":

    # get command line parameters and update paths
    options: argparse.Namespace = get_initial_user_input()

    # read user input and update config
    config: Params = update_config_from_user_input(options)

    # get the data_file paths to load parent outputs
    data_files: List[Path] = create_parent_models_data_file_paths(config)\
        if config.model.parent else []

    # loading the model object
    model: Model = pysd.load(
        str(config.model.model_file), initialize=False,
        data_files=data_files)

    # create results directory if it does not exist
    Path(config.model.out_folder).mkdir(parents=True, exist_ok=True)

    main(config, model)
