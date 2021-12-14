"""
Module population_p
Translated using PySD version 2.1.0
"""


def annual_population_growth_rate():
    """
    Real Name: Annual population growth rate
    Original Eqn: IF THEN ELSE(select Population evolution input=0, variation input pop , IF THEN ELSE(select Population evolution input=1, P timeseries pop growth rate, IF THEN ELSE (Time<P customized year pop evolution, P timeseries pop growth rate, P customized cte pop variation )))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        select_population_evolution_input() == 0,
        lambda: variation_input_pop(),
        lambda: if_then_else(
            select_population_evolution_input() == 1,
            lambda: p_timeseries_pop_growth_rate(),
            lambda: if_then_else(
                time() < p_customized_year_pop_evolution(),
                lambda: p_timeseries_pop_growth_rate(),
                lambda: p_customized_cte_pop_variation(),
            ),
        ),
    )


def historic_population(x):
    """
    Real Name: historic population
    Original Eqn: ( GET DIRECT LOOKUPS('../parameters.xlsx', 'Austria', 'time_historic_population', 'historic_population'))
    Units: people
    Limits: (None, None)
    Type: lookup
    Subs: None

    Historic population (1995-2015). Ref: World bank.
    """
    return _ext_lookup_historic_population(x)


def initial_population():
    """
    Real Name: initial population
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Austria', 'initial_population')
    Units: people
    Limits: (None, None)
    Type: constant
    Subs: None

    Initial value from WorldBank in 1995.
    """
    return _ext_constant_initial_population()


def input_population(x):
    """
    Real Name: input population
    Original Eqn: GET DIRECT LOOKUPS('../parameters.xlsx', 'Austria', 'time_index_projection', 'input_population')
    Units:
    Limits: (None, None)
    Type: lookup
    Subs: None

    Original values from SSP2 evolution.
    """
    return _ext_lookup_input_population(x)


def p_customized_cte_pop_variation():
    """
    Real Name: P customized cte pop variation
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'G14')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    From customized year, set annual constant variation.
    """
    return _ext_constant_p_customized_cte_pop_variation()


def p_customized_year_pop_evolution():
    """
    Real Name: P customized year pop evolution
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'E14')
    Units: 1/Year
    Limits: (None, None)
    Type: constant
    Subs: None

    From customized year, set annual constant variation.
    """
    return _ext_constant_p_customized_year_pop_evolution()


def p_pop_asymptote_millions():
    """
    Real Name: P pop asymptote millions
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'G15' )
    Units: Mpeople
    Limits: (None, None)
    Type: constant
    Subs: None

    Policy target of population in target year to be approached
        smoothly-asymptotically.
    """
    return _ext_constant_p_pop_asymptote_millions()


def p_timeseries_pop_growth_rate():
    """
    Real Name: P timeseries pop growth rate
    Original Eqn: GET DIRECT DATA('../../scenarios/scen_aut.xlsx', 'BAU', '12', 'E13')
    Units: 1/Year
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Annual population growth from timeseries. UN projections in their medium
        scenario (Medium fertility variant)
    """
    return _ext_data_p_timeseries_pop_growth_rate(time())


def pop_asymptote():
    """
    Real Name: pop asymptote
    Original Eqn: (P pop asymptote millions*1e+06)-1e+07
    Units: people
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (p_pop_asymptote_millions() * 1e06) - 1e07


def pop_until_p_customized_year_pop_evolution():
    """
    Real Name: pop until P customized year pop evolution
    Original Eqn: SAMPLE IF TRUE(Time<P customized year pop evolution, Population, Population)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Population until starting customized year of the policy target.
    """
    return _sample_if_true_pop_until_p_customized_year_pop_evolution()


def pop_variation():
    """
    Real Name: pop variation
    Original Eqn: IF THEN ELSE(Time<P customized year pop evolution, pop variation by scen , 0.05*pop variation by scen+0.05*pop variation delay 1 step+0.1*pop variation delay 2 step+0.15*pop variation delay 3 step +0.2*pop variation delay 4 step+0.3*pop variation delay 5 step+0.15*pop variation delay 6 step)
    Units: people/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Population growth. (Historic data from 1990-2010; projection 2011-2100)
        2011 UST$
    """
    return if_then_else(
        time() < p_customized_year_pop_evolution(),
        lambda: pop_variation_by_scen(),
        lambda: 0.05 * pop_variation_by_scen()
        + 0.05 * pop_variation_delay_1_step()
        + 0.1 * pop_variation_delay_2_step()
        + 0.15 * pop_variation_delay_3_step()
        + 0.2 * pop_variation_delay_4_step()
        + 0.3 * pop_variation_delay_5_step()
        + 0.15 * pop_variation_delay_6_step(),
    )


def pop_variation_asymptote_scen():
    """
    Real Name: pop variation asymptote scen
    Original Eqn: (pop until P customized year pop evolution-pop asymptote)*(-1/T asymptote pop)*EXP(-(Time -P customized year pop evolution)/T asymptote pop)
    Units: people/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Population variation to reach asymptote target.
    """
    return (
        (pop_until_p_customized_year_pop_evolution() - pop_asymptote())
        * (-1 / t_asymptote_pop())
        * np.exp(-(time() - p_customized_year_pop_evolution()) / t_asymptote_pop())
    )


def pop_variation_by_scen():
    """
    Real Name: pop variation by scen
    Original Eqn: IF THEN ELSE(Time<2014, variation historic pop, IF THEN ELSE(select Population evolution input=3:AND:Time<P customized year pop evolution,Population*Annual population growth rate, IF THEN ELSE(select Population evolution input=0,Population*Annual population growth rate, IF THEN ELSE(select Population evolution input=2,Population*Annual population growth rate, IF THEN ELSE(select Population evolution input=3,pop variation asymptote scen,Population*Annual population growth rate)))))
    Units: people/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Population variation depending on the policy target selected by the user.
    """
    return if_then_else(
        time() < 2014,
        lambda: variation_historic_pop(),
        lambda: if_then_else(
            logical_and(
                select_population_evolution_input() == 3,
                time() < p_customized_year_pop_evolution(),
            ),
            lambda: population() * annual_population_growth_rate(),
            lambda: if_then_else(
                select_population_evolution_input() == 0,
                lambda: population() * annual_population_growth_rate(),
                lambda: if_then_else(
                    select_population_evolution_input() == 2,
                    lambda: population() * annual_population_growth_rate(),
                    lambda: if_then_else(
                        select_population_evolution_input() == 3,
                        lambda: pop_variation_asymptote_scen(),
                        lambda: population() * annual_population_growth_rate(),
                    ),
                ),
            ),
        ),
    )


def pop_variation_delay_1_step():
    """
    Real Name: pop variation delay 1 step
    Original Eqn: DELAY FIXED ( pop variation by scen,0.5, pop variation by scen)
    Units: people/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _delayfixed_pop_variation_delay_1_step()


def pop_variation_delay_2_step():
    """
    Real Name: pop variation delay 2 step
    Original Eqn: DELAY FIXED ( pop variation by scen, 1, pop variation by scen)
    Units: people/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _delayfixed_pop_variation_delay_2_step()


def pop_variation_delay_3_step():
    """
    Real Name: pop variation delay 3 step
    Original Eqn: DELAY FIXED ( pop variation by scen, 2, pop variation by scen)
    Units: people/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _delayfixed_pop_variation_delay_3_step()


def pop_variation_delay_4_step():
    """
    Real Name: pop variation delay 4 step
    Original Eqn: DELAY FIXED ( pop variation by scen,3, pop variation by scen)
    Units: people/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _delayfixed_pop_variation_delay_4_step()


def pop_variation_delay_5_step():
    """
    Real Name: pop variation delay 5 step
    Original Eqn: DELAY FIXED ( pop variation by scen,4, pop variation by scen)
    Units: people/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _delayfixed_pop_variation_delay_5_step()


def pop_variation_delay_6_step():
    """
    Real Name: pop variation delay 6 step
    Original Eqn: DELAY FIXED ( pop variation by scen,5, pop variation by scen)
    Units: people/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _delayfixed_pop_variation_delay_6_step()


def population():
    """
    Real Name: Population
    Original Eqn: INTEG ( pop variation, initial population)
    Units: people
    Limits: (None, None)
    Type: component
    Subs: None

    Population projection.
    """
    return _integ_population()


def select_population_evolution_input():
    """
    Real Name: select Population evolution input
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'B11')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    0. From SSPs        1. Timeseries        2. From cusotmized year, set annual constant variation
    """
    return _ext_constant_select_population_evolution_input()


def smooth_pop():
    """
    Real Name: smooth pop
    Original Eqn: SMOOTH N(pop variation by scen, 4, pop variation by scen, 2 )
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _smooth_smooth_pop()


def smooth_probe():
    """
    Real Name: smooth probe
    Original Eqn: IF THEN ELSE(Time<P customized year pop evolution,pop variation by scen ,smooth pop)
    Units: people/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        time() < p_customized_year_pop_evolution(),
        lambda: pop_variation_by_scen(),
        lambda: smooth_pop(),
    )


def t_asymptote_pop():
    """
    Real Name: T asymptote pop
    Original Eqn: (Target year pop asymptote-P customized year pop evolution)/3
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (target_year_pop_asymptote() - p_customized_year_pop_evolution()) / 3


def target_year_pop_asymptote():
    """
    Real Name: Target year pop asymptote
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'I15')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Year when population target reaches around 95% of the target population
        (asymptote).
    """
    return _ext_constant_target_year_pop_asymptote()


def variation_historic_pop():
    """
    Real Name: variation historic pop
    Original Eqn: IF THEN ELSE(Time<2014, historic population(Time+1)-historic population(Time), 0)
    Units: people/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Population historic variation.
    """
    return if_then_else(
        time() < 2014,
        lambda: historic_population(time() + 1) - historic_population(time()),
        lambda: 0,
    )


def variation_input_pop():
    """
    Real Name: variation input pop
    Original Eqn: IF THEN ELSE(Time<2010, 0, -1+input population(Time+1)/input population(Time))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        time() < 2010,
        lambda: 0,
        lambda: -1 + input_population(time() + 1) / input_population(time()),
    )


_ext_lookup_historic_population = ExtLookup(
    "../parameters.xlsx",
    "Austria",
    "time_historic_population",
    "historic_population",
    {},
    _root,
    "_ext_lookup_historic_population",
)


_ext_constant_initial_population = ExtConstant(
    "../parameters.xlsx",
    "Austria",
    "initial_population",
    {},
    _root,
    "_ext_constant_initial_population",
)


_ext_lookup_input_population = ExtLookup(
    "../parameters.xlsx",
    "Austria",
    "time_index_projection",
    "input_population",
    {},
    _root,
    "_ext_lookup_input_population",
)


_ext_constant_p_customized_cte_pop_variation = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "G14",
    {},
    _root,
    "_ext_constant_p_customized_cte_pop_variation",
)


_ext_constant_p_customized_year_pop_evolution = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "E14",
    {},
    _root,
    "_ext_constant_p_customized_year_pop_evolution",
)


_ext_constant_p_pop_asymptote_millions = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "G15",
    {},
    _root,
    "_ext_constant_p_pop_asymptote_millions",
)


_ext_data_p_timeseries_pop_growth_rate = ExtData(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "12",
    "E13",
    "interpolate",
    {},
    _root,
    "_ext_data_p_timeseries_pop_growth_rate",
)


_sample_if_true_pop_until_p_customized_year_pop_evolution = SampleIfTrue(
    lambda: time() < p_customized_year_pop_evolution(),
    lambda: population(),
    lambda: population(),
    "_sample_if_true_pop_until_p_customized_year_pop_evolution",
)


_delayfixed_pop_variation_delay_1_step = DelayFixed(
    lambda: pop_variation_by_scen(),
    lambda: 0.5,
    lambda: pop_variation_by_scen(),
    time_step,
    "_delayfixed_pop_variation_delay_1_step",
)


_delayfixed_pop_variation_delay_2_step = DelayFixed(
    lambda: pop_variation_by_scen(),
    lambda: 1,
    lambda: pop_variation_by_scen(),
    time_step,
    "_delayfixed_pop_variation_delay_2_step",
)


_delayfixed_pop_variation_delay_3_step = DelayFixed(
    lambda: pop_variation_by_scen(),
    lambda: 2,
    lambda: pop_variation_by_scen(),
    time_step,
    "_delayfixed_pop_variation_delay_3_step",
)


_delayfixed_pop_variation_delay_4_step = DelayFixed(
    lambda: pop_variation_by_scen(),
    lambda: 3,
    lambda: pop_variation_by_scen(),
    time_step,
    "_delayfixed_pop_variation_delay_4_step",
)


_delayfixed_pop_variation_delay_5_step = DelayFixed(
    lambda: pop_variation_by_scen(),
    lambda: 4,
    lambda: pop_variation_by_scen(),
    time_step,
    "_delayfixed_pop_variation_delay_5_step",
)


_delayfixed_pop_variation_delay_6_step = DelayFixed(
    lambda: pop_variation_by_scen(),
    lambda: 5,
    lambda: pop_variation_by_scen(),
    time_step,
    "_delayfixed_pop_variation_delay_6_step",
)


_integ_population = Integ(
    lambda: pop_variation(), lambda: initial_population(), "_integ_population"
)


_ext_constant_select_population_evolution_input = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "B11",
    {},
    _root,
    "_ext_constant_select_population_evolution_input",
)


_smooth_smooth_pop = Smooth(
    lambda: pop_variation_by_scen(),
    lambda: 4,
    lambda: pop_variation_by_scen(),
    lambda: 2,
    "_smooth_smooth_pop",
)


_ext_constant_target_year_pop_asymptote = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "I15",
    {},
    _root,
    "_ext_constant_target_year_pop_asymptote",
)
