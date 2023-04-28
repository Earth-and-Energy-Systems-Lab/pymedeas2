"""
Python model 'pymedeas_cat.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np
import xarray as xr

from pysd.py_backend.functions import (
    invert_matrix,
    step,
    sum,
    integer,
    zidz,
    xidz,
    if_then_else,
)
from pysd.py_backend.statefuls import Integ, Initial, DelayFixed, SampleIfTrue, Smooth
from pysd.py_backend.external import ExtConstant, ExtLookup, ExtData
from pysd.py_backend.data import TabData
from pysd.py_backend.utils import load_model_data, load_modules
from pysd import Component

__pysd_version__ = "3.9.1"

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

# load modules from modules_pymedeas_cat directory
exec(load_modules("modules_pymedeas_cat", _modules, _root, []))


@component.add(
    name="PED liquids delayed",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_ped_liquids_delayed": 1},
    other_deps={
        "_delayfixed_ped_liquids_delayed": {
            "initial": {"ped_liquids": 1, "time_step": 1},
            "step": {"ped_liquids": 1},
        }
    },
)
def ped_liquids_delayed():
    return _delayfixed_ped_liquids_delayed()


_delayfixed_ped_liquids_delayed = DelayFixed(
    lambda: ped_liquids(),
    lambda: time_step(),
    lambda: ped_liquids(),
    time_step,
    "_delayfixed_ped_liquids_delayed",
)


@component.add(
    name="oil refinery share",
    units="EJ/Year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_oil_refinery_share",
        "__data__": "_ext_data_oil_refinery_share",
        "time": 1,
    },
)
def oil_refinery_share():
    return _ext_data_oil_refinery_share(time())


_ext_data_oil_refinery_share = ExtData(
    "../energy.xlsx",
    "Catalonia",
    "time_historic_imports",
    "Oil_refinery_transformation_loses_share",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_oil_refinery_share",
)


@component.add(
    name="CH4 anthro emissions RCP",
    units="Mton/Year",
    subscripts=["RCP Scenario"],
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_ch4_anthro_emissions_rcp",
        "__data__": "_ext_data_ch4_anthro_emissions_rcp",
        "time": 1,
    },
)
def ch4_anthro_emissions_rcp():
    """
    "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_ch4_anthro_emissions_rcp(time())


_ext_data_ch4_anthro_emissions_rcp = ExtData(
    "../climate.xlsx",
    "Catalonia",
    "year_emissions",
    "CH4_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    _root,
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    "_ext_data_ch4_anthro_emissions_rcp",
)


@component.add(
    name="Choose RCP",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_choose_rcp"},
)
def choose_rcp():
    """
    Choose RCP (Representative Concentration Pathway) 1. RCP 2.6 2. RCP 4.5 3. RCP 6.0 4. RCP 8.5
    """
    return _ext_constant_choose_rcp()


_ext_constant_choose_rcp = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "RCP_selection",
    {},
    _root,
    {},
    "_ext_constant_choose_rcp",
)


@component.add(
    name="energy variation by fuel pkm",
    subscripts=["fuel"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_pkm": 2},
)
def energy_variation_by_fuel_pkm():
    value = xr.DataArray(np.nan, {"fuel": _subscript_dict["fuel"]}, ["fuel"])
    value.loc[["gas"]] = sum(
        energy_pkm()
        .loc["gas", :]
        .reset_coords(drop=True)
        .rename({"Transport Modes pkm": "Transport Modes pkm!"}),
        dim=["Transport Modes pkm!"],
    )
    value.loc[["elect"]] = sum(
        energy_pkm()
        .loc["elect", :]
        .reset_coords(drop=True)
        .rename({"Transport Modes pkm": "Transport Modes pkm!"}),
        dim=["Transport Modes pkm!"],
    )
    return value


@component.add(
    name="HFC emissions",
    units="tons/Year",
    subscripts=["HFC type"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"choose_rcp": 3, "hfc_emissions_rcp": 4},
)
def hfc_emissions():
    """
    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare) Choose RCP: 1. RCP 2.6 2. RCP 4.5 3. RCP 6.0 4. RCP 8.5
    """
    return if_then_else(
        choose_rcp() == 1,
        lambda: hfc_emissions_rcp().loc["RCP26", :].reset_coords(drop=True),
        lambda: if_then_else(
            choose_rcp() == 2,
            lambda: hfc_emissions_rcp().loc["RCP45", :].reset_coords(drop=True),
            lambda: if_then_else(
                choose_rcp() == 3,
                lambda: hfc_emissions_rcp().loc["RCP60", :].reset_coords(drop=True),
                lambda: hfc_emissions_rcp().loc["RCP85", :].reset_coords(drop=True),
            ),
        ),
    )


@component.add(
    name="HFC emissions RCP",
    units="tons/Year",
    subscripts=["RCP Scenario", "HFC type"],
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_hfc_emissions_rcp",
        "__data__": "_ext_data_hfc_emissions_rcp",
        "time": 1,
    },
)
def hfc_emissions_rcp():
    """
    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_hfc_emissions_rcp(time())


_ext_data_hfc_emissions_rcp = ExtData(
    "../climate.xlsx",
    "Catalonia",
    "year_emissions",
    "HFC134a_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC134a"]},
    _root,
    {
        "RCP Scenario": _subscript_dict["RCP Scenario"],
        "HFC type": _subscript_dict["HFC type"],
    },
    "_ext_data_hfc_emissions_rcp",
)

_ext_data_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "Catalonia",
    "year_emissions",
    "HFC23_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC23"]},
)

_ext_data_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "Catalonia",
    "year_emissions",
    "HFC32_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC32"]},
)

_ext_data_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "Catalonia",
    "year_emissions",
    "HFC125_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC125"]},
)

_ext_data_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "Catalonia",
    "year_emissions",
    "HFC143a_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC143a"]},
)

_ext_data_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "Catalonia",
    "year_emissions",
    "HFC152a_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC152a"]},
)

_ext_data_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "Catalonia",
    "year_emissions",
    "HFC227ea_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC227ea"]},
)

_ext_data_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "Catalonia",
    "year_emissions",
    "HFC245ca_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC245ca"]},
)

_ext_data_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "Catalonia",
    "year_emissions",
    "HFC4310mee_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC4310mee"]},
)


@component.add(
    name="N2O Anthro Emissions",
    units="Mton N/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"choose_rcp": 3, "n2o_anthro_emissions_rcp": 4},
)
def n2o_anthro_emissions():
    """
    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare) Choose RCP: 1. RCP 2.6 2. RCP 4.5 3. RCP 6.0 4. RCP 8.5
    """
    return if_then_else(
        choose_rcp() == 1,
        lambda: float(n2o_anthro_emissions_rcp().loc["RCP26"]),
        lambda: if_then_else(
            choose_rcp() == 2,
            lambda: float(n2o_anthro_emissions_rcp().loc["RCP45"]),
            lambda: if_then_else(
                choose_rcp() == 3,
                lambda: float(n2o_anthro_emissions_rcp().loc["RCP60"]),
                lambda: float(n2o_anthro_emissions_rcp().loc["RCP85"]),
            ),
        ),
    )


@component.add(
    name="N2O Anthro Emissions RCP",
    units="Mton N/Year",
    subscripts=["RCP Scenario"],
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_n2o_anthro_emissions_rcp",
        "__data__": "_ext_data_n2o_anthro_emissions_rcp",
        "time": 1,
    },
)
def n2o_anthro_emissions_rcp():
    """
    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_n2o_anthro_emissions_rcp(time())


_ext_data_n2o_anthro_emissions_rcp = ExtData(
    "../climate.xlsx",
    "Catalonia",
    "year_emissions",
    "N2O_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    _root,
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    "_ext_data_n2o_anthro_emissions_rcp",
)


@component.add(
    name="PE losses conv gas for Elec EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_extraction_conv_gas_ej": 1,
        "imports_cat_conv_gas_from_row_ej": 1,
        "share_nat_gas_dem_for_elec": 1,
        "efficiency_gas_for_electricity": 1,
    },
)
def pe_losses_conv_gas_for_elec_ej():
    """
    (Primary) Energy losses in the generation of electricity in gas power centrals.
    """
    return (
        (real_extraction_conv_gas_ej() + imports_cat_conv_gas_from_row_ej())
        * share_nat_gas_dem_for_elec()
        * (1 - efficiency_gas_for_electricity())
    )


@component.add(
    name="PFC emissions",
    units="tons/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"choose_rcp": 3, "pfc_emissions_rcp": 4},
)
def pfc_emissions():
    """
    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare) Choose RCP: 1. RCP 2.6 2. RCP 4.5 3. RCP 6.0 4. RCP 8.5
    """
    return if_then_else(
        choose_rcp() == 1,
        lambda: float(pfc_emissions_rcp().loc["RCP26"]),
        lambda: if_then_else(
            choose_rcp() == 2,
            lambda: float(pfc_emissions_rcp().loc["RCP45"]),
            lambda: if_then_else(
                choose_rcp() == 3,
                lambda: float(pfc_emissions_rcp().loc["RCP60"]),
                lambda: float(pfc_emissions_rcp().loc["RCP85"]),
            ),
        ),
    )


@component.add(
    name="PFC emissions RCP",
    units="tons/Year",
    subscripts=["RCP Scenario"],
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_pfc_emissions_rcp",
        "__data__": "_ext_data_pfc_emissions_rcp",
        "time": 1,
    },
)
def pfc_emissions_rcp():
    """
    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_pfc_emissions_rcp(time())


_ext_data_pfc_emissions_rcp = ExtData(
    "../climate.xlsx",
    "Catalonia",
    "year_emissions",
    "PFCs_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    _root,
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    "_ext_data_pfc_emissions_rcp",
)


@component.add(
    name="SF6 emissions",
    units="tons/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"choose_rcp": 3, "sf6_emissions_rcp": 4},
)
def sf6_emissions():
    """
    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare) Choose RCP: 1. RCP 2.6 2. RCP 4.5 3. RCP 6.0 4. RCP 8.5
    """
    return if_then_else(
        choose_rcp() == 1,
        lambda: float(sf6_emissions_rcp().loc["RCP26"]),
        lambda: if_then_else(
            choose_rcp() == 2,
            lambda: float(sf6_emissions_rcp().loc["RCP45"]),
            lambda: if_then_else(
                choose_rcp() == 3,
                lambda: float(sf6_emissions_rcp().loc["RCP60"]),
                lambda: float(sf6_emissions_rcp().loc["RCP85"]),
            ),
        ),
    )


@component.add(
    name="SF6 emissions RCP",
    units="tons/Year",
    subscripts=["RCP Scenario"],
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_sf6_emissions_rcp",
        "__data__": "_ext_data_sf6_emissions_rcp",
        "time": 1,
    },
)
def sf6_emissions_rcp():
    """
    Historic data + projections "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare)
    """
    return _ext_data_sf6_emissions_rcp(time())


_ext_data_sf6_emissions_rcp = ExtData(
    "../climate.xlsx",
    "Catalonia",
    "year_emissions",
    "SF6_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    _root,
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    "_ext_data_sf6_emissions_rcp",
)


@component.add(
    name="Start policy leave in ground tot agg oil",
    units="Year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_start_policy_leave_in_ground_tot_agg_oil"
    },
)
def start_policy_leave_in_ground_tot_agg_oil():
    """
    Year when the policy to leave in the ground an amount of total aggregated oil RURR enters into force.
    """
    return _ext_constant_start_policy_leave_in_ground_tot_agg_oil()


_ext_constant_start_policy_leave_in_ground_tot_agg_oil = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "start_policy_year_agg_oil_underground",
    {},
    _root,
    {},
    "_ext_constant_start_policy_leave_in_ground_tot_agg_oil",
)
