"""
Module sectors_and_households
Translated using PySD version 3.0.0-dev
"""


@component.add(
    name="Annual GDPpc growth rate",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "select_gdppc_evolution_input": 2,
        "input_gdppc_annual_growth": 1,
        "p_customized_year_gdppc_evolution": 1,
        "p_customized_cte_gdppc_variation": 1,
        "time": 1,
        "p_timeseries_gdppc_growth_rate": 2,
    },
)
def annual_gdppc_growth_rate():
    return if_then_else(
        select_gdppc_evolution_input() == 0,
        lambda: input_gdppc_annual_growth(),
        lambda: if_then_else(
            select_gdppc_evolution_input() == 1,
            lambda: p_timeseries_gdppc_growth_rate(),
            lambda: if_then_else(
                time() < p_customized_year_gdppc_evolution(),
                lambda: p_timeseries_gdppc_growth_rate(),
                lambda: p_customized_cte_gdppc_variation(),
            ),
        ),
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
    "World",
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
    "World",
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
    "World",
    "beta_1_GFCF",
    {},
    _root,
    {},
    "_ext_constant_beta_1_gfcf",
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
    "../economy.xlsx", "World", "beta_1_HD", {}, _root, {}, "_ext_constant_beta_1_hd"
)


@component.add(
    name="capital share",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"labour_share": 1},
)
def capital_share():
    """
    Capital share.
    """
    return 1 - labour_share()


@component.add(
    name="CC sectoral",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"cc_total": 1, "share_cc": 1},
)
def cc_sectoral():
    """
    Capital compensation by industrial sectors
    """
    return cc_total() * share_cc()


@component.add(
    name="CC total",
    units="Mdollars",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cc_total": 1},
    other_deps={
        "_integ_cc_total": {
            "initial": {"initial_cc_total": 1},
            "step": {"variation_cc": 1, "cc_total_not_covered": 1},
        }
    },
)
def cc_total():
    """
    Capital compensation
    """
    return _integ_cc_total()


_integ_cc_total = Integ(
    lambda: variation_cc() - cc_total_not_covered(),
    lambda: initial_cc_total(),
    "_integ_cc_total",
)


@component.add(
    name="CC total not covered",
    units="Mdollars/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demand_not_covered_total_fd": 1, "capital_share": 1},
)
def cc_total_not_covered():
    """
    Gap between capital compensation required and real capital compensation (after energy-economy feedback)
    """
    return demand_not_covered_total_fd() * capital_share()


@component.add(
    name="Demand by sector FD",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_demand_by_sector_fd": 1},
    other_deps={
        "_integ_demand_by_sector_fd": {
            "initial": {"initial_demand": 1},
            "step": {
                "variation_demand_flow_fd": 1,
                "demand_not_covered_by_sector_fd": 1,
            },
        }
    },
)
def demand_by_sector_fd():
    """
    Final demand by 35 industrial sectors
    """
    return _integ_demand_by_sector_fd()


_integ_demand_by_sector_fd = Integ(
    lambda: variation_demand_flow_fd() - demand_not_covered_by_sector_fd(),
    lambda: initial_demand(),
    "_integ_demand_by_sector_fd",
)


@component.add(
    name="demand by sector FD adjusted",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demand_by_sector_fd": 1, "diff_demand": 1},
)
def demand_by_sector_fd_adjusted():
    """
    Demand by sector after adjustment to match the desired GDP level.
    """
    return demand_by_sector_fd() * diff_demand()


@component.add(
    name="demand not covered by sector FD",
    units="Mdollars/year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "real_demand_by_sector": 1, "demand_by_sector_fd": 1},
)
def demand_not_covered_by_sector_fd():
    return if_then_else(
        time() > 2009,
        lambda: demand_by_sector_fd() - real_demand_by_sector(),
        lambda: xr.DataArray(0, {"sectors": _subscript_dict["sectors"]}, ["sectors"]),
    )


@component.add(
    name="demand not covered total FD",
    units="Mdollars/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demand_not_covered_by_sector_fd": 1},
)
def demand_not_covered_total_fd():
    return sum(
        demand_not_covered_by_sector_fd().rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    )


@component.add(
    name="Desired annual GDP growth rate",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_gdp": 1, "desired_gdp_delayed_1yr": 1},
)
def desired_annual_gdp_growth_rate():
    """
    Desired annual GDP growth rate.
    """
    return -1 + desired_gdp() / desired_gdp_delayed_1yr()


@component.add(
    name="Desired GDP",
    units="T$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "total_demand": 1,
        "desired_gdppc": 1,
        "population": 1,
        "dollars_to_tdollars": 1,
    },
)
def desired_gdp():
    """
    Desired GDP level for each scenario (user selection). The factor "0.56" corrects for a discrepancy when the TIME STEP < frequency of historical data.
    """
    return if_then_else(
        time() < 2009,
        lambda: total_demand(),
        lambda: desired_gdppc() * population() / dollars_to_tdollars() - 0.56,
    )


@component.add(
    name="Desired GDP delayed 1yr",
    units="T$/year",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_desired_gdp_delayed_1yr": 1},
    other_deps={
        "_delayfixed_desired_gdp_delayed_1yr": {
            "initial": {},
            "step": {"desired_gdp": 1},
        }
    },
)
def desired_gdp_delayed_1yr():
    """
    Desired GDP delayed 1 year.
    """
    return _delayfixed_desired_gdp_delayed_1yr()


_delayfixed_desired_gdp_delayed_1yr = DelayFixed(
    lambda: desired_gdp(),
    lambda: 1,
    lambda: 29.16,
    time_step,
    "_delayfixed_desired_gdp_delayed_1yr",
)


@component.add(
    name="Desired GDPpc",
    units="$/person",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_desired_gdppc": 1},
    other_deps={
        "_integ_desired_gdppc": {
            "initial": {"gdppc_initial_year": 1},
            "step": {"desired_variation_gdppc": 1},
        }
    },
)
def desired_gdppc():
    return _integ_desired_gdppc()


_integ_desired_gdppc = Integ(
    lambda: desired_variation_gdppc(),
    lambda: gdppc_initial_year(),
    "_integ_desired_gdppc",
)


@component.add(
    name="Desired variation GDPpc",
    units="$/person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "variation_historic_gdppc": 1,
        "desired_gdppc": 1,
        "annual_gdppc_growth_rate": 1,
    },
)
def desired_variation_gdppc():
    return if_then_else(
        time() < 2013,
        lambda: variation_historic_gdppc(),
        lambda: desired_gdppc() * annual_gdppc_growth_rate(),
    )


@component.add(
    name="diff demand",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "total_demand": 1,
        "desired_annual_gdp_growth_rate": 1,
        "gdp_delayed_1yr": 1,
    },
)
def diff_demand():
    """
    Ratio between the desired GDP and the real GDP level after applying the demand function.
    """
    return if_then_else(
        time() < 2009,
        lambda: 1,
        lambda: (gdp_delayed_1yr() * (1 + desired_annual_gdp_growth_rate()))
        / total_demand(),
    )


@component.add(
    name="dollar per Mdollar",
    units="dollar/Mdollar",
    comp_type="Constant",
    comp_subtype="Normal",
)
def dollar_per_mdollar():
    """
    Dollars per million dollar (1 M$ = 1e6 $).
    """
    return 1000000.0


@component.add(
    name="GDPpc initial year",
    units="$/person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_gdp": 1, "historic_population": 1, "dollar_per_mdollar": 1},
)
def gdppc_initial_year():
    return historic_gdp(1995) / historic_population(1995) * dollar_per_mdollar()


@component.add(
    name="GFCF not covered",
    units="Mdollars/year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "gross_fixed_capital_formation": 1, "real_gfcf": 1},
)
def gfcf_not_covered():
    """
    Gap between gross fixed capital formation required and real gross fixed capital formation (after energy-economy feedback)
    """
    return if_then_else(
        time() < 2009,
        lambda: xr.DataArray(0, {"sectors": _subscript_dict["sectors"]}, ["sectors"]),
        lambda: gross_fixed_capital_formation() - real_gfcf(),
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
    Value of gross fixed capital formation
    """
    return _integ_gross_fixed_capital_formation()


_integ_gross_fixed_capital_formation = Integ(
    lambda: variation_gfcf() - gfcf_not_covered(),
    lambda: initial_gfcf(),
    "_integ_gross_fixed_capital_formation",
)


@component.add(
    name="growth capital share",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"growth_labour_share": 1, "labour_share": 2},
)
def growth_capital_share():
    """
    Historic capital share variation (own calculations from WIOD-SEA).
    """
    return -growth_labour_share() * labour_share() / (1 - labour_share())


@component.add(
    name="growth labour share",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "labour_share_growth": 1,
        "labor_share_cte": 1,
        "historic_labour_share_variation": 1,
    },
)
def growth_labour_share():
    """
    Real variation rate of labour share depending on activation.
    """
    return if_then_else(
        time() > 2013,
        lambda: if_then_else(
            time() > 2050, lambda: 0, lambda: labour_share_growth() * labor_share_cte()
        ),
        lambda: historic_labour_share_variation(),
    )


@component.add(
    name="historic capital compensation",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_capital_compensation",
        "__lookup__": "_ext_lookup_historic_capital_compensation",
    },
)
def historic_capital_compensation(x, final_subs=None):
    """
    Historical capital compensation (14 sectors).
    """
    return _ext_lookup_historic_capital_compensation(x, final_subs)


_ext_lookup_historic_capital_compensation = ExtLookup(
    "../economy.xlsx",
    "World",
    "time_index2014",
    "historic_capital_compensation",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_lookup_historic_capital_compensation",
)


@component.add(
    name="historic change in inventories",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_change_in_inventories",
        "__lookup__": "_ext_lookup_historic_change_in_inventories",
    },
)
def historic_change_in_inventories(x, final_subs=None):
    """
    Historical capital compensation (14 sectors).
    """
    return _ext_lookup_historic_change_in_inventories(x, final_subs)


_ext_lookup_historic_change_in_inventories = ExtLookup(
    "../economy.xlsx",
    "World",
    "time_index2009",
    "historic_change_in_inventories",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_lookup_historic_change_in_inventories",
)


@component.add(
    name="historic demand",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 4,
        "historic_gfcf": 1,
        "historic_hd": 1,
        "historic_goverment_expenditures": 1,
        "historic_change_in_inventories": 1,
    },
)
def historic_demand():
    """
    Historic demand (35 WIOD sectors). US$1995.
    """
    return (
        historic_gfcf(time())
        + historic_hd(time())
        + historic_goverment_expenditures(time())
        + historic_change_in_inventories(time())
    )


@component.add(
    name="historic demand next year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 4,
        "historic_gfcf": 1,
        "historic_hd": 1,
        "historic_goverment_expenditures": 1,
        "historic_change_in_inventories": 1,
    },
)
def historic_demand_next_year():
    return (
        historic_gfcf(time() + 1)
        + historic_hd(time() + 1)
        + historic_goverment_expenditures(time() + 1)
        + historic_change_in_inventories(time() + 1)
    )


@component.add(
    name="historic GDP",
    units="Mdollars",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_gdp",
        "__lookup__": "_ext_lookup_historic_gdp",
    },
)
def historic_gdp(x, final_subs=None):
    """
    Historic GDP Million dollars. Data derived from A matrix. US$1995.
    """
    return _ext_lookup_historic_gdp(x, final_subs)


_ext_lookup_historic_gdp = ExtLookup(
    "../economy.xlsx",
    "World",
    "time_index2014",
    "historic_GDP",
    {},
    _root,
    {},
    "_ext_lookup_historic_gdp",
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
    Historic gross fixed capital formation (WIOD-14 sectors).
    """
    return _ext_lookup_historic_gfcf(x, final_subs)


_ext_lookup_historic_gfcf = ExtLookup(
    "../economy.xlsx",
    "World",
    "time_index2009",
    "historic_GFCF",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_lookup_historic_gfcf",
)


@component.add(
    name="historic goverment expenditures",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_goverment_expenditures",
        "__lookup__": "_ext_lookup_historic_goverment_expenditures",
    },
)
def historic_goverment_expenditures(x, final_subs=None):
    """
    Historical capital compensation (14 sectors).
    """
    return _ext_lookup_historic_goverment_expenditures(x, final_subs)


_ext_lookup_historic_goverment_expenditures = ExtLookup(
    "../economy.xlsx",
    "World",
    "time_index2009",
    "historic_goverment_expenditures",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_lookup_historic_goverment_expenditures",
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
    Historical final demand by households (WIOD-14 sectors).
    """
    return _ext_lookup_historic_hd(x, final_subs)


_ext_lookup_historic_hd = ExtLookup(
    "../economy.xlsx",
    "World",
    "time_index2009",
    "historic_HD",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_lookup_historic_hd",
)


@component.add(
    name="historic labour compensation",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_labour_compensation",
        "__lookup__": "_ext_lookup_historic_labour_compensation",
    },
)
def historic_labour_compensation(x, final_subs=None):
    """
    Historical labour compensation (14 sectors).
    """
    return _ext_lookup_historic_labour_compensation(x, final_subs)


_ext_lookup_historic_labour_compensation = ExtLookup(
    "../economy.xlsx",
    "World",
    "time_index2014",
    "historic_labour_compensation",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_lookup_historic_labour_compensation",
)


@component.add(
    name="historic labour share variation",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "labour_compensation_share_next_step": 1,
        "labour_compensation_share": 2,
    },
)
def historic_labour_share_variation():
    """
    Historic variation of labour share (own calculations from WIOD-SEA).
    """
    return (
        labour_compensation_share_next_step() - labour_compensation_share()
    ) / labour_compensation_share()


@component.add(
    name="historic variation demand",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_demand_next_year": 1, "historic_demand": 1},
)
def historic_variation_demand():
    """
    Historic variation of demand (35 WIOD sectors). US$1995
    """
    return historic_demand_next_year() - historic_demand()


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
    Finald demand by Households
    """
    return _integ_household_demand()


_integ_household_demand = Integ(
    lambda: variation_household_demand() - household_demand_not_covered(),
    lambda: initial_household_demand(),
    "_integ_household_demand",
)


@component.add(
    name="Household demand not covered",
    units="Mdollars/year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "household_demand": 1, "real_household_demand": 1},
)
def household_demand_not_covered():
    """
    Gap between households consumption required and households real consumption (after energy-economy feedback)
    """
    return if_then_else(
        time() < 2009,
        lambda: xr.DataArray(0, {"sectors": _subscript_dict["sectors"]}, ["sectors"]),
        lambda: household_demand() - real_household_demand(),
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
    Economic households demand (in millionUS$1995)
    """
    return sum(household_demand().rename({"sectors": "sectors!"}), dim=["sectors!"])


@component.add(
    name="initial CC total",
    units="Mdollars",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_cc_total():
    return 10573900.0


@component.add(
    name="initial demand",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_initial_demand": 1},
    other_deps={
        "_initial_initial_demand": {"initial": {"historic_demand": 1}, "step": {}}
    },
)
def initial_demand():
    return _initial_initial_demand()


_initial_initial_demand = Initial(lambda: historic_demand(), "_initial_initial_demand")


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
    Initial gross fixed capital formation
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
    name="Initial Labour share",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_labour_share():
    """
    Historic 2014 Labour share
    """
    return 0.5621


@component.add(
    name="initial LC total",
    units="Mdollars",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_lc_total():
    """
    Initial labour compensation
    """
    return 18584700.0


@component.add(
    name="input GDPpc annual growth",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_input_gdppc_annual_growth",
        "__data__": "_ext_data_input_gdppc_annual_growth",
        "time": 1,
    },
)
def input_gdppc_annual_growth():
    """
    Original values for annual growth of GDPpc from SSP2.
    """
    return _ext_data_input_gdppc_annual_growth(time())


_ext_data_input_gdppc_annual_growth = ExtData(
    "../economy.xlsx",
    "World",
    "time_index_projection",
    "input_GDPpc_annual_growth",
    None,
    {},
    _root,
    {},
    "_ext_data_input_gdppc_annual_growth",
)


@component.add(
    name='"Labor share cte?"', units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def labor_share_cte():
    """
    0: Labor share: cte 1: Labor share evolves following "P labor share"
    """
    return 1


@component.add(
    name="labour compensation share",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "historic_labour_compensation": 2,
        "historic_capital_compensation": 1,
    },
)
def labour_compensation_share():
    return sum(
        historic_labour_compensation(time()).rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    ) / sum(
        historic_labour_compensation(time()).rename({"sectors": "sectors!"})
        + historic_capital_compensation(time()).rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    )


@component.add(
    name="labour compensation share next step",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "historic_labour_compensation": 2,
        "historic_capital_compensation": 1,
    },
)
def labour_compensation_share_next_step():
    return sum(
        historic_labour_compensation(time() + 1).rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    ) / sum(
        historic_labour_compensation(time() + 1).rename({"sectors": "sectors!"})
        + historic_capital_compensation(time() + 1).rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    )


@component.add(
    name="labour share",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_labour_share": 1},
    other_deps={
        "_integ_labour_share": {"initial": {}, "step": {"variation_labour_share": 1}}
    },
)
def labour_share():
    return _integ_labour_share()


_integ_labour_share = Integ(
    lambda: variation_labour_share(), lambda: 0.6374, "_integ_labour_share"
)


@component.add(
    name="Labour share growth",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "p_labour_share_2050": 1,
        "initial_labour_share": 1,
        "year_initial_labour_share": 1,
        "year_final_labour_share": 1,
    },
)
def labour_share_growth():
    """
    Mean cummulative growth rate of labour share.
    """
    return (p_labour_share_2050() / initial_labour_share()) ** (
        1 / (year_final_labour_share() - year_initial_labour_share())
    ) - 1


@component.add(
    name="LC",
    units="Mdollars",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_lc": 1},
    other_deps={
        "_integ_lc": {
            "initial": {"initial_lc_total": 1},
            "step": {"variation_lc": 1, "lc_not_covered": 1},
        }
    },
)
def lc():
    """
    Labour compensation
    """
    return _integ_lc()


_integ_lc = Integ(
    lambda: variation_lc() - lc_not_covered(), lambda: initial_lc_total(), "_integ_lc"
)


@component.add(
    name="LC not covered",
    units="Mdollars/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demand_not_covered_total_fd": 1, "labour_share": 1},
)
def lc_not_covered():
    """
    Gap between labour compensation required andreal labour compensation (after energy-economy feedback)
    """
    return demand_not_covered_total_fd() * labour_share()


@component.add(
    name="P customized cte GDPpc variation",
    units="1/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_customized_cte_gdppc_variation"},
)
def p_customized_cte_gdppc_variation():
    """
    From customized year, set annual constant variation.
    """
    return _ext_constant_p_customized_cte_gdppc_variation()


_ext_constant_p_customized_cte_gdppc_variation = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "constant_GDP_variation",
    {},
    _root,
    {},
    "_ext_constant_p_customized_cte_gdppc_variation",
)


@component.add(
    name="P customized year GDPpc evolution",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_customized_year_gdppc_evolution"},
)
def p_customized_year_gdppc_evolution():
    """
    From customized year, set annual constant variation.
    """
    return _ext_constant_p_customized_year_gdppc_evolution()


_ext_constant_p_customized_year_gdppc_evolution = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "start_year_gdp_variation",
    {},
    _root,
    {},
    "_ext_constant_p_customized_year_gdppc_evolution",
)


@component.add(
    name="P labour share 2050",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_labour_share_2050"},
)
def p_labour_share_2050():
    """
    Labour share targetted by 2050.
    """
    return _ext_constant_p_labour_share_2050()


_ext_constant_p_labour_share_2050 = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "p_labor_share_2050",
    {},
    _root,
    {},
    "_ext_constant_p_labour_share_2050",
)


@component.add(
    name="P timeseries GDPpc growth rate",
    units="1/year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_p_timeseries_gdppc_growth_rate",
        "__data__": "_ext_data_p_timeseries_gdppc_growth_rate",
        "time": 1,
    },
)
def p_timeseries_gdppc_growth_rate():
    """
    Annual GDPpc growth from timeseries.
    """
    return _ext_data_p_timeseries_gdppc_growth_rate(time())


_ext_data_p_timeseries_gdppc_growth_rate = ExtData(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "years_gdp_growth",
    "gdp_growth_timeseries",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_p_timeseries_gdppc_growth_rate",
)


@component.add(
    name='"pct GFCF vs GFCF+HD"',
    units="Dmnl",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gross_fixed_capital_formation": 2, "household_demand": 1},
)
def pct_gfcf_vs_gfcfhd():
    """
    Share of Gross Fixed Capital Formation in final demand by households and enterprises.
    """
    return gross_fixed_capital_formation() / (
        gross_fixed_capital_formation() + household_demand()
    )


@component.add(
    name="Real GFCF",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_demand_by_sector": 1,
        "share_consum_goverment_and_inventories": 1,
        "pct_gfcf_vs_gfcfhd": 1,
    },
)
def real_gfcf():
    """
    Real Gross Fixed Capital Formation
    """
    return (
        real_demand_by_sector()
        * (1 - share_consum_goverment_and_inventories())
        * pct_gfcf_vs_gfcfhd()
    )


@component.add(
    name="Real Household demand",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_demand_by_sector": 1,
        "share_consum_goverment_and_inventories": 1,
        "pct_gfcf_vs_gfcfhd": 1,
    },
)
def real_household_demand():
    return (
        real_demand_by_sector()
        * (1 - share_consum_goverment_and_inventories())
        * (1 - pct_gfcf_vs_gfcfhd())
    )


@component.add(
    name="select GDPpc evolution input",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_select_gdppc_evolution_input"},
)
def select_gdppc_evolution_input():
    """
    0. SSP2 1. Timeseries 2. From customized year, set annual constant variation
    """
    return _ext_constant_select_gdppc_evolution_input()


_ext_constant_select_gdppc_evolution_input = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "gdp_evolution_input",
    {},
    _root,
    {},
    "_ext_constant_select_gdppc_evolution_input",
)


@component.add(
    name="share CC",
    units="Dmnl",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "historic_capital_compensation": 2},
)
def share_cc():
    """
    Sectoral share of capital compensation. (Capital compensation[i]/Total capital compensation)
    """
    return historic_capital_compensation(time()) / sum(
        historic_capital_compensation(time()).rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    )


@component.add(
    name="share CC next step",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "historic_capital_compensation": 2},
)
def share_cc_next_step():
    return historic_capital_compensation(time() + 1) / sum(
        historic_capital_compensation(time() + 1).rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    )


@component.add(
    name="share consum goverment and inventories",
    units="Dmnl",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "historic_goverment_expenditures": 1,
        "historic_change_in_inventories": 1,
        "historic_demand": 1,
    },
)
def share_consum_goverment_and_inventories():
    return (
        historic_goverment_expenditures(time()) + historic_change_in_inventories(time())
    ) / historic_demand()


@component.add(
    name="total demand",
    units="Tdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demand_by_sector_fd": 1},
)
def total_demand():
    """
    Total final demand
    """
    return (
        sum(demand_by_sector_fd().rename({"sectors": "sectors!"}), dim=["sectors!"])
        / 1000000.0
    )


@component.add(
    name="total demand adjusted",
    units="Tdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demand_by_sector_fd_adjusted": 1},
)
def total_demand_adjusted():
    """
    Total demand after adjustment of the demand function.
    """
    return (
        sum(
            demand_by_sector_fd_adjusted().rename({"sectors": "sectors!"}),
            dim=["sectors!"],
        )
        / 1000000.0
    )


@component.add(
    name="variation CC",
    units="Mdollars/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "capital_share": 1,
        "growth_capital_share": 2,
        "desired_annual_gdp_growth_rate": 2,
        "real_demand": 1,
    },
)
def variation_cc():
    """
    Variation of capital compensation
    """
    return (
        capital_share()
        * (
            desired_annual_gdp_growth_rate()
            + growth_capital_share()
            + desired_annual_gdp_growth_rate() * growth_capital_share()
        )
        * real_demand()
    )


@component.add(
    name="variation CC sectoral",
    units="Mdollars/year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "cc_total": 2,
        "variation_cc": 1,
        "share_cc_next_step": 1,
        "share_cc": 1,
    },
)
def variation_cc_sectoral():
    """
    Variation of capital compensation by industrial sectors
    """
    return (
        cc_total() + variation_cc()
    ) * share_cc_next_step() - cc_total() * share_cc()


@component.add(
    name="variation demand flow FD",
    units="Mdollars/year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "historic_variation_demand": 1,
        "share_consum_goverment_and_inventories": 1,
        "variation_household_demand": 1,
        "variation_gfcf": 1,
    },
)
def variation_demand_flow_fd():
    """
    variation of final demand by industrial sectors
    """
    return if_then_else(
        time() < 2009,
        lambda: historic_variation_demand(),
        lambda: (variation_gfcf() + variation_household_demand())
        / (1 - share_consum_goverment_and_inventories()),
    )


@component.add(
    name="variation GFCF",
    units="Mdollars/year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "variation_historic_gfcf": 1,
        "beta_1_gfcf": 2,
        "cc_sectoral": 2,
        "variation_cc_sectoral": 1,
        "beta_0_gfcf": 1,
    },
)
def variation_gfcf():
    """
    Variation of gross fixed capital formation by industrial sectors
    """
    return if_then_else(
        time() < 2009,
        lambda: variation_historic_gfcf(),
        lambda: np.exp(beta_0_gfcf())
        * (
            (cc_sectoral() + variation_cc_sectoral()) ** beta_1_gfcf()
            - cc_sectoral() ** beta_1_gfcf()
        ),
    )


@component.add(
    name="variation historic demand",
    units="Mdollars/year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "historic_hd": 2},
)
def variation_historic_demand():
    """
    Variation of final demand by households
    """
    return historic_hd(time() + 1) - historic_hd(time())


@component.add(
    name="variation historic GDPpc",
    units="$/(person*year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "historic_population": 2,
        "historic_gdp": 2,
        "dollar_per_mdollar": 1,
    },
)
def variation_historic_gdppc():
    """
    Variation of historic GDP per capita.
    """
    return if_then_else(
        time() < 2013,
        lambda: (
            historic_gdp(time() + 1) / historic_population(time() + 1)
            - historic_gdp(time()) / historic_population(time())
        )
        * dollar_per_mdollar(),
        lambda: 0,
    )


@component.add(
    name="variation historic GFCF",
    units="Mdollars/year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "historic_gfcf": 2},
)
def variation_historic_gfcf():
    """
    Historic variation of gross fixed capital formation (WIOD-35 sectors)
    """
    return historic_gfcf(time() + 1) - historic_gfcf(time())


@component.add(
    name="variation household demand",
    units="Mdollars/year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "variation_historic_demand": 1,
        "beta_0_hd": 1,
        "beta_1_hd": 2,
        "lc": 2,
        "variation_lc": 1,
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


@component.add(
    name="variation labour share",
    units="1/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"growth_labour_share": 1, "labour_share": 1},
)
def variation_labour_share():
    """
    Real variation of labor share.
    """
    return growth_labour_share() * labour_share()


@component.add(
    name="variation LC",
    units="Mdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_demand": 1,
        "labour_share": 1,
        "growth_labour_share": 2,
        "desired_annual_gdp_growth_rate": 2,
    },
)
def variation_lc():
    """
    Variation of labour compensation
    """
    return (
        real_demand()
        * labour_share()
        * (
            desired_annual_gdp_growth_rate()
            + growth_labour_share()
            + desired_annual_gdp_growth_rate() * growth_labour_share()
        )
    )


@component.add(
    name="Year Final Labour share", comp_type="Constant", comp_subtype="Normal"
)
def year_final_labour_share():
    """
    Year of final labour share by scenarios to use in the mean accumulative growth rate.
    """
    return 2050


@component.add(
    name="Year Initial Labour share", comp_type="Constant", comp_subtype="Normal"
)
def year_initial_labour_share():
    """
    Last year with historical data to use in the mean cummulative growth rate.
    """
    return 2014
