"""
cmdline parser
"""
import json
import re
from pathlib import Path
from ast import literal_eval
import pandas as pd
from argparse import ArgumentParser, Action

from .config import read_config
from ._version import __version__


dict_models = json.load(open(
    Path(__file__).parent.joinpath('models.json')))

parser = ArgumentParser(
    description='MEDEAS models in Python',
    prog='pymedeas')

# getting the default values from the 'config.json' file
config = read_config()


#########################
# functions and actions #
#########################


def check_output(string):
    """
    Checks that out put file ends with .tab or .csv

    """
    if not string.endswith(('.tab', '.csv', '.nc')):
        parser.error(
            f'when parsing {string}'
            '\nThe output file name must be .tab, .csv or .nc...')

    return string


def split_columns(string):
    """
    Splits the return-columns argument or reads it from .txt
    --return-columns 'temperature c, "heat$"' -> ['temperature c', '"heat$"']
    --return-columns my_vars.txt -> ['temperature c', '"heat$"']

    """
    if string.endswith('.txt'):
        with open(string, 'r') as file:
            return [col.rstrip('\n').strip() for col in file]

    return [s.strip() for s in string.split(',')]


def split_vars(string):
    """
    Splits the arguments from new_values.
    'a=5' -> {'a': ('param', 5.)}
    'b=[[1,2],[1,10]]' -> {'b': ('param', pd.Series(index=[1,2], data=[1,10]))}
    'a:5' -> {'a': ('initial', 5.)}

    """
    try:
        if '=' in string:
            # new variable value
            var, value = string.split('=')
            type_ = 'param'

        if ':' in string:
            # initial time value
            var, value = string.split(':')
            type_ = 'initial'

        if all(char.isdigit() or char in [".", ","] for char in value.strip()):
            # value is float
            return {var.strip(): (type_, float(value))}

        # value is series
        assert type_ == 'param'
        value = literal_eval(value)
        assert len(value) == 2
        assert len(value[0]) == len(value[1])
        return {var.strip(): (type_,
                              pd.Series(index=value[0], data=value[1]))}

    except Exception:
        # error
        parser.error(
                f'when parsing {string}'
                '\nYou must use variable=new_value to redefine values or '
                'variable:initial_value to define initial value.'
                'variable must be a model component, new_value can be a '
                'float or a list of two list, initial_value must be a float'
                '...\n')


def check_output_file_paths(string):
    """
    check if the file path is a valid pathlib.Path
    returns a dictionary with parent model names as keys and paths to the
    results files as values
    """
    string = string.replace(" ", "")
    file_list = string.split(",")
    try:
        output_dict = {}
        for model_and_path in file_list:
            model_name, results_path = re.split(r":|=", model_and_path)
            output_dict[model_name] = results_path

        return output_dict

    except ValueError:
        # error
        parser.error(
            f'when parsing {string}'
            '\nYou must use model1:results_path1, model2:results_path2 to'
            ' set custom paths for the outputs of the specified models. '
            'You may also use "=" instead of ":"...\n')


class SplitVarsAction(Action):
    """
    Convert the list of split variables from new_values to a dictionary.
    [{'a': 5.}, {'b': pd.Series(index=[1, 2], data=[1, 10])}] ->
        {'a': 5., 'b': pd.Series(index=[1, 2], data=[1, 10])}
    """
    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        main_dict = {'param': {}, 'initial': {}}
        for var in values:
            for var_name, (type, val) in var.items():
                main_dict[type][var_name] = val
        setattr(namespace, self.dest, main_dict)


################
# main options #
################

parser.add_argument(
    '-v', '--version',
    action='version', version=f'pymedeas models {__version__}')

parser.add_argument(
    '-a', '--aggr', dest='aggregation', default=config.aggregation,
    choices=list(dict_models),
    help='select the sectorial aggregation to use')

parser.add_argument(
    '-m', '--model', dest='region', default=config.region,
    #choices=list(dict_models),
    help='select the model to use')

parser.add_argument(
    '-n', '--fname', dest='results_fname',
    type=check_output, metavar='FILE',
    help='name of the results file, default is '
         'results_{scenario sheet}_{initial time}_{final time}'
         '_{time step}.csv')

parser.add_argument(
    '-r', '--return-columns', dest='return_columns',
    action='store', type=split_columns,
    metavar='\'var1, var2, .., varN\' or FILE (.txt)',
    help='provide the return columns separated by commas or a .txt file'
         ' where each row is a variable, if all is given it will return all'
         ' columns, if default is given it will return default columns,'
         ' if not givemn will ask the user for the columns')

parser.add_argument(
    '-p', '--plot', dest='plot',
    action='store_true', default=config.plot,
    help='opens the plot gui after simulation')


parser.add_argument(
    '-f', '--ext', dest='results_file_path',
    type=check_output_file_paths, metavar='FILE', nargs='+',
    help='path/s of the file/s from which to import results from parent models'
    ', e.g. pymedeas_w: outputs/results_world.csv')

parser.add_argument(
    '-x', '--scen', dest='scenario_sheet',
    type=str, metavar='SHEET', default=config.scenario_sheet,
    help='scenario name (names should be the same as the input file tabs),'
         ' default is \'BAU\'')

parser.add_argument(
    '-e', '--export', dest='export_file',
    type=str, metavar='FILE',
    help='export to a pickle stateful objects states at the end of the '
         'simulation')

parser.add_argument(
    '-i', '--import-initial', dest='import_file',
    type=str, metavar='FILE',
    help='import stateful objects states from a pickle file,'
         'if given initial conditions from var:value will be ignored')

parser.add_argument(
    '-b', '--headless', dest='headless',
    action='store_true', default=config.headless,
    help='headless mode  (only CLI, no GUI)')

parser.add_argument(
    '-s', '--silent', dest='silent',
    action='store_true', default=config.silent,
    help='silent mode. No user input will be required during execution. Useful'
          'when running batch simulations')


###################
# Model arguments #
###################

model_arguments = parser.add_argument_group(
    'model arguments',
    'Modify model control variables.')

model_arguments.add_argument(
    '-F', '--final-time', dest='final_time',
    default=config.model_arguments.final_time,
    action='store', type=float, metavar='VALUE',
    help='modify final year of the simulation, default is {}'.format(
        config.model_arguments.final_time))

model_arguments.add_argument(
    '-T', '--time-step', dest='time_step',
    default=config.model_arguments.time_step,
    action='store', type=float, metavar='VALUE',
    help='modify time step (in years) of the simulation, default is {}'.format(
        config.model_arguments.time_step))

model_arguments.add_argument(
    '-S', '--saveper', dest='return_timestamp',
    default=config.model_arguments.return_timestamp,
    action='store', type=float, metavar='VALUE',
    help='modify time step (in years) of the output, default is '
         '{} year'.format(config.model_arguments.return_timestamp))


#######################
# Warnings and errors #
#######################

warn_err_arguments = parser.add_argument_group(
    'warning and errors arguments',
    'Modify warning and errors management.')

warn_err_arguments.add_argument(
    '--missing-values', dest='missing_values', default=config.missing_values,
    action='store', type=str, choices=['warning', 'raise', 'ignore', 'keep'],
    help='exception with missing values, \'warning\' (default) shows a '
         'warning message and interpolates the values, \'raise\' raises '
         'an error, \'ignore\' interpolates the values without showing '
         'anything, \'keep\' keeps the missing values')


########################
# Positional arguments #
########################

parser.add_argument('new_values',
                    metavar='variable=new_value', type=split_vars,
                    nargs='*', action=SplitVarsAction,
                    help='redefine the value of variable with new value.'
                    'variable must be a model component, new_value can be a '
                    'float or a a list of two list')

# The destionation new_values2 will never used as the previous argument
# is given also with nargs='*'. Nevertheless, the following variable
# is declared for documentation
parser.add_argument('new_values2',
                    metavar='variable:initial_value', type=split_vars,
                    nargs='*', action=SplitVarsAction,
                    help='redefine the initial value of variable.'
                    'variable must be a model stateful element, initial_value'
                    ' must be a float')


#########
# Usage #
#########

parser.usage = parser.format_usage().replace(
    "usage: pymedeas", "python run.py")
