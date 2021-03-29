#!/usr/bin/env python
__author__ = "Oleg Osychenko, Roger Samsó"
__maintainer__ = "Roger Samsó"
__status__ = "Development"


import re
import pandas as pd
import numpy as np
from pytools.logger.logger import log
import os
import xarray as xr
import pysd
import getopt
import sys
import json
from configparser import ConfigParser

from tkinter import Tk
from tkinter.filedialog import askopenfilename

from pysd.py_backend import functions # do NOT delete this import

import time


def update_paths(config):

    # load configuration file
    conf = ConfigParser()
    conf.read('config.ini')

    # assign region passed by user
    config['region'] = conf.get('inputs', 'MODEL')

    # assign folder where the model file resides (has to have same name than the model file)
    config['folder'] = os.path.join(os.getcwd(), config['region'])

    # reading configuation file inside model folder
    model_conf = ConfigParser()
    model_conf.read(os.path.join(config['folder'], 'config.ini'))

    #config['inputs_file'] = model_conf.get('inputs', 'inputs_file')
    #config['default_inputs_file'] = model_conf.get('inputs', 'default_inputs_file')
    config['model_py'] = config['region'] + '.py'
    # geographical level can be global, europe, country
    #config['geographical_level'] = model_conf.get('inputs', 'geographical_level')

    return config


def get_initial_user_input(config, run_params):
    """
    Ask for user input to update simulation parameters
    Get user input
    :param config: (dict) configuration parameters
    :param run_params: (dict) simulation parameters
    :return: updated conf  and run_params dictionaries according to user inputs
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hspbt:f:r:x:u:n:e:")

        for opt, arg in opts:
            if opt == '-h':
                print('Run run.py module followed by any of the following options:\n'
                    '-h --> help menu \n'
                    '-f --> final year of simulation (default is 2050) \n'
                    '-t --> time step of simulation (in years) (default is 0.03125 years) \n'
                    '-r --> time step of simulation result (in years) (default is 1 value per year) \n'
                    '-s --> silent mode \n'
                    '-b --> headless mode  (only CLI, no GUI) \n'
                    '-p --> opens the plot gui after simulation \n'
                    '-x --> scenario name (names should be the same as the input file tabs) \n'
                    '-n --> name of the results file (default is results_{scenario name}_{initial date}_{final date}_{time-step}.csv)\n'
                    '-e --> file from which to import external data (only applies for the EU model) \n\n'
                    'Use keyword argunemts to set model parameter values, or use the inputs file (e.g. eroi=5)\n'
                      )

                sys.exit()

            elif opt in ("-s", "--silent"):
                config["silent"] = True
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
        log.error("Wrong parameter definition (run 'python run.py -h' to see the description of available parameters)")
        sys.exit()
    return config, run_params


def compare_dataframes(df1, df2):
    """
    Compares two dataframes and gets a list, which contains a list for every row
     in the dataframes, and each of these lists contain the column number of the
      values that are different between the two df's
    :param df1: (dataframe) output of transforming an excel into a dataframe (inputs.xlsx)
    :param df2: (dataframe) output of transforming an excel into a dataframe (inputs_default.xlsx)
    :return: (list) a list for every row in the excel file. Each list contains the column numbers of the values that
    changed from one excel to another
    """

    df = df1[df1.ne(df2)]
    # makes the list of updated cells in the form:
    # elem_id+2=row_index_in_xlsx, when row[elem_id]=[idx_1, idx_2,...]
    lst = []
    for _, row in df.iterrows():
        mask = row.notnull()
        lst += [row[mask].index.tolist()]

    # setting a tolerance value to identify true differences between cells
    tol = 1 / 100000

    diff_list = []
    for row, values in enumerate(lst, 0):
        if values:
            int_list = []
            for val in values:
                if isinstance(df1.iloc[row, val], (int, float)) and isinstance(df2.iloc[row, val], (int, float)):
                    if abs(df1.iloc[row, val] - df2.iloc[row, val]) > tol:
                        int_list.append(val)
                    else:
                        continue
                else:
                    continue
            diff_list.append(int_list)
        else:
            diff_list.append([])

    return diff_list


def read_file(filename, enc='utf-8'):
    """
    This function reads a txt file and encodes it into
    :param filename: (str) name of the file to open
    :param enc: (str) encoding, defaults to utf8
    :return: the file encoded in enc
    """

    try:
        with open(filename, 'r', encoding=enc) as f:
            return f.read()
    except FileNotFoundError:
        raise


def store_results_csv(result, config, return_cols):

    """
    Separates between xarrays and pandas Series in the output of pysd
    Transforms all xarrays into series, with names equal to the name of the
    function and it's index
    Concatenates all results in a dataframe (final_results) which is returned
    Stores a pickle of the final results

    :param result: output from simulation
    :return: final_results (pd.DataFrame)
    """

    # separate between variables represented as pandas Series and those that are xarrays
    xarrays_names = [name for name in result.columns
                     if name in return_cols
                     if any([isinstance(result[name].loc[i], xr.core.dataarray.DataArray) for i in result.index])]

    series_names = [x for x in result.columns if x in return_cols if x not in xarrays_names]

    # df_xarrays is a df that will contain all xarrays disaggregated by indexes, in the form of time-series
    df_xarrays = convert_xarray_df_to_series_df(result[xarrays_names])

    # results_df is a df with only the model outputs that are time series
    results_df = result[series_names].astype(float)

    # concatenating the original df containing only time-series with the new df created from disaggregated xarrays
    final_results = pd.concat([results_df, df_xarrays], axis=1)

    file_path_csv = _results_naming(config, config["fname"], 'csv')

    # storing results to csv file
    final_results.transpose().to_csv(file_path_csv)
    log.info('Simulation results file is located in {}'.format(file_path_csv))

    try:
        with open(os.path.join(config['folder'], 'last_output_conf.txt'), 'w') as f:
            f.write(';'.join(final_results.columns))
    except FileNotFoundError:
        raise

    if final_results.isna().any().any():
        nan_vars = final_results.columns[final_results.isna().any()].tolist()
        log.warning("There are NaN's in the timeseries of the following variables\n\n: {}\n\n, which might indicate convergence issues, try decreasing the time step".format("\n".join(nan_vars)))

    return final_results


def convert_xarray_df_to_series_df(results_xarrays):
    """
    This function accepts a dataframe which contains xarrays in each column and time, and converts it into another
    dataframe with each column being a one-dimensional time-series of the original xarray
    """

    df_xarrays = pd.DataFrame(index=results_xarrays.index)

    # converting each individual xarray into time series
    for col in results_xarrays.columns:

        # b is a dataframe that will be concatenated at each time with the preceeding times
        b = pd.DataFrame()

        dates_nans = {}

        # it may be that for some dates it's an xarray and for some others a float or other. This happens when the
        # initial condition is set as a int or float, but in the following dates it is an xarray. If that happens, a
        # debug warning is sent
        for date in results_xarrays.index:
            a = results_xarrays[col].loc[date]
            if isinstance(a, xr.core.dataarray.DataArray):
                new_data = a.to_dataframe(name=str(date)).astype(float).T
                b = pd.concat([b, new_data], axis=0)
            elif isinstance(a, (int, np.ndarray)) or np.isnan(a):
                log.debug(f"The initial condition for variable {col} should be an xarray instead of a float")
                dates_nans[date] = a  # store the date and the value for
                # later use
            else:
                log.warning("Unknown type {} for {}".format(type(a), a))

        # fix the names of each column, separating subindexes with brackets and adding the name of the variable first
        b = fix_subindex_names_in_xarrays_to_df(b, col)

        if dates_nans:
            for date, value in dates_nans.items():
                b.loc[str(date)] = [value] * len(b.columns)
                b.sort_index(inplace=True, ascending=True)

        df_xarrays = pd.concat([df_xarrays, b], axis=1)

    # removing nans
    df_xarrays = df_xarrays.dropna()

    # converting index values from strings to floats
    df_xarrays.index = list(map(float, df_xarrays.index))

    return df_xarrays


def fix_subindex_names_in_xarrays_to_df(b, variable_name):
    """
    # this loop fixes the names of the columns, which are the sub-index or sub-indexes
    returns the new dataframe with fixed column names
    """

    new_cols = []

    for x in b.columns:
        if isinstance(x, tuple):  # two or more sub-indexes are tuples. Here converted to comma separated strings
            x = ', '.join(x)

        if '[' not in x:  # adding the name of the original variable name plus the sub-indexes between brackets
            new_cols.append(variable_name + '[' + x + ']')
        else:
            new_x = x.replace(']', ',') + x + ']'
            new_cols.append(new_x)

    b.columns = new_cols

    return b


def _results_naming(config, base_name, fmt):
    """This function renames old simulation results with the same name but adding
    _old in the end, or old_old if _old also exists

    :return (str) new file path
    """

    folder = config['folder']

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


def update_ctts(config, cells_updated):

    """

    :param config:
    :param cells_updated:
    :return: two dictionaries:
        updated_params: (dict) contains only the updated parameters (key) and values that will be passed to the pysd.run method

    """

    try:
        with open(os.path.join(config['folder'], 'constants.json'), 'r') as ctts:
            const_cells = json.load(ctts)
    except FileNotFoundError:
        print('constants.json file not found')

    updated_params = {}

    is_cntt = []
    for item in cells_updated:
        if item[0] in const_cells.keys():
            updated_params[const_cells[item[0]]['new_name']] = item[1]
            is_cntt.append(item[0])

    # cells that were updated and that are not constants
    remaining = list(set([cells[0] for cells in cells_updated]) - set(is_cntt))

    return remaining, updated_params


def updated_params_to_file(config, ext):
    """
    Store the new values of the updated params in a file
    :param config: (dict) configuration dictionary
    :param params: (dict) names of params as keys, new values as values
    :param ext: (str) extension of the file
    :return: None
    """
    params = config['update_params']
    file_path_params = _results_naming(config, 'updated_params', ext)

    with open(file_path_params, 'w') as f:
        for func, val in params.items():
            if isinstance(val, pd.Series):
                f.write(func + ',' + str(val.values) + '\n')
                if config['verbose']:
                    print('{}: {}'.format(func, val.values))
            else:
                f.write(func + ',' + str(val) + '\n')
                if config['verbose']:
                    print('{}: {}'.format(func, val))


def select_model_outputs(config, modelpy):


    # these are the outputs that are plot by default in the plot tool.
    # If they were different for different models, the list could be changed depending
    # on the value of config['region']

    if config['region'] == 'pymedeas_w':
        default_outputs = ['tpe_from_res_ej', # total primary energy supply from RES (MToe/Year)
                           'total_extraction_nre_ej', # Annual total extraction of non-renewable energy resources (EJ/Year)
                           'pes_oil_ej',
                           'pes_nat_gas',
                           'extraction_coal_ej',
                           'extraction_uranium_ej',
                           'share_conv_vs_total_gas_extraction',
                           'share_conv_vs_total_oil_extraction',
                           'real_demand_by_sector',
                           'real_total_output_by_sector',
                           'real_final_energy_by_sector_and_fuel',
                           'annual_gdp_growth_rate',
                           'abundance_coal',
                           'abundance_total_nat_gas',
                           'abundance_total_oil',
                           'current_mineral_resources_mt',
                           'current_mineral_reserves_mt',
                           'percent_res_vs_tpes', # Percent of primary energy from RES in the TPES (%)
                           'temperature_change', # Temperature of the Atmosphere and Upper Ocean, relative to preindustrial reference period (degreesC)
                           'total_land_requirements_renew_mha', # Land required for RES power plants and total bioenergy (land competition + marginal lands (MHa)
                           'share_blue_water_use_vs_ar', # Share of blue water used vs accessible runoff water (Dmnl)
                           'gdppc',  # GDP per capita (1995T$ per capita) ($/people)
                           'eroist_system',  # EROI standard of the system (Dmnl)
                           'tfes_intensity_ej_t',# Total final energy intensity (EJ/T$)
                           'real_tfec',  # Real total final energy consumption (EJ)
                           'gdp',  # Global GDP in T1995T$ (T$)
                           'population']  # Population projection (people)
    else:
        default_outputs = []

    #  make the list of 'step'-cached (i.e. functions of time) variables
    # Todo remove this regex, and use the model.compoents attribute
    pattern = re.compile(r"@cache\('step'\)\s*def ([\w\_]*)\(\)")

    all_columns = []
    i = 0
    for m in re.finditer(pattern, modelpy):
        funcname = m.group(1).strip()
        if not funcname.startswith('_'):
            i += 1
            all_columns.append(funcname)

    sorted_list = sorted(list(set(all_columns)))

    if config['silent']:
        col_ind = 'r'
    else:
        for num, var_name in enumerate(sorted_list, 1):
            print('{}: {}'.format(num, var_name))

        message ="\n\nPlease select the desired output variables:" \
                 "\n - 0 for all model variables" \
                 "\n - comma separated numbers from the list above for individual variables (e.g.: 1,4,5)" \
                 "\n - r for the same variables of the last simulation" \
                 "\n - + followed by the variable number to add individual variables to the last simulation output (e.g. +5,+19,+21)" \
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
                return_columns_set = set(list(map(sorted_list.__getitem__, col_indices)) + col_vars)
            except IndexError:
                log.warning('\t\tWrong numerical index, try again...')
                continue

            # check if the variable names are correct
            if return_columns_set.issubset(sorted_list):
                break
            else:
                log.warning('Wrong variable name, try again...')
    col_ind_split = [x.strip(' \t\n\b+') for x in col_ind.split(',')]
    col_indices = [int(x) - 1 for x in col_ind_split if x.isdigit()]
    col_vars = [x for x in col_ind_split if not x.isdigit()]

    return_columns_set = set(list(map(sorted_list.__getitem__, col_indices)) + col_vars)

    if -1 in col_indices:
        return_columns = sorted_list

    elif 'r' in col_vars:
        try:
            with open(os.path.join(config['folder'], 'last_output_conf.txt'), 'r', encoding='utf-8') as f:
                return_columns = sorted([x.strip().split('[')[0] for x in f.readline().split(";")])
        except:
            log.warning("no last configuration, take all vars")
            return_columns = sorted_list
        else:
            log.info('The number and type of output variables of the current '
                     'simulation will be the same as in the previous one.\nIf '
                     'you want to change the number of outputs please remove the'
                     ' "-s" (silent mode) from the options when you run a simulation')

    elif col_ind.lstrip().startswith('+'):
        try:
            with open(os.path.join(config['folder'], 'last_output_conf.txt'), 'r', encoding='utf-8') as f:
                return_columns_set.update([x.strip().split('[')[0] for x in f.readline().split(";")])
        except:
            log.warning("There is no previous simulation available, taking only the given variables instead")
        return_columns = sorted(list(return_columns_set))

    else:
        return_columns = sorted(list(return_columns_set))

    # adding the default variables to the choice of the user
    return_columns = list(set(return_columns + default_outputs))

    with open(os.path.join(config['folder'], 'last_output_conf.txt'), 'w', encoding='utf-8') as f:
        f.write(";".join(return_columns))

    return return_columns


def _chunks(l, n):
    """Yield successive n-sized chunks from a list."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def create_array(model, data, indexes, model_idxs):
    """
    Create and return xarray DataArray
    :param data: (list) data of the xarray
    :param indexes: (list) list of indexes of the matrix
    :param model_idxs: (dict) all indexes of the model
    :return: (xarray.DataArray) resulting xarray
    """
    if len(indexes) == 0:
        time_init = 2015
        time_final = getattr(model.components, 'final_time')()
        times = list(range(time_init, time_final + 1))
        array = pd.Series(data=data, index=times)

    else:
        if len(indexes) == 1:
            values = data
        elif len(indexes) == 2:
            values = (list(_chunks(data, len(model_idxs[indexes[1]]))))
        elif len(indexes) == 3:
            values = list_2_3d_array(data, len(model_idxs[indexes[0]]), len(model_idxs[indexes[1]]), len(model_idxs[indexes[2]]))
        coords = {}
        for x in indexes:
            coords[x] = model_idxs[x]

        array = xr.DataArray(data=values,
                             coords=coords,
                             dims=indexes)
    return array

def update_model_component(model, comp, new_value):
    """
    Creates a new function to replace the old one using the model.components
    method from pysd
    :param model: model object (pysd.model)
    :parameter: name of the component that needs to be changed
    """
    if hasattr(model.components, comp):

        if isinstance(new_value, pd.Series):
            new_value = series2lookup(new_value)

        if isinstance(new_value, str):
            # definition of the new function name
            new_name = "new_{}".format(comp)
            # execution of the new function
            if "lookup" in new_value:
                exec("def {}(x): return {}".format(new_name, new_value))
            else:
                exec("def {}(): return {}".format(new_name, new_value))

            # replacing the old function definition by the new one
            exec("model.components.{} = {}".format(comp, new_name))

        elif isinstance(new_value, (int, float, xr.DataArray)):
            setattr(model.components, comp, lambda: new_value)

        else:
            log.error('Provide a valid data structure')
            sys.exit(0)
    else:
        print('The model does not have a variable called {}'.format(comp))
        sys.exit(0)


def load_model(model_py):
    return pysd.load(os.path.join(model_py), initialize=False)


def run(config, model, run_params, return_columns):
    """

    :param config: (dict) configuration parameters
    :param model: (pysd.model) pysd model object
    :param run_params: (dict) simulation parameters
    :param return_columns: () variables that are to be written in the outputs file
    :return: (pandas.DataFrame) result of the simulation
    """

    # create default file name for the results file (if the user didn't pass any)
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
                                         os.path.join(config['folder'], config["fname"] + ".csv"))

    )
    if config['region'] == 'pymedeas_eu':
        print("- External data file: {}".format(config['extDataFilePath']))

    if config['update_params']:
        print("- Updated parameters:")
        for key, val in config['update_params'].items():
            if isinstance(val, (int, float)):
                print("\t-" + key + ':' + str(val))
            elif isinstance(val, xr.DataArray):
                print("\t-" + key + ':' + str(val.data.tolist()))
            elif isinstance(val, pd.Series):
                print("\t-" + key + ':\n' + str(val.index.tolist()) + '\n' + str(val.values.tolist()) )
            elif isinstance(val, str):
                if "lookup" in val:
                    print("\t-" + key + ':' + val.lstrip("functions.lookup(x, ").strip(")"))
                else:
                    print("\t-" + key + ':' + val)
        print("\n")
    else:
        print("\n")

    if return_columns[0] != '':
        return_columns = return_columns
    else:
        return_columns = None

    if not config['return_timestep'] is None:
        return_timestamps = np.arange(run_params['initial_time'], run_params['final_time'] + 0.01,
                                      float(config['return_timestep']))
    else:
        return_timestamps = None

    print("Starting simulation.")
    sim_start_time = time.time()
    stocks = model.run(run_params, return_columns=return_columns, return_timestamps=return_timestamps, progress=config['progress'])
    sim_time = time.time() - sim_start_time
    log.info(f"Total simulation time: {(sim_time/60.):.2f} minutes")
    stocks.index.name = 'time'

    return stocks


def list_2_3d_array(data, big_index, col_index, row_index):
    """
    Converts a list that represents a 3D matrix in a 3D array
    e.g. [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] -> [[[1, 2, 3],[10, 11, 12]],[[4, 5, 6],[13, 14, 15]],[[7, 8, 9],[16,17,18]]]
    :param big_index (int) length of the index that includes the col_index
    :param col_index (int) length of the index that takes several columns
    :param row_index (int) length of the index that takes several columns
    :return: list of lists representing 3D matrix
    """
    mat3d = []
    r = 0
    for i in range(0, big_index, 1):
        int_list = []
        b = r
        for row in range(row_index):
            small_list = data[b:b+row_index]
            int_list.append(small_list)
            b += col_index * big_index

        mat3d.append(int_list)
        r += row_index
    return mat3d


def user_select_data_file_gui(region):
    """
    Creates a GUI from which the use will be able to select the file from which
    to import external data for the EU model
    :return: (str) path to the file
    """
    defaultDir = os.path.join(os.getcwd(), region)
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename(initialdir=defaultDir, title="Select external data file", filetypes=(('.csv files', '*.csv'), ("All files", '*')))

    return filename


def user_select_data_file_headless(region):

    """
    Asks the user to select the csv file name from which to import data required
    to run the EU model in std output. It looks only in the pymedeas_w folder.
    :return: (str) filename of the file to load and extract data from
    """


    files_list = os.listdir(os.path.join(os.getcwd(), region))

    csv_list = [file for file in files_list if file.endswith('.csv')]

    if csv_list:
        val = input("\nPlease write the number associated with the results file of the {} model from which you "
                    "wish to import data:\n\t".format(region) + "\n\t".join("{}: {}".format(i, j)for i, j in enumerate(csv_list, 0)) + "\n\n here ->")
        try:
            val = int(val)
        except TypeError:
            print('Only numbers allowed')
            sys.exit(0)

        if (val >= 0) and (val < len(csv_list)):
            return csv_list[val]
        else:
            print("Please provide a number between 0 and {}".format(len(csv_list)-1))
            sys.exit(0)

    else:
        print('There are no csv files to import data from. Please run the parent model/s first')
        sys.exit(0)


def create_external_data_files_paths(config):

    """
    This function lists all csv (results) files in the pymedeas_w and/or pymedeas_eu folder/s and asks
    the user to choose one, so that all the external data required by the EU or country model
    can be imported.
    :return: (dict) dictionary containing the external data variable names as keys,
    and the actual data in the form of a string (functions.lookup(x, [...],[...]) as values
    """

    file_paths = {}

    def from_provided_external_file(config):
        """ this creates the file paths of the folders where the external data files to be imported are located
        when the user has provided them as a CLI parameter, after the -e
        """

        if len(config['extDataFname']) == 1:
            if not config['geographical_level'] == 'country':
                file_paths['global'] = os.path.join(os.getcwd(), 'pymedeas_w', config['extDataFname'][0])
            else:
                raise TypeError("Please provide two results files to run the country models, one from the global model and one from the european model")

        elif len(config['extDataFname']) == 2:
            file_paths['global'] = os.path.join(os.getcwd(), 'pymedeas_w', config['extDataFname'][0])
            file_paths['europe'] = os.path.join(os.getcwd(), 'pymedeas_eu', config['extDataFname'][1])
        elif len(config['extDataFname']) > 2:
            raise TypeError("the -e option takes either one or two file names. If you gave two file names, make sure"
                            "to not leave any blank space between them (e.g. file1.csv,file2.cv)")

        # if any of the file paths generated does not exist, kill the execution
        for path in file_paths:
            if not os.path.exists(file_paths.get(path)):
                print('The file {} cannot be found'.format(file_paths.get(path)))
                sys.exit(0)

        return file_paths

    if config['silent']:  # no user input asked during execution, hence external files must be provided beforehand
        if config['extDataFname']:  # external data files names provided
            file_paths = from_provided_external_file(config)
        else:  # silent mode and file names not provided -> error
            print('If you want to run in silent mode, please provide the name '
                  'of the results file/s from which you want to '
                  'import data. Examples below:\n'
                  '-e filename.csv (the file must be in the pymedeas_w folder)\n'
                  '-e filename1.csv,filename2.csv (the first file must be in the pymedeas_w folder and the second in the pymedeas_eu folder)\n')
            sys.exit(0)

    else:  # not silent, user may be asked for input
        if config['headless']:  # no graphical interface can be displayed, only CLI
            if config['extDataFname']:  # use filenames provided by user
                file_paths = from_provided_external_file(config)
            else:  # it won't open a graphical window to select the file but let you chose the file from CLI
                file_paths['global'] = os.path.join(os.getcwd(), 'pymedeas_w',
                                                        user_select_data_file_headless('pymedeas_w'))
                if config['geographical_level'] == 'country':
                    file_paths['europe'] = os.path.join(os.getcwd(), 'pymedeas_eu',
                                                        user_select_data_file_headless('pymedeas_eu'))
                elif len(config['extDataFname']) > 2:
                    raise TypeError("the -e option takes either one or two file names. If you gave two file names, make sure"
                            "to not leave any blank space between them (e.g. file1.csv,file2.cv)")

        else:  # the user will be asked for input and can be graphical
            if not config['extDataFname']:  # the used does not provide filenames when launching simulation
                if config['geographical_level'] == 'europe':
                    file_paths['global'] = user_select_data_file_gui("pymedeas_w")
                elif config['geographical_level'] == 'country':
                    file_paths['global'] = user_select_data_file_gui("pymedeas_w")
                    file_paths['europe'] = user_select_data_file_gui("pymedeas_eu")

            else:  # the user provides the file names
                file_paths = from_provided_external_file(config)

    config['extDataFilePath'] = file_paths

    return config


def load_external_data(config):
    # the user can select the file from which data
    # from World model will be extracted to run the EU model
    dfs = {region: pd.read_csv(path, index_col=0).T for region, path in config['extDataFilePath'].items()}
    dfs['global'].index = pd.to_numeric(dfs['global'].index)

    # loading data from the global model
    real_total_output_by_sector = [col for col in dfs['global'].columns if col.startswith("real_total_output_by_sector")]
    real_final_energy_by_sector_and_fuel = [col for col in dfs['global'].columns if col.startswith("real_final_energy_by_sector_and_fuel")]
    real_demand_by_sector = [col for col in dfs['global'].columns if col.startswith("real_demand_by_sector") and not 'delayed' in col]

    # list of imports for country models
    imports_world = [
                       "temperature_change",
                       "share_e_losses_cc",
                       "total_extraction_nre_ej",
                       "pes_oil_ej",
                       "extraction_coal_ej",
                       "share_conv_vs_total_gas_extraction",
                       "share_conv_vs_total_oil_extraction",
                       #"current_mineral_resources_mt",
                       # <----------- this may be a lookup in the world model, hence not in the output
                       #"current_mineral_reserves_mt",
                       # <----------- this may be a lookup in the world model, hence not in the output
                       "annual_gdp_growth_rate",
                       "abundance_coal",
                       "abundance_total_natx_gas",
                       "abundance_total_oil",
                       "pes_natx_gas",
                       "extraction_uranium_ej"] + \
                   real_demand_by_sector + \
                   real_total_output_by_sector + \
                   real_final_energy_by_sector_and_fuel

    dataDict = {}

    # formatting the data imported from the world model results to replace the hardcoded values
    for var in imports_world:
        try:
            serie = dfs['global'][var]
        except:
            print("Variable {} is not in the results file of the global model, the values will be "
                  "taken from the default BAU scenario".format(var))
        else:
            if '[' in var:
                dataDict[var.replace('[', '_sub').replace(', ', '_sub').replace(' ', '_').rstrip(']')] = series2lookup(serie)
            elif var in ["abundance_coal", "abundance_total_natx_gas", "abundance_total_oil"] and config["region"] == "pymedeas_eu":
                dataDict[var + "_world"] = series2lookup(serie)
            elif config['geographical_level'] == 'country' and var == 'share_conv_vs_total_gas_extraction':
                dataDict[var + "_world"] = series2lookup(serie)
            else:
                dataDict[var] = series2lookup(serie)

    if 'europe' in dfs.keys():  # if there's data to import from the eu model results

        dfs['europe'].index = pd.to_numeric(dfs['europe'].index)

        real_total_output_by_sector_eu = [col for col in dfs['europe'].columns if
                                       col.startswith("real_total_output_by_sector_eu")]
        real_final_energy_by_sector_and_fuel_eu = [col for col in dfs['europe'].columns if
                                                col.startswith("real_final_energy_by_sector_and_fuel_eu")]
        real_final_demand_by_sector_eu = [col for col in dfs['europe'].columns if
                                 col.startswith("real_final_demand_by_sector_eu") and not 'delayed' in col]

        # list of variables in the outputs of the eu model
        imports_europe = [
            "gdp_eu",
            "total_fe_elec_generation_twh_eu",
            "annual_gdp_growth_rate_eu"] + \
            real_final_demand_by_sector_eu +\
            real_final_energy_by_sector_and_fuel_eu +\
            real_total_output_by_sector_eu

        for var in imports_europe:
            try:
                serie = dfs['europe'][var]
            except:
                print("Variable {} is not in the results file of the european model, the values will be "
                      "taken from the default BAU scenario".format(var))
            else:
                if '[' in var:
                    dataDict[
                        var.replace('[', '_sub').replace(', ', '_sub').replace(',', '_sub').replace(' ', '_').rstrip(']')] = series2lookup(
                        serie)
                else:
                    dataDict[var] = series2lookup(serie)

    return dataDict, config


def series2lookup(serie):
    """
    Transformas a pandas DataFrame to a formatted lookup
    :param serie: (pd DataFrame)
    :return: (str)
    """

    dates = ", ".join(serie.index.astype(str))
    values = ",".join(map(str, serie.values.tolist()))

    return "functions.lookup(x,\n [{}],\n [{}])".format(dates, values)


