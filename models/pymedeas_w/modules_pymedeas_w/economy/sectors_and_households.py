"""
Module economy.sectors_and_households
Translated using PySD version 3.14.2
"""

@component.add(
    name="Annual_GDPpc_growth_rate",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"p_timeseries_gdppc_growth_rate": 1},
)
def annual_gdppc_growth_rate():
    return p_timeseries_gdppc_growth_rate()


@component.add(
    name="beta_0_GFCF",
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
    r"../economy.xlsx",
    "World",
    "beta_0_GFCF*",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_constant_beta_0_gfcf",
)


@component.add(
    name="beta_0_HD",
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
    r"../economy.xlsx",
    "World",
    "beta_0_HD*",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_constant_beta_0_hd",
)


@component.add(
    name="beta_1_GFCF",
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
    r"../economy.xlsx",
    "World",
    "beta_1_GFCF",
    {},
    _root,
    {},
    "_ext_constant_beta_1_gfcf",
)


@component.add(
    name="beta_1_HD",
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
    r"../economy.xlsx", "World", "beta_1_HD", {}, _root, {}, "_ext_constant_beta_1_hd"
)


@component.add(
    name="capital_share",
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
    name="CC_sectoral",
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
    name="CC_total",
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
    name="CC_total_not_covered",
    units="Mdollars/(year)",
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
    name="Demand_by_sector_FD",
    units="M$",
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
    name="demand_by_sector_FD_adjusted",
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
    name="demand_not_covered_by_sector_FD",
    units="Mdollars/(year)",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "end_historical_year": 1,
        "demand_by_sector_fd": 1,
        "nvs_1_year": 1,
        "real_demand_by_sector": 1,
    },
)
def demand_not_covered_by_sector_fd():
    return if_then_else(
        time() > end_historical_year(),
        lambda: (demand_by_sector_fd() - real_demand_by_sector()) / nvs_1_year(),
        lambda: xr.DataArray(0, {"sectors": _subscript_dict["sectors"]}, ["sectors"]),
    )


@component.add(
    name="demand_not_covered_total_FD",
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
    name="Desired_annual_GDP_growth_rate",
    units="Dmnl/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_gdp_next_year": 1, "desired_gdp": 1, "nvs_1_year": 1},
)
def desired_annual_gdp_growth_rate():
    """
    Desired annual GDP growth rate.
    """
    return (-1 + desired_gdp_next_year() / desired_gdp()) / nvs_1_year()


@component.add(
    name="Desired_GDP",
    units="T$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "total_demand": 1,
        "desired_gdppc": 1,
        "dollars_to_tdollars": 1,
        "population": 1,
    },
)
def desired_gdp():
    """
    Desired GDP level for each scenario (user selection). The factor "0.56" corrects for a discrepancy when the TIME STEP < frequency of historical data.
    """
    return if_then_else(
        time() < 2019,
        lambda: total_demand(),
        lambda: desired_gdppc() * population() / dollars_to_tdollars() - 0.56,
    )


@component.add(
    name="Desired_GDP_next_year",
    units="T$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "desired_gdp": 1,
        "historic_gdp_growth_rate": 1,
        "desired_gdppc": 1,
        "dollars_to_tdollars": 1,
        "annual_gdppc_growth_rate": 1,
        "population": 1,
    },
)
def desired_gdp_next_year():
    return if_then_else(
        time() < 2015,
        lambda: desired_gdp() * (1 + historic_gdp_growth_rate()),
        lambda: desired_gdppc()
        * population()
        / dollars_to_tdollars()
        * (1 + annual_gdppc_growth_rate()),
    )


@component.add(
    name="Desired_GDPpc",
    units="$/(person)",
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
    name="Desired_variation_GDPpc",
    units="$/(year*person)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "time_step": 2,
        "historic_gdppc": 1,
        "historic_gdppc_delayed": 1,
        "desired_gdppc": 1,
        "ts_growth_rate": 1,
    },
)
def desired_variation_gdppc():
    return if_then_else(
        time() < 2015,
        lambda: (historic_gdppc() - historic_gdppc_delayed()) / time_step(),
        lambda: (desired_gdppc() * ts_growth_rate()) / time_step(),
    )


@component.add(
    name="diff_demand",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "gdp_delayed_1yr": 1,
        "desired_annual_gdp_growth_rate": 1,
        "nvs_1_year": 1,
        "total_demand": 1,
    },
)
def diff_demand():
    """
    Ratio between the desired GDP and the real GDP level after applying the demand function.
    """
    return if_then_else(
        time() < 2019,
        lambda: 1,
        lambda: (
            gdp_delayed_1yr() * (1 + desired_annual_gdp_growth_rate()) * nvs_1_year()
        )
        / total_demand(),
    )


@component.add(
    name="dollar_per_Mdollar",
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
    name="end_historical_year",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_end_historical_year"},
)
def end_historical_year():
    return _ext_constant_end_historical_year()


_ext_constant_end_historical_year = ExtConstant(
    r"../parameters.xlsx",
    "Global",
    "end_historical_year",
    {},
    _root,
    {},
    "_ext_constant_end_historical_year",
)


@component.add(
    name="GDPpc_initial_year",
    units="$/person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_gdp": 1, "historic_population": 1, "dollar_per_mdollar": 1},
)
def gdppc_initial_year():
    return historic_gdp(1995) / historic_population(1995) * dollar_per_mdollar()


@component.add(
    name="GFCF_not_covered",
    units="Mdollars/(year)",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "end_historical_year": 1,
        "gross_fixed_capital_formation": 1,
        "real_gfcf": 1,
        "nvs_1_year": 1,
    },
)
def gfcf_not_covered():
    """
    Gap between gross fixed capital formation required and real gross fixed capital formation (after energy-economy feedback)
    """
    return (
        if_then_else(
            time() < end_historical_year(),
            lambda: xr.DataArray(
                0, {"sectors": _subscript_dict["sectors"]}, ["sectors"]
            ),
            lambda: gross_fixed_capital_formation() - real_gfcf(),
        )
        / nvs_1_year()
    )


@component.add(
    name="Gross_fixed_capital_formation",
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
    name="growth_capital_share",
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
    name="growth_labour_share",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "year_initial_labour_share": 1,
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
        time() >= year_initial_labour_share(),
        lambda: if_then_else(
            time() > 2050, lambda: 0, lambda: labour_share_growth() * labor_share_cte()
        ),
        lambda: historic_labour_share_variation(),
    )


@component.add(
    name="historic_capital_compensation",
    units="Mdollars/year",
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
    r"../economy.xlsx",
    "World",
    "time_index2019",
    "historic_capital_compensation",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_lookup_historic_capital_compensation",
)


@component.add(
    name="historic_change_in_inventories",
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
    r"../economy.xlsx",
    "World",
    "time_index2019",
    "historic_change_in_inventories",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_lookup_historic_change_in_inventories",
)


@component.add(
    name="historic_demand",
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
    name="historic_demand_next_TS",
    units="M$",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 4,
        "time_step": 4,
        "historic_gfcf": 1,
        "historic_hd": 1,
        "historic_goverment_expenditures": 1,
        "historic_change_in_inventories": 1,
    },
)
def historic_demand_next_ts():
    return (
        historic_gfcf(time() + time_step())
        + historic_hd(time() + time_step())
        + historic_goverment_expenditures(time() + time_step())
        + historic_change_in_inventories(time() + time_step())
    )


@component.add(
    name="historic_GDP",
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
    r"../economy.xlsx",
    "World",
    "time_index2019",
    "historic_GDP",
    {},
    _root,
    {},
    "_ext_lookup_historic_gdp",
)


@component.add(
    name="Historic_GDP_growth_rate",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 3, "historic_gdp": 3},
)
def historic_gdp_growth_rate():
    return (historic_gdp(time()) - historic_gdp(time() - 1)) / historic_gdp(time() - 1)


@component.add(
    name="Historic_GDPpc",
    units="$/person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "historic_gdp": 1, "historic_population": 1, "nvs_per_m": 1},
)
def historic_gdppc():
    return historic_gdp(time()) / historic_population(time()) * nvs_per_m()


@component.add(
    name="historic_GDPpc_delayed",
    units="$/person",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_historic_gdppc_delayed": 1},
    other_deps={
        "_delayfixed_historic_gdppc_delayed": {
            "initial": {"historic_gdppc": 1, "time_step": 1},
            "step": {"historic_gdppc": 1},
        }
    },
)
def historic_gdppc_delayed():
    return _delayfixed_historic_gdppc_delayed()


_delayfixed_historic_gdppc_delayed = DelayFixed(
    lambda: historic_gdppc(),
    lambda: time_step(),
    lambda: historic_gdppc(),
    time_step,
    "_delayfixed_historic_gdppc_delayed",
)


@component.add(
    name="historic_GFCF",
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
    r"../economy.xlsx",
    "World",
    "time_index2019",
    "historic_GFCF",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_lookup_historic_gfcf",
)


@component.add(
    name="historic_goverment_expenditures",
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
    r"../economy.xlsx",
    "World",
    "time_index2019",
    "historic_goverment_expenditures",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_lookup_historic_goverment_expenditures",
)


@component.add(
    name="historic_HD",
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
    r"../economy.xlsx",
    "World",
    "time_index2019",
    "historic_HD",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_lookup_historic_hd",
)


@component.add(
    name="historic_labour_compensation",
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
    r"../economy.xlsx",
    "World",
    "time_index2019",
    "historic_labour_compensation",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_lookup_historic_labour_compensation",
)


@component.add(
    name="historic_labour_compensation_share",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "historic_labour_compensation": 1, "historic_gdp": 1},
)
def historic_labour_compensation_share():
    return sum(
        historic_labour_compensation(time()).rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    ) / historic_gdp(time())


@component.add(
    name="historic_labour_share_variation",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "labour_compensation_share_next_step": 1,
        "historic_labour_compensation_share": 2,
    },
)
def historic_labour_share_variation():
    """
    Historic variation of labour share (own calculations from WIOD-SEA).
    """
    return (
        labour_compensation_share_next_step() - historic_labour_compensation_share()
    ) / historic_labour_compensation_share()


@component.add(
    name="historic_variation_demand",
    units="Mdollars/(year)",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_demand_next_ts": 1, "historic_demand": 1, "time_step": 1},
)
def historic_variation_demand():
    """
    Historic variation of demand (35 WIOD sectors). US$1995
    """
    return (historic_demand_next_ts() - historic_demand()) / time_step()


@component.add(
    name="Household_demand",
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
    name="Household_demand_not_covered",
    units="Mdollars/year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "end_historical_year": 1,
        "real_household_demand": 1,
        "household_demand": 1,
        "nvs_1_year": 1,
    },
)
def household_demand_not_covered():
    """
    Gap between households consumption required and households real consumption (after energy-economy feedback)
    """
    return (
        if_then_else(
            time() < end_historical_year(),
            lambda: xr.DataArray(
                0, {"sectors": _subscript_dict["sectors"]}, ["sectors"]
            ),
            lambda: household_demand() - real_household_demand(),
        )
        / nvs_1_year()
    )


@component.add(
    name="Household_demand_total",
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
    name="initial_CC_total",
    units="Mdollars",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_cc_total():
    return 10573900.0


@component.add(
    name="initial_demand",
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
    name="initial_GFCF",
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
    name="initial_household_demand",
    units="M$",
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
    name="Initial_Labour_share",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "year_initial_labour_share": 2,
        "historic_labour_compensation": 1,
        "historic_gdp": 1,
    },
)
def initial_labour_share():
    """
    Historic 2014 Labour share
    """
    return sum(
        historic_labour_compensation(year_initial_labour_share()).rename(
            {"sectors": "sectors!"}
        ),
        dim=["sectors!"],
    ) / historic_gdp(year_initial_labour_share())


@component.add(
    name="initial_LC_total",
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
    name='"Labor_share_cte?"', units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def labor_share_cte():
    """
    0: Labor share: cte 1: Labor share evolves following "P labor share"
    """
    return 1


@component.add(
    name="labour_compensation_share_next_step",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "time_step": 2,
        "historic_labour_compensation": 1,
        "historic_gdp": 1,
    },
)
def labour_compensation_share_next_step():
    return sum(
        historic_labour_compensation(time() + time_step()).rename(
            {"sectors": "sectors!"}
        ),
        dim=["sectors!"],
    ) / historic_gdp(time() + time_step())


@component.add(
    name="labour_share",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_labour_share": 1},
    other_deps={
        "_integ_labour_share": {
            "initial": {"historic_labour_compensation_share": 1},
            "step": {"variation_labour_share": 1},
        }
    },
)
def labour_share():
    return _integ_labour_share()


_integ_labour_share = Integ(
    lambda: variation_labour_share(),
    lambda: historic_labour_compensation_share(),
    "_integ_labour_share",
)


@component.add(
    name="Labour_share_growth",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "p_labour_share": 1,
        "initial_labour_share": 2,
        "time_step": 1,
        "year_initial_labour_share": 1,
        "year_final_labour_share": 1,
    },
)
def labour_share_growth():
    """
    Mean cummulative growth rate of labour share.
    """
    return (
        1 + (p_labour_share() - initial_labour_share()) / initial_labour_share()
    ) ** (time_step() / (year_final_labour_share() - year_initial_labour_share())) - 1


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
    name="LC_not_covered",
    units="Mdollars/(year)",
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
    name='"$_per_M$"', units="$/M$", comp_type="Constant", comp_subtype="Normal"
)
def nvs_per_m():
    return 1000000.0


@component.add(
    name="P_labour_share",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_labour_share"},
)
def p_labour_share():
    """
    Labour share targetted by 2050.
    """
    return _ext_constant_p_labour_share()


_ext_constant_p_labour_share = ExtConstant(
    r"../../scenarios/scen_w.xlsx",
    "NZP",
    "p_labor_share_2050",
    {},
    _root,
    {},
    "_ext_constant_p_labour_share",
)


@component.add(
    name="P_timeseries_GDPpc_growth_rate",
    units="Dmnl",
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
    r"../../scenarios/scen_w.xlsx",
    "NZP",
    "years_gdp_growth",
    "gdp_growth_timeseries",
    None,
    {},
    _root,
    {},
    "_ext_data_p_timeseries_gdppc_growth_rate",
)


@component.add(
    name='"pct_GFCF_vs_GFCF+HD"',
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
    name="Real_GFCF",
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
    name="Real_Household_demand",
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
    name="share_CC",
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
    name="share_CC_next_step",
    units="Dmnl",
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
    name="share_consum_goverment_and_inventories",
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
    name="total_demand",
    units="Tdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demand_by_sector_fd": 1, "m_to_t": 1},
)
def total_demand():
    """
    Total final demand
    """
    return (
        sum(demand_by_sector_fd().rename({"sectors": "sectors!"}), dim=["sectors!"])
        * m_to_t()
    )


@component.add(
    name="total_demand_adjusted",
    units="Tdollars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demand_by_sector_fd_adjusted": 1, "m_to_t": 1},
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
        * m_to_t()
    )


@component.add(
    name="TS_growth_rate",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"annual_gdppc_growth_rate": 1, "time_step": 1, "nvs_1_year": 1},
)
def ts_growth_rate():
    return (1 + annual_gdppc_growth_rate()) ** (time_step() / nvs_1_year()) - 1


@component.add(
    name="unit_correction_economic",
    units="1/Mdollars",
    comp_type="Constant",
    comp_subtype="Normal",
)
def unit_correction_economic():
    return 1


@component.add(
    name="variation_CC",
    units="Mdollars/(year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "capital_share": 1,
        "desired_annual_gdp_growth_rate": 2,
        "nvs_1_year": 1,
        "growth_capital_share": 2,
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
            + growth_capital_share() / nvs_1_year()
            + desired_annual_gdp_growth_rate() * growth_capital_share()
        )
        * real_demand()
    )


@component.add(
    name="variation_CC_sectoral",
    units="Mdollars/year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "cc_total": 2,
        "nvs_1_year": 2,
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
        cc_total() / nvs_1_year() + variation_cc()
    ) * share_cc_next_step() - cc_total() * share_cc() / nvs_1_year()


@component.add(
    name="variation_demand_flow_FD",
    units="Mdollars/(year)",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "end_historical_year": 1,
        "historic_variation_demand": 1,
        "share_consum_goverment_and_inventories": 1,
        "variation_gfcf": 1,
        "variation_household_demand": 1,
    },
)
def variation_demand_flow_fd():
    """
    variation of final demand by industrial sectors
    """
    return if_then_else(
        time() < end_historical_year(),
        lambda: historic_variation_demand(),
        lambda: (variation_gfcf() + variation_household_demand())
        / (1 - share_consum_goverment_and_inventories()),
    )


@component.add(
    name="variation_GFCF",
    units="Mdollars/(year)",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "end_historical_year": 1,
        "variation_historic_gfcf": 1,
        "nvs_1_year": 1,
        "cc_sectoral": 2,
        "beta_1_gfcf": 2,
        "beta_0_gfcf": 1,
        "unit_correction_economic": 2,
        "variation_cc_sectoral": 1,
    },
)
def variation_gfcf():
    """
    Variation of gross fixed capital formation by industrial sectors
    """
    return if_then_else(
        time() < end_historical_year(),
        lambda: variation_historic_gfcf(),
        lambda: np.exp(beta_0_gfcf())
        * (
            (
                (cc_sectoral() + variation_cc_sectoral() * nvs_1_year())
                * unit_correction_economic()
            )
            ** beta_1_gfcf()
            - (cc_sectoral() * unit_correction_economic()) ** beta_1_gfcf()
        ),
    )


@component.add(
    name="variation_historic_demand",
    units="Mdollars/year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "time_step": 2, "historic_hd": 2},
)
def variation_historic_demand():
    """
    Variation of final demand by households
    """
    return (historic_hd(time() + time_step()) - historic_hd(time())) / time_step()


@component.add(
    name="variation_historic_GDPpc",
    units="$/(person*year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "time_step": 3,
        "historic_population": 2,
        "dollar_per_mdollar": 1,
        "historic_gdp": 2,
    },
)
def variation_historic_gdppc():
    """
    Variation of historic GDP per capita.
    """
    return if_then_else(
        time() < 2013,
        lambda: (
            historic_gdp(time() + time_step())
            / historic_population(time() + time_step())
            - historic_gdp(time()) / historic_population(time())
        )
        * dollar_per_mdollar()
        / time_step(),
        lambda: 0,
    )


@component.add(
    name="variation_historic_GFCF",
    units="Mdollars/year",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "time_step": 2, "historic_gfcf": 2},
)
def variation_historic_gfcf():
    """
    Historic variation of gross fixed capital formation (WIOD-35 sectors)
    """
    return (historic_gfcf(time() + time_step()) - historic_gfcf(time())) / time_step()


@component.add(
    name="variation_household_demand",
    units="Mdollars/(year)",
    subscripts=["sectors"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "end_historical_year": 1,
        "variation_historic_demand": 1,
        "lc": 2,
        "nvs_1_year": 1,
        "beta_0_hd": 1,
        "beta_1_hd": 2,
        "variation_lc": 1,
        "unit_correction_economic": 2,
    },
)
def variation_household_demand():
    """
    Variation of final demand by households by industrial sectors
    """
    return if_then_else(
        time() < end_historical_year(),
        lambda: variation_historic_demand(),
        lambda: np.exp(beta_0_hd())
        * (
            ((lc() + variation_lc() * nvs_1_year()) * unit_correction_economic())
            ** beta_1_hd()
            - (lc() * unit_correction_economic()) ** beta_1_hd()
        ),
    )


@component.add(
    name="variation_labour_share",
    units="1/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"growth_labour_share": 1, "labour_share": 1, "time_step": 1},
)
def variation_labour_share():
    """
    Real variation of labor share.
    """
    return growth_labour_share() * labour_share() / time_step()


@component.add(
    name="variation_LC",
    units="Mdollars/(year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_demand": 1,
        "labour_share": 1,
        "desired_annual_gdp_growth_rate": 2,
        "nvs_1_year": 1,
        "growth_labour_share": 2,
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
            + growth_labour_share() / nvs_1_year()
            + desired_annual_gdp_growth_rate() * growth_labour_share()
        )
    )


@component.add(
    name="Year_Final_Labour_share",
    units="year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def year_final_labour_share():
    """
    Year of final labour share by scenarios to use in the mean accumulative growth rate.
    """
    return 2050


@component.add(
    name="Year_Initial_Labour_share",
    units="year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def year_initial_labour_share():
    """
    Last year with historical data to use in the mean cummulative growth rate.
    """
    return 2014
