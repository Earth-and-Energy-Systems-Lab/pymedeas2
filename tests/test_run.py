import pytest
import json

from tools.config import Params, ModelArguments, Model, ParentModel
from tools.tools import load, run


@pytest.fixture(scope="session")
def default_vars(proj_folder):
    """Get default vars from each model"""
    with open(proj_folder.joinpath("tools/models.json")) as json_file:
        data = json.load(json_file)

    new_dict = {
        aggr: {
            model: values["out_default"]
            for model, values in models.items()
        } for aggr, models in data.items()
    }

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
        aggregation="",
        region="",
        silent=True,
        headless=True,
        missing_values="ignore",
        scenario_sheet="NZP",
        progress=False,
        model=None
    )

    if model == "14pymedeas_w":
        model = "pymedeas_w"
        config.aggregation = "14sectors_cat"
        config.model_arguments.results_fname = "14w.nc"
        config.model_arguments.results_fpath =\
            tmp_dir.joinpath(config.model_arguments.results_fname)
        config.region = model
        config.model = Model(
            model_file=proj_folder.joinpath(
                "models/pymedeas_w/pymedeas_w.py"),
            subscripts_file="_subscripts_pymedeas_w.json",
            inputs_sheet="World",
            scenario_file="scen_w.xlsx",
            out_folder=tmp_dir,
            out_default=default_vars[config.aggregation][model],
            parent=[]
        )
    elif model == "14pymedeas_eu":
        model = "pymedeas_eu"
        config.aggregation = "14sectors_cat"
        config.model_arguments.results_fname = "14eu.nc"
        config.model_arguments.results_fpath =\
            tmp_dir.joinpath(config.model_arguments.results_fname)
        config.region = model
        config.model = Model(
            model_file=proj_folder.joinpath(
                "models/pymedeas_eu/pymedeas_eu.py"),
            subscripts_file="_subscripts_pymedeas_eu.json",
            inputs_sheet="Europe",
            scenario_file="scen_eu.xlsx",
            out_folder=tmp_dir,
            out_default=default_vars[config.aggregation][model],
            parent=[
                ParentModel(
                    name="pymedeas_w",
                    default_results_folder=tmp_dir,
                    results_file_path=tmp_dir.joinpath("14w.nc")
                )
            ]
        )
    elif model == "14pymedeas_cat":
        model = "pymedeas_cat"
        config.aggregation = "14sectors_cat"
        config.model_arguments.results_fname = "14cat.nc"
        config.model_arguments.results_fpath =\
            tmp_dir.joinpath(config.model_arguments.results_fname)
        config.region = model
        config.model = Model(
            model_file=proj_folder.joinpath(
                "models/pymedeas_cat/pymedeas_cat.py"),
            subscripts_file="_subscripts_pymedeas_cat.json",
            scenario_file="scen_cat.xlsx",
            inputs_sheet="Catalonia",
            out_folder=tmp_dir,
            out_default=default_vars[config.aggregation][model],
            parent=[
                ParentModel(
                    name="pymedeas_w",
                    default_results_folder=tmp_dir,
                    results_file_path=tmp_dir.joinpath("14w.nc")
                ),
                ParentModel(
                    name="pymedeas_eu",
                    default_results_folder=tmp_dir,
                    results_file_path=tmp_dir.joinpath("14eu.nc")
                )
            ]
        )

    # get the data_file paths to load parent outputs
    data_files = [parent.results_file_path for parent in config.model.parent]

    # loading the model object
    return load(config, data_files=data_files), config


@pytest.mark.filterwarnings("ignore")
@pytest.mark.parametrize(
    "model", ["14pymedeas_w", "14pymedeas_eu", "14pymedeas_cat"]
    )
def test_run_three_levels_14sectors_cat(tmp_path, proj_folder, default_vars, model):
    """Run of the 3 models in cascade"""

    model, config = select_model(
        tmp_path, proj_folder, model, default_vars)
    run(config, model)
