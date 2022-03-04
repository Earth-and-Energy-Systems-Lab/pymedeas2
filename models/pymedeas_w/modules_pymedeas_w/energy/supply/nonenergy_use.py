"""
Module nonenergy_use
Translated using PySD version 2.2.1
"""


@subs(["final sources"], _subscript_dict)
def annual_variation_nonenergy_use():
    """
    Real Name: Annual variation nonenergy use
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']

    Annual variation non-energy use by final fuel.
    """
    return if_then_else(
        time() > 2009,
        lambda: variation_nonenergy_use(),
        lambda: historic_nonenergy_use(time() + 1) - historic_nonenergy_use(time()),
    )


@subs(["final sources"], _subscript_dict)
def historic_nonenergy_use(x):
    """
    Real Name: historic nonenergy use
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Lookup
    Subs: ['final sources']

    Historic data non-energy use by final fuel.
    """
    return _ext_lookup_historic_nonenergy_use(x)


_ext_lookup_historic_nonenergy_use = ExtLookup(
    "../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_non_energy_use",
    {"final sources": _subscript_dict["final sources"]},
    _root,
    "_ext_lookup_historic_nonenergy_use",
)


@subs(["final sources"], _subscript_dict)
def initial_nonenergy_use():
    """
    Real Name: initial nonenergy use
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Constant
    Subs: ['final sources']

    Non-energy use consumption in the year 1995.
    """
    return _ext_constant_initial_nonenergy_use()


_ext_constant_initial_nonenergy_use = ExtConstant(
    "../energy.xlsx",
    "World",
    "initial_non_energy_use*",
    {"final sources": _subscript_dict["final sources"]},
    _root,
    "_ext_constant_initial_nonenergy_use",
)


@subs(["final sources"], _subscript_dict)
def nonenergy_use_demand_by_final_fuel_ej():
    """
    Real Name: "Non-energy use demand by final fuel EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Stateful
    Subs: ['final sources']

    Non-energy use demand by final fuel
    """
    return _integ_nonenergy_use_demand_by_final_fuel_ej()


_integ_nonenergy_use_demand_by_final_fuel_ej = Integ(
    lambda: annual_variation_nonenergy_use(),
    lambda: initial_nonenergy_use(),
    "_integ_nonenergy_use_demand_by_final_fuel_ej",
)


def total_real_nonenergy_use_consumption_ej():
    """
    Real Name: Total real nonenergy use consumption EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return sum(
        nonenergy_use_demand_by_final_fuel_ej().rename(
            {"final sources": "final sources!"}
        ),
        dim=["final sources!"],
    )


@subs(["final sources"], _subscript_dict)
def variation_nonenergy_use():
    """
    Real Name: variation nonenergy use
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Constant, Auxiliary
    Subs: ['final sources']


    """
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[{"final sources": ["electricity"]}] = 0
    value.loc[{"final sources": ["heat"]}] = 0
    value.loc[{"final sources": ["liquids"]}] = if_then_else(
        float(nonenergy_use_demand_by_final_fuel_ej().loc["liquids"]) > 0.01,
        lambda: 0.461414 * (gdp() - gdp_delayed_1yr()),
        lambda: 0,
    )
    value.loc[{"final sources": ["gases"]}] = if_then_else(
        float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"]) > 0.01,
        lambda: 0.123925 * (gdp() - gdp_delayed_1yr()),
        lambda: 0,
    )
    value.loc[{"final sources": ["solids"]}] = if_then_else(
        float(nonenergy_use_demand_by_final_fuel_ej().loc["solids"]) > 0.01,
        lambda: 0.0797511 * (gdp() - gdp_delayed_1yr()),
        lambda: 0,
    )
    return value
