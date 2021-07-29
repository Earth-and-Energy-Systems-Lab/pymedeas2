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
import pathlib

import plot_tool
from pytools.tools import get_initial_user_input,\
                          update_config_from_user_input, \
                          select_scenario_sheet,\
                          create_parent_models_data_file_paths,\
                          load_external_data,\
                          select_model_outputs,\
                          run,\
                          store_results_csv
from pysd.py_backend.functions import Model

warnings.filterwarnings("ignore")


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

    # updating from World model and others, used in regional models
    if config.model.parent:  # only pymedeas_w does not have a parent model
        create_parent_models_data_file_paths(config)
        update_pars = load_external_data(config,
                                         model.components._subscript_dict,
                                         model.components._namespace)

        if config.model_arguments.update_params:
            config.model_arguments.update_params.update(update_pars)
        else:
            config.model_arguments.update_params = update_pars

    if not config.model_arguments.return_columns:
        # list of columns that need to be present in the output file
        config.model_arguments.return_columns = select_model_outputs(config,
                                                                     model)
    elif config.model_arguments.return_columns[0] in ['all', 'default']:
        config.model_arguments.return_columns = select_model_outputs(
            config, model, config.model_arguments.return_columns[0])

    # run the simulation
    stock = run(config, model)

    result_df = store_results_csv(stock, config)

    # running the plot tool
    if config.plot:
        if not config.headless:
            plot_tool.main(config.model.out_folder, result_df,
                           config.scenario_sheet)
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

    # loading the model object
    model: Model = pysd.load(str(config.model.model_file), initialize=False)

    # create results directory if it does not exist
    pathlib.Path(config.model.out_folder).mkdir(parents=True, exist_ok=True)

    main(config, model)
