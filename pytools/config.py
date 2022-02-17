import pathlib
from typing import Optional, List, Union
from dataclasses import dataclass
import json
import dacite
from dacite import Config
from . import PROJ_FOLDER


@dataclass
class ModelArguments:  # configurations to send to PySD
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
    name: str
    default_results_folder: pathlib.Path
    results_file_path: Optional[pathlib.Path]  # if user provides it


@dataclass
class Model:
    model_file: pathlib.Path
    out_folder: pathlib.Path
    out_default: List[str]
    parent: Optional[List[ParentModel]]


@dataclass
class Params:
    model_arguments: ModelArguments
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
    with open(PROJ_FOLDER.joinpath('pytools', 'config.json')) as params:
        pars = json.load(params)

    # loading general config
    config = dacite.from_dict(data_class=Params, data=pars)

    return config


def read_model_config(config) -> Params:
    """Read model configuration"""
    with open(PROJ_FOLDER.joinpath('pytools', 'models.json')) as mod_pars:
        model_pars = json.load(mod_pars)

    if config.region not in model_pars.keys():
        raise ValueError(
            "Invalid region name " + config.region
            + "\nAvailable regions are:\n\t" + ", ".join(
                list(model_pars.keys())))

    # adding the model configuration to the Params object
    config.model = dacite.from_dict(data_class=Model,
                                    data=model_pars[config.region],
                                    config=Config(type_hooks={
                                        pathlib.Path: PROJ_FOLDER.joinpath}))
    return config
