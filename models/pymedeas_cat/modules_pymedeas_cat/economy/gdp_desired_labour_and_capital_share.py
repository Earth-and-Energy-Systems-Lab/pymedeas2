"""
Module gdp_desired_labour_and_capital_share
Translated using PySD version 3.0.0
"""


@component.add(
    name="Annual GDPpc growth rate",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
    name="capital share", units="Dmnl", comp_type="Stateful", comp_subtype="Integ"
)
def capital_share():
    """
    Ratio 'Capital compensation/GDP'
    """
    return _integ_capital_share()


_integ_capital_share = Integ(
    lambda: variation_capital_share(), lambda: 0.373314, "_integ_capital_share"
)


@component.add(
    name="capital share growth",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def capital_share_growth():
    """
    Real variation rate of capital share depending on activation.
    """
    return (p_capital_share() / initial_capital_share()) ** (
        1 / (year_final_capial_share() - year_initial_capital_share())
    ) - 1


@component.add(
    name="CC total", units="Mdollars", comp_type="Auxiliary", comp_subtype="Normal"
)
def cc_total():
    return gdp_aut() * capital_share() * 1000000.0


@component.add(
    name="Desire GDP next step", comp_type="Auxiliary", comp_subtype="Normal"
)
def desire_gdp_next_step():
    return desired_gdp() + desired_variation_gdp()


@component.add(
    name="Desired annual GDP growth rate",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def desired_annual_gdp_growth_rate():
    """
    Desired annual GDP growth rate.
    """
    return -1 + desire_gdp_next_step() / desired_gdp()


@component.add(
    name="Desired annual total demand growth rate",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def desired_annual_total_demand_growth_rate():
    """
    Real variation of Final Demand. Assumed to be equal according to sample data from WIOD.
    """
    return desired_annual_gdp_growth_rate()


@component.add(
    name="Desired annual total demand growth rate delayed 1 yr",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
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
    name="Desired GDP", units="T$", comp_type="Auxiliary", comp_subtype="Normal"
)
def desired_gdp():
    """
    Desired GDP level for each scenario (user selection).
    """
    return desired_gdppc() * population() / dollars_to_tdollars()


@component.add(
    name="Desired GDPpc", units="$/person", comp_type="Stateful", comp_subtype="Integ"
)
def desired_gdppc():
    return _integ_desired_gdppc()


_integ_desired_gdppc = Integ(
    lambda: desired_variation_gdppc(),
    lambda: gdppc_initial_year(),
    "_integ_desired_gdppc",
)


@component.add(
    name="Desired variation GDP", comp_type="Auxiliary", comp_subtype="Normal"
)
def desired_variation_gdp():
    return if_then_else(
        time() < 2015,
        lambda: desired_gdppc() * variation_historic_pop() / dollars_to_tdollars()
        + variation_historic_gdppc() * population() / dollars_to_tdollars()
        + variation_historic_gdppc() * variation_historic_pop() / dollars_to_tdollars(),
        lambda: desired_gdppc() * pop_variation() / dollars_to_tdollars()
        + desired_variation_gdppc() * population() / dollars_to_tdollars()
        + desired_variation_gdppc() * pop_variation() / dollars_to_tdollars(),
    )


@component.add(
    name="Desired variation GDPpc",
    units="$/person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def desired_variation_gdppc():
    """
    Desired variation of GDP per capita.
    """
    return if_then_else(
        time() < 2015,
        lambda: desired_variation_gdppc_per_scen(),
        lambda: smooth_desired_variation_gdppc(),
    )


@component.add(
    name="desired variation GDPpc per scen",
    units="$/person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def desired_variation_gdppc_per_scen():
    """
    Desired GDPpc variation depending on the policy target selected by the user.
    """
    return if_then_else(
        time() < 2015,
        lambda: variation_historic_gdppc(),
        lambda: if_then_else(
            np.logical_and(
                select_gdppc_evolution_input() == 3,
                time() < p_customized_year_gdppc_evolution(),
            ),
            lambda: desired_gdppc() * annual_gdppc_growth_rate(),
            lambda: if_then_else(
                select_gdppc_evolution_input() == 0,
                lambda: desired_gdppc() * annual_gdppc_growth_rate(),
                lambda: if_then_else(
                    select_gdppc_evolution_input() == 1,
                    lambda: desired_gdppc() * annual_gdppc_growth_rate(),
                    lambda: if_then_else(
                        select_gdppc_evolution_input() == 2,
                        lambda: desired_gdppc() * annual_gdppc_growth_rate(),
                        lambda: gdppc_variation_asymptote_scen(),
                    ),
                ),
            ),
        ),
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
)
def gdppc_initial_year():
    return historic_gdp(1995) / historic_population(1995) * dollar_per_mdollar()


@component.add(
    name="GDPpc until P customized year GDPpc evolution",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
)
def gdppc_until_p_customized_year_gdppc_evolution():
    """
    GDPpc until starting customized year of the policy target.
    """
    return _sampleiftrue_gdppc_until_p_customized_year_gdppc_evolution()


_sampleiftrue_gdppc_until_p_customized_year_gdppc_evolution = SampleIfTrue(
    lambda: time() < p_customized_year_gdppc_evolution(),
    lambda: desired_gdppc(),
    lambda: desired_gdppc(),
    "_sampleiftrue_gdppc_until_p_customized_year_gdppc_evolution",
)


@component.add(
    name="GDPpc variation asymptote scen",
    units="$/(Year*person)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def gdppc_variation_asymptote_scen():
    """
    Desired GDPpc variation to reach asymptote target.
    """
    return (
        (gdppc_until_p_customized_year_gdppc_evolution() - (p_gdppc_asymptote() - 1600))
        * (-1 / t_asymptote_gdppc())
        * np.exp(-(time() - p_customized_year_gdppc_evolution()) / t_asymptote_gdppc())
    )


@component.add(
    name="growth capital share", comp_type="Auxiliary", comp_subtype="Normal"
)
def growth_capital_share():
    return if_then_else(
        time() >= 2017,
        lambda: if_then_else(
            time() > 2050,
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
)
def growth_labour_share():
    """
    Real variation rate of labour share depending on activation.
    """
    return if_then_else(
        time() >= 2017,
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
    subscripts=["sectors"],
    comp_type="Lookup",
    comp_subtype="External",
)
def historic_capital_compensation(x, final_subs=None):
    """
    Historical capital compensation (14 sectors).
    """
    return _ext_lookup_historic_capital_compensation(x, final_subs)


_ext_lookup_historic_capital_compensation = ExtLookup(
    "../economy.xlsx",
    "Catalonia",
    "time_index2009",
    "historic_capital_compensation",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {
        "sectors": [
            "Agriculture",
            "Mining quarrying and energy supply",
            "Food Beverages and Tobacco",
            "Textiles and leather etc",
            "Coke refined petroleum nuclear fuel and chemicals etc",
            "Electrical and optical equipment and Transport equipment",
            "Other manufacturing",
            "Construction",
            "Distribution",
            "Hotels and restaurant",
            "Transport storage and communication",
            "Financial Intermediation",
            "Real estate renting and busine activitie",
            "Non Market Service",
        ]
    },
    "_ext_lookup_historic_capital_compensation",
)


@component.add(
    name="historic capital share",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def historic_capital_share():
    """
    Historic variation of capital share.
    """
    return sum(
        historic_capital_compensation(time()).rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    ) / historic_gdp(time())


@component.add(
    name="historic capital share growth",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def historic_capital_share_next_step():
    """
    Historical capital compensation share.SUM(historic capital compensation[sectors!](Time))/historic GDP(Time)
    """
    return sum(
        historic_capital_compensation(time() + 1).rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    ) / historic_gdp(time() + 1)


@component.add(
    name="historic GDP", units="Mdollars", comp_type="Lookup", comp_subtype="External"
)
def historic_gdp(x, final_subs=None):
    """
    Historic GDP Million dollars. Data derived from A matrix. US$1995.
    """
    return _ext_lookup_historic_gdp(x, final_subs)


_ext_lookup_historic_gdp = ExtLookup(
    "../economy.xlsx",
    "Catalonia",
    "time_index2014",
    "historic_GDP",
    {},
    _root,
    {},
    "_ext_lookup_historic_gdp",
)


@component.add(
    name="historic labour compensation",
    units="Mdollars",
    subscripts=["sectors"],
    comp_type="Lookup",
    comp_subtype="External",
)
def historic_labour_compensation(x, final_subs=None):
    """
    Historical labour compensation (14 sectors).
    """
    return _ext_lookup_historic_labour_compensation(x, final_subs)


_ext_lookup_historic_labour_compensation = ExtLookup(
    "../economy.xlsx",
    "Catalonia",
    "time_index2014",
    "historic_labour_compensation",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    {
        "sectors": [
            "Agriculture",
            "Mining quarrying and energy supply",
            "Food Beverages and Tobacco",
            "Textiles and leather etc",
            "Coke refined petroleum nuclear fuel and chemicals etc",
            "Electrical and optical equipment and Transport equipment",
            "Other manufacturing",
            "Construction",
            "Distribution",
            "Hotels and restaurant",
            "Transport storage and communication",
            "Financial Intermediation",
            "Real estate renting and busine activitie",
            "Non Market Service",
        ]
    },
    "_ext_lookup_historic_labour_compensation",
)


@component.add(
    name="historic labour share",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def historic_labour_share():
    """
    Historic variation of labour share.
    """
    return sum(
        historic_labour_compensation(time()).rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    ) / historic_gdp(time())


@component.add(
    name="historic labour share growth",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
)
def historic_labour_share_next_step():
    """
    Historic variation of labour share.
    """
    return sum(
        historic_labour_compensation(time() + 1).rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    ) / historic_gdp(time() + 1)


@component.add(
    name="Initial capital share",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def initial_capital_share():
    """
    Historic 2014 Labour share
    """
    return sum(
        historic_capital_compensation(2014).rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    ) / historic_gdp(2014)


@component.add(
    name="Initial Labour share",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def initial_labour_share():
    """
    Historic 2014 Labour share
    """
    return sum(
        historic_labour_compensation(2014).rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    ) / historic_gdp(2014)


@component.add(
    name="input GDPpc annual growth",
    units="Dmnl",
    comp_type="Data",
    comp_subtype="External",
)
def input_gdppc_annual_growth():
    """
    Original values for annual growth of GDPpc from SSP2.
    """
    return _ext_data_input_gdppc_annual_growth(time())


_ext_data_input_gdppc_annual_growth = ExtData(
    "../economy.xlsx",
    "Catalonia",
    "time_index_projection",
    "input_GDPpc_annual_growth",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_input_gdppc_annual_growth",
)


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
    name="labour share", units="Dmnl", comp_type="Stateful", comp_subtype="Integ"
)
def labour_share():
    """
    Ratio 'Labour compensation/GDP'
    """
    return _integ_labour_share()


_integ_labour_share = Integ(
    lambda: variation_labour_share(), lambda: 0.509901, "_integ_labour_share"
)


@component.add(
    name="Labour share growth",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def labour_share_growth():
    """
    Mean cummulative growth rate of labour share.
    """
    return (p_labour_share() / initial_labour_share()) ** (
        1 / (year_final_labour_share() - year_initial_labour_share())
    ) - 1


@component.add(name="LC", comp_type="Auxiliary", comp_subtype="Normal")
def lc():
    return labour_share() * gdp_aut() * 1000000.0


@component.add(
    name="P capital share", units="Dmnl", comp_type="Constant", comp_subtype="External"
)
def p_capital_share():
    """
    Capital share targetted by 2050.
    """
    return _ext_constant_p_capital_share()


_ext_constant_p_capital_share = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "p_capital_share",
    {},
    _root,
    {},
    "_ext_constant_p_capital_share",
)


@component.add(
    name="P customized cte GDPpc variation",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="External",
)
def p_customized_cte_gdppc_variation():
    """
    From customized year, set annual constant variation.
    """
    return _ext_constant_p_customized_cte_gdppc_variation()


_ext_constant_p_customized_cte_gdppc_variation = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "p_constant_gdp_variation",
    {},
    _root,
    {},
    "_ext_constant_p_customized_cte_gdppc_variation",
)


@component.add(
    name="P customized year GDPpc evolution",
    units="Year",
    comp_type="Constant",
    comp_subtype="External",
)
def p_customized_year_gdppc_evolution():
    """
    From customized year, set annual constant variation.
    """
    return _ext_constant_p_customized_year_gdppc_evolution()


_ext_constant_p_customized_year_gdppc_evolution = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "year_customized_gdp_evol",
    {},
    _root,
    {},
    "_ext_constant_p_customized_year_gdppc_evolution",
)


@component.add(
    name="P GDPpc asymptote",
    units="$/person",
    comp_type="Constant",
    comp_subtype="External",
)
def p_gdppc_asymptote():
    """
    Policy target of GDPpc in target year to be approached smoothly-asymptotically.
    """
    return _ext_constant_p_gdppc_asymptote()


_ext_constant_p_gdppc_asymptote = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "asymptote_GDPpc",
    {},
    _root,
    {},
    "_ext_constant_p_gdppc_asymptote",
)


@component.add(
    name="P labour share", units="Dmnl", comp_type="Constant", comp_subtype="External"
)
def p_labour_share():
    """
    Labour share targetted by 2050.
    """
    return _ext_constant_p_labour_share()


_ext_constant_p_labour_share = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "p_labour_share",
    {},
    _root,
    {},
    "_ext_constant_p_labour_share",
)


@component.add(
    name="P timeseries GDPpc growth rate",
    units="1/Year",
    comp_type="Data",
    comp_subtype="External",
)
def p_timeseries_gdppc_growth_rate():
    """
    Annual GDPpc growth from timeseries.
    """
    return _ext_data_p_timeseries_gdppc_growth_rate(time())


_ext_data_p_timeseries_gdppc_growth_rate = ExtData(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "year_gdp_timeseries",
    "p_timeseries_gdp_growth",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_p_timeseries_gdppc_growth_rate",
)


@component.add(
    name="select GDPpc evolution input",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def select_gdppc_evolution_input():
    """
    0. SSP2 1. Timeseries 2. From customized year, set annual constant variation
    """
    return _ext_constant_select_gdppc_evolution_input()


_ext_constant_select_gdppc_evolution_input = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "select_gdp_evolution",
    {},
    _root,
    {},
    "_ext_constant_select_gdppc_evolution_input",
)


@component.add(name="smooth Desired GDPpc", comp_type="Stateful", comp_subtype="Smooth")
def smooth_desired_gdppc():
    return _smooth_smooth_desired_gdppc()


_smooth_smooth_desired_gdppc = Smooth(
    lambda: desired_variation_gdppc_per_scen(),
    lambda: 2,
    lambda: desired_variation_gdppc_per_scen(),
    lambda: 2,
    "_smooth_smooth_desired_gdppc",
)


@component.add(
    name="smooth Desired variation GDPpc",
    units="$/person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def smooth_desired_variation_gdppc():
    return if_then_else(
        time() < p_customized_year_gdppc_evolution(),
        lambda: desired_variation_gdppc_per_scen(),
        lambda: smooth_desired_gdppc(),
    )


@component.add(name="T asymptote GDPpc", comp_type="Auxiliary", comp_subtype="Normal")
def t_asymptote_gdppc():
    return (target_year_gdppc_asymptote() - p_customized_year_gdppc_evolution()) / 3


@component.add(
    name="Target year GDPpc asymptote", comp_type="Constant", comp_subtype="External"
)
def target_year_gdppc_asymptote():
    return _ext_constant_target_year_gdppc_asymptote()


_ext_constant_target_year_gdppc_asymptote = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "target_year_asymptote_gdp",
    {},
    _root,
    {},
    "_ext_constant_target_year_gdppc_asymptote",
)


@component.add(
    name="variation capital share",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def variation_capital_share():
    """
    Real variation of capital share.
    """
    return capital_share() * growth_capital_share()


@component.add(name="variation CC", comp_type="Auxiliary", comp_subtype="Normal")
def variation_cc():
    return (
        gdp_aut()
        * capital_share()
        * (
            desired_annual_total_demand_growth_rate()
            + growth_capital_share()
            + desired_annual_total_demand_growth_rate() * growth_capital_share()
        )
        * 1000000.0
    )


@component.add(
    name="variation historic GDPpc",
    units="$/(person*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def variation_historic_gdppc():
    """
    Variation of historic GDPpc.
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
    name="variation labour share",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def variation_labour_share():
    """
    Real variation of labour share.
    """
    return growth_labour_share() * labour_share()


@component.add(name="variation LC", comp_type="Auxiliary", comp_subtype="Normal")
def variation_lc():
    return (
        gdp_aut()
        * labour_share()
        * (
            desired_annual_total_demand_growth_rate()
            + growth_labour_share()
            + desired_annual_total_demand_growth_rate() * growth_labour_share()
        )
        * 1000000.0
    )


@component.add(
    name="Year final capial share", comp_type="Constant", comp_subtype="Normal"
)
def year_final_capial_share():
    """
    Year of final capital share by scenarios to use in the mean accumulative growth rate.
    """
    return 2050


@component.add(
    name="Year Final Labour share", comp_type="Constant", comp_subtype="Normal"
)
def year_final_labour_share():
    """
    Year of final labour share by scenarios to use in the mean accumulative growth rate.
    """
    return 2050


@component.add(
    name="Year initial capital share", comp_type="Constant", comp_subtype="Normal"
)
def year_initial_capital_share():
    """
    Last year with historical data to use in the mean cummulative growth rate.
    """
    return 2018


@component.add(
    name="Year Initial Labour share", comp_type="Constant", comp_subtype="Normal"
)
def year_initial_labour_share():
    """
    Last year with historical data to use in the mean cummulative growth rate.
    """
    return 2018
