#!/usr/bin/env python
"""
This code allows parametrizing, launching and saving and plotting the
results of the pymedeas models.
"""
import sys
import warnings
import argparse
import platform
import shutil
from typing import List
from pathlib import Path

from pandas import DataFrame
from pysd.py_backend.statefuls import Model
import pysd

import plot_tool
from pytools.config import Params
from pytools.tools import get_initial_user_input,\
                          update_config_from_user_input, \
                          select_scenario_sheet,\
                          create_parent_models_data_file_paths,\
                          select_model_outputs,\
                          run,\
                          store_results_csv


warnings.filterwarnings("ignore")

__author__ = "Oleg Osychenko, Roger Samsó, Eneko Martin"
__maintainer__ = "Eneko Martin"
__status__ = "Development"

# check PySD version
if tuple(int(i) for i in pysd.__version__.split(".")[:2]) < (3, 0):
    raise RuntimeError(
        "\n\n"
        + "The current version of pymedeas models needs at least PySD 3.0"
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

            def not_xlsx(path, names):
                """Return not .xlsx files set"""
                path = Path(path)
                return {
                    name for name in names
                    if path.joinpath(name).is_file()
                    and not name.endswith('.xlsx')
                }

            bundle_dir = Path(__file__).parent
            executable_dir = Path(sys.argv[0]).resolve().parent

            try:
                # copying scenario files
                shutil.copytree(
                    executable_dir.joinpath("scenarios"),
                    bundle_dir.joinpath("scenarios"),
                    dirs_exist_ok=True,
                    ignore=not_xlsx
                )
                # copying model parameters files
                shutil.copytree(
                    executable_dir.joinpath("models"),
                    bundle_dir.joinpath("models"),
                    dirs_exist_ok=True,
                    ignore=not_xlsx
                )
            except shutil.Error as err:
                raise PermissionError(
                    f"\n\nUnable to copy '{err.args[0][0][0]}'...\n"
                    + f"Please, close '{err.args[0][0][0].split('~$')[-1]}'"
                    + " file before running the model.\n\n"
                ) from None

    # create results directory if it does not exist
    Path(config.model.out_folder).mkdir(parents=True, exist_ok=True)

    main(config, model)
