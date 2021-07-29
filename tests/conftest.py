import pytest
import pysd
from pytools.config import read_config, read_model_config
import pandas as pd
from copy import deepcopy
from . import PROJ_FOLDER


@pytest.fixture()
def config():
    # NOTE : it does not have the model configuration loaded at this point
    # (i.e. config.model = None)
    config = read_config()
    return config


###############################################################################
#           DEFAULT CONFIGURATIONS FOR THE THREE REGIONS                      #
###############################################################################

@pytest.fixture()
def default_world(config):
    _new_conf = deepcopy(config)
    # loading default model configurations
    _new_conf = read_model_config(_new_conf)
    return _new_conf


@pytest.fixture()
def default_eu(config):
    _new_conf = deepcopy(config)
    # changing default region to pymedeas_eu
    _new_conf.region = "pymedeas_eu"
    # loading default model configurations for eu
    _new_conf = read_model_config(_new_conf)
    return _new_conf


@pytest.fixture()
def default_aut(config):
    _new_conf = deepcopy(config)
    # changing default region to pymedeas_aut
    _new_conf.region = "pymedeas_aut"
    # loading default model configurations for austria
    _new_conf = read_model_config(_new_conf)
    return _new_conf


###############################################################################
#       DEFAULT CONFIGURATIONS FOR THE THREE REGIONS CHANGING PATHS           #
###############################################################################


@pytest.fixture()
def default_config_world(tmp_path, default_world):
    _new_conf = deepcopy(default_world)
    # setting the default results folder to the tests main folder
    _new_conf.model.out_folder = tmp_path.joinpath(
        "outputs", "pymedeas_w")
    # creating the temporary directory
    _new_conf.model.out_folder.mkdir(parents=True, exist_ok=True)
    return _new_conf


@pytest.fixture()
def default_config_eu(tmp_path, default_eu):
    _new_conf = deepcopy(default_eu)

    # setting the default results folder to the tests main folder
    _new_conf.model.out_folder = tmp_path.joinpath(
        "outputs", "pymedeas_eu")
    # creating the temporary results folder directory
    _new_conf.model.out_folder.mkdir(parents=True, exist_ok=True)

    # setting path to the results file of the parent model (pymedeas_w)
    _new_conf.model.parent[0].default_results_folder = tmp_path.joinpath(
        "outputs", "pymedeas_w")
    # creating the temporary folder for the parent model
    _new_conf.model.parent[0].default_results_folder.mkdir(parents=True,
                                                           exist_ok=True)
    return _new_conf


@pytest.fixture()
def default_config_aut(tmp_path, default_aut):
    _new_conf = deepcopy(default_aut)
    # setting path to the results file of the parent model (pymedeas_w)
    _new_conf.model.parent[0].default_results_folder = tmp_path.joinpath(
        "outputs", "pymedeas_w")
    # creating the temporary folder for the parent model
    _new_conf.model.parent[0].default_results_folder.mkdir(parents=True,
                                                           exist_ok=True)
    # setting path to the results file of the parent model (pymedeas_eu)
    _new_conf.model.parent[1].default_results_folder = tmp_path.joinpath(
        "outputs", "pymedeas_eu")
    # creating the temporary folder for the parent model
    _new_conf.model.parent[1].default_results_folder.mkdir(parents=True,
                                                           exist_ok=True)

    # setting the default results folder to the tests main folder
    _new_conf.model.out_folder = tmp_path.joinpath(
        "outputs", "pymedeas_aut")
    # creating the temporary results folder directory
    _new_conf.model.out_folder.mkdir(parents=True, exist_ok=True)

    return _new_conf


###############################################################################
#                     PySD MODEL OBJECTS                                      #
###############################################################################
# TODO Path objects are transformed to strings cause pysd expects a string
@pytest.fixture()
def world_model():
    model_path = str(PROJ_FOLDER.joinpath(
        "models", "pymedeas_w", "pymedeas_w.py").resolve())
    return pysd.load(model_path, initialize=False)


@pytest.fixture()
def eu_model():
    model_path = str(PROJ_FOLDER.joinpath(
        "models", "pymedeas_eu", "pymedeas_eu.py").resolve())
    return pysd.load(model_path, initialize=False)


@pytest.fixture()
def aut_model():
    model_path = str(PROJ_FOLDER.joinpath(
        "models", "pymedeas_aut", "pymedeas_aut.py").resolve())
    return pysd.load(model_path, initialize=False)


###############################################################################
#                   DEFAUL SIMULATION RESULTS                                 #
###############################################################################


@pytest.fixture()
def default_results():

    df = pd.DataFrame(
        data={"time": [1995.0, 1996.0, 1997.0, 1998.0],
              "a": [1, 2, 3, 4], "b": [5, 6, 7, 8]}).set_index("time")
    yield df

"""
@pytest.fixture()
def default_results_eu(default_config_eu):
    df = pd.read_csv(default_config_eu.model.out_folder.joinpath(
        "results_BAU_1995.0_1996.0_0.03125.csv"), index_col=0).T
    df.index = pd.to_numeric(df.index)

    yield df


@pytest.fixture()
def default_results_aut(default_config_aut):
    df = pd.read_csv(default_config_aut.model.out_folder.joinpath(
        "results_BAU_1995.0_1996.0_0.03125.csv"), index_col=0).T
    df.index = pd.to_numeric(df.index)
    yield df
"""

###############################################################################
#                 PREDEFINED CLI PARAMETERS                                   #
###############################################################################


@pytest.fixture()
def cli_input_long_names():

    cli_args = [
                "--model",
                "pymedeas_eu",
                "--final-time",
                "1996.0",
                "--time-step",
                "2.0",
                "--saveper",
                "5.0",
                "--scen",  # spreadhseet tab where the scenario data is located
                "test_scenario",
                "--ext",  # path of the resuls file of the parent model
                "pymedeas_w:" + \
                "outputs/pymedeas_w/" + \
                "results_BAU_1995.0_1996.0_0.03125.csv",
                "--silent",  # silent
                "--headless",  # headless
                "--fname",  # results file name
                "test_model.csv",
                "--return-columns",  # return columns
                "var1, var2, var3",
                "--export",  # export results to pickle format
                "outputs/exported.pickle",
                "--plot",  # plot results at the end
                "var1=5",
                "var2=7.5",
                "var3=[[1, 2, 3], [4, 5, 6]]",
                "var4:5"
                ]
    return cli_args


@pytest.fixture()
def cli_input_short_names():

    cli_args = [
                "-m",
                "pymedeas_eu",
                "-F",
                "1996.0",
                "-T",
                "2.0",
                "-S",
                "5.0",
                "-x",  # spreadhseet tab where the scenario data is located
                "test_scenario",
                "-f",  # path of the resuls file of the parent model
                "pymedeas_w:" + \
                "outputs/pymedeas_w/" + \
                "results_BAU_1995.0_1996.0_0.03125.csv",
                "-s",  # silent
                "-b",  # headless
                "-n",  # results file name
                "test_model.csv",
                "-r",  # return columns
                "var1, var2, var3",
                "-e",  # export results to pickle format
                "outputs/exported.pickle",
                "-p",  # plot results at the end
                "var1=5",
                "var2=7.5",
                "var3=[[1, 2, 3], [4, 5, 6]]",
                "var4:5"
                ]

    return cli_args


# grouping configurations that do not raise
@pytest.fixture(params=["cli_input_long_names",
                        "cli_input_short_names"])
def cli_input_not_raises(request,
                         cli_input_long_names,
                         cli_input_short_names):
    return {"cli_input_long_names": cli_input_long_names,
            "cli_input_short_names": cli_input_short_names}[request.param]


@pytest.fixture()
def cli_input_incorrect_parent_model_name():
    """
    ValueError should be raised when the user gives an incorrect model name
    when providing the parent results data file.
    """
    cli_args = ["--model",
                "pymedeas_eu",
                "--ext",
                "unexisting_model: tests/test_data/outputs/pymedeas_w/" +
                "results_BAU_1995.0_1996.0_0.03125.csv"]
    return cli_args


@pytest.fixture()
def cli_input_missing_parent_results_file_path():
    # when running eu and country models in silent mode, the user must provide
    # the parent results files to import from cli, otherwise a
    # MissingValueError is raised
    # In this configuration the pymedeas_eu results path is not provided.
    cli_args = ["--model",
                "pymedeas_aut",
                "--silent",
                "--ext",
                "pymedeas_w: tests/test_data/outputs/pymedeas_w/" +
                "results_BAU_1995.0_1996.0_0.03125.csv"
                ]
    return cli_args


# grouping configurations that raise ValueError
@pytest.fixture(params=["cli_input_incorrect_parent_model_name",
                        "cli_input_missing_parent_results_file_path"])
def cli_raises_value_error(request,
                           cli_input_incorrect_parent_model_name,
                           cli_input_missing_parent_results_file_path):
    return {"cli_input_incorrect_parent_model_name":
            cli_input_incorrect_parent_model_name,
            "cli_input_missing_parent_results_file_path":
            cli_input_missing_parent_results_file_path}[request.param]


@pytest.fixture()
def cli_input_invalid_parent_results_file_path():
    # when running eu and country models in silent mode, the user must provide
    # the parent results files to import from cli, otherwise a
    # FileNotFoundError is raised
    # In this configuration the pymedeas_w results path not a valid path.
    cli_args = ["--model",
                "pymedeas_eu",
                "--silent",
                "--ext",
                "pymedeas_w: non_existing_path/pymedeas_w/" +
                "results_BAU_1995.0_1996.0_0.03125.csv"
                ]
    return cli_args


@pytest.fixture()
def config_silent_no_parent_results_paths(default_eu):
    conf = deepcopy(default_eu)
    conf.silent = True
    return conf


###############################################################################
#           EXPECTED CONFIG AFTER CLI INPUT                                   #
###############################################################################


@pytest.fixture()
def expected_conf_cli_input_long_and_short(tmp_path, default_eu):
    # this one should crash the update of the config class, cause the path
    # does not exist

    updated_conf = deepcopy(default_eu)
    updated_conf.scenario_sheet = "test_scenario"
    updated_conf.silent = True
    updated_conf.headless = True
    updated_conf.plot = True
    updated_conf.model_arguments.final_time = 1996.0
    updated_conf.model_arguments.time_step = 2.0
    updated_conf.model_arguments.return_timestamp = 5.0
    updated_conf.model_arguments.return_columns = ["var1", "var2", "var3"]
    updated_conf.model.parent[0].results_file_path = tmp_path.joinpath(
        "outputs", "pymedeas_w", "results_BAU_1995.0_1996.0_0.03125.csv"
        ).resolve()
    updated_conf.model_arguments.export = tmp_path.joinpath(
        "outputs", "exported.pickle").resolve()
    updated_conf.model_arguments.results_fname = "test_model.csv"
    updated_conf.model_arguments.update_params = {"var1": 5.0,
                                                  "var2": 7.5,
                                                  "var3": pd.Series(
                                                      index=[1, 2, 3],
                                                      data=[4, 5, 6])}
    updated_conf.model_arguments.update_initials = {"var4": 5.0}

    return updated_conf


###############################################################################
#                GROUPING DEFAULT CONFIG FOR ALL MODELS                       #
###############################################################################


@pytest.fixture(params=["default_config_world",
                        "default_config_eu",
                        "default_config_aut"])
def config_all_models(
     request, default_config_world, default_config_eu, default_config_aut):
    return {"default_config_world": default_config_world,
            "default_config_eu": default_config_eu,
            "default_config_aut": default_config_aut}[request.param]


@pytest.fixture()
def avoid_output_vars():
    """vars to avoid in the outputs"""
    return ["historic", "delay", "next", "variation", "leontief",
            "ia_matrix", "year", "initial", "aux", "policy", "future"]


@pytest.fixture()
def all_outputs(default_config_world, avoid_output_vars, world_model):
    avoid_vars = avoid_output_vars + default_config_world.model.out_default
    expected_ = sorted([
        world_model.components._namespace[var_name]
        for var_name in world_model._default_return_columns(which='step')
        if all([a_var not in world_model.components._namespace[var_name]
                for a_var in avoid_vars])])

    expected = list(set(expected_ + default_config_world.model.out_default))

    return sorted(expected)
