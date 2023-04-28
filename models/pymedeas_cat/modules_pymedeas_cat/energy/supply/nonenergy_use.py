"""
Module energy.supply.nonenergy_use
Translated using PySD version 3.9.1
"""


@component.add(
    name='"Annual variation non-energy use"',
    units="EJ",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 3, "variation_nonenergy_use": 1, "historic_nonenergy_use": 2},
)
def annual_variation_nonenergy_use():
    """
    Annual variation non-energy use by final fuel.
    """
    return if_then_else(
        time() > 2009,
        lambda: variation_nonenergy_use(),
        lambda: historic_nonenergy_use(integer(time() + 1))
        - historic_nonenergy_use(integer(time())),
    )


@component.add(
    name='"Domestic economic demand non-energy sector"',
    units="Mdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_domestic_output_required_by_sector": 1},
)
def domestic_economic_demand_nonenergy_sector():
    """
    Domestic economic demand of the sector that includes industries which use fuels as the source for materials with non-energy uses.
    """
    return float(
        total_domestic_output_required_by_sector().loc[
            "Coke refined petroleum nuclear fuel and chemicals etc"
        ]
    )


@component.add(
    name='"Domestic economic demand non-energy sector delayed 1yr"',
    units="Mdollars",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_domestic_economic_demand_nonenergy_sector_delayed_1yr": 1},
    other_deps={
        "_delayfixed_domestic_economic_demand_nonenergy_sector_delayed_1yr": {
            "initial": {},
            "step": {"domestic_economic_demand_nonenergy_sector": 1},
        }
    },
)
def domestic_economic_demand_nonenergy_sector_delayed_1yr():
    """
    Domestic economic demand of the sector that includes industries which use fuels as the source for materials with non-energy uses delayed 1 year.
    """
    return _delayfixed_domestic_economic_demand_nonenergy_sector_delayed_1yr()


_delayfixed_domestic_economic_demand_nonenergy_sector_delayed_1yr = DelayFixed(
    lambda: domestic_economic_demand_nonenergy_sector(),
    lambda: 1,
    lambda: 0,
    time_step,
    "_delayfixed_domestic_economic_demand_nonenergy_sector_delayed_1yr",
)


@component.add(
    name="historic nonenergy use",
    units="EJ",
    subscripts=["final sources"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_nonenergy_use",
        "__lookup__": "_ext_lookup_historic_nonenergy_use",
    },
)
def historic_nonenergy_use(x, final_subs=None):
    """
    Historic data non-energy use by final fuel.
    """
    return _ext_lookup_historic_nonenergy_use(x, final_subs)


_ext_lookup_historic_nonenergy_use = ExtLookup(
    "../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_non_energy_use",
    {"final sources": _subscript_dict["final sources"]},
    _root,
    {"final sources": _subscript_dict["final sources"]},
    "_ext_lookup_historic_nonenergy_use",
)


@component.add(
    name="initial nonenergy use",
    units="EJ",
    subscripts=["final sources"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_nonenergy_use"},
)
def initial_nonenergy_use():
    """
    Non-energy use consumption in the year 1995.
    """
    return _ext_constant_initial_nonenergy_use()


_ext_constant_initial_nonenergy_use = ExtConstant(
    "../energy.xlsx",
    "Catalonia",
    "initial_non_energy_use*",
    {"final sources": _subscript_dict["final sources"]},
    _root,
    {"final sources": _subscript_dict["final sources"]},
    "_ext_constant_initial_nonenergy_use",
)


@component.add(
    name='"Non-energy use demand after scarcity"',
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nonenergy_use_demand_by_final_fuel_ej": 1, "scarcity_final_fuels": 1},
)
def nonenergy_use_demand_after_scarcity():
    return nonenergy_use_demand_by_final_fuel_ej() * (1 - scarcity_final_fuels())


@component.add(
    name='"Non-energy use demand by final fuel EJ"',
    units="EJ/Year",
    subscripts=["final sources"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_nonenergy_use_demand_by_final_fuel_ej": 1},
    other_deps={
        "_integ_nonenergy_use_demand_by_final_fuel_ej": {
            "initial": {"initial_nonenergy_use": 1},
            "step": {"annual_variation_nonenergy_use": 1},
        }
    },
)
def nonenergy_use_demand_by_final_fuel_ej():
    """
    Non-energy use demand by final fuel
    """
    return _integ_nonenergy_use_demand_by_final_fuel_ej()


_integ_nonenergy_use_demand_by_final_fuel_ej = Integ(
    lambda: annual_variation_nonenergy_use(),
    lambda: initial_nonenergy_use(),
    "_integ_nonenergy_use_demand_by_final_fuel_ej",
)


@component.add(
    name='"Total real non-energy use consumption EJ"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nonenergy_use_demand_by_final_fuel_ej": 1},
)
def total_real_nonenergy_use_consumption_ej():
    return sum(
        nonenergy_use_demand_by_final_fuel_ej().rename(
            {"final sources": "final sources!"}
        ),
        dim=["final sources!"],
    )


@component.add(
    name='"variation non-energy use"',
    units="EJ",
    subscripts=["final sources"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_economic_demand_nonenergy_sector": 3,
        "domestic_economic_demand_nonenergy_sector_delayed_1yr": 3,
    },
)
def variation_nonenergy_use():
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[["electricity"]] = 0
    value.loc[["heat"]] = 0
    value.loc[["liquids"]] = 8e-06 * (
        domestic_economic_demand_nonenergy_sector()
        - domestic_economic_demand_nonenergy_sector_delayed_1yr()
    )
    value.loc[["gases"]] = 1.8e-06 * (
        domestic_economic_demand_nonenergy_sector()
        - domestic_economic_demand_nonenergy_sector_delayed_1yr()
    )
    value.loc[["solids"]] = 9e-08 * (
        domestic_economic_demand_nonenergy_sector()
        - domestic_economic_demand_nonenergy_sector_delayed_1yr()
    )
    return value
