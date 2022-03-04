"""
Python model 'pymedeas_w.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np
import xarray as xr

from pysd.py_backend.functions import (
    zidz,
    sum,
    xidz,
    step,
    vmin,
    active_initial,
    invert_matrix,
    if_then_else,
    integer,
)
from pysd.py_backend.statefuls import SampleIfTrue, Integ, Initial, DelayFixed
from pysd.py_backend.external import ExtConstant, ExtData, ExtLookup
from pysd.py_backend.utils import load_modules, load_model_data
from pysd import subs

__pysd_version__ = "2.2.1"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent

_namespace, _subscript_dict, _dependencies, _modules = load_model_data(
    _root, "pymedeas_w"
)

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 1995,
    "final_time": lambda: 2050,
    "time_step": lambda: 0.03125,
    "saveper": lambda: 1,
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


def time():
    return __data["time"]()


def final_time():
    """
    Real Name: FINAL TIME
    Original Eqn:
    Units: year
    Limits: (None, None)
    Type: Constant
    Subs: []

    The final time for the simulation.
    """
    return __data["time"].final_time()


def initial_time():
    """
    Real Name: INITIAL TIME
    Original Eqn:
    Units: year
    Limits: (None, None)
    Type: Constant
    Subs: []

    The initial time for the simulation.
    """
    return __data["time"].initial_time()


def saveper():
    """
    Real Name: SAVEPER
    Original Eqn:
    Units: year
    Limits: (0.0, None)
    Type: Constant
    Subs: []

    The frequency with which output is stored.
    """
    return __data["time"].saveper()


def time_step():
    """
    Real Name: TIME STEP
    Original Eqn:
    Units: year
    Limits: (0.0, None)
    Type: Constant
    Subs: []

    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################

# load modules from modules_pymedeas_w directory
exec(load_modules("modules_pymedeas_w", _modules, _root, []))
