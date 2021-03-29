#!/usr/bin/env python
__author__ = "Oleg Osychenko, Roger Samsó"
__maintainer__ = "Roger Samsó"
__status__ = "Development"

"""
This code allows parametrizing, launching and saving and plotting the results of the pymedeas_w.py and pymedeas_eu models.
"""

import plot_tool
from pytools.tools import *
import os
import time
import warnings
warnings.filterwarnings("ignore")


def main(model, config, run_params, **kwargs):

    for key, val in kwargs.items():
        config['update_params'].update({key: val})

    # create path for the python model file
    model_file = os.path.join(config['folder'], config['model_py'])

    # list of columns that need to be present in the output file
    # TODO loading the model in utf should be avoided in further versions
    model_py = read_file(model_file, 'utf-8')
    return_columns = select_model_outputs(config, model_py)

    # run the simulation
    stock = run(config, model, run_params, return_columns)

    result_df = store_results_csv(stock, config, return_columns)

    # running the plot tool
    if config['plot']:
        if not config['headless']:
            plot_tool.main(config['folder'], result_df, config['scenario_sheet'])
        else:
            print('We prevented the plot GUI from popping up, since you are in '
                  'headless mode. To prevent this message from showing up again,'
                  ' please either remove the -p (plot) or -b (headless) from the'
                  ' simulation options')


if __name__ == "__main__":

    # default simulation parameters
    run_params = {'time_step': 0.03125,
                  'initial_time': 1995,
                  'final_time': 2050}

    # default configuration parameters
    config = {'model_name': '',
              'time': time.strftime('%H:%M'),
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

    config = update_paths(config)

    # get command line parameters:
    config, run_params = get_initial_user_input(config, run_params)

    # loading the model object
    model = load_model(os.path.join(config['folder'], config['model_py']))

    # parameters to update (fow now empty)
    new_pars = {}

    # updating from World model used in EU model
    if False:
        config = create_external_data_files_paths(config)
        update_pars, config = load_external_data(config)
        update_pars = new_pars.update(update_pars)

    main(model, config, run_params, **new_pars)

