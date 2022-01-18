"""
Module population
Translated using PySD version 2.2.0
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
    Original Eqn: ( GET DIRECT LOOKUPS('../parameters.xlsx', 'World', 'time_historic_population', 'historic_population'))
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
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'World', 'initial_population')
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
    Original Eqn: ( GET DIRECT LOOKUPS('../parameters.xlsx', 'World', 'time_index_projection', 'input_population'))
    Units: Mpeople
    Limits: (None, None)
    Type: lookup
    Subs: None

    Original values from SSP2 evolution.
    """
    return _ext_lookup_input_population(x)


def p_customized_cte_pop_variation():
    """
    Real Name: P customized cte pop variation
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'G12')
    Units: year
    Limits: (None, None)
    Type: constant
    Subs: None

    From customized year, set annual constant variation.
    """
    return _ext_constant_p_customized_cte_pop_variation()


def p_customized_year_pop_evolution():
    """
    Real Name: P customized year pop evolution
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'E12')
    Units: 1/year
    Limits: (None, None)
    Type: constant
    Subs: None

    From customized year, set annual constant variation.
    """
    return _ext_constant_p_customized_year_pop_evolution()


def p_timeseries_pop_growth_rate():
    """
    Real Name: P timeseries pop growth rate
    Original Eqn: GET DIRECT DATA('../../scenarios/scen_w.xlsx', 'BAU', '10', 'E11')
    Units: 1/year
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Annual population growth from timeseries. UN projections in their medium
        scenario (Medium fertility variant)
    """
    return _ext_data_p_timeseries_pop_growth_rate(time())


def pop_variation():
    """
    Real Name: pop variation
    Original Eqn: IF THEN ELSE(Time<2014, variation historic pop, Population*Annual population growth rate)
    Units: people/year
    Limits: (None, None)
    Type: component
    Subs: None

    Population growth. (Historic data from 1990-2010; projection 2011-2100)
        2011 UST$
    """
    return if_then_else(
        time() < 2014,
        lambda: variation_historic_pop(),
        lambda: population() * annual_population_growth_rate(),
    )


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
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'B9')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    0. From SSPs        1. Timeseries        2. From cusotmized year, set annual constant variation
    """
    return _ext_constant_select_population_evolution_input()


def variation_historic_pop():
    """
    Real Name: variation historic pop
    Original Eqn: IF THEN ELSE(Time<2014, historic population(Time+1)-historic population(Time), 0)
    Units: people/year
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
    "World",
    "time_historic_population",
    "historic_population",
    {},
    _root,
    "_ext_lookup_historic_population",
)


_ext_constant_initial_population = ExtConstant(
    "../parameters.xlsx",
    "World",
    "initial_population",
    {},
    _root,
    "_ext_constant_initial_population",
)


_ext_lookup_input_population = ExtLookup(
    "../parameters.xlsx",
    "World",
    "time_index_projection",
    "input_population",
    {},
    _root,
    "_ext_lookup_input_population",
)


_ext_constant_p_customized_cte_pop_variation = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "G12",
    {},
    _root,
    "_ext_constant_p_customized_cte_pop_variation",
)


_ext_constant_p_customized_year_pop_evolution = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "E12",
    {},
    _root,
    "_ext_constant_p_customized_year_pop_evolution",
)


_ext_data_p_timeseries_pop_growth_rate = ExtData(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "10",
    "E11",
    "interpolate",
    {},
    _root,
    "_ext_data_p_timeseries_pop_growth_rate",
)


_integ_population = Integ(
    lambda: pop_variation(), lambda: initial_population(), "_integ_population"
)


_ext_constant_select_population_evolution_input = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "B9",
    {},
    _root,
    "_ext_constant_select_population_evolution_input",
)
