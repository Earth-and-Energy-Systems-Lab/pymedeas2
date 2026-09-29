"""
Python model 'pymedeas_w.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np
import xarray as xr

from pysd.py_backend.functions import (
    invert_matrix,
    sum,
    if_then_else,
    xidz,
    zidz,
    active_initial,
    step,
)
from pysd.py_backend.statefuls import Integ, Initial, DelayFixed, SampleIfTrue
from pysd.py_backend.external import ExtConstant, ExtLookup, ExtData
from pysd.py_backend.utils import load_modules, load_model_data
from pysd import Component

__pysd_version__ = "3.14.3"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent

_subscript_dict, _modules = load_model_data(_root, "pymedeas_w")

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

# load modules from modules_pymedeas_w directory
exec(load_modules("modules_pymedeas_w", _modules, _root, []))


@component.add(
    name="mode shar pkm policy last year",
    subscripts=["Transport Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"start_year_policies_transport": 1, "mode_share_pkm_policy": 1},
)
def mode_shar_pkm_policy_last_year():
    return mode_share_pkm_policy(start_year_policies_transport())


@component.add(
    name="sensitivity rail mode share", comp_type="Constant", comp_subtype="Normal"
)
def sensitivity_rail_mode_share():
    return 0


@component.add(name="end historical pkm", comp_type="Constant", comp_subtype="Normal")
def end_historical_pkm():
    return 2023


@component.add(
    name="mode share pkm policy",
    subscripts=["Transport Modes"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_mode_share_pkm_policy",
        "__lookup__": "_ext_lookup_mode_share_pkm_policy",
    },
)
def mode_share_pkm_policy(x, final_subs=None):
    return _ext_lookup_mode_share_pkm_policy(x, final_subs)


_ext_lookup_mode_share_pkm_policy = ExtLookup(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "Year_transport_share",
    "pkm_share",
    {"Transport Modes": _subscript_dict["Transport Modes"]},
    _root,
    {"Transport Modes": _subscript_dict["Transport Modes"]},
    "_ext_lookup_mode_share_pkm_policy",
)


@component.add(
    name="mode share pkm aux",
    subscripts=["Transport Modes"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "mode_share_pkm_policy": 1,
        "sensitivity_rail_mode_share": 1,
    },
)
def mode_share_pkm_aux():
    return xr.DataArray(
        float(
            np.maximum(
                0,
                float(
                    np.minimum(
                        1,
                        float(mode_share_pkm_policy(time()).loc["Rail"])
                        + sensitivity_rail_mode_share(),
                    )
                ),
            )
        ),
        {"Transport Modes": _subscript_dict["Transport Modes"]},
        ["Transport Modes"],
    )
