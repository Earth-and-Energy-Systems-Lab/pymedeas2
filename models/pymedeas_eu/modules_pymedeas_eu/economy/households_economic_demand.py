"""
Module economy.households_economic_demand
Translated using PySD version 3.10.0
"""


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
    "Europe",
    "beta_0_HD*",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_constant_beta_0_hd",
)


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
    "../economy.xlsx", "Europe", "beta_1_HD", {}, _root, {}, "_ext_constant_beta_1_hd"
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
    "Europe",
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
    depends_on={"time": 1, "real_household_demand_by_sector": 1, "household_demand": 1},
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
    name="variation household demand",
    units="Mdollars/Year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "variation_historic_demand": 1,
        "lc": 2,
        "variation_lc": 1,
        "beta_0_hd": 1,
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
