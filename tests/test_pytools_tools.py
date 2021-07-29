import logging
from typing import Dict
import pytest
from datetime import datetime
import numpy as np
import pandas as pd
import pathlib

import pytools.tools as tools


def test_update_config_from_user_input_defaults_world(default_world):
    # user does not pass any input
    # I could have mocked the get_initial_user_input function
    options = tools.get_initial_user_input([])
    assert tools.update_config_from_user_input(options) == default_world


def test_update_config_from_user_input_defaults_eu(default_eu):
    options = tools.get_initial_user_input(["-m", "pymedeas_eu"])
    assert tools.update_config_from_user_input(options) == default_eu


def test_update_config_from_user_input_defaults_aut(default_aut):
    options = tools.get_initial_user_input(["-m", "pymedeas_aut"])
    assert tools.update_config_from_user_input(options) == default_aut


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


def test__rename_old_simulation_results_file_exists(config_all_models):

    file_path = config_all_models.model.out_folder.joinpath(
        "results_BAU_1995.0_1996.0_0.03125.csv")
    folder = file_path.parent
    fname = file_path.stem
    extension = file_path.suffix

    # creating the file in the tmp_path to simulate it already exists
    file_path.touch()

    # updating the config with the file path
    config_all_models.model_arguments.results_fpath = file_path

    # storing the creation time of the file
    creation_time: str = datetime.fromtimestamp(
        file_path.stat().st_ctime).strftime("%Y%m%d__%H%M%S")

    tools._rename_old_simulation_results(config_all_models)

    new_file_path = folder.joinpath(fname + "_{}".format(creation_time) +
                                    extension)
    # the path in the config remains unchanged
    assert config_all_models.model_arguments.results_fpath == file_path
    assert new_file_path.is_file()


def test__rename_old_simulation_results_file_not_exists(config_all_models):

    original_path = config_all_models.model_arguments.results_fpath = \
        config_all_models.model.out_folder.joinpath("new_file.csv")

    tools._rename_old_simulation_results(config_all_models)

    is_empty = not any(original_path.parent.iterdir())

    # no file was written
    assert is_empty
    # the path in the config remains unchanged
    assert config_all_models.model_arguments.results_fpath == original_path


def test_store_results_csv(mocker, caplog, default_config_world,
                           default_results):

    # set the path of the results file to a tmp_path
    default_config_world.model_arguments.results_fpath = \
        default_config_world.model.out_folder.joinpath(
            "test_random_results.csv")

    # mock the function so it just returns the default results file path
    mocker.patch('pytools.tools._rename_old_simulation_results',
                 return_value=default_config_world)

    with caplog.at_level(logging.INFO):
        tools.store_results_csv(default_results, default_config_world)
        assert caplog.messages[0].startswith('Simulation results file is')

    assert default_config_world.model.out_folder.joinpath(
        'last_output.txt').is_file()
    assert default_config_world.model_arguments.results_fpath.is_file()


def test_store_results_csv_df_has_nans(
     mocker, caplog, default_config_world):

    df = pd.DataFrame(data={"a": [1, 2, 3, np.nan], "b": [5, 6, 7, 8]})

    # creating a temporary results file path
    results_file_path = default_config_world.model.out_folder.joinpath(
            "test_random_results.csv")

    # set the path of the results file to a tmp_path
    default_config_world.model_arguments.results_fpath = results_file_path

    # mock the function so it just returns the default results file path
    mocker.patch('pytools.tools._rename_old_simulation_results',
                 return_value=default_config_world)

    with caplog.at_level(logging.WARNING):
        tools.store_results_csv(df, default_config_world)
        assert caplog.messages[0].startswith("There are NaN's in the")


def test_select_model_outputs_silent(default_config_world,
                                     world_model):

    # when silent, it should get the out vars from the last_output.txt file
    default_config_world.silent = True

    # creating the last_output.txt file and writing the defaults on it
    p = default_config_world.model.out_folder / "last_output.txt"
    p.write_text("\n".join(default_config_world.model.out_default))

    assert sorted(tools.select_model_outputs(
                  default_config_world, world_model)) == \
        sorted(default_config_world.model.out_default)


def test_select_model_outputs_select_default(default_config_world,
                                             world_model):

    assert sorted(tools.select_model_outputs(
                  default_config_world, world_model, select="default")) == \
        sorted(default_config_world.model.out_default)


def test_select_model_outputs_comma_separated_variables(mocker,
                                                        default_config_world,
                                                        world_model):
    # when the user passes the list of vars they want in the output as
    # comma separated variabl names
    return_vars = ["ch4_emissions_ctl", "cc_total", "cc_sectoral"]
    # overriding the builtin input function, to make it return the comma
    # separated variable names
    mocker.patch('builtins.input', return_value=", ".join(return_vars))

    assert sorted(tools.select_model_outputs(
                  default_config_world, world_model)) == \
        sorted(return_vars + default_config_world.model.out_default)


def test_select_model_outputs_comma_separated_variables_with_plus(
     mocker, default_config_world, world_model):

    # when the user passes the list of vars they want in the output as
    # comma separated variabl names with the plus sign
    return_vars = ["ch4_emissions_ctl", "cc_total", "cc_sectoral"]
    # overriding the builtin input function, to make it return the comma
    # separated variable names
    mocker.patch('builtins.input', return_value=", +".join(return_vars))

    # creating the last_output.txt file and writing the defaults on it
    p = default_config_world.model.out_folder / "last_output.txt"
    p.write_text("\n".join(default_config_world.model.out_default))

    assert sorted(tools.select_model_outputs(
                  default_config_world, world_model)) == sorted(
                      default_config_world.model.out_default + return_vars)


def test_select_model_outputs_all_outputs_input(mocker,
                                                all_outputs,
                                                default_config_world,
                                                world_model):

    # when the user passes a 0 is that they expect all outputs
    # overriding the builtin input function, to make it return 0
    mocker.patch('builtins.input', return_value="0")

    assert sorted(tools.select_model_outputs(
                  default_config_world, world_model)) == all_outputs


def test_select_model_outputs_all_outputs_select_all(all_outputs,
                                                     default_config_world,
                                                     world_model):

    assert sorted(
        tools.select_model_outputs(
                  default_config_world,
                  world_model,
                  select="all")) == all_outputs


def test_load_external_data(default_config_eu, eu_model):

    namespace = eu_model.components._namespace
    subscripts = eu_model.components._subscript_dict

    default_config_eu.model.parent[0].results_file_path = \
        default_config_eu.model.parent[0].default_results_folder.joinpath(
            "results_parent.csv")

    # creating a dummy results csv file for the parent model
    fake_data = {"time": [1995.0, 1996.0]}
    for dic in default_config_eu.model.parent[0].input_vars.values():
        if dic["subs"]:
            if dic["subs"] == ["sectors"]:
                for i in range(1, 10):
                    subs = "[sector_" + str(i) + "]"
                    fake_data.update({dic["name_in_parent"] + subs: [1, 2]})
            if dic["subs"] == ["final sources", "sectors"]:
                for j in range(1, 3):
                    for k in range(1, 10):
                        subs = "[source_" + str(j) + ",sector_" + str(k) + "]"
                        fake_data.update(
                            {dic["name_in_parent"] + subs: [1, 2]})
        else:
            fake_data.update({dic["name_in_parent"]: [1, 2]})

    df = pd.DataFrame(data=fake_data).set_index("time").T
    df.to_csv(default_config_eu.model.parent[0].results_file_path)

    result = tools.load_external_data(config=default_config_eu,
                                      subscripts=subscripts,
                                      namespace=namespace)

    required_vars = [val["name_in_parent"] for val in
                     default_config_eu.model.parent[0].input_vars.values()]

    assert isinstance(result, Dict)
    assert list(set(required_vars) - set(result.keys())) == []


def test_select_scenario_sheet(world_model, default_config_world):

    sheet = default_config_world.scenario_sheet

    # does not return
    assert tools.select_scenario_sheet(world_model, sheet) is None

    assert all(filter(lambda x: x == "Materials",
                      world_model._external_elements[0].sheets))
    assert world_model._external_elements[100].sheets == ["Parameters"]


def test_user_select_data_file_headless(mocker, default_config_eu):

    files = [default_config_eu.model.parent[0].default_results_folder.joinpath(
             file_name) for file_name in ["f1.csv", "f2.csv", "f3.csv"]]
    # creating 3 files
    for val in files:
        val.touch()

    # overriding the builtin input function, to make it return 0
    mocker.patch('builtins.input', return_value="2")
    parent = default_config_eu.model.parent[0]

    assert tools.user_select_data_file_headless(parent) == files[2]


def test_user_select_data_file_headless_input_number_outside_bounds(
     mocker, default_config_eu):

    # overriding the builtin input function, to make it return 0
    mocker.patch('builtins.input', return_value="1500")
    parent = default_config_eu.model.parent[0]

    with pytest.raises(ValueError):
        tools.user_select_data_file_headless(parent)


def test_user_select_data_file_headless_invalid_input_type(
     mocker, default_config_eu):

    # overriding the builtin input function, to make it return 0
    mocker.patch('builtins.input', return_value="hello world")
    parent = default_config_eu.model.parent[0]

    # create results file so it does not raises for missing results files
    file1 = default_config_eu.model.parent[0].default_results_folder.joinpath(
        "file1.csv")
    file2 = default_config_eu.model.parent[0].default_results_folder.joinpath(
        "file2.csv")
    file1.touch()
    file2.touch()

    with pytest.raises(SystemExit) as e:
        tools.user_select_data_file_headless(parent)
    assert e.type == SystemExit
    assert e.value.code == 0


def test_user_select_data_file_headless_missing_results_files(
     default_config_eu):

    with pytest.raises(ValueError):
        tools.user_select_data_file_headless(default_config_eu.model.parent[0])


def test_create_parent_models_data_file_paths_silent_no_paths_from_user(
     config_silent_no_parent_results_paths):
    """
    If running country model in silent mode, the results file paths of the
    parent must be passed from cli, otherwise a SystemExit occurs
    """
    with pytest.raises(SystemExit) as e:
        tools.create_parent_models_data_file_paths(
            config_silent_no_parent_results_paths)
    assert e.type == SystemExit
    assert e.value.code == 0


def test_create_parent_models_data_file_paths_no_silent_paths_from_user(
     default_aut):
    """
    If running country model and the results file paths of the
    parent are passed from cli. Basically, under this configuration, this
    function should do nothing
    """

    path1 = default_aut.model.parent[0].default_results_folder / "file1.csv"
    path2 = default_aut.model.parent[1].default_results_folder / "file2.csv"

    default_aut.model.parent[0].results_file_path = path1
    default_aut.model.parent[1].results_file_path = path2

    tools.create_parent_models_data_file_paths(default_aut)

    assert default_aut.model.parent[0].results_file_path == path1
    assert default_aut.model.parent[1].results_file_path == path2


def test_create_parent_models_data_file_paths_not_silent_headless(mocker,
                                                                  default_eu):
    # here we test the case were the user did not provide paths through CLI

    return_path = default_eu.model.parent[0].default_results_folder.joinpath(
                  "file.csv")
    # mock the user_select_data_file_headless function
    mocker.patch('pytools.tools.user_select_data_file_headless',
                 return_value=return_path)

    default_eu.headless = True
    assert tools.create_parent_models_data_file_paths(default_eu) is None
    assert default_eu.model.parent[0].results_file_path == return_path


def test_create_parent_models_data_file_paths_not_silent_not_headless(
     mocker, default_eu):
    # here we test the case were the user did not provide paths through CLI

    return_path = default_eu.model.parent[0].default_results_folder.joinpath(
                  "file.csv")
    # mock the user_select_data_file_headless function
    mocker.patch(
     'pytools.tools.user_select_data_file_gui', return_value=return_path)

    default_eu.headless = False
    assert tools.create_parent_models_data_file_paths(default_eu) is None
    assert default_eu.model.parent[0].results_file_path == return_path


def test_run_no_file_path_from_user(
     mocker, capsys, default_aut, aut_model):

    # mocking the return of the run method of the pysd Model class
    return_df = pd.DataFrame(data={"a": [1, 2, 3], "b": [4, 5, 6]})
    mocker.patch("pysd.py_backend.functions.Model.run", return_value=return_df)

    # configuring parents file paths
    default_aut.model.parent[0].results_file_path = \
        default_aut.model.parent[0].default_results_folder.joinpath(
            "result1.csv")

    default_aut.model.parent[1].results_file_path = \
        default_aut.model.parent[1].default_results_folder.joinpath(
            "result1.csv")

    _ = tools.run(default_aut, aut_model)

    out, err = capsys.readouterr()

    assert "External data file for pymedeas_eu:" in out

    assert default_aut.model_arguments.results_fname == \
        "results_{}_{}_{}_{}.csv".format(
                default_aut.scenario_sheet,
                default_aut.model_arguments.initial_time,
                default_aut.model_arguments.final_time,
                default_aut.model_arguments.time_step
                )


def test_run_file_path_from_user(mocker, default_world, world_model):

    # mocking the return of the run method of the pysd Model class
    return_df = pd.DataFrame(data={"a": [1, 2, 3], "b": [4, 5, 6]})
    mocker.patch("pysd.py_backend.functions.Model.run", return_value=return_df)

    default_world.model_arguments.results_fname = "results.csv"

    _ = tools.run(default_world, world_model)

    assert default_world.model_arguments.results_fpath == \
        default_world.model.out_folder.joinpath(
            default_world.model_arguments.results_fname)


@pytest.mark.skip(reason="not implemented")
def test_user_select_data_file_gui():
    assert False
