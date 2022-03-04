"""
Module gdp_desired_labour_and_capital_share
Translated using PySD version 2.2.1
"""


def annual_gdppc_growth_rate():
    """
    Real Name: Annual GDPpc growth rate
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
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


def capital_share():
    """
    Real Name: capital share
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Ratio 'Capital compensation/GDP'
    """
    return _integ_capital_share()


_integ_capital_share = Integ(
    lambda: variation_capital_share(), lambda: 0.413596, "_integ_capital_share"
)


def capital_share_growth():
    """
    Real Name: capital share growth
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Real variation rate of capital share depending on activation.
    """
    return (p_capital_share() / initial_capital_share()) ** (
        1 / (year_final_capial_share() - year_initial_capital_share())
    ) - 1


def cc_total():
    """
    Real Name: CC total
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Capital compensation
    """
    return _integ_cc_total()


_integ_cc_total = Integ(
    lambda: variation_cc() - cc_total_not_covered(),
    lambda: initial_cc_total(),
    "_integ_cc_total",
)


def cc_total_not_covered():
    """
    Real Name: CC total not covered
    Original Eqn:
    Units: Mdollars/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Gap between capital compensation required and real capital compensation (after energy-economy feedback)
    """
    return demand_not_covered_total_fd() * capital_share()


def desire_gdp_next_step():
    """
    Real Name: Desire GDP next step
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return desired_gdp() + desired_variation_gdp()


def desired_annual_gdp_growth_rate():
    """
    Real Name: Desired annual GDP growth rate
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Desired annual GDP growth rate.
    """
    return -1 + desire_gdp_next_step() / desired_gdp()


def desired_annual_total_demand_growth_rate():
    """
    Real Name: Desired annual total demand growth rate
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Real variation of Final Demand. Assumed to be equal according to sample data from WIOD.
    """
    return desired_annual_gdp_growth_rate()


def desired_annual_total_demand_growth_rate_delayed_1_yr():
    """
    Real Name: Desired annual total demand growth rate delayed 1 yr
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: []

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


def desired_gdp():
    """
    Real Name: Desired GDP
    Original Eqn:
    Units: T$
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Desired GDP level for each scenario (user selection).
    """
    return desired_gdppc() * population() / dollars_to_tdollars()


def desired_gdp_delayed_1yr():
    """
    Real Name: Desired GDP delayed 1yr
    Original Eqn:
    Units: T$/Year
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Desired GDP delayed 1 year.
    """
    return _delayfixed_desired_gdp_delayed_1yr()


_delayfixed_desired_gdp_delayed_1yr = DelayFixed(
    lambda: desired_gdp(),
    lambda: 1,
    lambda: 8.6,
    time_step,
    "_delayfixed_desired_gdp_delayed_1yr",
)


def desired_gdppc():
    """
    Real Name: Desired GDPpc
    Original Eqn:
    Units: $/person
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _integ_desired_gdppc()


_integ_desired_gdppc = Integ(
    lambda: desired_variation_gdppc(),
    lambda: gdppc_initial_year(),
    "_integ_desired_gdppc",
)


def desired_variation_gdp():
    """
    Real Name: Desired variation GDP
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return if_then_else(
        time() < 2015,
        lambda: desired_gdppc() * variation_historic_pop() / dollars_to_tdollars()
        + variation_historic_gdppc() * population() / dollars_to_tdollars()
        + variation_historic_gdppc() * variation_historic_pop() / dollars_to_tdollars(),
        lambda: desired_gdppc() * pop_variation() / dollars_to_tdollars()
        + desired_variation_gdppc() * population() / dollars_to_tdollars()
        + desired_variation_gdppc() * pop_variation() / dollars_to_tdollars(),
    )


def desired_variation_gdppc():
    """
    Real Name: Desired variation GDPpc
    Original Eqn:
    Units: $/person
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Desired variation of GDP per capita.
    """
    return if_then_else(
        time() < 2015,
        lambda: desired_variation_gdppc_per_scen(),
        lambda: smooth_desired_variation_gdppc(),
    )


def desired_variation_gdppc_per_scen():
    """
    Real Name: desired variation GDPpc per scen
    Original Eqn:
    Units: $/person
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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


def dollar_per_mdollar():
    """
    Real Name: dollar per Mdollar
    Original Eqn:
    Units: dollar/Mdollar
    Limits: (None, None)
    Type: Constant
    Subs: []

    Dollars per million dollar (1 M$ = 1e6 $).
    """
    return 1000000.0


def gdppc_initial_year():
    """
    Real Name: GDPpc initial year
    Original Eqn:
    Units: $/person
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return historic_gdp(1995) / historic_population(1995) * dollar_per_mdollar()


def gdppc_until_p_customized_year_gdppc_evolution():
    """
    Real Name: GDPpc until P customized year GDPpc evolution
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    GDPpc until starting customized year of the policy target.
    """
    return if_then_else(
        time() < p_customized_year_gdppc_evolution(),
        lambda: desired_gdppc(),
        lambda: desired_gdppc(),
    )


def gdppc_variation_asymptote_scen():
    """
    Real Name: GDPpc variation asymptote scen
    Original Eqn:
    Units: $/(Year*person)
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Desired GDPpc variation to reach asymptote target.
    """
    return (
        (gdppc_until_p_customized_year_gdppc_evolution() - (p_gdppc_asymptote() - 1600))
        * (-1 / t_asymptote_gdppc())
        * np.exp(-(time() - p_customized_year_gdppc_evolution()) / t_asymptote_gdppc())
    )


def growth_capital_share():
    """
    Real Name: growth capital share
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return if_then_else(
        time() > 2014,
        lambda: if_then_else(
            time() > 2050,
            lambda: 0,
            lambda: capital_share_growth() * laborcapital_share_cte(),
        ),
        lambda: historic_capital_share_growth(),
    )


def growth_labour_share():
    """
    Real Name: growth labour share
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Real variation rate of labour share depending on activation.
    """
    return if_then_else(
        time() > 2014,
        lambda: if_then_else(
            time() > 2050,
            lambda: 0,
            lambda: labour_share_growth() * laborcapital_share_cte(),
        ),
        lambda: historic_labour_share_growth(),
    )


@subs(["sectors"], _subscript_dict)
def historic_capital_compensation(x):
    """
    Real Name: historic capital compensation
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Lookup
    Subs: ['sectors']

    Historical capital compensation (14 sectors).
    """
    return _ext_lookup_historic_capital_compensation(x)


_ext_lookup_historic_capital_compensation = ExtLookup(
    "../economy.xlsx",
    "Europe",
    "time_index2009",
    "historic_capital_compensation",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_lookup_historic_capital_compensation",
)


def historic_capital_share():
    """
    Real Name: historic capital share
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Historical capital compensation share.
    """
    return sum(
        historic_capital_compensation(time()).rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    ) / historic_gdp(time())


def historic_capital_share_growth():
    """
    Real Name: historic capital share growth
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Historic variation of capital share.
    """
    return (
        historic_capital_share_next_step() - historic_capital_share()
    ) / historic_capital_share()


def historic_capital_share_next_step():
    """
    Real Name: historic capital share next step
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return sum(
        historic_capital_compensation(time() + 1).rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    ) / historic_gdp(time() + 1)


def historic_gdp(x):
    """
    Real Name: historic GDP
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Lookup
    Subs: []

    Historic GDP Million dollars. Data derived from A matrix. US$1995.
    """
    return _ext_lookup_historic_gdp(x)


_ext_lookup_historic_gdp = ExtLookup(
    "../economy.xlsx",
    "Europe",
    "time_index2014",
    "historic_GDP",
    {},
    _root,
    "_ext_lookup_historic_gdp",
)


@subs(["sectors"], _subscript_dict)
def historic_labour_compensation(x):
    """
    Real Name: historic labour compensation
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Lookup
    Subs: ['sectors']

    Historical labour compensation (14 sectors).
    """
    return _ext_lookup_historic_labour_compensation(x)


_ext_lookup_historic_labour_compensation = ExtLookup(
    "../economy.xlsx",
    "Europe",
    "time_index2014",
    "historic_labour_compensation",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_lookup_historic_labour_compensation",
)


def historic_labour_share():
    """
    Real Name: historic labour share
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Historical capital compensation share.
    """
    return sum(
        historic_labour_compensation(time()).rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    ) / historic_gdp(time())


def historic_labour_share_growth():
    """
    Real Name: historic labour share growth
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Historic variation of labour share.
    """
    return (
        historic_labour_share_next_step() - historic_labour_share()
    ) / historic_labour_share()


def historic_labour_share_next_step():
    """
    Real Name: historic labour share next step
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return sum(
        historic_labour_compensation(time() + 1).rename({"sectors": "sectors!"}),
        dim=["sectors!"],
    ) / historic_gdp(time() + 1)


def initial_capital_share():
    """
    Real Name: Initial capital share
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Historic 2015 Labour share
    """
    return 0.407001


def initial_cc_total():
    """
    Real Name: initial CC total
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Constant
    Subs: []

    Initial capital compensation
    """
    return 3594330.0


def initial_labour_share():
    """
    Real Name: Initial Labour share
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Historic 2015 Labour share
    """
    return 0.473592


def initial_lc_total():
    """
    Real Name: initial LC total
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Constant
    Subs: []

    Initial labour compensation
    """
    return 4181720.0


def input_gdppc_annual_growth():
    """
    Real Name: input GDPpc annual growth
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Data
    Subs: []

    Original values for annual growth of GDPpc from SSP2.
    """
    return _ext_data_input_gdppc_annual_growth(time())


_ext_data_input_gdppc_annual_growth = ExtData(
    "../economy.xlsx",
    "Europe",
    "time_index_projection",
    "input_GDPpc_annual_growth",
    None,
    {},
    _root,
    "_ext_data_input_gdppc_annual_growth",
)


def laborcapital_share_cte():
    """
    Real Name: "Labor/Capital share cte?"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    0: Labor share: cte 1: Labor share evolves following "P labor share"
    """
    return 1


def labour_share():
    """
    Real Name: labour share
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Ratio 'Labour compensation/GDP'
    """
    return _integ_labour_share()


_integ_labour_share = Integ(
    lambda: variation_labour_share(), lambda: 0.481186, "_integ_labour_share"
)


def labour_share_growth():
    """
    Real Name: Labour share growth
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Mean cummulative growth rate of labour share.
    """
    return (p_labour_share() / initial_labour_share()) ** (
        1 / (year_final_labour_share() - year_initial_labour_share())
    ) - 1


def lc():
    """
    Real Name: LC
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Labour compensation
    """
    return _integ_lc()


_integ_lc = Integ(
    lambda: variation_lc() - lc_not_covered(), lambda: initial_lc_total(), "_integ_lc"
)


def lc_not_covered():
    """
    Real Name: LC not covered
    Original Eqn:
    Units: Mdollars/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Gap between labour compensation required and real labour compensation (after energy-economy feedback)
    """
    return demand_not_covered_total_fd() * labour_share()


def p_capital_share():
    """
    Real Name: P capital share
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Capital share targetted by 2050.
    """
    return _ext_constant_p_capital_share()


_ext_constant_p_capital_share = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "p_capital_share",
    {},
    _root,
    "_ext_constant_p_capital_share",
)


def p_customized_cte_gdppc_variation():
    """
    Real Name: P customized cte GDPpc variation
    Original Eqn:
    Units: 1/Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    From customized year, set annual constant variation.
    """
    return _ext_constant_p_customized_cte_gdppc_variation()


_ext_constant_p_customized_cte_gdppc_variation = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "p_constant_gdp_variation",
    {},
    _root,
    "_ext_constant_p_customized_cte_gdppc_variation",
)


def p_customized_year_gdppc_evolution():
    """
    Real Name: P customized year GDPpc evolution
    Original Eqn:
    Units: Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    From customized year, set annual constant variation.
    """
    return _ext_constant_p_customized_year_gdppc_evolution()


_ext_constant_p_customized_year_gdppc_evolution = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "year_customized_gdp_evol",
    {},
    _root,
    "_ext_constant_p_customized_year_gdppc_evolution",
)


def p_gdppc_asymptote():
    """
    Real Name: P GDPpc asymptote
    Original Eqn:
    Units: $/person
    Limits: (None, None)
    Type: Constant
    Subs: []

    Policy target of GDPpc in target year to be approached smoothly-asymptotically.
    """
    return _ext_constant_p_gdppc_asymptote()


_ext_constant_p_gdppc_asymptote = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "asymptote_GDPpc",
    {},
    _root,
    "_ext_constant_p_gdppc_asymptote",
)


def p_labour_share():
    """
    Real Name: P labour share
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Labour share targetted by 2050.
    """
    return _ext_constant_p_labour_share()


_ext_constant_p_labour_share = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "p_labour_share",
    {},
    _root,
    "_ext_constant_p_labour_share",
)


def p_timeseries_gdppc_growth_rate():
    """
    Real Name: P timeseries GDPpc growth rate
    Original Eqn:
    Units: 1/Year
    Limits: (None, None)
    Type: Data
    Subs: []

    Annual GDPpc growth from timeseries.
    """
    return _ext_data_p_timeseries_gdppc_growth_rate(time())


_ext_data_p_timeseries_gdppc_growth_rate = ExtData(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "year_gdp_timeseries",
    "p_timeseries_gdp_growth",
    "interpolate",
    {},
    _root,
    "_ext_data_p_timeseries_gdppc_growth_rate",
)


def select_gdppc_evolution_input():
    """
    Real Name: select GDPpc evolution input
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    0. SSP2 1. Timeseries 2. From customized year, set annual constant variation
    """
    return _ext_constant_select_gdppc_evolution_input()


_ext_constant_select_gdppc_evolution_input = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "select_gdp_evolution",
    {},
    _root,
    "_ext_constant_select_gdppc_evolution_input",
)


def smooth_desired_gdppc():
    """
    Real Name: smooth Desired GDPpc
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _smooth_smooth_desired_gdppc()


_smooth_smooth_desired_gdppc = Smooth(
    lambda: desired_variation_gdppc_per_scen(),
    lambda: 2,
    lambda: desired_variation_gdppc_per_scen(),
    lambda: 2,
    "_smooth_smooth_desired_gdppc",
)


def smooth_desired_variation_gdppc():
    """
    Real Name: smooth Desired variation GDPpc
    Original Eqn:
    Units: $/person
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return if_then_else(
        time() < p_customized_year_gdppc_evolution(),
        lambda: desired_variation_gdppc_per_scen(),
        lambda: smooth_desired_gdppc(),
    )


def t_asymptote_gdppc():
    """
    Real Name: T asymptote GDPpc
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (target_year_gdppc_asymptote() - p_customized_year_gdppc_evolution()) / 3


def target_year_gdppc_asymptote():
    """
    Real Name: Target year GDPpc asymptote
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return _ext_constant_target_year_gdppc_asymptote()


_ext_constant_target_year_gdppc_asymptote = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "target_year_asymptote_gdp",
    {},
    _root,
    "_ext_constant_target_year_gdppc_asymptote",
)


def variation_capital_share():
    """
    Real Name: variation capital share
    Original Eqn:
    Units: 1/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Real variation of capital share.
    """
    return capital_share() * growth_capital_share()


def variation_cc():
    """
    Real Name: variation CC
    Original Eqn:
    Units: Mdollars/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Variation of capital compensation
    """
    return (
        capital_share()
        * (
            desired_annual_total_demand_growth_rate()
            + growth_capital_share()
            + desired_annual_total_demand_growth_rate() * growth_capital_share()
        )
        * gdp_eu()
        * 1000000.0
    )


def variation_historic_gdppc():
    """
    Real Name: variation historic GDPpc
    Original Eqn:
    Units: $/(person*Year)
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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


def variation_labour_share():
    """
    Real Name: variation labour share
    Original Eqn:
    Units: 1/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Real variation of labour share.
    """
    return growth_labour_share() * labour_share()


def variation_lc():
    """
    Real Name: variation LC
    Original Eqn:
    Units: Mdollars
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Variation of labour compensation
    """
    return (
        gdp_eu()
        * 1000000.0
        * labour_share()
        * (
            desired_annual_total_demand_growth_rate()
            + growth_labour_share()
            + desired_annual_total_demand_growth_rate() * growth_labour_share()
        )
    )


def year_final_capial_share():
    """
    Real Name: Year final capial share
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Constant
    Subs: []

    Year of final capital share by scenarios to use in the mean accumulative growth rate.
    """
    return 2050


def year_final_labour_share():
    """
    Real Name: Year Final Labour share
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Constant
    Subs: []

    Year of final labour share by scenarios to use in the mean accumulative growth rate.
    """
    return 2050


def year_initial_capital_share():
    """
    Real Name: Year initial capital share
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Constant
    Subs: []

    Last year with historical data to use in the mean cummulative growth rate.
    """
    return 2015


def year_initial_labour_share():
    """
    Real Name: Year Initial Labour share
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Constant
    Subs: []

    Last year with historical data to use in the mean cummulative growth rate.
    """
    return 2015
