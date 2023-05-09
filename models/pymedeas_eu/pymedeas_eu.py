"""
Python model 'pymedeas_eu.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np
import xarray as xr

from pysd.py_backend.functions import (
    integer,
    invert_matrix,
    if_then_else,
    step,
    zidz,
    xidz,
    sum,
)
from pysd.py_backend.statefuls import Integ, SampleIfTrue, DelayFixed, Smooth, Initial
from pysd.py_backend.external import ExtConstant, ExtLookup, ExtData
from pysd.py_backend.data import TabData
from pysd.py_backend.utils import load_modules, load_model_data
from pysd import Component

__pysd_version__ = "3.10.0"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent

_subscript_dict, _modules = load_model_data(_root, "pymedeas_eu")

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
    name="FINAL TIME", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Year",
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
    units="Year",
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

# load modules from modules_pymedeas_eu directory
exec(load_modules("modules_pymedeas_eu", _modules, _root, []))


@component.add(
    name="CO2 LULCF",
    units="GtCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"past_trends_co2_lucf": 1},
)
def co2_lulcf():
    """
    CO2 emissions from Land-Use Change and Forestry.
    """
    return past_trends_co2_lucf()


@component.add(
    name="Cumulative emissions to 1995",
    units="GtC",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_cumulative_emissions_to_1995"},
)
def cumulative_emissions_to_1995():
    """
    Cumulative emissions 1751-1995 due to carbon emissions from fossil fuel consumption, cement production and land-use changes. Data from CDIAC and World Resources Institute.
    """
    return _ext_constant_cumulative_emissions_to_1995()


_ext_constant_cumulative_emissions_to_1995 = ExtConstant(
    "../parameters.xlsx",
    "Europe",
    "cumulative_emissions_to_1995",
    {},
    _root,
    {},
    "_ext_constant_cumulative_emissions_to_1995",
)


@component.add(
    name="Past trends CO2 LUCF",
    units="GtCO2",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_past_trends_co2_lucf",
        "__data__": "_ext_data_past_trends_co2_lucf",
        "time": 1,
    },
)
def past_trends_co2_lucf():
    """
    Historic CO2 emissions from Land-Use Change and Forestry.
    """
    return _ext_data_past_trends_co2_lucf(time())


_ext_data_past_trends_co2_lucf = ExtData(
    "../land.xlsx",
    "Europe",
    "time",
    "historic_co2_emissions_from_land_use_change_and_forestry",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_past_trends_co2_lucf",
)
