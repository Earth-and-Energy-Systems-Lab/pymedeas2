"""
Module energy.supply.nonenergy_use
Translated using PySD version 3.14.2
"""

@component.add(
    name='"a_lin_reg_non-energy"',
    units="EJ/(year*T$)",
    subscripts=["final_sources"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def a_lin_reg_nonenergy():
    value = xr.DataArray(
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    value.loc[["electricity"]] = 0
    value.loc[["heat"]] = 0
    value.loc[["liquids"]] = 0.461414
    value.loc[["gases"]] = 0.123925
    value.loc[["solids"]] = 0.0797511
    return value


@component.add(
    name='"Annual_variation_non-energy_use"',
    units="EJ/(year*year)",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "variation_nonenergy_use": 1,
        "historic_nonenergy_use": 2,
        "time_step": 2,
    },
)
def annual_variation_nonenergy_use():
    """
    Annual variation non-energy use by final fuel.
    """
    return if_then_else(
        time() > 2009,
        lambda: variation_nonenergy_use(),
        lambda: (
            historic_nonenergy_use(time() + time_step())
            - historic_nonenergy_use(time())
        )
        / time_step(),
    )


@component.add(
    name="historic_nonenergy_use",
    units="EJ/year",
    subscripts=["final_sources"],
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
    r"../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_non_energy_use",
    {"final_sources": _subscript_dict["final_sources"]},
    _root,
    {"final_sources": _subscript_dict["final_sources"]},
    "_ext_lookup_historic_nonenergy_use",
)


@component.add(
    name="initial_nonenergy_use",
    units="EJ/year",
    subscripts=["final_sources"],
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
    r"../energy.xlsx",
    "Europe",
    "initial_non_energy_use*",
    {"final_sources": _subscript_dict["final_sources"]},
    _root,
    {"final_sources": _subscript_dict["final_sources"]},
    "_ext_constant_initial_nonenergy_use",
)


@component.add(
    name='"Non-energy_use_demand_by_final_fuel"',
    units="EJ/year",
    subscripts=["final_sources"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_nonenergy_use_demand_by_final_fuel": 1},
    other_deps={
        "_integ_nonenergy_use_demand_by_final_fuel": {
            "initial": {"initial_nonenergy_use": 1},
            "step": {"annual_variation_nonenergy_use": 1},
        }
    },
)
def nonenergy_use_demand_by_final_fuel():
    """
    Non-energy use demand by final fuel
    """
    return _integ_nonenergy_use_demand_by_final_fuel()


_integ_nonenergy_use_demand_by_final_fuel = Integ(
    lambda: annual_variation_nonenergy_use(),
    lambda: initial_nonenergy_use(),
    "_integ_nonenergy_use_demand_by_final_fuel",
)


@component.add(
    name='"Total_real_non-energy_use_consumption_EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nonenergy_use_demand_by_final_fuel": 1},
)
def total_real_nonenergy_use_consumption_ej():
    return sum(
        nonenergy_use_demand_by_final_fuel().rename(
            {"final_sources": "final_sources!"}
        ),
        dim=["final_sources!"],
    )


@component.add(
    name='"variation_non-energy_use"',
    units="EJ/(year*year)",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nonenergy_use_demand_by_final_fuel": 1,
        "gdp_delayed_1yr": 1,
        "nvs_1_year": 1,
        "gdp_eu": 1,
        "a_lin_reg_nonenergy": 1,
    },
)
def variation_nonenergy_use():
    return if_then_else(
        nonenergy_use_demand_by_final_fuel() > 0.01,
        lambda: a_lin_reg_nonenergy() * (gdp_eu() - gdp_delayed_1yr()) / nvs_1_year(),
        lambda: xr.DataArray(
            0, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
        ),
    )
