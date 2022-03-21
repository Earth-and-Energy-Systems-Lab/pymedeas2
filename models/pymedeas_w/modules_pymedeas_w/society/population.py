"""
Module population
Translated using PySD version 2.2.3
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
    "World",
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
    "World",
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
    "World",
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
    Units: year
    Limits: (None, None)
    Type: Constant
    Subs: []

    From customized year, set annual constant variation.
    """
    return _ext_constant_p_customized_cte_pop_variation()


_ext_constant_p_customized_cte_pop_variation = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "Constant_population_variation",
    {},
    _root,
    "_ext_constant_p_customized_cte_pop_variation",
)


def p_customized_year_pop_evolution():
    """
    Real Name: P customized year pop evolution
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Constant
    Subs: []

    From customized year, set annual constant variation.
    """
    return _ext_constant_p_customized_year_pop_evolution()


_ext_constant_p_customized_year_pop_evolution = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "start_year_population_variation",
    {},
    _root,
    "_ext_constant_p_customized_year_pop_evolution",
)


def p_timeseries_pop_growth_rate():
    """
    Real Name: P timeseries pop growth rate
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Data
    Subs: []

    Annual population growth from timeseries. UN projections in their medium scenario (Medium fertility variant)
    """
    return _ext_data_p_timeseries_pop_growth_rate(time())


_ext_data_p_timeseries_pop_growth_rate = ExtData(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "years_pop_growth",
    "pop_growth_timeseries",
    "interpolate",
    {},
    _root,
    "_ext_data_p_timeseries_pop_growth_rate",
)


def pop_variation():
    """
    Real Name: pop variation
    Original Eqn:
    Units: people/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Population growth. (Historic data from 1990-2010; projection 2011-2100) 2011 UST$
    """
    return if_then_else(
        time() < 2014,
        lambda: variation_historic_pop(),
        lambda: population() * annual_population_growth_rate(),
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
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "pop_evolution_input",
    {},
    _root,
    "_ext_constant_select_population_evolution_input",
)


def variation_historic_pop():
    """
    Real Name: variation historic pop
    Original Eqn:
    Units: people/year
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
