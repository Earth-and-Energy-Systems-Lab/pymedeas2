import pytest
import os
import time
from tests.__init__ import ROOT_DIR

from importlib.machinery import SourceFileLoader
from importlib import import_module
tools = import_module("toolbox.tools", ROOT_DIR)


@pytest.fixture(scope="module")
def results_file(tmpdir):
    os.system("touch {}".format(os.path.join(tmpdir, "results.csv")))


@pytest.fixture()
def conf(tmpdir):
    return {
        'model_name': '',
        'time': time.strftime('%H:%M'),
        'silent': False,
        'verbose': False,
        'return_timestep': 1.0,  # results will be stored every year
        'scenario_sheet': 'BAU',
        'plot': False,
        'run_params': {},
        'update_params': {},
        'folder': tmpdir
    }


def test_naming_results_file1(conf):
    assert tools._results_naming(conf, 'results', 'csv') == os.path.join(conf['folder'],'results.csv')
    assert tools._results_naming(conf, 'hello_world', 'txt') == os.path.join(conf['folder'],'hello_world.txt')
    os.system("touch {}".format(os.path.join(conf['folder'], "results.csv")))
    tools._results_naming(conf, 'results', 'csv')
    assert os.path.isfile(os.path.join(conf['folder'],'results_old.csv')) == True
    tools._results_naming(conf, 'results', 'csv')
    assert os.path.isfile(os.path.join(conf['folder'],'results_old_old.csv')) == True


