"""
Module households_economic_demand
Translated using PySD version 2.2.1
"""


@subs(["sectors"], _subscript_dict)
def beta_0_hd():
    """
    Real Name: beta 0 HD
    Original Eqn: GET DIRECT CONSTANTS('../economy.xlsx', 'Europe', 'beta_0_HD*')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['sectors']

    Beta coefficient of panel data regression of households demand.
    """
    return _ext_constant_beta_0_hd()


def beta_1_hd():
    """
    Real Name: beta 1 HD
    Original Eqn: GET DIRECT CONSTANTS('../economy.xlsx', 'Europe', 'beta_1_HD')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Beta coefficient of panel data regression of households demand.
    """
    return _ext_constant_beta_1_hd()


def historic_hd(x):
    """
    Real Name: historic HD
    Original Eqn: GET DIRECT LOOKUPS('../economy.xlsx', 'Europe', 'time_index2009', 'historic_HD')
    Units: Mdollars
    Limits: (None, None)
    Type: lookup
    Subs: ['sectors']

    Historical final demand by households (14 sectors).
    """
    return _ext_lookup_historic_hd(x)


@subs(["sectors"], _subscript_dict)
def household_demand():
    """
    Real Name: Household demand
    Original Eqn: INTEG ( variation household demand[sectors]-Household demand not covered[ sectors], initial household demand[sectors])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Sectorial domestic final demand made by Households
    """
    return _integ_household_demand()


@subs(["sectors"], _subscript_dict)
def household_demand_not_covered():
    """
    Real Name: Household demand not covered
    Original Eqn: IF THEN ELSE(Time<2009,0,Household demand[sectors]-Real Household demand by sector[sectors])
    Units: Mdollars/Year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Gap between households consumption required and households real
        consumption (after energy-economy feedback)
    """
    return if_then_else(
        time() < 2009,
        lambda: 0,
        lambda: household_demand() - real_household_demand_by_sector(),
    )


def household_demand_total():
    """
    Real Name: Household demand total
    Original Eqn: SUM(Household demand[sectors!])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: None

    Whole economy domestic households demand
    """
    return sum(household_demand(), dim=("sectors",))


@subs(["sectors"], _subscript_dict)
def initial_household_demand():
    """
    Real Name: initial household demand
    Original Eqn: historic HD[sectors](1995)
    Units:
    Limits: (None, None)
    Type: constant
    Subs: ['sectors']

    Initial final demand by households
    """
    return historic_hd(1995)


@subs(["sectors"], _subscript_dict)
def variation_historic_demand():
    """
    Real Name: variation historic demand
    Original Eqn: historic HD[sectors](INTEGER(Time+1))-historic HD[sectors](INTEGER(Time))
    Units: Mdollars/Year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Variation of final demand by households
    """
    return historic_hd(integer(time() + 1)) - historic_hd(integer(time()))


@subs(["sectors"], _subscript_dict)
def variation_household_demand():
    """
    Real Name: variation household demand
    Original Eqn: IF THEN ELSE(Time<2009, variation historic demand[sectors], EXP(beta 0 HD[sectors])*((LC+variation LC)^beta 1 HD-LC^beta 1 HD) )
    Units: Mdollars/Year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Variation of final demand by households by industrial sectors
    """
    return if_then_else(
        time() < 2009,
        lambda: variation_historic_demand(),
        lambda: np.exp(beta_0_hd())
        * ((lc() + variation_lc()) ** beta_1_hd() - lc() ** beta_1_hd()),
    )


_ext_constant_beta_0_hd = ExtConstant(
    "../economy.xlsx",
    "Europe",
    "beta_0_HD*",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_constant_beta_0_hd",
)


_ext_constant_beta_1_hd = ExtConstant(
    "../economy.xlsx", "Europe", "beta_1_HD", {}, _root, "_ext_constant_beta_1_hd"
)


_ext_lookup_historic_hd = ExtLookup(
    "../economy.xlsx",
    "Europe",
    "time_index2009",
    "historic_HD",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_lookup_historic_hd",
)


@subs(["sectors"], _subscript_dict)
def _integ_init_household_demand():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for household_demand
    Limits: None
    Type: setup
    Subs: ['sectors']

    Provides initial conditions for household_demand function
    """
    return initial_household_demand()


@subs(["sectors"], _subscript_dict)
def _integ_input_household_demand():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for household_demand
    Limits: None
    Type: component
    Subs: ['sectors']

    Provides derivative for household_demand function
    """
    return variation_household_demand() - household_demand_not_covered()


_integ_household_demand = Integ(
    _integ_input_household_demand,
    _integ_init_household_demand,
    "_integ_household_demand",
)
