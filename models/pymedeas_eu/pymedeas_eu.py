"""
Python model 'pymedeas_eu.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np
import xarray as xr

from pysd.py_backend.functions import (
    integer,
    if_then_else,
    zidz,
    sum,
    xidz,
    invert_matrix,
    step,
)
from pysd.py_backend.statefuls import Initial, DelayFixed, SampleIfTrue, Smooth, Integ
from pysd.py_backend.external import ExtData, ExtLookup, ExtConstant
from pysd.py_backend.data import TabData
from pysd.py_backend.utils import load_model_data, load_modules
from pysd import Component

__pysd_version__ = "3.9.1"

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
    name="activate Affores program",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_activate_affores_program"},
)
def activate_affores_program():
    """
    0. Deactivated. 1. Activated.
    """
    return _ext_constant_activate_affores_program()


_ext_constant_activate_affores_program = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "NZP",
    "activate_afforestation_program",
    {},
    _root,
    {},
    "_ext_constant_activate_affores_program",
)


@component.add(
    name="Adapt CO2 emissions unconv gas",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 4},
)
def adapt_co2_emissions_unconv_gas():
    """
    Unconventional gas emissions are 3,53 tCO2/toe vs 2,35 for conventional. Since we have all natural gas modeled in an aggregated manner, this function corrects these emissions assuming that unconventional gas would follow the share un relation to natural gas as estimated by [Mohr&Evans2011](BG) for 2050 and 2100 (linear interpolation).
    """
    return if_then_else(
        time() < 2050,
        lambda: 0.01 + (0.22 - 0.01) * (time() - 2000) / 50,
        lambda: if_then_else(
            time() < 2100,
            lambda: 0.22 + (0.6 - 0.22) * (time() - 2050) / 50,
            lambda: 0.6,
        ),
    )


@component.add(
    name="BioE CO2 emissions",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gco2_per_mj_conv_gas": 1,
        "oil_liquids_saved_by_biofuels_ej": 1,
        "solid_bioe_emissions_relevant_ej": 1,
        "pes_tot_biogas_for_heatcom": 1,
        "mj_per_ej": 1,
        "g_per_gt": 1,
    },
)
def bioe_co2_emissions():
    """
    CO2 emissions from biomass. We assume that biofuels have an emission intensity similar to natural gas (due to ILUCs, see Technical Report), and for the rest (traditional biomass, biomass for electricity and biomass for heat) we asssume that the carbon balance is null.
    """
    return (
        gco2_per_mj_conv_gas()
        * (
            oil_liquids_saved_by_biofuels_ej()
            + solid_bioe_emissions_relevant_ej()
            + pes_tot_biogas_for_heatcom()
        )
        * mj_per_ej()
        / g_per_gt()
    )


@component.add(
    name="C per CO2", units="GtC/GTCO2e", comp_type="Constant", comp_subtype="Normal"
)
def c_per_co2():
    """
    1 kg of CO2 contains 3/11 of carbon.
    """
    return 3 / 11


@component.add(
    name="Carbon emissions GtC",
    units="GtC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_co2_emissions_gtco2": 1, "c_per_co2": 1},
)
def carbon_emissions_gtc():
    """
    Total anual carbon emissions.
    """
    return total_co2_emissions_gtco2() * c_per_co2()


@component.add(
    name="CH4 anthro emissions",
    units="Mton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_ch4_emissions_fossil_fuels": 1,
        "choose_rcp": 3,
        "ch4_anthro_emissions_rcp": 4,
        "ratio_power_plants_energy_conversion_extraction_and_distribution_vs_total_ch4_emissions": 1,
    },
)
def ch4_anthro_emissions():
    """
    "Representative Concentration Pathways" (RCPs, see http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=compare) except Power Plants, Energy Conversion, Extraction, and Distribution. Corrected with endogenous data "Total CH4 emissions fossil fuels" Choose RCP: 1. RCP 2.6 2. RCP 4.5 3. RCP 6.0 4. RCP 8.5
    """
    return total_ch4_emissions_fossil_fuels() + if_then_else(
        choose_rcp() == 1,
        lambda: float(ch4_anthro_emissions_rcp().loc["RCP26"]),
        lambda: if_then_else(
            choose_rcp() == 2,
            lambda: float(ch4_anthro_emissions_rcp().loc["RCP45"]),
            lambda: if_then_else(
                choose_rcp() == 3,
                lambda: float(ch4_anthro_emissions_rcp().loc["RCP60"]),
                lambda: float(ch4_anthro_emissions_rcp().loc["RCP85"]),
            ),
        ),
    ) * (
        1
        - ratio_power_plants_energy_conversion_extraction_and_distribution_vs_total_ch4_emissions()
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
    "Europe",
    "year_emissions",
    "CH4_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    _root,
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    "_ext_data_ch4_anthro_emissions_rcp",
)


@component.add(
    name="CH4 emissions coal without CTL",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "consumption_ue_coal_emissions_relevant_ej": 1,
        "gch4_per_mj_coal": 1,
        "mj_per_ej": 1,
        "g_per_mt": 1,
    },
)
def ch4_emissions_coal_without_ctl():
    """
    CH4 emissions coal.
    """
    return (
        consumption_ue_coal_emissions_relevant_ej()
        * gch4_per_mj_coal()
        * mj_per_ej()
        / g_per_mt()
    )


@component.add(
    name="CH4 emissions conv gas without GTL",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pec_conv_gas": 1,
        "ped_nat_gas_for_gtl_ej": 1,
        "share_conv_vs_total_gas_extraction": 1,
        "gch4_per_mj_conv_gas": 1,
        "mj_per_ej": 1,
        "g_per_mt": 1,
    },
)
def ch4_emissions_conv_gas_without_gtl():
    """
    CH4 emissions conventional gas.
    """
    return (
        (
            pec_conv_gas()
            - ped_nat_gas_for_gtl_ej() * share_conv_vs_total_gas_extraction()
        )
        * gch4_per_mj_conv_gas()
        * mj_per_ej()
        / g_per_mt()
    )


@component.add(
    name="CH4 emissions CTL",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_coal_for_ctl_ej": 1,
        "gch4_per_mj_ctl": 1,
        "mj_per_ej": 1,
        "g_per_mt": 1,
    },
)
def ch4_emissions_ctl():
    """
    CH4 emissions CTL.
    """
    return extraction_coal_for_ctl_ej() * gch4_per_mj_ctl() * mj_per_ej() / g_per_mt()


@component.add(
    name="CH4 emissions GTL",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_nat_gas_for_gtl_ej": 1,
        "gch4_per_mj_gtl": 1,
        "mj_per_ej": 1,
        "g_per_mt": 1,
    },
)
def ch4_emissions_gtl():
    """
    CH4 emissions GTL.
    """
    return ped_nat_gas_for_gtl_ej() * gch4_per_mj_gtl() * mj_per_ej() / g_per_mt()


@component.add(
    name="CH4 emissions unconv gas",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pec_unconv_gas": 1,
        "ped_nat_gas_for_gtl_ej": 1,
        "share_conv_vs_total_gas_extraction": 1,
        "gch4_per_mj_unconv_gas": 1,
        "mj_per_ej": 1,
        "g_per_mt": 1,
    },
)
def ch4_emissions_unconv_gas():
    """
    CH4 emissions unconventional gas.
    """
    return (
        (
            pec_unconv_gas()
            - ped_nat_gas_for_gtl_ej() * (1 - share_conv_vs_total_gas_extraction())
        )
        * gch4_per_mj_unconv_gas()
        * mj_per_ej()
        / g_per_mt()
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
    "../../scenarios/scen_eu.xlsx",
    "NZP",
    "RCP_GHG_emissions_select",
    {},
    _root,
    {},
    "_ext_constant_choose_rcp",
)


@component.add(
    name="CO2 emissions coal without CTL",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "consumption_ue_coal_emissions_relevant_ej": 1,
        "gco2_per_mj_coal": 1,
        "mj_per_ej": 1,
        "g_per_gt": 1,
    },
)
def co2_emissions_coal_without_ctl():
    """
    Emissions from coal withoug accounting for CTL-related emissions.
    """
    return (
        consumption_ue_coal_emissions_relevant_ej()
        * gco2_per_mj_coal()
        * mj_per_ej()
        / g_per_gt()
    )


@component.add(
    name="CO2 emissions conv gas without GTL",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_consumption_ue_conv_gas_emissions_relevant_ej": 1,
        "gco2_per_mj_conv_gas": 1,
        "mj_per_ej": 1,
        "g_per_gt": 1,
    },
)
def co2_emissions_conv_gas_without_gtl():
    """
    CO2 emissions from conventional gas (withouth GTL) when the gas extraction is disaggregated in conventional and unconventional resource, and CO2 emissions from total gas when the extraction is aggregated.
    """
    return (
        real_consumption_ue_conv_gas_emissions_relevant_ej()
        * gco2_per_mj_conv_gas()
        * mj_per_ej()
        / g_per_gt()
    )


@component.add(
    name="CO2 emissions conv oil",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_consumption_ue_conv_oil_emissions_relevant_ej": 1,
        "gco2_per_mj_conv_oil": 1,
        "mj_per_ej": 1,
        "g_per_gt": 1,
    },
)
def co2_emissions_conv_oil():
    """
    CO2 emissions from conventional oil.
    """
    return (
        real_consumption_ue_conv_oil_emissions_relevant_ej()
        * gco2_per_mj_conv_oil()
        * mj_per_ej()
        / g_per_gt()
    )


@component.add(
    name="CO2 emissions CTL",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gco2_per_mj_ctl": 1,
        "extraction_coal_for_ctl_ej": 1,
        "mj_per_ej": 1,
        "g_per_gt": 1,
    },
)
def co2_emissions_ctl():
    """
    CO2 emissions associated to CTL production.
    """
    return gco2_per_mj_ctl() * extraction_coal_for_ctl_ej() * mj_per_ej() / g_per_gt()


@component.add(
    name="CO2 emissions GTL",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_nat_gas_for_gtl_ej": 1,
        "gco2_per_mj_gtl": 1,
        "mj_per_ej": 1,
        "g_per_gt": 1,
    },
)
def co2_emissions_gtl():
    """
    CO2 emissions associated to GTL production.
    """
    return ped_nat_gas_for_gtl_ej() * gco2_per_mj_gtl() * mj_per_ej() / g_per_gt()


@component.add(
    name="CO2 emissions unconv gas",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_consumption_unconv_gas_emissions_relevant_ej": 1,
        "gco2_per_mj_unconv_gas": 1,
        "mj_per_ej": 1,
        "g_per_gt": 1,
    },
)
def co2_emissions_unconv_gas():
    """
    CO2 emissions from unconventional gas.
    """
    return (
        real_consumption_unconv_gas_emissions_relevant_ej()
        * gco2_per_mj_unconv_gas()
        * mj_per_ej()
        / g_per_gt()
    )


@component.add(
    name="CO2 emissions unconv oil",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_consumption_unconv_oil_emissions_relevant_ej": 1,
        "gco2_per_mj_unconv_oil": 2,
        "gco2_per_mj_shale_oil": 1,
        "adapt_emissions_shale_oil": 1,
        "mj_per_ej": 1,
        "g_per_gt": 1,
    },
)
def co2_emissions_unconv_oil():
    """
    CO2 emissions from unconventional oil.
    """
    return (
        (
            real_consumption_unconv_oil_emissions_relevant_ej()
            * (
                gco2_per_mj_unconv_oil()
                + (gco2_per_mj_shale_oil() - gco2_per_mj_unconv_oil())
                * adapt_emissions_shale_oil()
            )
        )
        * mj_per_ej()
        / g_per_gt()
    )


@component.add(
    name="CO2 fossil fuel emissions",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_emissions_conv_gas_without_gtl": 1,
        "co2_emissions_unconv_gas": 1,
        "co2_emissions_gtl": 1,
        "co2_emissions_conv_oil": 1,
        "co2_emissions_unconv_oil": 1,
        "co2_emissions_coal_without_ctl": 1,
        "co2_emissions_ctl": 1,
    },
)
def co2_fossil_fuel_emissions():
    """
    Total CO2 emissions from fossil fuels.
    """
    return (
        co2_emissions_conv_gas_without_gtl()
        + co2_emissions_unconv_gas()
        + co2_emissions_gtl()
        + co2_emissions_conv_oil()
        + co2_emissions_unconv_oil()
        + co2_emissions_coal_without_ctl()
        + co2_emissions_ctl()
    )


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
    name="cum materials to extract for RES elec",
    units="Mt",
    subscripts=["materials"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cum_materials_to_extract_for_res_elec": 1},
    other_deps={
        "_integ_cum_materials_to_extract_for_res_elec": {
            "initial": {"initial_cumulated_material_requirements_for_res_elec_1995": 1},
            "step": {"total_materials_to_extract_for_res_elec_mt": 1},
        }
    },
)
def cum_materials_to_extract_for_res_elec():
    """
    Cumulative materials to be mined for the installation and O&M of RES for electricity generation.
    """
    return _integ_cum_materials_to_extract_for_res_elec()


_integ_cum_materials_to_extract_for_res_elec = Integ(
    lambda: total_materials_to_extract_for_res_elec_mt(),
    lambda: xr.DataArray(
        initial_cumulated_material_requirements_for_res_elec_1995(),
        {"materials": _subscript_dict["materials"]},
        ["materials"],
    ),
    "_integ_cum_materials_to_extract_for_res_elec",
)


@component.add(
    name="cum materials to extract for RES elec from 2015",
    units="Mt",
    subscripts=["materials"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cum_materials_to_extract_for_res_elec_from_2015": 1},
    other_deps={
        "_integ_cum_materials_to_extract_for_res_elec_from_2015": {
            "initial": {"initial_cumulated_material_requirements_for_res_elec_1995": 1},
            "step": {"total_materials_to_extract_for_res_elec_from_2015_mt": 1},
        }
    },
)
def cum_materials_to_extract_for_res_elec_from_2015():
    """
    Cumulative materials to be mined for the installation and O&M of RES for electricity generation.
    """
    return _integ_cum_materials_to_extract_for_res_elec_from_2015()


_integ_cum_materials_to_extract_for_res_elec_from_2015 = Integ(
    lambda: total_materials_to_extract_for_res_elec_from_2015_mt(),
    lambda: xr.DataArray(
        initial_cumulated_material_requirements_for_res_elec_1995(),
        {"materials": _subscript_dict["materials"]},
        ["materials"],
    ),
    "_integ_cum_materials_to_extract_for_res_elec_from_2015",
)


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
    name="g per Gt", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def g_per_gt():
    """
    Unit conversion.
    """
    return 1000000000000000.0


@component.add(
    name="g per Mt", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def g_per_mt():
    """
    1e12 grams = 1 Mtonne.
    """
    return 1000000000000.0


@component.add(
    name="gCH4 per MJ coal",
    units="GtCO2/MToe",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gch4_per_mj_coal"},
)
def gch4_per_mj_coal():
    """
    CH4 emissions associated to the extraction of coal. Ref: Fig. 2 Howarth (2015).
    """
    return _ext_constant_gch4_per_mj_coal()


_ext_constant_gch4_per_mj_coal = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gch4_coal",
    {},
    _root,
    {},
    "_ext_constant_gch4_per_mj_coal",
)


@component.add(
    name="gCH4 per MJ conv gas",
    units="GtCO2/MToe",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gch4_per_mj_conv_gas"},
)
def gch4_per_mj_conv_gas():
    """
    CH4 emissions associated to the extraction of conventional gas. Ref: Fig. 2 Howarth (2015).
    """
    return _ext_constant_gch4_per_mj_conv_gas()


_ext_constant_gch4_per_mj_conv_gas = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gch4_conv_gas",
    {},
    _root,
    {},
    "_ext_constant_gch4_per_mj_conv_gas",
)


@component.add(
    name="gCH4 per MJ CTL",
    units="GtCO2/MToe",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gch4_per_mj_ctl"},
)
def gch4_per_mj_ctl():
    """
    CH4 emission factor of CTL.
    """
    return _ext_constant_gch4_per_mj_ctl()


_ext_constant_gch4_per_mj_ctl = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gch4_ctl",
    {},
    _root,
    {},
    "_ext_constant_gch4_per_mj_ctl",
)


@component.add(
    name="gCH4 per MJ GTL",
    units="GtCO2/MToe",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gch4_per_mj_gtl"},
)
def gch4_per_mj_gtl():
    """
    CH4 emission factor of GTL.
    """
    return _ext_constant_gch4_per_mj_gtl()


_ext_constant_gch4_per_mj_gtl = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gch4_gtl",
    {},
    _root,
    {},
    "_ext_constant_gch4_per_mj_gtl",
)


@component.add(
    name="gCH4 per MJ oil",
    units="GtCO2/MToe",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gch4_per_mj_oil"},
)
def gch4_per_mj_oil():
    """
    CH4 emissions associated to the extraction of oil. Ref: Fig. 2 Howarth (2015).
    """
    return _ext_constant_gch4_per_mj_oil()


_ext_constant_gch4_per_mj_oil = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gch4_oil",
    {},
    _root,
    {},
    "_ext_constant_gch4_per_mj_oil",
)


@component.add(
    name="gCH4 per MJ unconv gas",
    units="GtCO2/MToe",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gch4_per_mj_unconv_gas"},
)
def gch4_per_mj_unconv_gas():
    """
    CH4 emissions associated to the extraction of unconventional gas (shale gas). Ref: Fig. 2 Howarth (2015).
    """
    return _ext_constant_gch4_per_mj_unconv_gas()


_ext_constant_gch4_per_mj_unconv_gas = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gch4_unconventional_gas",
    {},
    _root,
    {},
    "_ext_constant_gch4_per_mj_unconv_gas",
)


@component.add(
    name="gCO2 per MJ coal",
    units="gCO2/MJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gco2_per_mj_coal"},
)
def gco2_per_mj_coal():
    """
    CO2 emission factor coal.
    """
    return _ext_constant_gco2_per_mj_coal()


_ext_constant_gco2_per_mj_coal = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_coal",
    {},
    _root,
    {},
    "_ext_constant_gco2_per_mj_coal",
)


@component.add(
    name="gCO2 per MJ conv gas",
    units="gCO2/MJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gco2_per_mj_conv_gas"},
)
def gco2_per_mj_conv_gas():
    """
    CO2 emission factor conventional natural gas.
    """
    return _ext_constant_gco2_per_mj_conv_gas()


_ext_constant_gco2_per_mj_conv_gas = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_conventional_gas",
    {},
    _root,
    {},
    "_ext_constant_gco2_per_mj_conv_gas",
)


@component.add(
    name="gCO2 per MJ conv oil",
    units="gCO2/MJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gco2_per_mj_conv_oil"},
)
def gco2_per_mj_conv_oil():
    """
    CO2 emission factor conventional oil.
    """
    return _ext_constant_gco2_per_mj_conv_oil()


_ext_constant_gco2_per_mj_conv_oil = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_conventional_oil",
    {},
    _root,
    {},
    "_ext_constant_gco2_per_mj_conv_oil",
)


@component.add(
    name="gCO2 per MJ CTL",
    units="gCO2/MJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gco2_per_mj_ctl"},
)
def gco2_per_mj_ctl():
    """
    CO2 emissions coefficient of CTL.
    """
    return _ext_constant_gco2_per_mj_ctl()


_ext_constant_gco2_per_mj_ctl = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_ctl",
    {},
    _root,
    {},
    "_ext_constant_gco2_per_mj_ctl",
)


@component.add(
    name="gCO2 per MJ GTL",
    units="gCO2/MJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gco2_per_mj_gtl"},
)
def gco2_per_mj_gtl():
    """
    CO2 emissions coefficient of GTL.
    """
    return _ext_constant_gco2_per_mj_gtl()


_ext_constant_gco2_per_mj_gtl = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_gtl",
    {},
    _root,
    {},
    "_ext_constant_gco2_per_mj_gtl",
)


@component.add(
    name="gCO2 per MJ shale oil",
    units="gCO2/MJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gco2_per_mj_shale_oil"},
)
def gco2_per_mj_shale_oil():
    """
    CO2 emission factor shale oil.
    """
    return _ext_constant_gco2_per_mj_shale_oil()


_ext_constant_gco2_per_mj_shale_oil = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_shale_oil",
    {},
    _root,
    {},
    "_ext_constant_gco2_per_mj_shale_oil",
)


@component.add(
    name="gCO2 per MJ unconv gas",
    units="gCO2/MJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gco2_per_mj_unconv_gas"},
)
def gco2_per_mj_unconv_gas():
    """
    CO2 emission factor of unconventional gas.
    """
    return _ext_constant_gco2_per_mj_unconv_gas()


_ext_constant_gco2_per_mj_unconv_gas = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_unconventional_gas",
    {},
    _root,
    {},
    "_ext_constant_gco2_per_mj_unconv_gas",
)


@component.add(
    name="gCO2 per MJ unconv oil",
    units="gCO2/MJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gco2_per_mj_unconv_oil"},
)
def gco2_per_mj_unconv_oil():
    """
    Emission factor unconventional oil (tar sands/extra heavy oil).
    """
    return _ext_constant_gco2_per_mj_unconv_oil()


_ext_constant_gco2_per_mj_unconv_oil = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_unconventional_oil",
    {},
    _root,
    {},
    "_ext_constant_gco2_per_mj_unconv_oil",
)


@component.add(
    name="GWP 100 year",
    subscripts=["GHGs non CO2"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gwp_100_year"},
)
def gwp_100_year():
    return _ext_constant_gwp_100_year()


_ext_constant_gwp_100_year = ExtConstant(
    "../climate.xlsx",
    "Global",
    "GWP_100_year*",
    {"GHGs non CO2": _subscript_dict["GHGs non CO2"]},
    _root,
    {"GHGs non CO2": _subscript_dict["GHGs non CO2"]},
    "_ext_constant_gwp_100_year",
)


@component.add(
    name="GWP 20 year",
    subscripts=["GHGs non CO2"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gwp_20_year"},
)
def gwp_20_year():
    return _ext_constant_gwp_20_year()


_ext_constant_gwp_20_year = ExtConstant(
    "../climate.xlsx",
    "Global",
    "GWP_20_year*",
    {"GHGs non CO2": _subscript_dict["GHGs non CO2"]},
    _root,
    {"GHGs non CO2": _subscript_dict["GHGs non CO2"]},
    "_ext_constant_gwp_20_year",
)


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
    "Europe",
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
    "Europe",
    "year_emissions",
    "HFC23_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC23"]},
)

_ext_data_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "Europe",
    "year_emissions",
    "HFC32_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC32"]},
)

_ext_data_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "Europe",
    "year_emissions",
    "HFC125_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC125"]},
)

_ext_data_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "Europe",
    "year_emissions",
    "HFC143a_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC143a"]},
)

_ext_data_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "Europe",
    "year_emissions",
    "HFC152a_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC152a"]},
)

_ext_data_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "Europe",
    "year_emissions",
    "HFC227ea_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC227ea"]},
)

_ext_data_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "Europe",
    "year_emissions",
    "HFC245ca_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC245ca"]},
)

_ext_data_hfc_emissions_rcp.add(
    "../climate.xlsx",
    "Europe",
    "year_emissions",
    "HFC4310mee_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"], "HFC type": ["HFC4310mee"]},
)


@component.add(
    name='"include materials for overgrids?"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def include_materials_for_overgrids():
    """
    1. Include materials for overgrids in the CED of RES elec var 0: NOT include materials for overgrids in the CED of RES elec var
    """
    return 0


@component.add(
    name="materials for new RES elec per capacity installed",
    units="kg/MW",
    subscripts=["RES elec", "materials"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "materials_per_new_capacity_installed_res": 1,
        "materials_per_new_res_elec_capacity_installed_hvdcs": 1,
        "materials_per_new_res_elec_capacity_installed_material_overgrid_high_power": 1,
        "include_materials_for_overgrids": 1,
    },
)
def materials_for_new_res_elec_per_capacity_installed():
    value = xr.DataArray(
        np.nan,
        {
            "RES elec": _subscript_dict["RES elec"],
            "materials": _subscript_dict["materials"],
        },
        ["RES elec", "materials"],
    )
    value.loc[_subscript_dict["RES ELEC DISPATCHABLE"], :] = 0
    value.loc[_subscript_dict["RES ELEC VARIABLE"], :] = (
        materials_per_new_capacity_installed_res()
        + (
            (
                materials_per_new_res_elec_capacity_installed_hvdcs()
                + materials_per_new_res_elec_capacity_installed_material_overgrid_high_power()
            )
            * include_materials_for_overgrids()
        )
    ).values
    return value


@component.add(
    name='"materials for O&M per capacity installed RES elec"',
    units="kg/MW",
    subscripts=["RES elec", "materials"],
    comp_type="Constant",
    comp_subtype="External, Normal",
    depends_on={
        "__external__": "_ext_constant_materials_for_om_per_capacity_installed_res_elec"
    },
)
def materials_for_om_per_capacity_installed_res_elec():
    """
    Materials requirements for operation and maintenance per unit of new installed capacity of RES elec.
    """
    value = xr.DataArray(
        np.nan,
        {
            "RES elec": _subscript_dict["RES elec"],
            "materials": _subscript_dict["materials"],
        },
        ["RES elec", "materials"],
    )
    value.loc[_subscript_dict["RES ELEC DISPATCHABLE"], :] = 0
    def_subs = xr.zeros_like(value, dtype=bool)
    def_subs.loc[["wind onshore", "wind offshore", "solar PV", "CSP"], :] = True
    value.values[
        def_subs.values
    ] = _ext_constant_materials_for_om_per_capacity_installed_res_elec().values[
        def_subs.values
    ]
    return value


_ext_constant_materials_for_om_per_capacity_installed_res_elec = ExtConstant(
    "../materials.xlsx",
    "Global",
    "materials_for_om_per_capacity_installed_res_elec*",
    {
        "RES elec": _subscript_dict["RES ELEC VARIABLE"],
        "materials": _subscript_dict["materials"],
    },
    _root,
    {
        "RES elec": _subscript_dict["RES elec"],
        "materials": _subscript_dict["materials"],
    },
    "_ext_constant_materials_for_om_per_capacity_installed_res_elec",
)


@component.add(
    name="materials per new RES elec capacity installed HVDCs",
    units="kg/MW",
    subscripts=["materials"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_materials_per_new_res_elec_capacity_installed_hvdcs"
    },
)
def materials_per_new_res_elec_capacity_installed_hvdcs():
    """
    Materials requirements for inter-regional grids (HVDCs) per unit of new installed capacity of RES variable for electricity.
    """
    return _ext_constant_materials_per_new_res_elec_capacity_installed_hvdcs()


_ext_constant_materials_per_new_res_elec_capacity_installed_hvdcs = ExtConstant(
    "../materials.xlsx",
    "Global",
    "materials_per_new_res_elec_capacity_installed_hvdcs*",
    {"materials": _subscript_dict["materials"]},
    _root,
    {"materials": _subscript_dict["materials"]},
    "_ext_constant_materials_per_new_res_elec_capacity_installed_hvdcs",
)


@component.add(
    name="materials per new RES elec capacity installed material overgrid high power",
    units="kg/MW",
    subscripts=["materials"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_materials_per_new_res_elec_capacity_installed_material_overgrid_high_power"
    },
)
def materials_per_new_res_elec_capacity_installed_material_overgrid_high_power():
    """
    Materials requirements for overgrid high power per unit of new installed capacity of RES variable for electricity.
    """
    return (
        _ext_constant_materials_per_new_res_elec_capacity_installed_material_overgrid_high_power()
    )


_ext_constant_materials_per_new_res_elec_capacity_installed_material_overgrid_high_power = ExtConstant(
    "../materials.xlsx",
    "Global",
    "materials_per_new_res_elec_capacity_installed_material_overgrid_high_power*",
    {"materials": _subscript_dict["materials"]},
    _root,
    {"materials": _subscript_dict["materials"]},
    "_ext_constant_materials_per_new_res_elec_capacity_installed_material_overgrid_high_power",
)


@component.add(
    name="materials required for new RES elec Mt",
    units="Mt",
    subscripts=["RES elec", "materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "res_elec_capacity_under_construction_tw": 1,
        "materials_for_new_res_elec_per_capacity_installed": 1,
        "m_per_t": 1,
        "kg_per_mt": 1,
    },
)
def materials_required_for_new_res_elec_mt():
    """
    Annual materials required for the installation of new capacity of RES for electricity by technology.
    """
    return (
        res_elec_capacity_under_construction_tw()
        * materials_for_new_res_elec_per_capacity_installed()
        * m_per_t()
        / kg_per_mt()
    )


@component.add(
    name='"materials required for O&M RES elec Mt"',
    units="Mt",
    subscripts=["RES elec", "materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "installed_capacity_res_elec": 1,
        "materials_for_om_per_capacity_installed_res_elec": 1,
        "m_per_t": 1,
        "kg_per_mt": 1,
    },
)
def materials_required_for_om_res_elec_mt():
    """
    Annual materials required for the operation and maintenance of the capacity of RES for electricity in operation by technology.
    """
    return (
        installed_capacity_res_elec()
        * materials_for_om_per_capacity_installed_res_elec()
        * m_per_t()
        / kg_per_mt()
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
    "Europe",
    "year_emissions",
    "N2O_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    _root,
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    "_ext_data_n2o_anthro_emissions_rcp",
)


@component.add(
    name="new C GtC",
    units="GtC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"carbon_emissions_gtc": 1},
)
def new_c_gtc():
    """
    Annual carbon emissions.
    """
    return carbon_emissions_gtc()


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
    "Europe",
    "year_emissions",
    "PFCs_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    _root,
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    "_ext_data_pfc_emissions_rcp",
)


@component.add(
    name="ratio Power Plants Energy Conversion Extraction and Distribution vs total CH4 emissions",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ratio_power_plants_energy_conversion_extraction_and_distribution_vs_total_ch4_emissions():
    return 0.2752


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
    "Europe",
    "year_emissions",
    "SF6_emissions",
    "interpolate",
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    _root,
    {"RCP Scenario": _subscript_dict["RCP Scenario"]},
    "_ext_data_sf6_emissions_rcp",
)


@component.add(
    name="Start policy leave in ground coal",
    units="Year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_start_policy_leave_in_ground_coal"},
)
def start_policy_leave_in_ground_coal():
    """
    Year when the policy to leave in the ground an amount of coal RURR enters into force.
    """
    return _ext_constant_start_policy_leave_in_ground_coal()


_ext_constant_start_policy_leave_in_ground_coal = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "NZP",
    "start_policy_year_coal_underground",
    {},
    _root,
    {},
    "_ext_constant_start_policy_leave_in_ground_coal",
)


@component.add(
    name="Start policy leave in ground tot agg gas",
    units="Year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_start_policy_leave_in_ground_tot_agg_gas"
    },
)
def start_policy_leave_in_ground_tot_agg_gas():
    """
    Year when the policy to leave in the ground an amount of total aggregated gas RURR enters into force.
    """
    return _ext_constant_start_policy_leave_in_ground_tot_agg_gas()


_ext_constant_start_policy_leave_in_ground_tot_agg_gas = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "NZP",
    "start_policy_year_agg_gas_underground",
    {},
    _root,
    {},
    "_ext_constant_start_policy_leave_in_ground_tot_agg_gas",
)


@component.add(
    name="Total CH4 emissions fossil fuels",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ch4_emissions_conv_gas_without_gtl": 1,
        "ch4_emissions_unconv_gas": 1,
        "ch4_emissions_coal_without_ctl": 1,
        "ch4_emissions_oil": 1,
        "ch4_emissions_ctl": 1,
        "ch4_emissions_gtl": 1,
    },
)
def total_ch4_emissions_fossil_fuels():
    """
    Total CH4 emissions from fossil fuels.
    """
    return (
        ch4_emissions_conv_gas_without_gtl()
        + ch4_emissions_unconv_gas()
        + ch4_emissions_coal_without_ctl()
        + float(ch4_emissions_oil().loc["electricity"])
        + ch4_emissions_ctl()
        + ch4_emissions_gtl()
    )


@component.add(
    name="Total cumulative emissions GtC",
    units="GtC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_total_cumulative_emissions_gtc": 1},
    other_deps={
        "_integ_total_cumulative_emissions_gtc": {
            "initial": {"cumulative_emissions_to_1995": 1},
            "step": {"new_c_gtc": 1},
        }
    },
)
def total_cumulative_emissions_gtc():
    """
    Total cumulative emissions.
    """
    return _integ_total_cumulative_emissions_gtc()


_integ_total_cumulative_emissions_gtc = Integ(
    lambda: new_c_gtc(),
    lambda: cumulative_emissions_to_1995(),
    "_integ_total_cumulative_emissions_gtc",
)


@component.add(
    name="Total cumulative emissions GtCO2",
    units="GtCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_cumulative_emissions_gtc": 1, "c_per_co2": 1},
)
def total_cumulative_emissions_gtco2():
    """
    Total cumulative emissions.
    """
    return total_cumulative_emissions_gtc() / c_per_co2()


@component.add(
    name="Total materials required for new RES elec Mt",
    units="Mt",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"materials_required_for_new_res_elec_mt": 1},
)
def total_materials_required_for_new_res_elec_mt():
    """
    Total annual materials requirements per new installed capacity of RES for electricity generation.
    """
    return sum(
        materials_required_for_new_res_elec_mt().rename({"RES elec": "RES elec!"}),
        dim=["RES elec!"],
    )


@component.add(
    name='"Total materials required for O&M RES elec Mt"',
    units="Mt",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"materials_required_for_om_res_elec_mt": 1},
)
def total_materials_required_for_om_res_elec_mt():
    """
    Total annual materials required for the operation and maintenance of the capacity of RES for electricity in operation by technology.
    """
    return sum(
        materials_required_for_om_res_elec_mt().rename({"RES elec": "RES elec!"}),
        dim=["RES elec!"],
    )


@component.add(
    name="Total materials to extract for RES elec from 2015 Mt",
    units="Mt/Year",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "total_materials_to_extract_for_res_elec_mt": 1},
)
def total_materials_to_extract_for_res_elec_from_2015_mt():
    """
    Annual materials to be mined for the installation and O&M of RES for electricity generation from 2015.
    """
    return if_then_else(
        time() < 2015,
        lambda: xr.DataArray(
            0, {"materials": _subscript_dict["materials"]}, ["materials"]
        ),
        lambda: total_materials_to_extract_for_res_elec_mt(),
    )


@component.add(
    name="Total materials to extract for RES elec Mt",
    units="Mt/Year",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_materials_required_for_res_elec_mt": 1,
        "recycling_rates_minerals_alt_techn": 1,
    },
)
def total_materials_to_extract_for_res_elec_mt():
    """
    Annual materials to be mined for the installation and O&M of RES for electricity generation.
    """
    return total_materials_required_for_res_elec_mt() * (
        1 - recycling_rates_minerals_alt_techn()
    )


@component.add(
    name="Total recycled materials for RES elec Mt",
    units="Mt",
    subscripts=["materials"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_materials_required_for_res_elec_mt": 1,
        "total_materials_to_extract_for_res_elec_mt": 1,
    },
)
def total_recycled_materials_for_res_elec_mt():
    """
    Total recycled materials for RES technologies for the generation of electricity.
    """
    return (
        total_materials_required_for_res_elec_mt()
        - total_materials_to_extract_for_res_elec_mt()
    )
