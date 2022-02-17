"""
Module exports_demand
Translated using PySD version 2.2.1
"""


@subs(["sectors"], _subscript_dict)
def beta_0_exp_0():
    """
    Real Name: beta 0 EXP 0
    Original Eqn: GET DIRECT CONSTANTS('../economy.xlsx', 'Catalonia', 'beta_0_EXP_0*')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['sectors']

    Beta coefficient of panel data regression of export demand (level 0,
        world).
    """
    return _ext_constant_beta_0_exp_0()


@subs(["sectors"], _subscript_dict)
def beta_0_exp_1():
    """
    Real Name: beta 0 EXP 1
    Original Eqn: GET DIRECT CONSTANTS('../economy.xlsx', 'Catalonia', 'beta_0_EXP_1*')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['sectors']

    Beta coefficient of panel data regression of export demand (level 1,
        intermediate nesting).
    """
    return _ext_constant_beta_0_exp_1()


def beta_1_exp_0():
    """
    Real Name: beta 1 EXP 0
    Original Eqn: GET DIRECT CONSTANTS('../economy.xlsx', 'Catalonia', 'beta_1_EXP_0')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Beta coefficient of panel data regression of exports demand (level 0,
        world).
    """
    return _ext_constant_beta_1_exp_0()


def beta_1_exp_1():
    """
    Real Name: beta 1 EXP 1
    Original Eqn: GET DIRECT CONSTANTS('../economy.xlsx', 'Catalonia', 'beta_1_EXP_1')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Beta coefficient of panel data regression of exports demand (level 1,
        intermediate nesting).
    """
    return _ext_constant_beta_1_exp_1()


@subs(["sectors"], _subscript_dict)
def exports_demand_not_covered_row():
    """
    Real Name: Exports demand not covered RoW
    Original Eqn: IF THEN ELSE(Time<2009,0,Exports demand to RoW[sectors]-Real Exports demand to RoW by sector[sectors])
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
        lambda: exports_demand_to_row() - real_exports_demand_to_row_by_sector(),
    )


@subs(["sectors"], _subscript_dict)
def exports_demand_not_covered_to_roeu():
    """
    Real Name: Exports demand not covered to RoEU
    Original Eqn: IF THEN ELSE(Time<2009,0,Exports demand to RoEU[sectors]-Real Exports demand to RoEU by sector[sectors])
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
        lambda: exports_demand_to_roeu() - real_exports_demand_to_roeu_by_sector(),
    )


@subs(["sectors"], _subscript_dict)
def exports_demand_to_roeu():
    """
    Real Name: Exports demand to RoEU
    Original Eqn: INTEG ( variation exports demand to RoEU[sectors]-Exports demand not covered to RoEU[sectors], Initial exports demand to RoEU[sectors])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Sectorial value of exports
    """
    return _integ_exports_demand_to_roeu()


@subs(["sectors"], _subscript_dict)
def exports_demand_to_row():
    """
    Real Name: Exports demand to RoW
    Original Eqn: INTEG ( variation exports demand to RoW[sectors]-Exports demand not covered RoW[ sectors], Initial exports demand to RoW[sectors])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Sectorial value of exports
    """
    return _integ_exports_demand_to_row()


def gdp_eu28_next_step():
    """
    Real Name: GDP EU28 next step
    Original Eqn: GDP EU28*(1+Annual GDP growth rate EU28)
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return gdp_eu28() * (1 + annual_gdp_growth_rate_eu28())


def historic_exports_demand_0(x):
    """
    Real Name: historic exports demand 0
    Original Eqn: GET DIRECT LOOKUPS('../economy.xlsx', 'Catalonia', 'time_index_2009', 'historic_exports_demand_0')
    Units: Mdollars
    Limits: (None, None)
    Type: lookup
    Subs: ['sectors']

    Historic final exports to level 0 (Rest of the World).
    """
    return _ext_lookup_historic_exports_demand_0(x)


def historic_exports_demand_1(x):
    """
    Real Name: historic exports demand 1
    Original Eqn: GET DIRECT LOOKUPS('../economy.xlsx', 'Catalonia', 'time_index_2009', 'historic_exports_demand_1')
    Units: Mdollars
    Limits: (None, None)
    Type: lookup
    Subs: ['sectors']

    Historic final exports to level 1 (intermediate nesting).
    """
    return _ext_lookup_historic_exports_demand_1(x)


@subs(["sectors"], _subscript_dict)
def initial_exports_demand_to_roeu():
    """
    Real Name: Initial exports demand to RoEU
    Original Eqn: historic exports demand 1[sectors](1995)
    Units: Mdollars
    Limits: (None, None)
    Type: constant
    Subs: ['sectors']

    Initial value of sectorial exports
    """
    return historic_exports_demand_1(1995)


@subs(["sectors"], _subscript_dict)
def initial_exports_demand_to_row():
    """
    Real Name: Initial exports demand to RoW
    Original Eqn: historic exports demand 0[sectors](1995)
    Units: Mdollars
    Limits: (None, None)
    Type: constant
    Subs: ['sectors']

    Initial value of sectorial exports
    """
    return historic_exports_demand_0(1995)


def real_demand_world_next_step():
    """
    Real Name: real demand world next step
    Original Eqn: Real demand World*(1+Annual GDP growth rate World)
    Units: Mdollar
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return real_demand_world() * (1 + annual_gdp_growth_rate_world())


def total_exports():
    """
    Real Name: Total exports
    Original Eqn: Total exports to RoEU+Total exports to RoW
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return total_exports_to_roeu() + total_exports_to_row()


def total_exports_to_roeu():
    """
    Real Name: Total exports to RoEU
    Original Eqn: SUM(Exports demand to RoEU[sectors!])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: None

    Whole economy exports
    """
    return sum(exports_demand_to_roeu(), dim=("sectors",))


def total_exports_to_row():
    """
    Real Name: Total exports to RoW
    Original Eqn: SUM(Exports demand to RoW[sectors!])
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: None

    Whole economy exports
    """
    return sum(exports_demand_to_row(), dim=("sectors",))


@subs(["sectors"], _subscript_dict)
def variation_exports_demand_to_roeu():
    """
    Real Name: variation exports demand to RoEU
    Original Eqn: IF THEN ELSE(Exports demand to RoEU[sectors]<0, 0, IF THEN ELSE(Time<2009, variation historic exports demand to RoEU[sectors], EXP(beta 0 EXP 1[sectors])*(GDP EU28 next step^beta 1 EXP 1-GDP EU28^beta 1 EXP 1)))
    Units: Mdollars/Year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Variation of exports by industrial sectors
    """
    return if_then_else(
        exports_demand_to_roeu() < 0,
        lambda: 0,
        lambda: if_then_else(
            time() < 2009,
            lambda: variation_historic_exports_demand_to_roeu(),
            lambda: np.exp(beta_0_exp_1())
            * (gdp_eu28_next_step() ** beta_1_exp_1() - gdp_eu28() ** beta_1_exp_1()),
        ),
    )


@subs(["sectors"], _subscript_dict)
def variation_exports_demand_to_row():
    """
    Real Name: variation exports demand to RoW
    Original Eqn: IF THEN ELSE(Exports demand to RoW[sectors]<0, 0, IF THEN ELSE(Time<2009, variation historic exports demand row[sectors], EXP(beta 0 EXP 0[sectors])*(real demand world next step^beta 1 EXP 0-Real demand World^beta 1 EXP 0)))
    Units: Mdollars/Year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Variation of exports by industrial sectors
    """
    return if_then_else(
        exports_demand_to_row() < 0,
        lambda: 0,
        lambda: if_then_else(
            time() < 2009,
            lambda: variation_historic_exports_demand_row(),
            lambda: np.exp(beta_0_exp_0())
            * (
                real_demand_world_next_step() ** beta_1_exp_0()
                - real_demand_world() ** beta_1_exp_0()
            ),
        ),
    )


@subs(["sectors"], _subscript_dict)
def variation_historic_exports_demand_row():
    """
    Real Name: variation historic exports demand row
    Original Eqn: historic exports demand 0[sectors](INTEGER(Time+1))-historic exports demand 0[sectors](INTEGER(Time))
    Units: Mdollars/Year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Historic variation of exports (WIOD-35 sectors)
    """
    return historic_exports_demand_0(integer(time() + 1)) - historic_exports_demand_0(
        integer(time())
    )


@subs(["sectors"], _subscript_dict)
def variation_historic_exports_demand_to_roeu():
    """
    Real Name: variation historic exports demand to RoEU
    Original Eqn: historic exports demand 1[sectors](INTEGER(Time+1))-historic exports demand 1[sectors](INTEGER(Time))
    Units: Mdollars/Year
    Limits: (None, None)
    Type: component
    Subs: ['sectors']

    Historic variation of exports (WIOD-35 sectors)
    """
    return historic_exports_demand_1(integer(time() + 1)) - historic_exports_demand_1(
        integer(time())
    )


_ext_constant_beta_0_exp_0 = ExtConstant(
    "../economy.xlsx",
    "Catalonia",
    "beta_0_EXP_0*",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_constant_beta_0_exp_0",
)


_ext_constant_beta_0_exp_1 = ExtConstant(
    "../economy.xlsx",
    "Catalonia",
    "beta_0_EXP_1*",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_constant_beta_0_exp_1",
)


_ext_constant_beta_1_exp_0 = ExtConstant(
    "../economy.xlsx",
    "Catalonia",
    "beta_1_EXP_0",
    {},
    _root,
    "_ext_constant_beta_1_exp_0",
)


_ext_constant_beta_1_exp_1 = ExtConstant(
    "../economy.xlsx",
    "Catalonia",
    "beta_1_EXP_1",
    {},
    _root,
    "_ext_constant_beta_1_exp_1",
)


@subs(["sectors"], _subscript_dict)
def _integ_init_exports_demand_to_roeu():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for exports_demand_to_roeu
    Limits: None
    Type: setup
    Subs: ['sectors']

    Provides initial conditions for exports_demand_to_roeu function
    """
    return initial_exports_demand_to_roeu()


@subs(["sectors"], _subscript_dict)
def _integ_input_exports_demand_to_roeu():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for exports_demand_to_roeu
    Limits: None
    Type: component
    Subs: ['sectors']

    Provides derivative for exports_demand_to_roeu function
    """
    return variation_exports_demand_to_roeu() - exports_demand_not_covered_to_roeu()


_integ_exports_demand_to_roeu = Integ(
    _integ_input_exports_demand_to_roeu,
    _integ_init_exports_demand_to_roeu,
    "_integ_exports_demand_to_roeu",
)


@subs(["sectors"], _subscript_dict)
def _integ_init_exports_demand_to_row():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for exports_demand_to_row
    Limits: None
    Type: setup
    Subs: ['sectors']

    Provides initial conditions for exports_demand_to_row function
    """
    return initial_exports_demand_to_row()


@subs(["sectors"], _subscript_dict)
def _integ_input_exports_demand_to_row():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for exports_demand_to_row
    Limits: None
    Type: component
    Subs: ['sectors']

    Provides derivative for exports_demand_to_row function
    """
    return variation_exports_demand_to_row() - exports_demand_not_covered_row()


_integ_exports_demand_to_row = Integ(
    _integ_input_exports_demand_to_row,
    _integ_init_exports_demand_to_row,
    "_integ_exports_demand_to_row",
)


_ext_lookup_historic_exports_demand_0 = ExtLookup(
    "../economy.xlsx",
    "Catalonia",
    "time_index_2009",
    "historic_exports_demand_0",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_lookup_historic_exports_demand_0",
)


_ext_lookup_historic_exports_demand_1 = ExtLookup(
    "../economy.xlsx",
    "Catalonia",
    "time_index_2009",
    "historic_exports_demand_1",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_lookup_historic_exports_demand_1",
)
