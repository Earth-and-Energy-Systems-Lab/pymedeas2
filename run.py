#!/usr/bin/env python
__author__ = "Oleg Osychenko, Roger Samsó, Eneko Martin"
__maintainer__ = "Eneko Martin"
__status__ = "Development"

"""
This code allows parametrizing, launching and saving and plotting the
results of the pymedeas models.
"""
import os
import warnings

from datetime import datetime

import plot_tool
from pytools.tools import *

warnings.filterwarnings("ignore")


def main(config, run_params):
    """
    Main function for running the model
    """

    # loading the model object
    model = load_model(os.path.join(config['folder'], config['model_py']))

    # select scenario sheet
    select_scenario_sheet(model, config['scenario_sheet'])

    # updating from World model and others, used in regional models
    if config['region'] != 'world':
        create_external_data_files_paths(config)
        update_pars = load_external_data(config,
                                         model.components._subscript_dict,
                                         model.components._namespace)
        for key, val in update_pars.items():
            # update components from parents
            config['update_params'].update({key: val})
            update_model_component(model, key, val)

    # list of columns that need to be present in the output file
    return_columns = select_model_outputs(config, model)

    # run the simulation
    stock = run(config, model, run_params, return_columns)

    result_df = store_results_csv(stock, config, return_columns)

    # running the plot tool
    if config['plot']:
        if not config['headless']:
            plot_tool.main(config['folder'], result_df,
                           config['scenario_sheet'])
        else:
            print(
                '\nWe prevented the plot GUI from popping up, since you are in '
                'headless mode. To prevent this message from showing up again,'
                ' please either remove the -p (plot) or -b (headless) from the'
                ' simulation options.\n')


if __name__ == "__main__":
    # default simulation parameters
    run_params = {'time_step': 0.03125,
                  'initial_time': 1995,
                  'final_time': 2050}

    # default configuration parameters
    config = {'region': 'world',
              'datetime': datetime.now().strftime("%d_%m_%Y_%H_%M"),
              'silent': False,
              'verbose': False,
              'headless': False,
              'extDataFname': '',
              'extDataFilePath': '',
              'return_timestep': 1.0,  # results will be stored every year
              'scenario_sheet': 'BAU',
              'progress': True,
              'plot': False,
              'run_params': run_params,
              'update_params': {},
              'fname': None}

    # get command line parameters and update paths
    get_initial_user_input(config, run_params)
    update_paths(config)

    main(config, run_params)
