"""
Module energy.supply.hydrgen_and_synthetic
Translated using PySD version 3.14.2
"""

@component.add(
    name="efficiency_electricity_to_synthetic",
    units="Dmnl",
    subscripts=["E_to_synthetic"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_efficiency_electricity_to_synthetic"},
)
def efficiency_electricity_to_synthetic():
    return _ext_constant_efficiency_electricity_to_synthetic()


_ext_constant_efficiency_electricity_to_synthetic = ExtConstant(
    r"../energy.xlsx",
    "Europe",
    "ETS*",
    {"E_to_synthetic": _subscript_dict["E_to_synthetic"]},
    _root,
    {"E_to_synthetic": _subscript_dict["E_to_synthetic"]},
    "_ext_constant_efficiency_electricity_to_synthetic",
)


@component.add(
    name="Electricity_consumption_for_synthetic_fuels",
    units="EJ/year",
    subscripts=["E_to_synthetic"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "electricity_demand_for_synthetic_fuels": 1,
        "abundance_electricity": 1,
    },
)
def electricity_consumption_for_synthetic_fuels():
    """
    Consumption of electricity for hydrogen and synthetic fuels generation taking into account the scarcity effect
    """
    return electricity_demand_for_synthetic_fuels() * abundance_electricity()


@component.add(
    name="Electricity_demand_for_synthetic_fuels",
    units="EJ/year",
    subscripts=["E_to_synthetic"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "policy_ets": 1, "efficiency_electricity_to_synthetic": 1},
)
def electricity_demand_for_synthetic_fuels():
    """
    Demand of electricity for hydrogen and synthetic fuels production
    """
    return policy_ets(time()) / efficiency_electricity_to_synthetic()


@component.add(
    name="policy_ETS",
    units="EJ/year",
    subscripts=["E_to_synthetic"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_policy_ets",
        "__lookup__": "_ext_lookup_policy_ets",
    },
)
def policy_ets(x, final_subs=None):
    return _ext_lookup_policy_ets(x, final_subs)


_ext_lookup_policy_ets = ExtLookup(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_synthetic",
    "p_ETS",
    {"E_to_synthetic": _subscript_dict["E_to_synthetic"]},
    _root,
    {"E_to_synthetic": _subscript_dict["E_to_synthetic"]},
    "_ext_lookup_policy_ets",
)


@component.add(
    name="Synthethic_fuel_generation",
    subscripts=["E_to_synthetic"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "efficiency_electricity_to_synthetic": 1,
        "electricity_consumption_for_synthetic_fuels": 1,
    },
)
def synthethic_fuel_generation():
    return (
        efficiency_electricity_to_synthetic()
        * electricity_consumption_for_synthetic_fuels()
    )


@component.add(
    name="Synthethic_fuel_generation_delayed",
    units="EJ/year",
    subscripts=["E_to_synthetic"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_synthethic_fuel_generation_delayed": 1},
    other_deps={
        "_delayfixed_synthethic_fuel_generation_delayed": {
            "initial": {"time_step": 1},
            "step": {"synthethic_fuel_generation": 1},
        }
    },
)
def synthethic_fuel_generation_delayed():
    return _delayfixed_synthethic_fuel_generation_delayed()


_delayfixed_synthethic_fuel_generation_delayed = DelayFixed(
    lambda: synthethic_fuel_generation(),
    lambda: time_step(),
    lambda: xr.DataArray(
        0, {"E_to_synthetic": _subscript_dict["E_to_synthetic"]}, ["E_to_synthetic"]
    ),
    time_step,
    "_delayfixed_synthethic_fuel_generation_delayed",
)


@component.add(
    name="Total_electricity_demand_for_synthetic",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"electricity_demand_for_synthetic_fuels": 1},
)
def total_electricity_demand_for_synthetic():
    return sum(
        electricity_demand_for_synthetic_fuels().rename(
            {"E_to_synthetic": "E_to_synthetic!"}
        ),
        dim=["E_to_synthetic!"],
    )
