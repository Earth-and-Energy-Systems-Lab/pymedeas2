#!/usr/bin/env python
"""
This code allows parametrizing, launching and saving the results of the
pymedeas models.
"""
import warnings
import argparse

from typing import List
from pathlib import Path

from pysd.py_backend.model import Model
import pysd

from tools.config import Params
from tools.tools import (get_initial_user_input, update_config_from_user_input,
                         load, create_parent_models_data_file_paths, run)

warnings.filterwarnings("ignore")

# check PySD version
if tuple(int(i) for i in pysd.__version__.split(".")[:2]) < (3, 0):
    raise RuntimeError(
        "\n\n"
        + "The current version of pymedeas models needs at least PySD 3.0"
        + " You are running:\n\tPySD "
        + pysd.__version__
        + "\nPlease update PySD library with your package manager, "
        + "via PyPI or conda-forge."
    )


if __name__ == "__main__":

    # get command line parameters and update paths
    options: argparse.Namespace = get_initial_user_input()

    # read user input and update config
    config: Params = update_config_from_user_input(options)

    # get the data_file paths to load parent outputs
    data_files: List[Path] = create_parent_models_data_file_paths(config)\
        if config.model.parent else []

    # loading the model object
    model: Model = load(config, data_files)

    # create results directory if it does not exist
    Path(config.model.out_folder).mkdir(parents=True, exist_ok=True)

    run(config, model)
