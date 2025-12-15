"""
Python model 'pymedeas_cat.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np
import xarray as xr

from pysd.py_backend.functions import (
    sum,
    if_then_else,
    xidz,
    invert_matrix,
    step,
    zidz,
    integer,
)
from pysd.py_backend.statefuls import Integ, Initial, DelayFixed, SampleIfTrue, Smooth
from pysd.py_backend.external import ExtConstant, ExtData, ExtLookup
from pysd.py_backend.data import TabData
from pysd.py_backend.utils import load_model_data, load_modules
from pysd import Component

__pysd_version__ = "3.14.3"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent

_subscript_dict, _modules = load_model_data(_root, "pymedeas_cat")

component = Component()

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


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="year", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="year", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="year",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP",
    units="year",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################

# load modules from modules_pymedeas_cat directory
exec(load_modules("modules_pymedeas_cat", _modules, _root, []))


@component.add(
    name="Initial global energy intensity 2019",
    units="EJ/Tdollars",
    subscripts=["SECTORS and HOUSEHOLDS"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_final_energy_intensity": 1, "mdollar_per_tdollar": 1},
)
def initial_global_energy_intensity_2019():
    """
    Initial global energy intensity by sector 2009
    """
    return (
        sum(
            historic_final_energy_intensity(2019).rename(
                {"final sources": "final sources!"}
            ),
            dim=["final sources!"],
        )
        * mdollar_per_tdollar()
    )
