import pytest
import pysd
import json

from pytools.config import Params, ModelArguments, Model, ParentModel
from run import main


@pytest.fixture(scope="session")
def default_vars(proj_folder):
    """Get default vars from each model"""
    with open(proj_folder.joinpath("pytools/models.json")) as json_file:
        data = json.load(json_file)

    new_dict = {}
    for key, value in data.items():
        new_dict[key] = value["out_default"]

    return new_dict


def select_model(tmp_dir, proj_folder, model, default_vars):
    """Select model configuration"""
    config = Params(
        model_arguments=ModelArguments(
            initial_time=1995.0,
            time_step=0.1,
            final_time=1995.1,
            return_timestamp=1.0,
            update_params=None,
            update_initials={},
            return_columns=["default"],
            results_fname="",
            results_fpath="",
            export=None
        ),
        region="",
        silent=True,
        headless=True,
        missing_values="ignore",
        scenario_sheet="BAU",
        plot=False,
        progress=False,
        model=None
    )

    if model == "pymedeas_w":
        config.model_arguments.results_fname = "w.csv"
        config.model_arguments.results_fpath =\
            tmp_dir.joinpath(config.model_arguments.results_fname)
        config.region = model
        config.model = Model(
            model_file=proj_folder.joinpath(
                "models/pymedeas_w/pymedeas_w.py"),
            out_folder=tmp_dir,
            out_default=default_vars[model],
            parent=[]
        )
    elif model == "pymedeas_eu":
        config.model_arguments.results_fname = "eu.csv"
        config.model_arguments.results_fpath =\
            tmp_dir.joinpath(config.model_arguments.results_fname)
        config.region = model
        config.model = Model(
            model_file=proj_folder.joinpath(
                "models/pymedeas_eu/pymedeas_eu.py"),
            out_folder=tmp_dir,
            out_default=default_vars[model],
            parent=[
                ParentModel(
                    name="pymedeas_w",
                    default_results_folder=tmp_dir,
                    results_file_path=tmp_dir.joinpath("w.csv")
                )
            ]
        )
    elif model == "pymedeas_cat":
        config.model_arguments.results_fname = "cat.csv"
        config.model_arguments.results_fpath =\
            tmp_dir.joinpath(config.model_arguments.results_fname)
        config.region = model
        config.model = Model(
            model_file=proj_folder.joinpath(
                "models/pymedeas_cat/pymedeas_cat.py"),
            out_folder=tmp_dir,
            out_default=default_vars[model],
            parent=[
                ParentModel(
                    name="pymedeas_w",
                    default_results_folder=tmp_dir,
                    results_file_path=tmp_dir.joinpath("w.csv")
                ),
                ParentModel(
                    name="pymedeas_eu",
                    default_results_folder=tmp_dir,
                    results_file_path=tmp_dir.joinpath("eu.csv")
                )
            ]
        )

    # get the data_file paths to load parent outputs
    data_files = [parent.results_file_path for parent in config.model.parent]

    # loading the model object
    return pysd.load(
        config.model.model_file, initialize=False,
        data_files=data_files), config


@pytest.mark.filterwarnings("ignore")
def test_run_three_levels(tmp_path, proj_folder, default_vars):
    """Run of the 3 models in cascade"""

    model, config = select_model(
        tmp_path, proj_folder, "pymedeas_w", default_vars)
    main(config, model)

    model, config = select_model(
        tmp_path, proj_folder, "pymedeas_eu", default_vars)
    main(config, model)

    model, config = select_model(
        tmp_path, proj_folder, "pymedeas_cat", default_vars)
    main(config, model)
