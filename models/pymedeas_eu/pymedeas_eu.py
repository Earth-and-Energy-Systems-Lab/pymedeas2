"""
Python model 'pymedeas_eu.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np
import xarray as xr

from pysd.py_backend.functions import (
    xidz,
    invert_matrix,
    step,
    zidz,
    integer,
    sum,
    if_then_else,
)
from pysd.py_backend.statefuls import SampleIfTrue, Initial, DelayFixed, Integ
from pysd.py_backend.external import ExtLookup, ExtData, ExtConstant
from pysd.py_backend.data import TabData
from pysd.py_backend.utils import load_modules, load_model_data
from pysd import Component

__pysd_version__ = "3.14.2"

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
    name="FINAL_TIME", units="year", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL_TIME", units="year", comp_type="Constant", comp_subtype="Normal"
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
    name="TIME_STEP",
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

# load modules from modules_pymedeas_eu directory
exec(load_modules("modules_pymedeas_eu", _modules, _root, []))


@component.add(
    name="Pipeline_transport_evolution",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_pipeline_transport_fecgl_in_2015": 1, "fec_gasesliquids": 1},
)
def pipeline_transport_evolution():
    """
    Pipeline transport. IEA definition: Pipeline transport includes energy used in the support and operation of pipelines transporting gases, liquids, slurries and other commodities, including the energy used for pump stations and maintenance of the pipeline.
    """
    return share_pipeline_transport_fecgl_in_2015() * fec_gasesliquids()
