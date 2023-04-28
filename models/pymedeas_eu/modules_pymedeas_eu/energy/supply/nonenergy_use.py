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
    "Europe",
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
    "Europe",
    "initial_non_energy_use*",
    {"final sources": _subscript_dict["final sources"]},
    _root,
    {"final sources": _subscript_dict["final sources"]},
    "_ext_constant_initial_nonenergy_use",
)


@component.add(
    name='"Non-energy use demand by final fuel EJ"',
    units="EJ",
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
        "nonenergy_use_demand_by_final_fuel_ej": 3,
        "gdp_eu": 3,
        "gdp_delayed_1yr": 3,
    },
)
def variation_nonenergy_use():
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[["electricity"]] = 0
    value.loc[["heat"]] = 0
    value.loc[["liquids"]] = if_then_else(
        float(nonenergy_use_demand_by_final_fuel_ej().loc["liquids"]) > 0.01,
        lambda: 0.461414 * (gdp_eu() - gdp_delayed_1yr()),
        lambda: 0,
    )
    value.loc[["gases"]] = if_then_else(
        float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"]) > 0.01,
        lambda: 0.123925 * (gdp_eu() - gdp_delayed_1yr()),
        lambda: 0,
    )
    value.loc[["solids"]] = if_then_else(
        float(nonenergy_use_demand_by_final_fuel_ej().loc["solids"]) > 0.01,
        lambda: 0.0797511 * (gdp_eu() - gdp_delayed_1yr()),
        lambda: 0,
    )
    return value
