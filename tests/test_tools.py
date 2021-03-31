import pytest
import os
import sys
from datetime import datetime

sys.path.append(os.pardir)
import pytools.tools as tools


@pytest.fixture()
def conf(tmpdir):
    return {
        'region': 'world',
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
        'run_params': {'time_step': 0.03125,
                       'initial_time': 1995,
                       'final_time': 2050},
        'update_params': {},
        'fname': None,
        'folder': tmpdir}

def test_naming_results_file(conf):
    assert tools._results_naming(conf, 'results', 'csv') == os.path.join(conf['folder'], 'results.csv')
    assert tools._results_naming(conf, 'hello_world', 'txt') == os.path.join(conf['folder'],'hello_world.txt')
    os.system("touch {}".format(os.path.join(conf['folder'], "results.csv")))
    tools._results_naming(conf, 'results', 'csv')
    assert os.path.isfile(os.path.join(conf['folder'],'results_old.csv')) == True
    os.system("touch {}".format(os.path.join(conf['folder'], "results.csv")))
    tools._results_naming(conf, 'results', 'csv')
    assert os.path.isfile(os.path.join(conf['folder'],'results_old_old.csv')) == True

def test_update_paths(conf):
    conf['region'] = 'non-existent'
    with pytest.raises(ValueError, match=r"Invalid region name non-existent.*"):
        tools.update_paths(conf)


