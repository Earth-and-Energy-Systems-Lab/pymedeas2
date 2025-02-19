import pathlib
import sys
from typing import Optional, List, Union
from dataclasses import dataclass
import json
import dacite
from dacite import Config
from . import PROJ_FOLDER


@dataclass
class ModelArguments:  # configurations to send to PySD
    """Holds the model arguments"""
    initial_time: float
    time_step: float
    final_time: float
    return_timestamp: float
    update_params: Optional[dict]  # dict of model pars to update at runtime
    update_initials: Union[dict, str]
    return_columns: Optional[List[str]]
    results_fname: Optional[str]
    results_fpath: Optional[pathlib.Path]
    export: Optional[pathlib.Path]  # export to pickle file


@dataclass
class ParentModel:
    """Holds information about a parent model"""
    name: str
    default_results_folder: pathlib.Path
    results_file_path: Optional[pathlib.Path]  # if user provides it


@dataclass
class Model:
    """Holds the main model parameters"""
    model_file: pathlib.Path
    subscripts_file: str
    scenario_file: str
    inputs_sheet: str
    out_default: List[str]
    parent: Optional[List[ParentModel]]
    out_folder: pathlib.Path = None


@dataclass
class Params:
    """Holds the main parameters for loading a model"""
    model_arguments: ModelArguments
    aggregation: str
    region: str
    silent: bool
    headless: bool
    missing_values: str  # default is 'warning'
    scenario_sheet: str
    plot: bool
    progress: bool  # default is True, not modifiable through CLI
    model: Optional[Model]


def read_config() -> Params:
    """Read main configuration"""
    # default simulation parameters
    # None values are given in argparser.py
    config_path = PROJ_FOLDER / 'pytools' / 'config.json'
    with config_path.open(encoding='utf-8') as params:
        pars = json.load(params)

    # loading general config
    config = dacite.from_dict(data_class=Params, data=pars)

    return config


def read_model_config(config: Params) -> None:
    """Read model configuration"""
    models_path = PROJ_FOLDER / 'pytools' / 'models.json'
    with models_path.open(encoding='utf-8') as mod_pars:
        model_pars = json.load(mod_pars)

    if config.aggregation not in model_pars.keys():
        raise ValueError(
            "Invalid aggregation '" + config.aggregation
            + "'\nAvailable aggregations are:\n\t" + ", ".join(
                list(model_pars)))

    if config.region not in model_pars[config.aggregation].keys():
        raise ValueError(
            "Invalid region name " + config.region
            + "\nAvailable regions are:\n\t" + ", ".join(
                list(model_pars[config.aggregation])))

    # adding the model configuration to the Params object
    config.model = dacite.from_dict(
        data_class=Model,
        data=model_pars[config.aggregation][config.region],
        config=Config(type_hooks={pathlib.Path: PROJ_FOLDER.joinpath})
    )

    # if running in a bundle, write outputs in the user's home directory
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        config.model.out_folder = pathlib.Path.home().joinpath(
            'pymedeas',
            'outputs',
            config.aggregation,
            config.region)
    else:
        config.model.out_folder = PROJ_FOLDER.joinpath(
            'outputs',
            config.aggregation,
            config.region)
