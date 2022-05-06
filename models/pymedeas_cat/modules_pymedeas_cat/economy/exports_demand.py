"""
Module exports_demand
Translated using PySD version 3.0.0-dev
"""


@component.add(
    name="Exports demand not covered RoW",
    units="Mdollars/Year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "real_exports_demand_to_row_by_sector": 1,
        "exports_demand_to_row": 1,
    },
)
def exports_demand_not_covered_row():
    """
    Gap between exports required and real exports (after energy-economy feedback)
    """
    return if_then_else(
        time() < 2009,
        lambda: xr.DataArray(0, {"sectors": _subscript_dict["sectors"]}, ["sectors"]),
        lambda: exports_demand_to_row() - real_exports_demand_to_row_by_sector(),
    )


@component.add(
    name="Exports demand to RoEU",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_exports_demand_to_roeu": 1},
    other_deps={
        "_integ_exports_demand_to_roeu": {
            "initial": {"initial_exports_demand_to_roeu": 1},
            "step": {
                "variation_exports_demand_to_roeu": 1,
                "exports_demand_not_covered_to_roeu": 1,
            },
        }
    },
)
def exports_demand_to_roeu():
    """
    Sectorial value of exports
    """
    return _integ_exports_demand_to_roeu()


_integ_exports_demand_to_roeu = Integ(
    lambda: variation_exports_demand_to_roeu() - exports_demand_not_covered_to_roeu(),
    lambda: initial_exports_demand_to_roeu(),
    "_integ_exports_demand_to_roeu",
)


@component.add(
    name="beta 0 EXP 0",
    units="Dmnl",
    subscripts=["sectors"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_beta_0_exp_0"},
)
def beta_0_exp_0():
    """
    Beta coefficient of panel data regression of export demand (level 0, world).
    """
    return _ext_constant_beta_0_exp_0()


_ext_constant_beta_0_exp_0 = ExtConstant(
    "../economy.xlsx",
    "Catalonia",
    "beta_0_EXP_0*",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_constant_beta_0_exp_0",
)


@component.add(
    name="beta 0 EXP 1",
    units="Dmnl",
    subscripts=["sectors"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_beta_0_exp_1"},
)
def beta_0_exp_1():
    """
    Beta coefficient of panel data regression of export demand (level 1, intermediate nesting).
    """
    return _ext_constant_beta_0_exp_1()


_ext_constant_beta_0_exp_1 = ExtConstant(
    "../economy.xlsx",
    "Catalonia",
    "beta_0_EXP_1*",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_constant_beta_0_exp_1",
)


@component.add(
    name="beta 1 EXP 0",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_beta_1_exp_0"},
)
def beta_1_exp_0():
    """
    Beta coefficient of panel data regression of exports demand (level 0, world).
    """
    return _ext_constant_beta_1_exp_0()


_ext_constant_beta_1_exp_0 = ExtConstant(
    "../economy.xlsx",
    "Catalonia",
    "beta_1_EXP_0",
    {},
    _root,
    {},
    "_ext_constant_beta_1_exp_0",
)


@component.add(
    name="beta 1 EXP 1",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_beta_1_exp_1"},
)
def beta_1_exp_1():
    """
    Beta coefficient of panel data regression of exports demand (level 1, intermediate nesting).
    """
    return _ext_constant_beta_1_exp_1()


_ext_constant_beta_1_exp_1 = ExtConstant(
    "../economy.xlsx",
    "Catalonia",
    "beta_1_EXP_1",
    {},
    _root,
    {},
    "_ext_constant_beta_1_exp_1",
)


@component.add(
    name="Exports demand not covered to RoEU",
    units="Mdollars/Year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "real_exports_demand_to_roeu_by_sector": 1,
        "exports_demand_to_roeu": 1,
    },
)
def exports_demand_not_covered_to_roeu():
    """
    Gap between exports required and real exports (after energy-economy feedback)
    """
    return if_then_else(
        time() < 2009,
        lambda: xr.DataArray(0, {"sectors": _subscript_dict["sectors"]}, ["sectors"]),
        lambda: exports_demand_to_roeu() - real_exports_demand_to_roeu_by_sector(),
    )


@component.add(
    name="Exports demand to RoW",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_exports_demand_to_row": 1},
    other_deps={
        "_integ_exports_demand_to_row": {
            "initial": {"initial_exports_demand_to_row": 1},
            "step": {
                "variation_exports_demand_to_row": 1,
                "exports_demand_not_covered_row": 1,
            },
        }
    },
)
def exports_demand_to_row():
    """
    Sectorial value of exports
    """
    return _integ_exports_demand_to_row()


_integ_exports_demand_to_row = Integ(
    lambda: variation_exports_demand_to_row() - exports_demand_not_covered_row(),
    lambda: initial_exports_demand_to_row(),
    "_integ_exports_demand_to_row",
)


@component.add(
    name="GDP EU28 next step",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gdp_eu28": 1, "annual_gdp_growth_rate_eu28": 1},
)
def gdp_eu28_next_step():
    return gdp_eu28() * (1 + annual_gdp_growth_rate_eu28())


@component.add(
    name="historic exports demand 0",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_exports_demand_0",
        "__lookup__": "_ext_lookup_historic_exports_demand_0",
    },
)
def historic_exports_demand_0(x, final_subs=None):
    """
    Historic final exports to level 0 (Rest of the World).
    """
    return _ext_lookup_historic_exports_demand_0(x, final_subs)


_ext_lookup_historic_exports_demand_0 = ExtLookup(
    "../economy.xlsx",
    "Catalonia",
    "time_index_2009",
    "historic_exports_demand_0",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_lookup_historic_exports_demand_0",
)


@component.add(
    name="historic exports demand 1",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_exports_demand_1",
        "__lookup__": "_ext_lookup_historic_exports_demand_1",
    },
)
def historic_exports_demand_1(x, final_subs=None):
    """
    Historic final exports to level 1 (intermediate nesting).
    """
    return _ext_lookup_historic_exports_demand_1(x, final_subs)


_ext_lookup_historic_exports_demand_1 = ExtLookup(
    "../economy.xlsx",
    "Catalonia",
    "time_index_2009",
    "historic_exports_demand_1",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_lookup_historic_exports_demand_1",
)


@component.add(
    name="Initial exports demand to RoEU",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_exports_demand_1": 1},
)
def initial_exports_demand_to_roeu():
    """
    Initial value of sectorial exports
    """
    return historic_exports_demand_1(1995)


@component.add(
    name="Initial exports demand to RoW",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_exports_demand_0": 1},
)
def initial_exports_demand_to_row():
    """
    Initial value of sectorial exports
    """
    return historic_exports_demand_0(1995)


@component.add(
    name="real demand world next step",
    units="Mdollar",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_demand_world": 1, "annual_gdp_growth_rate_world": 1},
)
def real_demand_world_next_step():
    return real_demand_world() * (1 + annual_gdp_growth_rate_world())


@component.add(
    name="Total exports",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_exports_to_roeu": 1, "total_exports_to_row": 1},
)
def total_exports():
    return total_exports_to_roeu() + total_exports_to_row()


@component.add(
    name="Total exports to RoEU",
    units="Mdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"exports_demand_to_roeu": 1},
)
def total_exports_to_roeu():
    """
    Whole economy exports
    """
    return sum(
        exports_demand_to_roeu().rename({"sectors": "sectors!"}), dim=["sectors!"]
    )


@component.add(
    name="Total exports to RoW",
    units="Mdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"exports_demand_to_row": 1},
)
def total_exports_to_row():
    """
    Whole economy exports
    """
    return sum(
        exports_demand_to_row().rename({"sectors": "sectors!"}), dim=["sectors!"]
    )


@component.add(
    name="variation exports demand to RoEU",
    units="Mdollars/Year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "exports_demand_to_roeu": 1,
        "gdp_eu28": 1,
        "variation_historic_exports_demand_to_roeu": 1,
        "beta_1_exp_1": 2,
        "gdp_eu28_next_step": 1,
        "beta_0_exp_1": 1,
        "time": 1,
    },
)
def variation_exports_demand_to_roeu():
    """
    Variation of exports by industrial sectors
    """
    return if_then_else(
        exports_demand_to_roeu() < 0,
        lambda: xr.DataArray(0, {"sectors": _subscript_dict["sectors"]}, ["sectors"]),
        lambda: if_then_else(
            time() < 2009,
            lambda: variation_historic_exports_demand_to_roeu(),
            lambda: np.exp(beta_0_exp_1())
            * (gdp_eu28_next_step() ** beta_1_exp_1() - gdp_eu28() ** beta_1_exp_1()),
        ),
    )


@component.add(
    name="variation exports demand to RoW",
    units="Mdollars/Year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "exports_demand_to_row": 1,
        "real_demand_world_next_step": 1,
        "beta_1_exp_0": 2,
        "beta_0_exp_0": 1,
        "real_demand_world": 1,
        "variation_historic_exports_demand_row": 1,
        "time": 1,
    },
)
def variation_exports_demand_to_row():
    """
    Variation of exports by industrial sectors
    """
    return if_then_else(
        exports_demand_to_row() < 0,
        lambda: xr.DataArray(0, {"sectors": _subscript_dict["sectors"]}, ["sectors"]),
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


@component.add(
    name="variation historic exports demand row",
    units="Mdollars/Year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "historic_exports_demand_0": 2},
)
def variation_historic_exports_demand_row():
    """
    Historic variation of exports (WIOD-35 sectors)
    """
    return historic_exports_demand_0(integer(time() + 1)) - historic_exports_demand_0(
        integer(time())
    )


@component.add(
    name="variation historic exports demand to RoEU",
    units="Mdollars/Year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "historic_exports_demand_1": 2},
)
def variation_historic_exports_demand_to_roeu():
    """
    Historic variation of exports (WIOD-35 sectors)
    """
    return historic_exports_demand_1(integer(time() + 1)) - historic_exports_demand_1(
        integer(time())
    )
