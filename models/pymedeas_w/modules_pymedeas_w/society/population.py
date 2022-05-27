"""
Module population
Translated using PySD version 3.0.1
"""


@component.add(
    name="Annual population growth rate",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "select_population_evolution_input": 2,
        "variation_input_pop": 1,
        "p_customized_cte_pop_variation": 1,
        "time": 1,
        "p_customized_year_pop_evolution": 1,
        "p_timeseries_pop_growth_rate": 2,
    },
)
def annual_population_growth_rate():
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


@component.add(
    name="historic population",
    units="people",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_population",
        "__lookup__": "_ext_lookup_historic_population",
    },
)
def historic_population(x, final_subs=None):
    """
    Historic population (1995-2015). Ref: World bank.
    """
    return _ext_lookup_historic_population(x, final_subs)


_ext_lookup_historic_population = ExtLookup(
    "../parameters.xlsx",
    "World",
    "time_historic_population",
    "historic_population",
    {},
    _root,
    {},
    "_ext_lookup_historic_population",
)


@component.add(
    name="initial population",
    units="people",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_population"},
)
def initial_population():
    """
    Initial value from WorldBank in 1995.
    """
    return _ext_constant_initial_population()


_ext_constant_initial_population = ExtConstant(
    "../parameters.xlsx",
    "World",
    "initial_population",
    {},
    _root,
    {},
    "_ext_constant_initial_population",
)


@component.add(
    name="input population",
    units="Mpeople",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_input_population",
        "__lookup__": "_ext_lookup_input_population",
    },
)
def input_population(x, final_subs=None):
    """
    Original values from SSP2 evolution.
    """
    return _ext_lookup_input_population(x, final_subs)


_ext_lookup_input_population = ExtLookup(
    "../parameters.xlsx",
    "World",
    "time_index_projection",
    "input_population",
    {},
    _root,
    {},
    "_ext_lookup_input_population",
)


@component.add(
    name="P customized cte pop variation",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_customized_cte_pop_variation"},
)
def p_customized_cte_pop_variation():
    """
    From customized year, set annual constant variation.
    """
    return _ext_constant_p_customized_cte_pop_variation()


_ext_constant_p_customized_cte_pop_variation = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "Constant_population_variation",
    {},
    _root,
    {},
    "_ext_constant_p_customized_cte_pop_variation",
)


@component.add(
    name="P customized year pop evolution",
    units="1/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_customized_year_pop_evolution"},
)
def p_customized_year_pop_evolution():
    """
    From customized year, set annual constant variation.
    """
    return _ext_constant_p_customized_year_pop_evolution()


_ext_constant_p_customized_year_pop_evolution = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "start_year_population_variation",
    {},
    _root,
    {},
    "_ext_constant_p_customized_year_pop_evolution",
)


@component.add(
    name="P timeseries pop growth rate",
    units="1/year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_p_timeseries_pop_growth_rate",
        "__data__": "_ext_data_p_timeseries_pop_growth_rate",
        "time": 1,
    },
)
def p_timeseries_pop_growth_rate():
    """
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
    {},
    "_ext_data_p_timeseries_pop_growth_rate",
)


@component.add(
    name="pop variation",
    units="people/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "variation_historic_pop": 1,
        "population": 1,
        "annual_population_growth_rate": 1,
    },
)
def pop_variation():
    """
    Population growth. (Historic data from 1990-2010; projection 2011-2100) 2011 UST$
    """
    return if_then_else(
        time() < 2014,
        lambda: variation_historic_pop(),
        lambda: population() * annual_population_growth_rate(),
    )


@component.add(
    name="Population",
    units="people",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_population": 1},
    other_deps={
        "_integ_population": {
            "initial": {"initial_population": 1},
            "step": {"pop_variation": 1},
        }
    },
)
def population():
    """
    Population projection.
    """
    return _integ_population()


_integ_population = Integ(
    lambda: pop_variation(), lambda: initial_population(), "_integ_population"
)


@component.add(
    name="select Population evolution input",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_select_population_evolution_input"},
)
def select_population_evolution_input():
    """
    0. From SSPs 1. Timeseries 2. From cusotmized year, set annual constant variation
    """
    return _ext_constant_select_population_evolution_input()


_ext_constant_select_population_evolution_input = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "pop_evolution_input",
    {},
    _root,
    {},
    "_ext_constant_select_population_evolution_input",
)


@component.add(
    name="variation historic pop",
    units="people/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 3, "historic_population": 2},
)
def variation_historic_pop():
    """
    Population historic variation.
    """
    return if_then_else(
        time() < 2014,
        lambda: historic_population(time() + 1) - historic_population(time()),
        lambda: 0,
    )


@component.add(
    name="variation input pop",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 3, "input_population": 2},
)
def variation_input_pop():
    return if_then_else(
        time() < 2010,
        lambda: 0,
        lambda: -1 + input_population(time() + 1) / input_population(time()),
    )
