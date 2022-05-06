"""
Module households_economic_demand_and_investment
Translated using PySD version 3.0.0-dev
"""


@component.add(
    name="beta 1 HD",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_beta_1_hd"},
)
def beta_1_hd():
    """
    Beta coefficient of panel data regression of households demand.
    """
    return _ext_constant_beta_1_hd()


_ext_constant_beta_1_hd = ExtConstant(
    "../economy.xlsx",
    "Catalonia",
    "beta_1_HD",
    {},
    _root,
    {},
    "_ext_constant_beta_1_hd",
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
    "Catalonia",
    "beta_0_GFCF*",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_constant_beta_0_gfcf",
)


@component.add(
    name="beta 0 HD",
    units="Dmnl",
    subscripts=["sectors"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_beta_0_hd"},
)
def beta_0_hd():
    """
    Beta coefficient of panel data regression of households demand.
    """
    return _ext_constant_beta_0_hd()


_ext_constant_beta_0_hd = ExtConstant(
    "../economy.xlsx",
    "Catalonia",
    "beta_0_HD*",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_constant_beta_0_hd",
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
    "Catalonia",
    "beta_1_GFCF",
    {},
    _root,
    {},
    "_ext_constant_beta_1_gfcf",
)


@component.add(
    name="GFCF not covered",
    units="Mdollars/Year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "real_gfcf_by_sector": 1,
        "gross_fixed_capital_formation": 1,
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
    "Catalonia",
    "time_index2009",
    "historic_GFCF",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_lookup_historic_gfcf",
)


@component.add(
    name="historic HD",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_hd",
        "__lookup__": "_ext_lookup_historic_hd",
    },
)
def historic_hd(x, final_subs=None):
    """
    Historical final demand by households (14 sectors).
    """
    return _ext_lookup_historic_hd(x, final_subs)


_ext_lookup_historic_hd = ExtLookup(
    "../economy.xlsx",
    "Catalonia",
    "time_index2009",
    "historic_HD",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_lookup_historic_hd",
)


@component.add(
    name="Household demand",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_household_demand": 1},
    other_deps={
        "_integ_household_demand": {
            "initial": {"initial_household_demand": 1},
            "step": {
                "variation_household_demand": 1,
                "household_demand_not_covered": 1,
            },
        }
    },
)
def household_demand():
    """
    Sectorial domestic final demand made by Households
    """
    return _integ_household_demand()


_integ_household_demand = Integ(
    lambda: variation_household_demand() - household_demand_not_covered(),
    lambda: initial_household_demand(),
    "_integ_household_demand",
)


@component.add(
    name="Household demand not covered",
    units="Mdollars/Year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "household_demand": 1, "real_household_demand_by_sector": 1},
)
def household_demand_not_covered():
    """
    Gap between households consumption required and households real consumption (after energy-economy feedback)
    """
    return if_then_else(
        time() < 2009,
        lambda: xr.DataArray(0, {"sectors": _subscript_dict["sectors"]}, ["sectors"]),
        lambda: household_demand() - real_household_demand_by_sector(),
    )


@component.add(
    name="Household demand total",
    units="Mdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"household_demand": 1},
)
def household_demand_total():
    """
    Whole economy domestic households demand
    """
    return sum(household_demand().rename({"sectors": "sectors!"}), dim=["sectors!"])


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
    name="initial household demand",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_hd": 1},
)
def initial_household_demand():
    """
    Initial final demand by households
    """
    return historic_hd(1995)


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
    name="variation GFCF",
    units="Mdollars/Year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gross_fixed_capital_formation": 1,
        "beta_0_gfcf": 1,
        "variation_historic_gfcf": 1,
        "beta_1_gfcf": 2,
        "variation_cc": 1,
        "time": 1,
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
    name="variation historic demand",
    units="Mdollars/Year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "historic_hd": 2},
)
def variation_historic_demand():
    """
    Variation of final demand by households
    """
    return historic_hd(integer(time() + 1)) - historic_hd(integer(time()))


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


@component.add(
    name="variation household demand",
    units="Mdollars/Year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "variation_historic_demand": 1,
        "beta_0_hd": 1,
        "variation_lc": 1,
        "lc": 2,
        "beta_1_hd": 2,
    },
)
def variation_household_demand():
    """
    Variation of final demand by households by industrial sectors
    """
    return if_then_else(
        time() < 2009,
        lambda: variation_historic_demand(),
        lambda: np.exp(beta_0_hd())
        * ((lc() + variation_lc()) ** beta_1_hd() - lc() ** beta_1_hd()),
    )
