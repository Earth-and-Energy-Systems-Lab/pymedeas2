import logging
import pytest
from datetime import datetime
import numpy as np
import pandas as pd
from pysd.py_backend.model import Model

import pytools.tools as tools

world = [
    ("14sectors_cat", "pymedeas_w")
]
all_regions = [
    ("14sectors_cat", "pymedeas_w"),
    ("14sectors_cat", "pymedeas_eu"),
    ("14sectors_cat", "pymedeas_cat"),
    ("16sectors_qb", "pymedeas_w"),
    ("16sectors_qb", "pymedeas_qb")
]
sub_regions = [
    ("14sectors_cat", "pymedeas_eu"),
    ("14sectors_cat", "pymedeas_cat"),
    ("16sectors_qb", "pymedeas_qb")
]


@pytest.mark.parametrize(
    "aggregation,region",
    all_regions,
    ids=[">".join(region) for region in all_regions]
)
def test_update_config_from_user_input_defaults(aggregation,
                                                region, default_config):
    """Update config from user imput"""
    options = tools.get_initial_user_input(["-a", aggregation, "-m", region])
    assert tools.update_config_from_user_input(options) == default_config


@pytest.mark.parametrize(
    "aggregation,region",
    all_regions,
    ids=[">".join(region) for region in all_regions]
)
def test_load_model(aggregation, region, default_config):
    """Update config from user imput"""
    model = tools.load_model(aggregation, region)
    assert isinstance(model, Model)


@pytest.mark.parametrize(
    "aggregation,region",
    [("14sectors_cat", "pymedeas_eu")]
)
def test_update_config_from_user_input_not_raising(
      cli_input_not_raises, expected_conf_cli_input_long_and_short):

    # if the parent results folder and the export pickle folder do not exist,
    # it will raise. Therefore they must exist.
    base_tmp_folder = expected_conf_cli_input_long_and_short. \
                    model_arguments.export.parent.parent
    results_file_path = base_tmp_folder.joinpath(
        cli_input_not_raises[11].split(":")[1])
    pickle_file_path = base_tmp_folder.joinpath(cli_input_not_raises[19])
    # creating results folder (hence the pickle folder too, but I leave it
    # there in case the config of the test ever changes)
    results_file_path.parent.mkdir(parents=True, exist_ok=True)
    pickle_file_path.parent.mkdir(parents=True, exist_ok=True)
    # creating results file
    results_file_path.touch(exist_ok=True)

    options = tools.get_initial_user_input(cli_input_not_raises)
    result_config = tools.update_config_from_user_input(
        options, base_path=base_tmp_folder)

    for attr in dir(expected_conf_cli_input_long_and_short):
        if not attr.startswith("_") and attr != "model_arguments":
            assert getattr(expected_conf_cli_input_long_and_short, attr) == \
                    getattr(result_config, attr)

    model_args_def = expected_conf_cli_input_long_and_short.model_arguments
    model_args_res = result_config.model_arguments

    for attr in dir(model_args_def):
        if not attr.startswith("_") and attr != "update_params":
            assert getattr(model_args_def, attr) == \
                        getattr(model_args_res, attr)

    for key, value in model_args_def.update_params.items():
        if isinstance(value, pd.Series):
            assert model_args_def.update_params[key].equals(
                model_args_res.update_params[key])
        else:
            assert model_args_def.update_params[key] == \
                model_args_res.update_params[key]


def test_update_config_from_user_input_raises_valueerror(
      cli_raises_value_error):
    with pytest.raises(ValueError):
        options = tools.get_initial_user_input(
             cli_raises_value_error)
        tools.update_config_from_user_input(options)


def test_update_config_from_user_input_raises_filenotfounderror(
      cli_input_invalid_parent_results_file_path):
    with pytest.raises(FileNotFoundError):
        options = tools.get_initial_user_input(
             cli_input_invalid_parent_results_file_path)
        tools.update_config_from_user_input(options)


@pytest.mark.parametrize(
    "aggregation,region",
    all_regions,
    ids=[">".join(region) for region in all_regions]
)
def test__rename_old_simulation_results_file_exists(default_config_tmp):
    """Rename old simulations results"""
    file_path = default_config_tmp.model.out_folder.joinpath(
        "results_BAU_1995.0_1996.0_0.03125.csv")
    folder = file_path.parent
    fname = file_path.stem
    extension = file_path.suffix

    # creating the file in the tmp_path to simulate it already exists
    file_path.touch()

    # updating the config with the file path
    default_config_tmp.model_arguments.results_fpath = file_path

    # storing the creation time of the file
    creation_time: str = datetime.fromtimestamp(
        file_path.stat().st_ctime).strftime("%Y%m%d__%H%M%S")

    tools._rename_old_simulation_results(default_config_tmp)

    new_file_path = folder.joinpath(fname + "_{}".format(creation_time) +
                                    extension)
    # the path in the config remains unchanged
    assert default_config_tmp.model_arguments.results_fpath == file_path
    assert new_file_path.is_file()

@pytest.mark.parametrize(
    "aggregation,region",
    all_regions,
    ids=[">".join(region) for region in all_regions]
)
def test__rename_old_simulation_results_file_not_exists(default_config_tmp):
    """Do not rename old simulations results"""
    original_path = default_config_tmp.model_arguments.results_fpath = \
        default_config_tmp.model.out_folder.joinpath("new_file.csv")

    tools._rename_old_simulation_results(default_config_tmp)

    is_empty = not any(original_path.parent.iterdir())

    # no file was written
    assert is_empty
    # the path in the config remains unchanged
    assert default_config_tmp.model_arguments.results_fpath == original_path


@pytest.mark.parametrize(
    "aggregation,region",
    world,
    ids=[">".join(region) for region in world]
)
def test_store_results_csv(mocker, caplog, default_config_tmp,
                           default_results):

    # set the path of the results file to a tmp_path
    default_config_tmp.model_arguments.results_fpath = \
        default_config_tmp.model.out_folder.joinpath(
            "test_random_results.csv")

    # mock the function so it just returns the default results file path
    mocker.patch('pytools.tools._rename_old_simulation_results',
                 return_value=default_config_tmp)

    with caplog.at_level(logging.INFO):
        tools.store_results_csv(default_results, default_config_tmp)
        assert caplog.messages[0].startswith('Simulation results file is')

    assert default_config_tmp.model.out_folder.joinpath(
        'last_output.txt').is_file()
    assert default_config_tmp.model_arguments.results_fpath.is_file()


@pytest.mark.parametrize(
    "aggregation,region",
    world,
    ids=[">".join(region) for region in world]
)
def test_store_results_csv_df_has_nans(
     mocker, caplog, default_config_tmp):

    df = pd.DataFrame(data={"a": [1, 2, 3, np.nan], "b": [5, 6, 7, 8]})

    # creating a temporary results file path
    results_file_path = default_config_tmp.model.out_folder.joinpath(
            "test_random_results.csv")

    # set the path of the results file to a tmp_path
    default_config_tmp.model_arguments.results_fpath = results_file_path

    # mock the function so it just returns the default results file path
    mocker.patch('pytools.tools._rename_old_simulation_results',
                 return_value=default_config_tmp)

    with caplog.at_level(logging.WARNING):
        tools.store_results_csv(df, default_config_tmp)
        assert caplog.messages[0].startswith("There are NaN's in the")


@pytest.mark.parametrize(
    "aggregation,region",
    world,
    ids=[">".join(region) for region in world]
)
def test_select_model_outputs_silent(default_config_tmp,
                                     model):

    # when silent, it should get the out vars from the last_output.txt file
    default_config_tmp.silent = True

    # creating the last_output.txt file and writing the defaults on it
    p = default_config_tmp.model.out_folder / "last_output.txt"
    p.write_text("\n".join(default_config_tmp.model.out_default))

    assert sorted(tools.select_model_outputs(
                  default_config_tmp, model)) == \
        sorted(default_config_tmp.model.out_default)


@pytest.mark.parametrize(
    "aggregation,region",
    world,
    ids=[">".join(region) for region in world]
)
def test_select_model_outputs_select_default(default_config_tmp,
                                             model):

    assert sorted(tools.select_model_outputs(
                  default_config_tmp, model, select="default")) == \
        sorted(default_config_tmp.model.out_default)


@pytest.mark.parametrize(
    "aggregation,region",
    world,
    ids=[">".join(region) for region in world]
)
def test_select_model_outputs_comma_separated_variables(mocker,
                                                        default_config_tmp,
                                                        model):
    # when the user passes the list of vars they want in the output as
    # comma separated variabl names
    return_vars = ["ch4_emissions_ctl", "cc_total", "cc_sectoral"]
    # overriding the builtin input function, to make it return the comma
    # separated variable names
    mocker.patch('builtins.input', return_value=", ".join(return_vars))

    assert sorted(tools.select_model_outputs(
                  default_config_tmp, model)) == \
        sorted(return_vars + default_config_tmp.model.out_default)


@pytest.mark.parametrize(
    "aggregation,region",
    world,
    ids=[">".join(region) for region in world]
)
def test_select_model_outputs_comma_separated_variables_with_plus(
     mocker, default_config_tmp, model):

    # when the user passes the list of vars they want in the output as
    # comma separated variabl names with the plus sign
    return_vars = ["ch4_emissions_ctl", "cc_total", "cc_sectoral"]
    # overriding the builtin input function, to make it return the comma
    # separated variable names
    mocker.patch('builtins.input', return_value=", +".join(return_vars))

    # creating the last_output.txt file and writing the defaults on it
    p = default_config_tmp.model.out_folder / "last_output.txt"
    p.write_text("\n".join(default_config_tmp.model.out_default))

    assert sorted(tools.select_model_outputs(
                  default_config_tmp, model)) == sorted(
                      default_config_tmp.model.out_default + return_vars)


@pytest.mark.parametrize(
    "aggregation,region",
    world,
    ids=[">".join(region) for region in world]
)
def test_select_model_outputs_all_outputs_input(mocker,
                                                all_outputs,
                                                default_config_tmp,
                                                model):

    # when the user passes a 0 is that they expect all outputs
    # overriding the builtin input function, to make it return 0
    mocker.patch('builtins.input', return_value="0")

    assert sorted(tools.select_model_outputs(
                  default_config_tmp, model)) == all_outputs


@pytest.mark.parametrize(
    "aggregation,region",
    world,
    ids=[">".join(region) for region in world]
)
def test_select_model_outputs_all_outputs_select_all(all_outputs,
                                                     default_config_tmp,
                                                     model):

    assert sorted(
        tools.select_model_outputs(
                  default_config_tmp,
                  model,
                  select="all")) == all_outputs


@pytest.mark.parametrize(
    "aggregation,region",
    sub_regions,
    ids=[">".join(region) for region in sub_regions]
)
def test_user_select_data_file_headless(mocker, default_config_tmp):

    files = [default_config_tmp.model.parent[0].default_results_folder.joinpath(
             file_name) for file_name in ["f1.csv", "f2.csv", "f3.csv"]]
    # creating 3 files
    for val in files:
        val.touch()

    # overriding the builtin input function, to make it return 0
    mocker.patch('builtins.input', return_value="2")
    parent = default_config_tmp.model.parent[0]

    assert tools.user_select_data_file_headless(parent) == files[2]


@pytest.mark.parametrize(
    "aggregation,region",
    sub_regions,
    ids=[">".join(region) for region in sub_regions]
)
def test_user_select_data_file_headless_input_number_outside_bounds(
     mocker, default_config_tmp):

    # overriding the builtin input function, to make it return 0
    mocker.patch('builtins.input', return_value="1500")
    parent = default_config_tmp.model.parent[0]

    with pytest.raises(ValueError):
        tools.user_select_data_file_headless(parent)


@pytest.mark.parametrize(
    "aggregation,region",
    sub_regions,
    ids=[">".join(region) for region in sub_regions]
)
def test_user_select_data_file_headless_invalid_input_type(
     mocker, default_config_tmp):
    """Error when invalid input type for parent files"""

    # overriding the builtin input function, to make it return 0
    mocker.patch('builtins.input', return_value="hello world")
    parent = default_config_tmp.model.parent[0]

    # create results file so it does not raises for missing results files
    file1 = default_config_tmp.model.parent[0].default_results_folder.joinpath(
        "file1.csv")
    file2 = default_config_tmp.model.parent[0].default_results_folder.joinpath(
        "file2.csv")
    file1.touch()
    file2.touch()

    with pytest.raises(SystemExit) as e:
        tools.user_select_data_file_headless(parent)
    assert e.type == SystemExit
    assert e.value.code == 0


@pytest.mark.parametrize(
    "aggregation,region",
    sub_regions,
    ids=[">".join(region) for region in sub_regions]
)
def test_user_select_data_file_headless_missing_results_files(
     default_config_tmp):
    """Error when missing results for parent models"""
    with pytest.raises(ValueError):
        tools.user_select_data_file_headless(
            default_config_tmp.model.parent[0])


@pytest.mark.parametrize(
    "aggregation,region",
    sub_regions,
    ids=[">".join(region) for region in sub_regions]
)
def test_create_parent_models_data_file_paths_silent_no_paths_from_user(
     default_config_tmp):
    """
    If running country model in silent mode, the results file paths of the
    parent must be passed from cli, otherwise a SystemExit occurs
    """
    default_config_tmp.silent = True
    with pytest.raises(SystemExit) as e:
        tools.create_parent_models_data_file_paths(
            default_config_tmp)
    assert e.type == SystemExit
    assert e.value.code == 0


@pytest.mark.parametrize(
    "aggregation,region",
    sub_regions,
    ids=[">".join(region) for region in sub_regions]
)
def test_create_parent_models_data_file_paths_no_silent_paths_from_user(
     default_config_tmp):
    """
    If running country model and the results file paths of the
    parent are passed from cli. Basically, under this configuration, this
    function should do nothing
    """
    paths = {}
    for parent in default_config_tmp.model.parent:
        paths[parent.name] =\
            parent.default_results_folder / f"file{parent.name}.csv"
        parent.results_file_path = paths[parent.name]

    tools.create_parent_models_data_file_paths(default_config_tmp)

    for parent in default_config_tmp.model.parent:
        assert parent.results_file_path == paths[parent.name]


@pytest.mark.parametrize("headless", [True, False], ids=["headless", "no-headless"])
@pytest.mark.parametrize(
    "aggregation,region",
    sub_regions,
    ids=[">".join(region) for region in sub_regions]
)
def test_create_parent_models_data_file_paths_not_silent(mocker,
                                                         headless,
                                                         default_config_tmp):
    """test the case were the user did not provide paths through CLI"""
    default_config_tmp.headless = headless
    for parent in default_config_tmp.model.parent:
        filename = f"file_{parent.name}.csv"
        return_path = parent.default_results_folder.joinpath(filename)

        if headless:
            # mock the user_select_data_file_headless function
            mocker.patch('pytools.tools.user_select_data_file_headless',
                         return_value=return_path)
        else:
            # mock the user_select_data_file_gui function
            mocker.patch('pytools.tools.user_select_data_file_gui',
                         return_value=return_path)

        assert set(tools.create_parent_models_data_file_paths(default_config_tmp))\
            == {return_path}
        assert parent.results_file_path == return_path

        # as we are using a mocker we cannot do more that one return from
        # user_select_data_file_headless
        break


@pytest.mark.parametrize(
    "aggregation,region",
    sub_regions,
    ids=[">".join(region) for region in sub_regions]
)
def test_run_no_file_path_from_user(mocker, capsys, default_config_tmp, model):

    # mocking the return of the run method of the pysd Model class
    return_df = pd.DataFrame(data={"a": [1, 2, 3], "b": [4, 5, 6]})
    mocker.patch("pysd.py_backend.model.Model.run", return_value=return_df)

    # configuring parents file paths
    for parent in default_config_tmp.model.parent:
        parent.results_file_path = parent.default_results_folder.joinpath(
            "result1.csv")

    tools.run(default_config_tmp, model)

    out = capsys.readouterr()[0]

    for parent in default_config_tmp.model.parent:
        assert f"External data file for {parent.name}:" in out

    assert default_config_tmp.model_arguments.results_fname == \
        "results_{}_{}_{}_{}.csv".format(
                default_config_tmp.scenario_sheet,
                int(default_config_tmp.model_arguments.initial_time),
                int(default_config_tmp.model_arguments.final_time),
                default_config_tmp.model_arguments.time_step
                )


@pytest.mark.parametrize(
    "aggregation,region",
    world,
    ids=[">".join(region) for region in world]
)
def test_run_file_path_from_user(mocker, default_config_tmp, model):

    # mocking the return of the run method of the pysd Model class
    return_df = pd.DataFrame(data={"a": [1, 2, 3], "b": [4, 5, 6]})
    mocker.patch("pysd.py_backend.model.Model.run", return_value=return_df)

    default_config_tmp.model_arguments.results_fname = "results.csv"

    tools.run(default_config_tmp, model)

    assert default_config_tmp.model_arguments.results_fpath == \
        default_config_tmp.model.out_folder.joinpath(
            default_config_tmp.model_arguments.results_fname)


@pytest.mark.skip(reason="not implemented")
def test_user_select_data_file_gui():
    assert False
