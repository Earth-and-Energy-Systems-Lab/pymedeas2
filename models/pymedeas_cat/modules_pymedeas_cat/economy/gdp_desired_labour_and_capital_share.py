"""
Module gdp_desired_labour_and_capital_share
Translated using PySD version 2.2.0
"""


def annual_gdppc_growth_rate():
    """
    Real Name: Annual GDPpc growth rate
    Original Eqn: IF THEN ELSE(select GDPpc evolution input=0, input GDPpc annual growth, IF THEN ELSE(select GDPpc evolution input=1, P timeseries GDPpc growth rate, IF THEN ELSE (Time<P customized year GDPpc evolution, P timeseries GDPpc growth rate, P customized cte GDPpc variation )))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


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
    Original Eqn: INTEG ( variation capital share, 0.373314)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Ratio 'Capital compensation/GDP'
    """
    return _integ_capital_share()


def capital_share_growth():
    """
    Real Name: capital share growth
    Original Eqn: ((P capital share/Initial capital share)^(1/(Year final capial share-Year initial capital share)))-1
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Real variation rate of capital share depending on activation.
    """
    return (
        (p_capital_share() / initial_capital_share())
        ** (1 / (year_final_capial_share() - year_initial_capital_share()))
    ) - 1


def cc_total():
    """
    Real Name: CC total
    Original Eqn: GDP AUT*capital share*1e+06
    Units: Mdollars
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return gdp_aut() * capital_share() * 1e06


def desire_gdp_next_step():
    """
    Real Name: Desire GDP next step
    Original Eqn: Desired GDP+Desired variation GDP
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return desired_gdp() + desired_variation_gdp()


def desired_annual_gdp_growth_rate():
    """
    Real Name: Desired annual GDP growth rate
    Original Eqn: (-1+Desire GDP next step/Desired GDP)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Desired annual GDP growth rate.
    """
    return -1 + desire_gdp_next_step() / desired_gdp()


def desired_annual_total_demand_growth_rate():
    """
    Real Name: Desired annual total demand growth rate
    Original Eqn: Desired annual GDP growth rate
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Real variation of Final Demand. Assumed to be equal according to sample
        data from WIOD.
    """
    return desired_annual_gdp_growth_rate()


def desired_annual_total_demand_growth_rate_delayed_1_yr():
    """
    Real Name: Desired annual total demand growth rate delayed 1 yr
    Original Eqn: DELAY FIXED(Desired annual total demand growth rate, 1, 0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Lagged variation of final demand
    """
    return _delayfixed_desired_annual_total_demand_growth_rate_delayed_1_yr()


def desired_gdp():
    """
    Real Name: Desired GDP
    Original Eqn: Desired GDPpc*Population/dollars to Tdollars
    Units: T$
    Limits: (None, None)
    Type: component
    Subs: None

    Desired GDP level for each scenario (user selection).
    """
    return desired_gdppc() * population() / dollars_to_tdollars()


def desired_gdppc():
    """
    Real Name: Desired GDPpc
    Original Eqn: INTEG ( Desired variation GDPpc, GDPpc initial year)
    Units: $/person
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_desired_gdppc()


def desired_variation_gdp():
    """
    Real Name: Desired variation GDP
    Original Eqn: IF THEN ELSE(Time<2015,Desired GDPpc*variation historic pop/dollars to Tdollars+variation historic GDPpc*Population /dollars to Tdollars+variation historic GDPpc*variation historic pop/dollars to Tdollars,Desired GDPpc*pop variation/dollars to Tdollars +Desired variation GDPpc*Population /dollars to Tdollars+Desired variation GDPpc *pop variation/dollars to Tdollars)
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


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
    Original Eqn: IF THEN ELSE(Time<2015, desired variation GDPpc per scen, smooth Desired variation GDPpc)
    Units: $/person
    Limits: (None, None)
    Type: component
    Subs: None

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
    Original Eqn: IF THEN ELSE(Time<2015, variation historic GDPpc, IF THEN ELSE(select GDPpc evolution input=3:AND:Time<P customized year GDPpc evolution,Desired GDPpc*Annual GDPpc growth rate, IF THEN ELSE(select GDPpc evolution input=0,Desired GDPpc*Annual GDPpc growth rate, IF THEN ELSE(select GDPpc evolution input=1,Desired GDPpc*Annual GDPpc growth rate, IF THEN ELSE(select GDPpc evolution input=2,Desired GDPpc*Annual GDPpc growth rate, GDPpc variation asymptote scen)))))
    Units: $/person
    Limits: (None, None)
    Type: component
    Subs: None

    Desired GDPpc variation depending on the policy target selected by the
        user.
    """
    return if_then_else(
        time() < 2015,
        lambda: variation_historic_gdppc(),
        lambda: if_then_else(
            logical_and(
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
    Original Eqn: 1e+06
    Units: dollar/Mdollar
    Limits: (None, None)
    Type: constant
    Subs: None

    Dollars per million dollar (1 M$ = 1e6 $).
    """
    return 1e06


def gdppc_initial_year():
    """
    Real Name: GDPpc initial year
    Original Eqn: historic GDP(1995)/historic population(1995)*dollar per Mdollar
    Units: $/person
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return historic_gdp(1995) / historic_population(1995) * dollar_per_mdollar()


def gdppc_until_p_customized_year_gdppc_evolution():
    """
    Real Name: GDPpc until P customized year GDPpc evolution
    Original Eqn: SAMPLE IF TRUE( Time<P customized year GDPpc evolution, Desired GDPpc, Desired GDPpc)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    GDPpc until starting customized year of the policy target.
    """
    return _sample_if_true_gdppc_until_p_customized_year_gdppc_evolution()


def gdppc_variation_asymptote_scen():
    """
    Real Name: GDPpc variation asymptote scen
    Original Eqn: (GDPpc until P customized year GDPpc evolution-(P GDPpc asymptote -1600))*(-1/T asymptote GDPpc ) *EXP(-(Time-P customized year GDPpc evolution)/T asymptote GDPpc )
    Units: $/(Year*person)
    Limits: (None, None)
    Type: component
    Subs: None

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
    Original Eqn: IF THEN ELSE(Time>=2017,IF THEN ELSE(Time>2050,0,capital share growth*"Labor/Capital share cte?"),historic capital share growth )
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        time() >= 2017,
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
    Original Eqn: IF THEN ELSE(Time>=2017,IF THEN ELSE(Time>2050,0,Labour share growth*"Labor/Capital share cte?"),historic labour share growth)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

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


def historic_capital_compensation(x):
    """
    Real Name: historic capital compensation
    Original Eqn: GET DIRECT LOOKUPS('../economy.xlsx', 'Catalonia', 'time_index2009', 'historic_capital_compensation')
    Units: Mdollars
    Limits: (None, None)
    Type: lookup
    Subs: ['sectors']

    Historical capital compensation (14 sectors).
    """
    return _ext_lookup_historic_capital_compensation(x)


def historic_capital_share():
    """
    Real Name: historic capital share
    Original Eqn: SUM(historic capital compensation[sectors!](Time))/historic GDP(Time)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Historic variation of capital share.
    """
    return sum(historic_capital_compensation(time()), dim=("sectors",)) / historic_gdp(
        time()
    )


def historic_capital_share_growth():
    """
    Real Name: historic capital share growth
    Original Eqn: (historic capital share next step-historic capital share)/historic capital share
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Historic variation of capital share.
    """
    return (
        historic_capital_share_next_step() - historic_capital_share()
    ) / historic_capital_share()


def historic_capital_share_next_step():
    """
    Real Name: historic capital share next step
    Original Eqn: SUM(historic capital compensation[sectors!](Time+1))/historic GDP(Time+1)
    Units:
    Limits: (None, None)
    Type: component
    Subs: None

    Historical capital compensation share.SUM(historic capital
        compensation[sectors!](Time))/historic GDP(Time)
    """
    return sum(
        historic_capital_compensation(time() + 1), dim=("sectors",)
    ) / historic_gdp(time() + 1)


def historic_gdp(x):
    """
    Real Name: historic GDP
    Original Eqn: GET DIRECT LOOKUPS('../economy.xlsx', 'Catalonia', 'time_index2014', 'historic_GDP')
    Units: Mdollars
    Limits: (None, None)
    Type: lookup
    Subs: None

    Historic GDP Million dollars. Data derived from A matrix. US$1995.
    """
    return _ext_lookup_historic_gdp(x)


def historic_labour_compensation(x):
    """
    Real Name: historic labour compensation
    Original Eqn: GET DIRECT LOOKUPS('../economy.xlsx', 'Catalonia', 'time_index2014', 'historic_labour_compensation')
    Units: Mdollars
    Limits: (None, None)
    Type: lookup
    Subs: ['sectors']

    Historical labour compensation (14 sectors).
    """
    return _ext_lookup_historic_labour_compensation(x)


def historic_labour_share():
    """
    Real Name: historic labour share
    Original Eqn: SUM(historic labour compensation[sectors!](Time))/historic GDP(Time)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Historic variation of labour share.
    """
    return sum(historic_labour_compensation(time()), dim=("sectors",)) / historic_gdp(
        time()
    )


def historic_labour_share_growth():
    """
    Real Name: historic labour share growth
    Original Eqn: (historic labour share next step-historic labour share)/historic labour share
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Historic variation of labour share.
    """
    return (
        historic_labour_share_next_step() - historic_labour_share()
    ) / historic_labour_share()


def historic_labour_share_next_step():
    """
    Real Name: historic labour share next step
    Original Eqn: SUM(historic labour compensation[sectors!](Time+1))/historic GDP(Time+1)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Historic variation of labour share.
    """
    return sum(
        historic_labour_compensation(time() + 1), dim=("sectors",)
    ) / historic_gdp(time() + 1)


def initial_capital_share():
    """
    Real Name: Initial capital share
    Original Eqn: SUM(historic capital compensation[sectors!](2014))/historic GDP(2014)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Historic 2014 Labour share
    """
    return sum(historic_capital_compensation(2014), dim=("sectors",)) / historic_gdp(
        2014
    )


def initial_labour_share():
    """
    Real Name: Initial Labour share
    Original Eqn: SUM(historic labour compensation[sectors!](2014))/historic GDP(2014)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Historic 2014 Labour share
    """
    return sum(historic_labour_compensation(2014), dim=("sectors",)) / historic_gdp(
        2014
    )


def input_gdppc_annual_growth():
    """
    Real Name: input GDPpc annual growth
    Original Eqn: GET DIRECT DATA('../economy.xlsx', 'Catalonia', 'time_index_projection', 'input_GDPpc_annual_growth')
    Units: Dmnl
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Original values for annual growth of GDPpc from SSP2.
    """
    return _ext_data_input_gdppc_annual_growth(time())


def laborcapital_share_cte():
    """
    Real Name: "Labor/Capital share cte?"
    Original Eqn: 1
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    0: Labor share: cte        1: Labor share evolves following "P labor share"
    """
    return 1


def labour_share():
    """
    Real Name: labour share
    Original Eqn: INTEG ( variation labour share, 0.509901)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Ratio 'Labour compensation/GDP'
    """
    return _integ_labour_share()


def labour_share_growth():
    """
    Real Name: Labour share growth
    Original Eqn: ((P labour share/Initial Labour share)^(1/(Year Final Labour share-Year Initial Labour share)))-1
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Mean cummulative growth rate of labour share.
    """
    return (
        (p_labour_share() / initial_labour_share())
        ** (1 / (year_final_labour_share() - year_initial_labour_share()))
    ) - 1


def lc():
    """
    Real Name: LC
    Original Eqn: labour share*GDP AUT*1e+06
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return labour_share() * gdp_aut() * 1e06


def p_capital_share():
    """
    Real Name: P capital share
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'F3')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Capital share targetted by 2050.
    """
    return _ext_constant_p_capital_share()


def p_customized_cte_gdppc_variation():
    """
    Real Name: P customized cte GDPpc variation
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'G7')
    Units: 1/Year
    Limits: (None, None)
    Type: constant
    Subs: None

    From customized year, set annual constant variation.
    """
    return _ext_constant_p_customized_cte_gdppc_variation()


def p_customized_year_gdppc_evolution():
    """
    Real Name: P customized year GDPpc evolution
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'E7')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    From customized year, set annual constant variation.
    """
    return _ext_constant_p_customized_year_gdppc_evolution()


def p_gdppc_asymptote():
    """
    Real Name: P GDPpc asymptote
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'G8')
    Units: $/person
    Limits: (None, None)
    Type: constant
    Subs: None

    Policy target of GDPpc in target year to be approached
        smoothly-asymptotically.
    """
    return _ext_constant_p_gdppc_asymptote()


def p_labour_share():
    """
    Real Name: P labour share
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'C3')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Labour share targetted by 2050.
    """
    return _ext_constant_p_labour_share()


def p_timeseries_gdppc_growth_rate():
    """
    Real Name: P timeseries GDPpc growth rate
    Original Eqn: GET DIRECT DATA('../../scenarios/scen_aut.xlsx', 'BAU', '5', 'E6')
    Units: 1/Year
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Annual GDPpc growth from timeseries.
    """
    return _ext_data_p_timeseries_gdppc_growth_rate(time())


def select_gdppc_evolution_input():
    """
    Real Name: select GDPpc evolution input
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'B4')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    0. SSP2        1. Timeseries        2. From customized year, set annual constant variation
    """
    return _ext_constant_select_gdppc_evolution_input()


def smooth_desired_gdppc():
    """
    Real Name: smooth Desired GDPpc
    Original Eqn: SMOOTH N(desired variation GDPpc per scen, 2, desired variation GDPpc per scen, 2)
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _smooth_smooth_desired_gdppc()


def smooth_desired_variation_gdppc():
    """
    Real Name: smooth Desired variation GDPpc
    Original Eqn: IF THEN ELSE(Time<P customized year GDPpc evolution,desired variation GDPpc per scen,smooth Desired GDPpc)
    Units: $/person
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        time() < p_customized_year_gdppc_evolution(),
        lambda: desired_variation_gdppc_per_scen(),
        lambda: smooth_desired_gdppc(),
    )


def t_asymptote_gdppc():
    """
    Real Name: T asymptote GDPpc
    Original Eqn: (Target year GDPpc asymptote-P customized year GDPpc evolution)/3
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (target_year_gdppc_asymptote() - p_customized_year_gdppc_evolution()) / 3


def target_year_gdppc_asymptote():
    """
    Real Name: Target year GDPpc asymptote
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'I8')
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return _ext_constant_target_year_gdppc_asymptote()


def variation_capital_share():
    """
    Real Name: variation capital share
    Original Eqn: capital share*growth capital share
    Units: 1/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Real variation of capital share.
    """
    return capital_share() * growth_capital_share()


def variation_cc():
    """
    Real Name: variation CC
    Original Eqn: GDP AUT*capital share*(Desired annual total demand growth rate+growth capital share+Desired annual total demand growth rate*growth capital share)*1e+06
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        gdp_aut()
        * capital_share()
        * (
            desired_annual_total_demand_growth_rate()
            + growth_capital_share()
            + desired_annual_total_demand_growth_rate() * growth_capital_share()
        )
        * 1e06
    )


def variation_historic_gdppc():
    """
    Real Name: variation historic GDPpc
    Original Eqn: IF THEN ELSE(Time<2013, (historic GDP(Time+1)/historic population(Time+1)-historic GDP(Time)/historic population(Time ))*dollar per Mdollar, 0)
    Units: $/(person*Year)
    Limits: (None, None)
    Type: component
    Subs: None

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
    Original Eqn: growth labour share*labour share
    Units: 1/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Real variation of labour share.
    """
    return growth_labour_share() * labour_share()


def variation_lc():
    """
    Real Name: variation LC
    Original Eqn: GDP AUT*labour share*(Desired annual total demand growth rate +growth labour share+Desired annual total demand growth rate *growth labour share)*1e+06
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        gdp_aut()
        * labour_share()
        * (
            desired_annual_total_demand_growth_rate()
            + growth_labour_share()
            + desired_annual_total_demand_growth_rate() * growth_labour_share()
        )
        * 1e06
    )


def year_final_capial_share():
    """
    Real Name: Year final capial share
    Original Eqn: 2050
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None

    Year of final capital share by scenarios to use in the mean accumulative
        growth rate.
    """
    return 2050


def year_final_labour_share():
    """
    Real Name: Year Final Labour share
    Original Eqn: 2050
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None

    Year of final labour share by scenarios to use in the mean accumulative
        growth rate.
    """
    return 2050


def year_initial_capital_share():
    """
    Real Name: Year initial capital share
    Original Eqn: 2018
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None

    Last year with historical data to use in the mean cummulative growth rate.
    """
    return 2018


def year_initial_labour_share():
    """
    Real Name: Year Initial Labour share
    Original Eqn: 2018
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None

    Last year with historical data to use in the mean cummulative growth rate.
    """
    return 2018


_integ_capital_share = Integ(
    lambda: variation_capital_share(), lambda: 0.373314, "_integ_capital_share"
)


_delayfixed_desired_annual_total_demand_growth_rate_delayed_1_yr = DelayFixed(
    lambda: desired_annual_total_demand_growth_rate(),
    lambda: 1,
    lambda: 0,
    time_step,
    "_delayfixed_desired_annual_total_demand_growth_rate_delayed_1_yr",
)


_integ_desired_gdppc = Integ(
    lambda: desired_variation_gdppc(),
    lambda: gdppc_initial_year(),
    "_integ_desired_gdppc",
)


_sample_if_true_gdppc_until_p_customized_year_gdppc_evolution = SampleIfTrue(
    lambda: time() < p_customized_year_gdppc_evolution(),
    lambda: desired_gdppc(),
    lambda: desired_gdppc(),
    "_sample_if_true_gdppc_until_p_customized_year_gdppc_evolution",
)


_ext_lookup_historic_capital_compensation = ExtLookup(
    "../economy.xlsx",
    "Catalonia",
    "time_index2009",
    "historic_capital_compensation",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_lookup_historic_capital_compensation",
)


_ext_lookup_historic_gdp = ExtLookup(
    "../economy.xlsx",
    "Catalonia",
    "time_index2014",
    "historic_GDP",
    {},
    _root,
    "_ext_lookup_historic_gdp",
)


_ext_lookup_historic_labour_compensation = ExtLookup(
    "../economy.xlsx",
    "Catalonia",
    "time_index2014",
    "historic_labour_compensation",
    {"sectors": _subscript_dict["sectors"]},
    _root,
    "_ext_lookup_historic_labour_compensation",
)


_ext_data_input_gdppc_annual_growth = ExtData(
    "../economy.xlsx",
    "Catalonia",
    "time_index_projection",
    "input_GDPpc_annual_growth",
    "interpolate",
    {},
    _root,
    "_ext_data_input_gdppc_annual_growth",
)


_integ_labour_share = Integ(
    lambda: variation_labour_share(), lambda: 0.509901, "_integ_labour_share"
)


_ext_constant_p_capital_share = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "F3",
    {},
    _root,
    "_ext_constant_p_capital_share",
)


_ext_constant_p_customized_cte_gdppc_variation = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "G7",
    {},
    _root,
    "_ext_constant_p_customized_cte_gdppc_variation",
)


_ext_constant_p_customized_year_gdppc_evolution = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "E7",
    {},
    _root,
    "_ext_constant_p_customized_year_gdppc_evolution",
)


_ext_constant_p_gdppc_asymptote = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "G8",
    {},
    _root,
    "_ext_constant_p_gdppc_asymptote",
)


_ext_constant_p_labour_share = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "C3",
    {},
    _root,
    "_ext_constant_p_labour_share",
)


_ext_data_p_timeseries_gdppc_growth_rate = ExtData(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "5",
    "E6",
    "interpolate",
    {},
    _root,
    "_ext_data_p_timeseries_gdppc_growth_rate",
)


_ext_constant_select_gdppc_evolution_input = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "B4",
    {},
    _root,
    "_ext_constant_select_gdppc_evolution_input",
)


_smooth_smooth_desired_gdppc = Smooth(
    lambda: desired_variation_gdppc_per_scen(),
    lambda: 2,
    lambda: desired_variation_gdppc_per_scen(),
    lambda: 2,
    "_smooth_smooth_desired_gdppc",
)


_ext_constant_target_year_gdppc_asymptote = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "I8",
    {},
    _root,
    "_ext_constant_target_year_gdppc_asymptote",
)
