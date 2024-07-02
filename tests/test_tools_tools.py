import logging
import pytest
from datetime import datetime
import numpy as np
import pandas as pd
from pysd.py_backend.model import Model

import tools.tools as tools

world = [("14sectors_cat", "pymedeas_w")]

eu = [("14sectors_cat", "pymedeas_eu")]

all_regions = [
    ("14sectors_cat", "pymedeas_w"),
    ("14sectors_cat", "pymedeas_eu"),
    ("14sectors_cat", "pymedeas_cat"),
]
sub_regions = [
    ("14sectors_cat", "pymedeas_eu"),
    ("14sectors_cat", "pymedeas_cat"),
]


@pytest.mark.parametrize("aggregation,region", world)
def test_get_initial_user_input_without_arguments(
    mocker, aggregation, region, default_config
):

    mocker.patch("sys.argv", return_value=["run.py"])
    options = tools.get_initial_user_input()
    assert tools.update_config_from_user_input(options) == default_config


@pytest.mark.parametrize(
    "aggregation,region", all_regions, ids=[">".join(region) for region in all_regions]
)
def test_update_config_from_user_input_defaults(aggregation, region, default_config):
    """Update config from user imput"""
    options = tools.get_initial_user_input(["-a", aggregation, "-m", region])
    assert tools.update_config_from_user_input(options) == default_config


@pytest.mark.parametrize(
    "aggregation,region", all_regions, ids=[">".join(region) for region in all_regions]
)
def test_load_model(aggregation, region, default_config):
    """Update config from user imput"""
    model = tools.load_model(aggregation, region)
    assert isinstance(model, Model)


@pytest.mark.parametrize("aggregation,region", eu)
def test_update_config_from_user_input_not_raising(
    cli_input_not_raises, expected_conf_cli_input_long_and_short
):

    # if the parent results folder and the export pickle folder do not exist,
    # it will raise. Therefore they must exist.
    base_tmp_folder = (
        expected_conf_cli_input_long_and_short.model_arguments.export.parent.parent
    )
    results_file_path = base_tmp_folder.joinpath(cli_input_not_raises[11].split(":")[1])
    pickle_file_path = base_tmp_folder.joinpath(cli_input_not_raises[19])
    # creating results folder (hence the pickle folder too, but I leave it
    # there in case the config of the test ever changes)
    results_file_path.parent.mkdir(parents=True, exist_ok=True)
    pickle_file_path.parent.mkdir(parents=True, exist_ok=True)
    # creating results file
    results_file_path.touch(exist_ok=True)

    options = tools.get_initial_user_input(cli_input_not_raises)
    result_config = tools.update_config_from_user_input(
        options, base_path=base_tmp_folder
    )

    for attr in dir(expected_conf_cli_input_long_and_short):
        if not attr.startswith("_") and attr != "model_arguments":
            assert getattr(expected_conf_cli_input_long_and_short, attr) == getattr(
                result_config, attr
            )

    model_args_def = expected_conf_cli_input_long_and_short.model_arguments
    model_args_res = result_config.model_arguments

    for attr in dir(model_args_def):
        if not attr.startswith("_") and attr != "update_params":
            assert getattr(model_args_def, attr) == getattr(model_args_res, attr)

    for key, value in model_args_def.update_params.items():
        if isinstance(value, pd.Series):
            assert model_args_def.update_params[key].equals(
                model_args_res.update_params[key]
            )
        else:
            assert (
                model_args_def.update_params[key] == model_args_res.update_params[key]
            )


def test_update_config_from_user_input_raises_valueerror(cli_raises_value_error):
    with pytest.raises(ValueError):
        options = tools.get_initial_user_input(cli_raises_value_error)
        tools.update_config_from_user_input(options)


def test_update_config_from_user_input_raises_filenotfounderror(
    cli_input_invalid_parent_results_file_path,
):
    with pytest.raises(FileNotFoundError):
        options = tools.get_initial_user_input(
            cli_input_invalid_parent_results_file_path
        )
        tools.update_config_from_user_input(options)


@pytest.mark.parametrize(
    "aggregation,region", sub_regions, ids=[">".join(region) for region in sub_regions]
)
def test_user_select_data_file_headless(mocker, default_config_tmp):

    files = [
        default_config_tmp.model.parent[0].default_results_folder.joinpath(file_name)
        for file_name in ["f1.nc", "f2.nc", "f3.nc"]
    ]
    # creating 3 files
    for val in files:
        val.touch()

    # overriding the builtin input function, to make it return 0
    mocker.patch("builtins.input", return_value="2")
    parent = default_config_tmp.model.parent[0]

    assert tools.user_select_data_file_headless(parent) == files[2]


@pytest.mark.parametrize(
    "aggregation,region", sub_regions, ids=[">".join(region) for region in sub_regions]
)
def test_user_select_data_file_headless_input_number_outside_bounds(
    mocker, default_config_tmp
):

    # overriding the builtin input function, to make it return 0
    mocker.patch("builtins.input", return_value="1500")
    parent = default_config_tmp.model.parent[0]

    with pytest.raises(ValueError):
        tools.user_select_data_file_headless(parent)


@pytest.mark.parametrize(
    "aggregation,region", sub_regions, ids=[">".join(region) for region in sub_regions]
)
def test_user_select_data_file_headless_invalid_input_type(mocker, default_config_tmp):
    """Error when invalid input type for parent files"""

    # overriding the builtin input function, to make it return 0
    mocker.patch("builtins.input", return_value="hello world")
    parent = default_config_tmp.model.parent[0]

    # create results file so it does not raises for missing results files
    file1 = default_config_tmp.model.parent[0].default_results_folder.joinpath(
        "file1.nc"
    )
    file2 = default_config_tmp.model.parent[0].default_results_folder.joinpath(
        "file2.nc"
    )
    file1.touch()
    file2.touch()

    with pytest.raises(SystemExit) as e:
        tools.user_select_data_file_headless(parent)
    assert e.type == SystemExit
    assert e.value.code == 0


@pytest.mark.parametrize(
    "aggregation,region", sub_regions, ids=[">".join(region) for region in sub_regions]
)
def test_user_select_data_file_headless_missing_results_files(default_config_tmp):
    """Error when missing results for parent models"""
    with pytest.raises(ValueError):
        tools.user_select_data_file_headless(default_config_tmp.model.parent[0])


@pytest.mark.parametrize(
    "aggregation,region", sub_regions, ids=[">".join(region) for region in sub_regions]
)
def test_create_parent_models_data_file_paths_silent_no_paths_from_user(
    default_config_tmp,
):
    """
    If running country model in silent mode, the results file paths of the
    parent must be passed from cli, otherwise a SystemExit occurs
    """
    default_config_tmp.silent = True
    with pytest.raises(SystemExit) as e:
        tools.create_parent_models_data_file_paths(default_config_tmp)
    assert e.type == SystemExit
    assert e.value.code == 0


@pytest.mark.parametrize(
    "aggregation,region", sub_regions, ids=[">".join(region) for region in sub_regions]
)
def test_create_parent_models_data_file_paths_no_silent_paths_from_user(
    default_config_tmp,
):
    """
    If running country model and the results file paths of the
    parent are passed from cli. Basically, under this configuration, this
    function should do nothing
    """
    paths = {}
    for parent in default_config_tmp.model.parent:
        paths[parent.name] = parent.default_results_folder / f"file{parent.name}.csv"
        parent.results_file_path = paths[parent.name]

    tools.create_parent_models_data_file_paths(default_config_tmp)

    for parent in default_config_tmp.model.parent:
        assert parent.results_file_path == paths[parent.name]


@pytest.mark.parametrize("headless", [True, False], ids=["headless", "no-headless"])
@pytest.mark.parametrize(
    "aggregation,region", sub_regions, ids=[">".join(region) for region in sub_regions]
)
def test_create_parent_models_data_file_paths_not_silent(
    mocker, headless, default_config_tmp
):
    """test the case were the user did not provide paths through CLI"""
    default_config_tmp.headless = headless
    for parent in default_config_tmp.model.parent:
        filename = f"file_{parent.name}.csv"
        return_path = parent.default_results_folder.joinpath(filename)

        if headless:
            # mock the user_select_data_file_headless function
            mocker.patch(
                "tools.tools.user_select_data_file_headless", return_value=return_path
            )
        else:
            # mock the user_select_data_file_gui function
            mocker.patch(
                "tools.tools.user_select_data_file_gui", return_value=return_path
            )

        assert set(tools.create_parent_models_data_file_paths(default_config_tmp)) == {
            return_path
        }
        assert parent.results_file_path == return_path

        # as we are using a mocker we cannot do more that one return from
        # user_select_data_file_headless
        break


@pytest.mark.parametrize(
    "aggregation,region", sub_regions, ids=[">".join(region) for region in sub_regions]
)
def test_run_no_file_path_from_user(mocker, capsys, default_config_tmp, model):

    # mocking the return of the run method of the pysd Model class
    return_df = pd.DataFrame(data={"a": [1, 2, 3], "b": [4, 5, 6]})
    mocker.patch("pysd.py_backend.model.Model.run", return_value=return_df)

    # configuring parents file paths
    for parent in default_config_tmp.model.parent:
        parent.results_file_path = parent.default_results_folder.joinpath("result1.csv")

    tools.run(default_config_tmp, model)

    out = capsys.readouterr()[0]

    for parent in default_config_tmp.model.parent:
        assert f"External data file for {parent.name}:" in out

    assert (
        default_config_tmp.model_arguments.results_fname
        == "results_{}_{}_{}_{}.nc".format(
            default_config_tmp.scenario_sheet,
            int(default_config_tmp.model_arguments.initial_time),
            int(default_config_tmp.model_arguments.final_time),
            default_config_tmp.model_arguments.time_step,
        )
    )


@pytest.mark.parametrize(
    "aggregation,region", world, ids=[">".join(region) for region in world]
)
def test_run_file_path_from_user(mocker, default_config_tmp, model):

    # mocking the return of the run method of the pysd Model class
    return_df = pd.DataFrame(data={"a": [1, 2, 3], "b": [4, 5, 6]})
    mocker.patch("pysd.py_backend.model.Model.run", return_value=return_df)

    default_config_tmp.model_arguments.results_fname = "results.csv"

    tools.run(default_config_tmp, model)

    assert (
        default_config_tmp.model_arguments.results_fpath
        == default_config_tmp.model.out_folder.joinpath(
            default_config_tmp.model_arguments.results_fname
        )
    )


@pytest.mark.skip(reason="not implemented")
def test_user_select_data_file_gui():
    assert False


def test_rename_existing_file(tmp_path):
    # Create a temporary file
    file_path = tmp_path / "filename.nc"
    file_path.write_text("test content")

    # Get the original creation time
    creation_time = datetime.fromtimestamp(file_path.stat().st_ctime)
    creation_time_str = creation_time.strftime("%Y%m%d")

    # Call the function to rename the existing file
    tools.rename_existing_file(file_path)

    # Construct the expected new file name
    expected_new_file_name = f"filename_{creation_time_str}.nc"
    expected_new_file_path = tmp_path / expected_new_file_name

    # Check that the original file does not exist anymore
    assert not file_path.exists()

    # Check that the renamed file exists
    assert expected_new_file_path.exists()

    # Check the content of the renamed file
    assert expected_new_file_path.read_text() == "test content"
