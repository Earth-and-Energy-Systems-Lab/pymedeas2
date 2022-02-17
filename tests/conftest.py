import pytest
from pathlib import Path

from copy import deepcopy
import pandas as pd
import pysd

from pytools.config import read_config, read_model_config


@pytest.fixture(scope="session")
def proj_folder():
    """main folder"""
    return Path(__file__).parent.parent.resolve()


@pytest.fixture(scope="session")
def config():
    """read model configuration"""
    # NOTE : it does not have the model configuration loaded at this point
    # (i.e. config.model = None)
    config = read_config()
    return config


@pytest.fixture(scope="function")
def default_config(config, region):
    """create the default config"""
    _new_conf = deepcopy(config)
    # changing default region
    _new_conf.region = region
    # loading default model configurations
    return read_model_config(_new_conf)


@pytest.fixture(scope="function")
def default_config_tmp(tmp_path, default_config, region):
    """create the default config with tmp_paths"""

    # setting the default results folder to the tests main folder
    default_config.model.out_folder = tmp_path.joinpath(
        "outputs", region)
    # creating the temporary results folder directory
    default_config.model.out_folder.mkdir(parents=True, exist_ok=True)

    # setting path to the results file of the parent model (pymedeas_w)
    for parent in default_config.model.parent:
        parent.default_results_folder = tmp_path.joinpath(
        "outputs", parent.name)
        parent.default_results_folder.mkdir(parents=True, exist_ok=True)

    return default_config


@pytest.fixture()
def model(proj_folder, default_config):
    """pysd model object"""
    return pysd.load(proj_folder.joinpath(default_config.model.model_file),
                     initialize=False)


@pytest.fixture()
def doc(model):
    """return model documentation"""
    def clean_name(name):
        """Remove outside commas from variables"""
        if name.startswith('"') and name.endswith('"'):
            return name[1:-1]
        else:
            return name

    doc = model.doc()
    doc["Clean Name"] = doc["Real Name"].apply(clean_name)

    return doc


###############################################################################
#                   DEFAUL SIMULATION RESULTS                                 #
###############################################################################


@pytest.fixture()
def default_results():

    df = pd.DataFrame(
        data={"time": [1995.0, 1996.0, 1997.0, 1998.0],
              "a": [1, 2, 3, 4], "b": [5, 6, 7, 8]}).set_index("time")
    yield df

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
                "pymedeas_cat",
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


###############################################################################
#           EXPECTED CONFIG AFTER CLI INPUT                                   #
###############################################################################


@pytest.fixture()
def expected_conf_cli_input_long_and_short(tmp_path, default_config):
    # this one should crash the update of the config class, cause the path
    # does not exist

    updated_conf = deepcopy(default_config)
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


@pytest.fixture(scope="session")
def avoid_output_vars():
    """vars to avoid in the outputs"""
    return ["historic", "delay", "next", "variation", "leontief",
            "ia_matrix", "year", "initial", "aux", "policy", "future"]


@pytest.fixture()
def all_outputs(default_config, avoid_output_vars, model):
    """Get all possible output list from a model"""
    avoid_vars = avoid_output_vars + default_config.model.out_default
    expected_ = sorted([
        model.components._namespace[var_name]
        for var_name in model._default_return_columns(which='step')
        if all([a_var not in model.components._namespace[var_name]
                for a_var in avoid_vars])])

    expected = list(set(expected_ + default_config.model.out_default))

    return sorted(expected)
