"""
Module investment__exports_demand
Translated using PySD version 2.1.0
"""


@subs(["sectors"], _subscript_dict)
def beta_0_exp():
    """
    Real Name: beta 0 EXP
    Original Eqn: GET DIRECT CONSTANTS('../economy.xlsx', 'Europe', 'beta_0_EXP*')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['sectors']

    Beta coefficient of panel data regression of export demand.
    """
    return _ext_constant_beta_0_exp()


@subs(["sectors"], _subscript_dict)
def beta_0_gfcf():
    """
    Real Name: beta 0 GFCF
    Original Eqn: GET DIRECT CONSTANTS('../economy.xlsx', 'Europe', 'beta_0_GFCF*')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['sectors']

    Beta coefficient of panel data regression of gross fixed capital formation.
    """
    return _ext_constant_beta_0_gfcf()


def beta_1_exp():
    """
    Real Name: beta 1 EXP
    Original Eqn: GET DIRECT CONSTANTS('../economy.xlsx', 'Europe', 'beta_1_EXP')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Beta coefficient of panel data regression of exports demand.
    """
    return _ext_constant_beta_1_exp()


def beta_1_gfcf():
    """
    Real Name: beta 1 GFCF
    Original Eqn: GET DIRECT CONSTANTS('../economy.xlsx', 'Europe', 'beta_1_GFCF')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Beta coefficient of panel data regression of gross fixed capital formation.
    """
    return _ext_constant_beta_1_gfcf()


@subs(["sectors"], _subscript_dict)
def exports_demand():
    """
    Real Name: Exports demand
    Original Eqn: INTEG ( variation exports demand[sectors]-Exports demand not covered[sectors], Initial exports demand[sectors])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Sectorial value of exports
    """
    return _integ_exports_demand()


@subs(["sectors"], _subscript_dict)
def exports_demand_not_covered():
    """
    Real Name: Exports demand not covered
    Original Eqn: IF THEN ELSE(Time<2009,0,Exports demand[sectors]-Real Exports demand by sector[sectors])
    Units: Mdollars/Year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Gap between exports required and real exports (after energy-economy
        feedback)
    """
    return if_then_else(
        time() < 2009,
        lambda: 0,
        lambda: exports_demand() - real_exports_demand_by_sector(),
    )


@subs(["sectors"], _subscript_dict)
def gfcf_not_covered():
    """
    Real Name: GFCF not covered
    Original Eqn: IF THEN ELSE(Time<2009,0,Gross fixed capital formation[sectors]-Real GFCF by sector[sectors])
    Units: Mdollars/Year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Gap between gross fixed capital formation required and real gross fixed
        capital formation (after energy-economy feedback)
    """
    return if_then_else(
        time() < 2009,
        lambda: 0,
        lambda: gross_fixed_capital_formation() - real_gfcf_by_sector(),
    )


@subs(["sectors"], _subscript_dict)
def gross_fixed_capital_formation():
    """
    Real Name: Gross fixed capital formation
    Original Eqn: INTEG ( variation GFCF[sectors]-GFCF not covered[sectors], initial GFCF[sectors])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Sectorial domestic value of gross fixed capital formation
    """
    return _integ_gross_fixed_capital_formation()


def historic_exports_demand(x):
    """
    Real Name: historic exports demand
    Original Eqn: GET DIRECT LOOKUPS('../economy.xlsx', 'Europe', 'time_index_2009', 'historic_exports_demand')
    Units: Mdollars
    Limits: (None, None)
    Type: lookup
    Subs: ['sectors']

    Historic final exports to RoW.
    """
    return _ext_lookup_historic_exports_demand(x)


def historic_gfcf(x):
    """
    Real Name: historic GFCF
    Original Eqn: GET DIRECT LOOKUPS('../economy.xlsx', 'Europe', 'time_index2009', 'historic_GFCF')
    Units: Mdollars
    Limits: (None, None)
    Type: lookup
    Subs: ['sectors']

    Historic gross fixed capital formation (14 sectors).
    """
    return _ext_lookup_historic_gfcf(x)


@subs(["sectors"], _subscript_dict)
def initial_exports_demand():
    """
    Real Name: Initial exports demand
    Original Eqn: historic exports demand[sectors](1995)
    Units: Mdollars
    Limits: (None, None)
    Type: constant
    Subs: ['sectors']

    Initial value of sectorial exports
    """
    return historic_exports_demand(1995)


@subs(["sectors"], _subscript_dict)
def initial_gfcf():
    """
    Real Name: initial GFCF
    Original Eqn: historic GFCF[sectors](1995)
    Units: Mdollars
    Limits: (None, None)
    Type: constant
    Subs: ['sectors']

    Initial value of gross fixed capital formation
    """
    return historic_gfcf(1995)


def real_demand_world_next_step():
    """
    Real Name: real demand world next step
    Original Eqn: Real demand World*(1+Annual GDP growth rate World)
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return real_demand_world() * (1 + annual_gdp_growth_rate_world())


def total_exports():
    """
    Real Name: Total exports
    Original Eqn: SUM(Exports demand[sectors!])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: None

    Whole economy exports
    """
    return sum(exports_demand(), dim=("sectors",))


def total_gfcf():
    """
    Real Name: Total GFCF
    Original Eqn: SUM(Gross fixed capital formation[sectors!])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: None

    Whole economy domestic gross fixed capital formation
    """
    return sum(gross_fixed_capital_formation(), dim=("sectors",))


@subs(["sectors"], _subscript_dict)
def variation_exports_demand():
    """
    Real Name: variation exports demand
    Original Eqn: IF THEN ELSE(Exports demand[sectors]<0, 0, IF THEN ELSE(Time<2009, variation historic exports demand[sectors], EXP(beta 0 EXP[sectors])*(real demand world next step^beta 1 EXP-Real demand World^beta 1 EXP)))
    Units: Mdollars/Year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Variation of exports by industrial sectors
    """
    return if_then_else(
        exports_demand() < 0,
        lambda: 0,
        lambda: if_then_else(
            time() < 2009,
            lambda: variation_historic_exports_demand(),
            lambda: np.exp(beta_0_exp())
            * (
                real_demand_world_next_step() ** beta_1_exp()
                - real_demand_world() ** beta_1_exp()
            ),
        ),
    )


@subs(["sectors"], _subscript_dict)
def variation_gfcf():
    """
    Real Name: variation GFCF
    Original Eqn: IF THEN ELSE(Gross fixed capital formation[sectors]<=0, 0, IF THEN ELSE(Time<2009, variation historic GFCF[sectors],EXP(beta 0 GFCF[sectors])*((CC total +variation CC) ^beta 1 GFCF-CC total^beta 1 GFCF)))
    Units: Mdollars/Year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Variation of domestic gross fixed capital formation by industrial sectors
    """
    return if_then_else(
        gross_fixed_capital_formation() <= 0,
        lambda: 0,
        lambda: if_then_else(
            time() < 2009,
            lambda: variation_historic_gfcf(),
            lambda: np.exp(beta_0_gfcf())
            * (
                (cc_total() + variation_cc()) ** beta_1_gfcf()
                - cc_total() ** beta_1_gfcf()
            ),
        ),
    )


@subs(["sectors"], _subscript_dict)
def variation_historic_exports_demand():
    """
    Real Name: variation historic exports demand
    Original Eqn: historic exports demand[sectors](INTEGER(Time+1))-historic exports demand[sectors](INTEGER(Time))
    Units: Mdollars/Year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Historic variation of exports (WIOD-35 sectors)
    """
    return historic_exports_demand(integer(time() + 1)) - historic_exports_demand(
        integer(time())
    )


@subs(["sectors"], _subscript_dict)
def variation_historic_gfcf():
    """
    Real Name: variation historic GFCF
    Original Eqn: historic GFCF[sectors](INTEGER(Time+1))-historic GFCF[sectors](INTEGER(Time))
    Units: Mdollars/Year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Historic variation of gross fixed capital formation (WIOD-35 sectors)
    """
    return historic_gfcf(integer(time() + 1)) - historic_gfcf(integer(time()))


_ext_constant_beta_0_exp = ExtConstant(
    "../economy.xlsx",
    "Europe",
    "beta_0_EXP*",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_constant_beta_0_exp",
)


_ext_constant_beta_0_gfcf = ExtConstant(
    "../economy.xlsx",
    "Europe",
    "beta_0_GFCF*",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_constant_beta_0_gfcf",
)


_ext_constant_beta_1_exp = ExtConstant(
    "../economy.xlsx", "Europe", "beta_1_EXP", {}, _root, "_ext_constant_beta_1_exp"
)


_ext_constant_beta_1_gfcf = ExtConstant(
    "../economy.xlsx", "Europe", "beta_1_GFCF", {}, _root, "_ext_constant_beta_1_gfcf"
)


@subs(["sectors"], _subscript_dict)
def _integ_init_exports_demand():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for exports_demand
    Limits: None
    Type: setup
    Subs: ['sectors']

    Provides initial conditions for exports_demand function
    """
    return initial_exports_demand()


@subs(["sectors"], _subscript_dict)
def _integ_input_exports_demand():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for exports_demand
    Limits: None
    Type: component
    Subs: ['sectors']

    Provides derivative for exports_demand function
    """
    return variation_exports_demand() - exports_demand_not_covered()


_integ_exports_demand = Integ(
    _integ_input_exports_demand, _integ_init_exports_demand, "_integ_exports_demand"
)


@subs(["sectors"], _subscript_dict)
def _integ_init_gross_fixed_capital_formation():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for gross_fixed_capital_formation
    Limits: None
    Type: setup
    Subs: ['sectors']

    Provides initial conditions for gross_fixed_capital_formation function
    """
    return initial_gfcf()


@subs(["sectors"], _subscript_dict)
def _integ_input_gross_fixed_capital_formation():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for gross_fixed_capital_formation
    Limits: None
    Type: component
    Subs: ['sectors']

    Provides derivative for gross_fixed_capital_formation function
    """
    return variation_gfcf() - gfcf_not_covered()


_integ_gross_fixed_capital_formation = Integ(
    _integ_input_gross_fixed_capital_formation,
    _integ_init_gross_fixed_capital_formation,
    "_integ_gross_fixed_capital_formation",
)


_ext_lookup_historic_exports_demand = ExtLookup(
    "../economy.xlsx",
    "Europe",
    "time_index_2009",
    "historic_exports_demand",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_lookup_historic_exports_demand",
)


_ext_lookup_historic_gfcf = ExtLookup(
    "../economy.xlsx",
    "Europe",
    "time_index2009",
    "historic_GFCF",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_lookup_historic_gfcf",
)
