"""
Module economy.gdp_desired_labour_and_capital_share
Translated using PySD version 3.14.0
"""

@component.add(
    name="Annual GDPpc growth rate",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"p_timeseries_gdppc_growth_rate": 1},
)
def annual_gdppc_growth_rate():
    return p_timeseries_gdppc_growth_rate()


@component.add(
    name="capital share",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_capital_share": 1},
    other_deps={
        "_integ_capital_share": {
            "initial": {"historic_capital_share": 1},
            "step": {"variation_capital_share": 1},
        }
    },
)
def capital_share():
    """
    Ratio 'Capital compensation/GDP'
    """
    return _integ_capital_share()


_integ_capital_share = Integ(
    lambda: variation_capital_share(),
    lambda: historic_capital_share(),
    "_integ_capital_share",
)


@component.add(
    name="capital share growth",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "p_capital_share": 1,
        "initial_capital_share": 2,
        "year_initial_capital_share": 1,
        "time_step": 1,
        "year_final_capial_share": 1,
    },
)
def capital_share_growth():
    """
    Real variation rate of capital share depending on activation.
    """
    return (
        1 + (p_capital_share() - initial_capital_share()) / initial_capital_share()
    ) ** (time_step() / (year_final_capial_share() - year_initial_capital_share())) - 1


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
    Capital compensation ** Debugging. MAX(0, diff) function introduced to avoid negative values. Original: variation CC-CC total not covered
    """
    return _integ_cc_total()


_integ_cc_total = Integ(
    lambda: np.maximum(0, variation_cc() - cc_total_not_covered()),
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
    name="Desired annual GDP growth rate",
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
    name="Desired annual total demand growth rate",
    units="Dmnl/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_annual_gdp_growth_rate": 1},
)
def desired_annual_total_demand_growth_rate():
    """
    Real variation of Final Demand. Assumed to be equal according to sample data from WIOD.
    """
    return desired_annual_gdp_growth_rate()


@component.add(
    name="Desired annual total demand growth rate delayed 1 yr",
    units="Dmnl/year",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_desired_annual_total_demand_growth_rate_delayed_1_yr": 1},
    other_deps={
        "_delayfixed_desired_annual_total_demand_growth_rate_delayed_1_yr": {
            "initial": {},
            "step": {"desired_annual_total_demand_growth_rate": 1},
        }
    },
)
def desired_annual_total_demand_growth_rate_delayed_1_yr():
    """
    Lagged variation of final demand
    """
    return _delayfixed_desired_annual_total_demand_growth_rate_delayed_1_yr()


_delayfixed_desired_annual_total_demand_growth_rate_delayed_1_yr = DelayFixed(
    lambda: desired_annual_total_demand_growth_rate(),
    lambda: 1,
    lambda: 0,
    time_step,
    "_delayfixed_desired_annual_total_demand_growth_rate_delayed_1_yr",
)


@component.add(
    name="Desired GDP",
    units="T$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_gdppc": 1, "population": 1, "dollars_to_tdollars": 1},
)
def desired_gdp():
    """
    Desired GDP level for each scenario (user selection).
    """
    return desired_gdppc() * population() / dollars_to_tdollars()


@component.add(
    name="Desired GDP next year",
    units="T$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "historic_gdp_growth_rate": 1,
        "desired_gdp": 1,
        "dollars_to_tdollars": 1,
        "population": 1,
        "annual_gdppc_growth_rate": 1,
        "desired_gdppc": 1,
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
    units="$/(year*person)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "historic_gdppc": 1,
        "historic_gdppc_delayed": 1,
        "time_step": 2,
        "ts_growth_rate": 1,
        "desired_gdppc": 1,
    },
)
def desired_variation_gdppc():
    """
    Desired variation of GDP per capita.
    """
    return if_then_else(
        time() < 2015,
        lambda: (historic_gdppc() - historic_gdppc_delayed()) / time_step(),
        lambda: (desired_gdppc() * ts_growth_rate()) / time_step(),
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
    name="growth capital share",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "year_initial_capital_share": 1,
        "capital_share_growth": 1,
        "laborcapital_share_cte": 1,
        "year_final_capial_share": 1,
        "historic_capital_share_growth": 1,
    },
)
def growth_capital_share():
    return if_then_else(
        time() >= year_initial_capital_share(),
        lambda: if_then_else(
            time() > year_final_capial_share(),
            lambda: 0,
            lambda: capital_share_growth() * laborcapital_share_cte(),
        ),
        lambda: historic_capital_share_growth(),
    )


@component.add(
    name="growth labour share",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "year_initial_labour_share": 1,
        "laborcapital_share_cte": 1,
        "labour_share_growth": 1,
        "historic_labour_share_growth": 1,
    },
)
def growth_labour_share():
    """
    Real variation rate of labour share depending on activation.
    """
    return if_then_else(
        time() >= year_initial_labour_share(),
        lambda: if_then_else(
            time() > 2050,
            lambda: 0,
            lambda: labour_share_growth() * laborcapital_share_cte(),
        ),
        lambda: historic_labour_share_growth(),
    )


@component.add(
    name="historic capital compensation",
    units="Mdollars",
    subscripts=[np.str_("sectors")],
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
    "Europe",
    "time_index2009",
    "historic_capital_compensation",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_lookup_historic_capital_compensation",
)


@component.add(
    name="historic capital share",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "historic_capital_compensation": 1, "historic_gdp": 1},
)
def historic_capital_share():
    """
    Historical capital compensation share.
    """
    return sum(
        historic_capital_compensation(time()).rename({np.str_("sectors"): "sectors!"}),
        dim=["sectors!"],
    ) / historic_gdp(time())


@component.add(
    name="historic capital share growth",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_capital_share_next_step": 1, "historic_capital_share": 2},
)
def historic_capital_share_growth():
    """
    Historic variation of capital share.
    """
    return (
        historic_capital_share_next_step() - historic_capital_share()
    ) / historic_capital_share()


@component.add(
    name="historic capital share next step",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "time_step": 2,
        "historic_capital_compensation": 1,
        "historic_gdp": 1,
    },
)
def historic_capital_share_next_step():
    return sum(
        historic_capital_compensation(time() + time_step()).rename(
            {np.str_("sectors"): "sectors!"}
        ),
        dim=["sectors!"],
    ) / historic_gdp(time() + time_step())


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
    "Europe",
    "time_index2014",
    "historic_GDP",
    {},
    _root,
    {},
    "_ext_lookup_historic_gdp",
)


@component.add(
    name="Historic GDP growth rate",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 3, "historic_gdp": 3},
)
def historic_gdp_growth_rate():
    return (historic_gdp(time() + 1) - historic_gdp(time())) / historic_gdp(time())


@component.add(
    name="Historic GDPpc",
    units="$/person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "historic_gdp": 1, "historic_population": 1, "nvs_per_m": 1},
)
def historic_gdppc():
    return historic_gdp(time()) / historic_population(time()) * nvs_per_m()


@component.add(
    name="historic GDPpc delayed",
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
    name="historic labour compensation",
    units="Mdollars",
    subscripts=[np.str_("sectors")],
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
    "Europe",
    "time_index2014",
    "historic_labour_compensation",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {"sectors": _subscript_dict["sectors"]},
    "_ext_lookup_historic_labour_compensation",
)


@component.add(
    name="historic labour share",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "historic_labour_compensation": 1, "historic_gdp": 1},
)
def historic_labour_share():
    """
    Historical capital compensation share.
    """
    return sum(
        historic_labour_compensation(time()).rename({np.str_("sectors"): "sectors!"}),
        dim=["sectors!"],
    ) / historic_gdp(time())


@component.add(
    name="historic labour share growth",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_labour_share_next_step": 1, "historic_labour_share": 2},
)
def historic_labour_share_growth():
    """
    Historic variation of labour share.
    """
    return (
        historic_labour_share_next_step() - historic_labour_share()
    ) / historic_labour_share()


@component.add(
    name="historic labour share next step",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "time_step": 2,
        "historic_labour_compensation": 1,
        "historic_gdp": 1,
    },
)
def historic_labour_share_next_step():
    return sum(
        historic_labour_compensation(time() + time_step()).rename(
            {np.str_("sectors"): "sectors!"}
        ),
        dim=["sectors!"],
    ) / historic_gdp(time() + time_step())


@component.add(
    name="Initial capital share",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "year_initial_capital_share": 2,
        "historic_capital_compensation": 1,
        "historic_gdp": 1,
    },
)
def initial_capital_share():
    """
    Historic 2015 Labour share
    """
    return sum(
        historic_capital_compensation(year_initial_capital_share()).rename(
            {np.str_("sectors"): "sectors!"}
        ),
        dim=["sectors!"],
    ) / historic_gdp(year_initial_capital_share())


@component.add(
    name="initial CC total",
    units="Mdollars",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_cc_total():
    """
    Initial capital compensation
    """
    return 3594330.0


@component.add(
    name="Initial Labour share",
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
    Historic 2015 Labour share
    """
    return sum(
        historic_labour_compensation(year_initial_labour_share()).rename(
            {np.str_("sectors"): "sectors!"}
        ),
        dim=["sectors!"],
    ) / historic_gdp(year_initial_labour_share())


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
    return 4181720.0


@component.add(
    name='"Labor/Capital share cte?"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def laborcapital_share_cte():
    """
    0: Labor share: cte 1: Labor share evolves following "P labor share"
    """
    return 1


@component.add(
    name="labour share",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_labour_share": 1},
    other_deps={
        "_integ_labour_share": {
            "initial": {"historic_labour_share": 1},
            "step": {"variation_labour_share": 1},
        }
    },
)
def labour_share():
    """
    Ratio 'Labour compensation/GDP'
    """
    return _integ_labour_share()


_integ_labour_share = Integ(
    lambda: variation_labour_share(),
    lambda: historic_labour_share(),
    "_integ_labour_share",
)


@component.add(
    name="Labour share growth",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "p_labour_share": 1,
        "initial_labour_share": 2,
        "year_final_labour_share": 1,
        "year_initial_labour_share": 1,
        "time_step": 1,
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
    Labour compensation ** Debugging. MAX(0, diff) function introduced to avoid negative values. Original: variation LC-LC not covered
    """
    return _integ_lc()


_integ_lc = Integ(
    lambda: np.maximum(0, variation_lc() - lc_not_covered()),
    lambda: initial_lc_total(),
    "_integ_lc",
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
    Gap between labour compensation required and real labour compensation (after energy-economy feedback)
    """
    return demand_not_covered_total_fd() * labour_share()


@component.add(
    name='"$ per M$"', units="$/M$", comp_type="Constant", comp_subtype="Normal"
)
def nvs_per_m():
    return 1000000.0


@component.add(
    name="P capital share",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_capital_share"},
)
def p_capital_share():
    """
    Capital share targetted by 2050.
    """
    return _ext_constant_p_capital_share()


_ext_constant_p_capital_share = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "NZP",
    "p_capital_share",
    {},
    _root,
    {},
    "_ext_constant_p_capital_share",
)


@component.add(
    name="P labour share",
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
    "../../scenarios/scen_eu.xlsx",
    "NZP",
    "p_labour_share",
    {},
    _root,
    {},
    "_ext_constant_p_labour_share",
)


@component.add(
    name="P timeseries GDPpc growth rate",
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
    "../../scenarios/scen_eu.xlsx",
    "NZP",
    "year_gdp_timeseries",
    "p_timeseries_gdp_growth",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_p_timeseries_gdppc_growth_rate",
)


@component.add(
    name="TS growth rate",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"annual_gdppc_growth_rate": 1, "nvs_1_year": 1, "time_step": 1},
)
def ts_growth_rate():
    return (1 + annual_gdppc_growth_rate()) ** (time_step() / nvs_1_year()) - 1


@component.add(
    name="variation capital share",
    units="1/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"capital_share": 1, "growth_capital_share": 1, "time_step": 1},
)
def variation_capital_share():
    """
    Real variation of capital share.
    """
    return capital_share() * growth_capital_share() / time_step()


@component.add(
    name="variation CC",
    units="Mdollars/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "capital_share": 1,
        "growth_capital_share": 2,
        "desired_annual_total_demand_growth_rate": 2,
        "nvs_1_year": 1,
        "gdp_eu": 1,
        "m_to_t": 1,
    },
)
def variation_cc():
    """
    Variation of capital compensation
    """
    return (
        capital_share()
        * (
            desired_annual_total_demand_growth_rate()
            + growth_capital_share() / nvs_1_year()
            + desired_annual_total_demand_growth_rate() * growth_capital_share()
        )
        * gdp_eu()
        / m_to_t()
    )


@component.add(
    name="variation historic GDPpc",
    units="$/(person*year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "historic_population": 2,
        "historic_gdp": 2,
        "time_step": 3,
        "dollar_per_mdollar": 1,
    },
)
def variation_historic_gdppc():
    """
    Variation of historic GDPpc.
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
    name="variation labour share",
    units="1/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"growth_labour_share": 1, "labour_share": 1, "time_step": 1},
)
def variation_labour_share():
    """
    Real variation of labour share.
    """
    return growth_labour_share() * labour_share() / time_step()


@component.add(
    name="variation LC",
    units="Mdollars/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gdp_eu": 1,
        "labour_share": 1,
        "growth_labour_share": 2,
        "desired_annual_total_demand_growth_rate": 2,
        "nvs_1_year": 1,
        "m_to_t": 1,
    },
)
def variation_lc():
    """
    Variation of labour compensation
    """
    return (
        gdp_eu()
        * labour_share()
        * (
            desired_annual_total_demand_growth_rate()
            + growth_labour_share() / nvs_1_year()
            + desired_annual_total_demand_growth_rate() * growth_labour_share()
        )
        / m_to_t()
    )


@component.add(
    name="Year final capial share",
    units="year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def year_final_capial_share():
    """
    Year of final capital share by scenarios to use in the mean accumulative growth rate.
    """
    return 2050


@component.add(
    name="Year Final Labour share",
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
    name="Year initial capital share",
    units="year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def year_initial_capital_share():
    """
    Last year with historical data to use in the mean cummulative growth rate.
    """
    return 2015


@component.add(
    name="Year Initial Labour share",
    units="year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def year_initial_labour_share():
    """
    Last year with historical data to use in the mean cummulative growth rate.
    """
    return 2015
