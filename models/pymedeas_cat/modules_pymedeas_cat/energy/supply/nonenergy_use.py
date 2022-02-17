"""
Module nonenergy_use
Translated using PySD version 2.2.1
"""


@subs(["final sources"], _subscript_dict)
def annual_variation_nonenergy_use():
    """
    Real Name: "Annual variation non-energy use"
    Original Eqn: IF THEN ELSE(Time>2009, "variation non-energy use"[final sources], historic nonenergy use[final sources](INTEGER(Time+1))-historic nonenergy use[final sources](INTEGER(Time)))
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Annual variation non-energy use by final fuel.
    """
    return if_then_else(
        time() > 2009,
        lambda: variation_nonenergy_use(),
        lambda: historic_nonenergy_use(integer(time() + 1))
        - historic_nonenergy_use(integer(time())),
    )


def historic_nonenergy_use(x):
    """
    Real Name: historic nonenergy use
    Original Eqn: GET DIRECT LOOKUPS('../energy.xlsx', 'Austria', 'time_historic_data', 'historic_non_energy_use')
    Units: EJ
    Limits: (None, None)
    Type: lookup
    Subs: ['final sources']

    Historic data non-energy use by final fuel.
    """
    return _ext_lookup_historic_nonenergy_use(x)


@subs(["final sources"], _subscript_dict)
def initial_nonenergy_use():
    """
    Real Name: initial nonenergy use
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'initial_non_energy_use*')
    Units: EJ
    Limits: (None, None)
    Type: constant
    Subs: ['final sources']

    Non-energy use consumption in the year 1995.
    """
    return _ext_constant_initial_nonenergy_use()


@subs(["final sources"], _subscript_dict)
def nonenergy_use_demand_by_final_fuel_ej():
    """
    Real Name: "Non-energy use demand by final fuel EJ"
    Original Eqn: INTEG ( "Annual variation non-energy use"[final sources], initial nonenergy use[final sources])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['final sources']

    Non-energy use demand by final fuel
    """
    return _integ_nonenergy_use_demand_by_final_fuel_ej()


def total_real_nonenergy_use_consumption_ej():
    """
    Real Name: "Total real non-energy use consumption EJ"
    Original Eqn: SUM("Non-energy use demand by final fuel EJ"[final sources!])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return sum(nonenergy_use_demand_by_final_fuel_ej(), dim=("final sources",))


@subs(["final sources"], _subscript_dict)
def variation_nonenergy_use():
    """
    Real Name: "variation non-energy use"
    Original Eqn:
      0
      0
      IF THEN ELSE("Non-energy use demand by final fuel EJ"[liquids]>0.01,0.461414*(GDP AUT-GDP delayed 1yr),0)
      IF THEN ELSE("Non-energy use demand by final fuel EJ"[gases]>0.01,0.123925*(GDP AUT-GDP delayed 1yr),0)
      IF THEN ELSE("Non-energy use demand by final fuel EJ"[solids]>0.01,0.0797511*(GDP AUT-GDP delayed 1yr),0)
    Units: EJ
    Limits: (None, None)
    Type: constant
    Subs: ['final sources']


    """
    return xrmerge(
        xr.DataArray(0, {"final sources": ["electricity"]}, ["final sources"]),
        xr.DataArray(0, {"final sources": ["heat"]}, ["final sources"]),
        rearrange(
            if_then_else(
                float(nonenergy_use_demand_by_final_fuel_ej().loc["liquids"]) > 0.01,
                lambda: 0.461414 * (gdp_aut() - gdp_delayed_1yr()),
                lambda: 0,
            ),
            ["final sources"],
            {"final sources": ["liquids"]},
        ),
        rearrange(
            if_then_else(
                float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"]) > 0.01,
                lambda: 0.123925 * (gdp_aut() - gdp_delayed_1yr()),
                lambda: 0,
            ),
            ["final sources"],
            {"final sources": ["gases"]},
        ),
        rearrange(
            if_then_else(
                float(nonenergy_use_demand_by_final_fuel_ej().loc["solids"]) > 0.01,
                lambda: 0.0797511 * (gdp_aut() - gdp_delayed_1yr()),
                lambda: 0,
            ),
            ["final sources"],
            {"final sources": ["solids"]},
        ),
    )


_ext_lookup_historic_nonenergy_use = ExtLookup(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_non_energy_use",
    {"final sources": _subscript_dict["final sources"]},
    _root,
    "_ext_lookup_historic_nonenergy_use",
)


_ext_constant_initial_nonenergy_use = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "initial_non_energy_use*",
    {"final sources": _subscript_dict["final sources"]},
    _root,
    "_ext_constant_initial_nonenergy_use",
)


@subs(["final sources"], _subscript_dict)
def _integ_init_nonenergy_use_demand_by_final_fuel_ej():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for nonenergy_use_demand_by_final_fuel_ej
    Limits: None
    Type: setup
    Subs: ['final sources']

    Provides initial conditions for nonenergy_use_demand_by_final_fuel_ej function
    """
    return initial_nonenergy_use()


@subs(["final sources"], _subscript_dict)
def _integ_input_nonenergy_use_demand_by_final_fuel_ej():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for nonenergy_use_demand_by_final_fuel_ej
    Limits: None
    Type: component
    Subs: ['final sources']

    Provides derivative for nonenergy_use_demand_by_final_fuel_ej function
    """
    return annual_variation_nonenergy_use()


_integ_nonenergy_use_demand_by_final_fuel_ej = Integ(
    _integ_input_nonenergy_use_demand_by_final_fuel_ej,
    _integ_init_nonenergy_use_demand_by_final_fuel_ej,
    "_integ_nonenergy_use_demand_by_final_fuel_ej",
)
