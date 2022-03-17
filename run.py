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
import platform
import shutil
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

    config.model_arguments.return_columns = sorted([
        "gdppc",
        "temperature_change",
        "total_co2_emissions_gtco2",
        "eroist_system",
        "share_res_electricity_generation",
        "scarcity_final_fuels",
        "tfec_per_capita"
    ])

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

    # if it's bundled, copy user modifiable files to the bundle tempdir
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        if platform.system() != 'Darwin':

            bundle_dir = Path(__file__).parent
            executable_dir = Path(sys.argv[0]).resolve().parent

            # copying scenario files
            shutil.copytree(
                executable_dir.joinpath("scenarios"),
                bundle_dir.joinpath("scenarios"),
                dirs_exist_ok=True
            )
            # copying model parameters files
            shutil.copytree(
                executable_dir.joinpath("models"),
                bundle_dir.joinpath("models"),
                dirs_exist_ok=True
            )

    # create results directory if it does not exist
    Path(config.model.out_folder).mkdir(parents=True, exist_ok=True)

    main(config, model)
