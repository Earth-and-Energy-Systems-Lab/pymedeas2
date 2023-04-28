"""
Module economy.exports_demand
Translated using PySD version 3.9.1
"""


@component.add(
    name="beta 0 EXP",
    units="Dmnl",
    subscripts=["sectors"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_beta_0_exp"},
)
def beta_0_exp():
    """
    Beta coefficient of panel data regression of export demand.
    """
    return _ext_constant_beta_0_exp()


_ext_constant_beta_0_exp = ExtConstant(
    "../economy.xlsx",
    "Europe",
    "beta_0_EXP*",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_constant_beta_0_exp",
)


@component.add(
    name="beta 0 GFCF",
    units="Dmnl",
    subscripts=["sectors"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_beta_0_gfcf"},
)
def beta_0_gfcf():
    """
    Beta coefficient of panel data regression of gross fixed capital formation.
    """
    return _ext_constant_beta_0_gfcf()


_ext_constant_beta_0_gfcf = ExtConstant(
    "../economy.xlsx",
    "Europe",
    "beta_0_GFCF*",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_constant_beta_0_gfcf",
)


@component.add(
    name="beta 1 EXP",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_beta_1_exp"},
)
def beta_1_exp():
    """
    Beta coefficient of panel data regression of exports demand.
    """
    return _ext_constant_beta_1_exp()


_ext_constant_beta_1_exp = ExtConstant(
    "../economy.xlsx", "Europe", "beta_1_EXP", {}, _root, {}, "_ext_constant_beta_1_exp"
)


@component.add(
    name="beta 1 GFCF",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_beta_1_gfcf"},
)
def beta_1_gfcf():
    """
    Beta coefficient of panel data regression of gross fixed capital formation.
    """
    return _ext_constant_beta_1_gfcf()


_ext_constant_beta_1_gfcf = ExtConstant(
    "../economy.xlsx",
    "Europe",
    "beta_1_GFCF",
    {},
    _root,
    {},
    "_ext_constant_beta_1_gfcf",
)


@component.add(
    name="Exports demand",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_exports_demand": 1},
    other_deps={
        "_integ_exports_demand": {
            "initial": {"initial_exports_demand": 1},
            "step": {"variation_exports_demand": 1, "exports_demand_not_covered": 1},
        }
    },
)
def exports_demand():
    """
    Sectorial value of exports
    """
    return _integ_exports_demand()


_integ_exports_demand = Integ(
    lambda: variation_exports_demand() - exports_demand_not_covered(),
    lambda: initial_exports_demand(),
    "_integ_exports_demand",
)


@component.add(
    name="Exports demand not covered",
    units="Mdollars/Year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "exports_demand": 1, "real_exports_demand_by_sector": 1},
)
def exports_demand_not_covered():
    """
    Gap between exports required and real exports (after energy-economy feedback)
    """
    return if_then_else(
        time() < 2009,
        lambda: xr.DataArray(0, {"sectors": _subscript_dict["sectors"]}, ["sectors"]),
        lambda: exports_demand() - real_exports_demand_by_sector(),
    )


@component.add(
    name="GFCF not covered",
    units="Mdollars/Year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "gross_fixed_capital_formation": 1,
        "real_gfcf_by_sector": 1,
    },
)
def gfcf_not_covered():
    """
    Gap between gross fixed capital formation required and real gross fixed capital formation (after energy-economy feedback)
    """
    return if_then_else(
        time() < 2009,
        lambda: xr.DataArray(0, {"sectors": _subscript_dict["sectors"]}, ["sectors"]),
        lambda: gross_fixed_capital_formation() - real_gfcf_by_sector(),
    )


@component.add(
    name="Gross fixed capital formation",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_gross_fixed_capital_formation": 1},
    other_deps={
        "_integ_gross_fixed_capital_formation": {
            "initial": {"initial_gfcf": 1},
            "step": {"variation_gfcf": 1, "gfcf_not_covered": 1},
        }
    },
)
def gross_fixed_capital_formation():
    """
    Sectorial domestic value of gross fixed capital formation
    """
    return _integ_gross_fixed_capital_formation()


_integ_gross_fixed_capital_formation = Integ(
    lambda: variation_gfcf() - gfcf_not_covered(),
    lambda: initial_gfcf(),
    "_integ_gross_fixed_capital_formation",
)


@component.add(
    name="historic exports demand",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_exports_demand",
        "__lookup__": "_ext_lookup_historic_exports_demand",
    },
)
def historic_exports_demand(x, final_subs=None):
    """
    Historic final exports to RoW.
    """
    return _ext_lookup_historic_exports_demand(x, final_subs)


_ext_lookup_historic_exports_demand = ExtLookup(
    "../economy.xlsx",
    "Europe",
    "time_index_2009",
    "historic_exports_demand",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_lookup_historic_exports_demand",
)


@component.add(
    name="historic GFCF",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_gfcf",
        "__lookup__": "_ext_lookup_historic_gfcf",
    },
)
def historic_gfcf(x, final_subs=None):
    """
    Historic gross fixed capital formation (14 sectors).
    """
    return _ext_lookup_historic_gfcf(x, final_subs)


_ext_lookup_historic_gfcf = ExtLookup(
    "../economy.xlsx",
    "Europe",
    "time_index2009",
    "historic_GFCF",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_lookup_historic_gfcf",
)


@component.add(
    name="Initial exports demand",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_exports_demand": 1},
)
def initial_exports_demand():
    """
    Initial value of sectorial exports
    """
    return historic_exports_demand(1995)


@component.add(
    name="initial GFCF",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_gfcf": 1},
)
def initial_gfcf():
    """
    Initial value of gross fixed capital formation
    """
    return historic_gfcf(1995)


@component.add(
    name="real demand world next step",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_demand_world": 1, "annual_gdp_growth_rate_world": 1},
)
def real_demand_world_next_step():
    return real_demand_world() * (1 + annual_gdp_growth_rate_world())


@component.add(
    name="Total exports",
    units="Mdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"exports_demand": 1},
)
def total_exports():
    """
    Whole economy exports
    """
    return sum(exports_demand().rename({"sectors": "sectors!"}), dim=["sectors!"])


@component.add(
    name="Total GFCF",
    units="Mdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gross_fixed_capital_formation": 1},
)
def total_gfcf():
    """
    Whole economy domestic gross fixed capital formation
    """
    return sum(
        gross_fixed_capital_formation().rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    )


@component.add(
    name="variation exports demand",
    units="Mdollars/Year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "exports_demand": 1,
        "time": 1,
        "variation_historic_exports_demand": 1,
        "real_demand_world": 1,
        "beta_0_exp": 1,
        "real_demand_world_next_step": 1,
        "beta_1_exp": 2,
    },
)
def variation_exports_demand():
    """
    Variation of exports by industrial sectors
    """
    return if_then_else(
        exports_demand() < 0,
        lambda: xr.DataArray(0, {"sectors": _subscript_dict["sectors"]}, ["sectors"]),
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


@component.add(
    name="variation GFCF",
    units="Mdollars/Year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gross_fixed_capital_formation": 1,
        "time": 1,
        "variation_cc": 1,
        "variation_historic_gfcf": 1,
        "beta_1_gfcf": 2,
        "beta_0_gfcf": 1,
        "cc_total": 2,
    },
)
def variation_gfcf():
    """
    Variation of domestic gross fixed capital formation by industrial sectors
    """
    return if_then_else(
        gross_fixed_capital_formation() <= 0,
        lambda: xr.DataArray(0, {"sectors": _subscript_dict["sectors"]}, ["sectors"]),
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


@component.add(
    name="variation historic exports demand",
    units="Mdollars/Year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "historic_exports_demand": 2},
)
def variation_historic_exports_demand():
    """
    Historic variation of exports (WIOD-35 sectors)
    """
    return historic_exports_demand(integer(time() + 1)) - historic_exports_demand(
        integer(time())
    )


@component.add(
    name="variation historic GFCF",
    units="Mdollars/Year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "historic_gfcf": 2},
)
def variation_historic_gfcf():
    """
    Historic variation of gross fixed capital formation (WIOD-35 sectors)
    """
    return historic_gfcf(integer(time() + 1)) - historic_gfcf(integer(time()))
