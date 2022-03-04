"""
Module population
Translated using PySD version 2.2.1
"""


def annual_population_growth_rate():
    """
    Real Name: Annual population growth rate
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


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
    Original Eqn:
    Units: people
    Limits: (None, None)
    Type: Lookup
    Subs: []

    Historic population (1995-2015). Ref: World bank.
    """
    return _ext_lookup_historic_population(x)


_ext_lookup_historic_population = ExtLookup(
    "../parameters.xlsx",
    "Europe",
    "time_historic_population",
    "historic_population",
    {},
    _root,
    "_ext_lookup_historic_population",
)


def initial_population():
    """
    Real Name: initial population
    Original Eqn:
    Units: people
    Limits: (None, None)
    Type: Constant
    Subs: []

    Initial value from WorldBank in 1995.
    """
    return _ext_constant_initial_population()


_ext_constant_initial_population = ExtConstant(
    "../parameters.xlsx",
    "Europe",
    "initial_population",
    {},
    _root,
    "_ext_constant_initial_population",
)


def input_population(x):
    """
    Real Name: input population
    Original Eqn:
    Units: Mpeople
    Limits: (None, None)
    Type: Lookup
    Subs: []

    Original values from SSP2 evolution.
    """
    return _ext_lookup_input_population(x)


_ext_lookup_input_population = ExtLookup(
    "../parameters.xlsx",
    "Europe",
    "time_index_projection",
    "input_population",
    {},
    _root,
    "_ext_lookup_input_population",
)


def p_customized_cte_pop_variation():
    """
    Real Name: P customized cte pop variation
    Original Eqn:
    Units: Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    From customized year, set annual constant variation.
    """
    return _ext_constant_p_customized_cte_pop_variation()


_ext_constant_p_customized_cte_pop_variation = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "p_constant_pop_variation",
    {},
    _root,
    "_ext_constant_p_customized_cte_pop_variation",
)


def p_customized_year_pop_evolution():
    """
    Real Name: P customized year pop evolution
    Original Eqn:
    Units: 1/Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    From customized year, set annual constant variation.
    """
    return _ext_constant_p_customized_year_pop_evolution()


_ext_constant_p_customized_year_pop_evolution = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "year_customized_pop_evol",
    {},
    _root,
    "_ext_constant_p_customized_year_pop_evolution",
)


def p_pop_asymptote_millions():
    """
    Real Name: P pop asymptote millions
    Original Eqn:
    Units: Mpeople
    Limits: (None, None)
    Type: Constant
    Subs: []

    Policy target of population in target year to be approached smoothly-asymptotically.
    """
    return _ext_constant_p_pop_asymptote_millions()


_ext_constant_p_pop_asymptote_millions = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "p_pop_asymptote",
    {},
    _root,
    "_ext_constant_p_pop_asymptote_millions",
)


def p_timeseries_pop_growth_rate():
    """
    Real Name: P timeseries pop growth rate
    Original Eqn:
    Units: 1/Year
    Limits: (None, None)
    Type: Data
    Subs: []

    Annual population growth from timeseries. UN projections in their medium scenario (Medium fertility variant)
    """
    return _ext_data_p_timeseries_pop_growth_rate(time())


_ext_data_p_timeseries_pop_growth_rate = ExtData(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "year_pop_timeseries",
    "p_timeseries_pop_growth",
    "interpolate",
    {},
    _root,
    "_ext_data_p_timeseries_pop_growth_rate",
)


def pop_asymptote():
    """
    Real Name: pop asymptote
    Original Eqn:
    Units: people
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return p_pop_asymptote_millions() * 1000000.0 - 10000000.0


def pop_until_p_customized_year_pop_evolution():
    """
    Real Name: pop until P customized year pop evolution
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Population until starting customized year of the policy target.
    """
    return _sampleiftrue_pop_until_p_customized_year_pop_evolution()


_sampleiftrue_pop_until_p_customized_year_pop_evolution = SampleIfTrue(
    lambda: time() < p_customized_year_pop_evolution(),
    lambda: population(),
    lambda: population(),
    "_sampleiftrue_pop_until_p_customized_year_pop_evolution",
)


def pop_variation():
    """
    Real Name: pop variation
    Original Eqn:
    Units: people/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Population growth. (Historic data from 1990-2010; projection 2011-2100) 2011 UST$
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
    Original Eqn:
    Units: people/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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
    Original Eqn:
    Units: people/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Population variation depending on the policy target selected by the user.
    """
    return if_then_else(
        time() < 2014,
        lambda: variation_historic_pop(),
        lambda: if_then_else(
            np.logical_and(
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
    Original Eqn:
    Units: people/Year
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _delayfixed_pop_variation_delay_1_step()


_delayfixed_pop_variation_delay_1_step = DelayFixed(
    lambda: pop_variation_by_scen(),
    lambda: 0.5,
    lambda: pop_variation_by_scen(),
    time_step,
    "_delayfixed_pop_variation_delay_1_step",
)


def pop_variation_delay_2_step():
    """
    Real Name: pop variation delay 2 step
    Original Eqn:
    Units: people/Year
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _delayfixed_pop_variation_delay_2_step()


_delayfixed_pop_variation_delay_2_step = DelayFixed(
    lambda: pop_variation_by_scen(),
    lambda: 1,
    lambda: pop_variation_by_scen(),
    time_step,
    "_delayfixed_pop_variation_delay_2_step",
)


def pop_variation_delay_3_step():
    """
    Real Name: pop variation delay 3 step
    Original Eqn:
    Units: people/Year
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _delayfixed_pop_variation_delay_3_step()


_delayfixed_pop_variation_delay_3_step = DelayFixed(
    lambda: pop_variation_by_scen(),
    lambda: 2,
    lambda: pop_variation_by_scen(),
    time_step,
    "_delayfixed_pop_variation_delay_3_step",
)


def pop_variation_delay_4_step():
    """
    Real Name: pop variation delay 4 step
    Original Eqn:
    Units: people/Year
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _delayfixed_pop_variation_delay_4_step()


_delayfixed_pop_variation_delay_4_step = DelayFixed(
    lambda: pop_variation_by_scen(),
    lambda: 3,
    lambda: pop_variation_by_scen(),
    time_step,
    "_delayfixed_pop_variation_delay_4_step",
)


def pop_variation_delay_5_step():
    """
    Real Name: pop variation delay 5 step
    Original Eqn:
    Units: people/Year
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _delayfixed_pop_variation_delay_5_step()


_delayfixed_pop_variation_delay_5_step = DelayFixed(
    lambda: pop_variation_by_scen(),
    lambda: 4,
    lambda: pop_variation_by_scen(),
    time_step,
    "_delayfixed_pop_variation_delay_5_step",
)


def pop_variation_delay_6_step():
    """
    Real Name: pop variation delay 6 step
    Original Eqn:
    Units: people/Year
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _delayfixed_pop_variation_delay_6_step()


_delayfixed_pop_variation_delay_6_step = DelayFixed(
    lambda: pop_variation_by_scen(),
    lambda: 5,
    lambda: pop_variation_by_scen(),
    time_step,
    "_delayfixed_pop_variation_delay_6_step",
)


def population():
    """
    Real Name: Population
    Original Eqn:
    Units: people
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Population projection.
    """
    return _integ_population()


_integ_population = Integ(
    lambda: pop_variation(), lambda: initial_population(), "_integ_population"
)


def select_population_evolution_input():
    """
    Real Name: select Population evolution input
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    0. From SSPs 1. Timeseries 2. From cusotmized year, set annual constant variation
    """
    return _ext_constant_select_population_evolution_input()


_ext_constant_select_population_evolution_input = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "select_pop_evolution",
    {},
    _root,
    "_ext_constant_select_population_evolution_input",
)


def smooth_pop():
    """
    Real Name: smooth pop
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _smooth_smooth_pop()


_smooth_smooth_pop = Smooth(
    lambda: pop_variation_by_scen(),
    lambda: 4,
    lambda: pop_variation_by_scen(),
    lambda: 2,
    "_smooth_smooth_pop",
)


def smooth_probe():
    """
    Real Name: smooth probe
    Original Eqn:
    Units: people/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return if_then_else(
        time() < p_customized_year_pop_evolution(),
        lambda: pop_variation_by_scen(),
        lambda: smooth_pop(),
    )


def t_asymptote_pop():
    """
    Real Name: T asymptote pop
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (target_year_pop_asymptote() - p_customized_year_pop_evolution()) / 3


def target_year_pop_asymptote():
    """
    Real Name: Target year pop asymptote
    Original Eqn:
    Units: Year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Year when population target reaches around 95% of the target population (asymptote).
    """
    return _ext_constant_target_year_pop_asymptote()


_ext_constant_target_year_pop_asymptote = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "target_year_asymptote_pop",
    {},
    _root,
    "_ext_constant_target_year_pop_asymptote",
)


def variation_historic_pop():
    """
    Real Name: variation historic pop
    Original Eqn:
    Units: people/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return if_then_else(
        time() < 2010,
        lambda: 0,
        lambda: -1 + input_population(time() + 1) / input_population(time()),
    )
