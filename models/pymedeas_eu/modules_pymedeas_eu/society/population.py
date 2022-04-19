"""
Module population
Translated using PySD version 3.0.0
"""


@component.add(
    name="Annual population growth rate",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
)
def historic_population(x, final_subs=None):
    """
    Historic population (1995-2015). Ref: World bank.
    """
    return _ext_lookup_historic_population(x, final_subs)


_ext_lookup_historic_population = ExtLookup(
    "../parameters.xlsx",
    "Europe",
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
)
def initial_population():
    """
    Initial value from WorldBank in 1995.
    """
    return _ext_constant_initial_population()


_ext_constant_initial_population = ExtConstant(
    "../parameters.xlsx",
    "Europe",
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
)
def input_population(x, final_subs=None):
    """
    Original values from SSP2 evolution.
    """
    return _ext_lookup_input_population(x, final_subs)


_ext_lookup_input_population = ExtLookup(
    "../parameters.xlsx",
    "Europe",
    "time_index_projection",
    "input_population",
    {},
    _root,
    {},
    "_ext_lookup_input_population",
)


@component.add(
    name="P customized cte pop variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="External",
)
def p_customized_cte_pop_variation():
    """
    From customized year, set annual constant variation.
    """
    return _ext_constant_p_customized_cte_pop_variation()


_ext_constant_p_customized_cte_pop_variation = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "p_constant_pop_variation",
    {},
    _root,
    {},
    "_ext_constant_p_customized_cte_pop_variation",
)


@component.add(
    name="P customized year pop evolution",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="External",
)
def p_customized_year_pop_evolution():
    """
    From customized year, set annual constant variation.
    """
    return _ext_constant_p_customized_year_pop_evolution()


_ext_constant_p_customized_year_pop_evolution = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "year_customized_pop_evol",
    {},
    _root,
    {},
    "_ext_constant_p_customized_year_pop_evolution",
)


@component.add(
    name="P pop asymptote millions",
    units="Mpeople",
    comp_type="Constant",
    comp_subtype="External",
)
def p_pop_asymptote_millions():
    """
    Policy target of population in target year to be approached smoothly-asymptotically.
    """
    return _ext_constant_p_pop_asymptote_millions()


_ext_constant_p_pop_asymptote_millions = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "p_pop_asymptote",
    {},
    _root,
    {},
    "_ext_constant_p_pop_asymptote_millions",
)


@component.add(
    name="P timeseries pop growth rate",
    units="1/Year",
    comp_type="Data",
    comp_subtype="External",
)
def p_timeseries_pop_growth_rate():
    """
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
    {},
    "_ext_data_p_timeseries_pop_growth_rate",
)


@component.add(
    name="pop asymptote", units="people", comp_type="Auxiliary", comp_subtype="Normal"
)
def pop_asymptote():
    return p_pop_asymptote_millions() * 1000000.0 - 10000000.0


@component.add(
    name="pop until P customized year pop evolution",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
)
def pop_until_p_customized_year_pop_evolution():
    """
    Population until starting customized year of the policy target.
    """
    return _sampleiftrue_pop_until_p_customized_year_pop_evolution()


_sampleiftrue_pop_until_p_customized_year_pop_evolution = SampleIfTrue(
    lambda: time() < p_customized_year_pop_evolution(),
    lambda: population(),
    lambda: population(),
    "_sampleiftrue_pop_until_p_customized_year_pop_evolution",
)


@component.add(
    name="pop variation",
    units="people/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def pop_variation():
    """
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


@component.add(
    name="pop variation asymptote scen",
    units="people/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def pop_variation_asymptote_scen():
    """
    Population variation to reach asymptote target.
    """
    return (
        (pop_until_p_customized_year_pop_evolution() - pop_asymptote())
        * (-1 / t_asymptote_pop())
        * np.exp(-(time() - p_customized_year_pop_evolution()) / t_asymptote_pop())
    )


@component.add(
    name="pop variation by scen",
    units="people/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def pop_variation_by_scen():
    """
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


@component.add(
    name="pop variation delay 1 step",
    units="people/Year",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
)
def pop_variation_delay_1_step():
    return _delayfixed_pop_variation_delay_1_step()


_delayfixed_pop_variation_delay_1_step = DelayFixed(
    lambda: pop_variation_by_scen(),
    lambda: 0.5,
    lambda: pop_variation_by_scen(),
    time_step,
    "_delayfixed_pop_variation_delay_1_step",
)


@component.add(
    name="pop variation delay 2 step",
    units="people/Year",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
)
def pop_variation_delay_2_step():
    return _delayfixed_pop_variation_delay_2_step()


_delayfixed_pop_variation_delay_2_step = DelayFixed(
    lambda: pop_variation_by_scen(),
    lambda: 1,
    lambda: pop_variation_by_scen(),
    time_step,
    "_delayfixed_pop_variation_delay_2_step",
)


@component.add(
    name="pop variation delay 3 step",
    units="people/Year",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
)
def pop_variation_delay_3_step():
    return _delayfixed_pop_variation_delay_3_step()


_delayfixed_pop_variation_delay_3_step = DelayFixed(
    lambda: pop_variation_by_scen(),
    lambda: 2,
    lambda: pop_variation_by_scen(),
    time_step,
    "_delayfixed_pop_variation_delay_3_step",
)


@component.add(
    name="pop variation delay 4 step",
    units="people/Year",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
)
def pop_variation_delay_4_step():
    return _delayfixed_pop_variation_delay_4_step()


_delayfixed_pop_variation_delay_4_step = DelayFixed(
    lambda: pop_variation_by_scen(),
    lambda: 3,
    lambda: pop_variation_by_scen(),
    time_step,
    "_delayfixed_pop_variation_delay_4_step",
)


@component.add(
    name="pop variation delay 5 step",
    units="people/Year",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
)
def pop_variation_delay_5_step():
    return _delayfixed_pop_variation_delay_5_step()


_delayfixed_pop_variation_delay_5_step = DelayFixed(
    lambda: pop_variation_by_scen(),
    lambda: 4,
    lambda: pop_variation_by_scen(),
    time_step,
    "_delayfixed_pop_variation_delay_5_step",
)


@component.add(
    name="pop variation delay 6 step",
    units="people/Year",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
)
def pop_variation_delay_6_step():
    return _delayfixed_pop_variation_delay_6_step()


_delayfixed_pop_variation_delay_6_step = DelayFixed(
    lambda: pop_variation_by_scen(),
    lambda: 5,
    lambda: pop_variation_by_scen(),
    time_step,
    "_delayfixed_pop_variation_delay_6_step",
)


@component.add(
    name="Population", units="people", comp_type="Stateful", comp_subtype="Integ"
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
)
def select_population_evolution_input():
    """
    0. From SSPs 1. Timeseries 2. From cusotmized year, set annual constant variation
    """
    return _ext_constant_select_population_evolution_input()


_ext_constant_select_population_evolution_input = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "select_pop_evolution",
    {},
    _root,
    {},
    "_ext_constant_select_population_evolution_input",
)


@component.add(name="smooth pop", comp_type="Stateful", comp_subtype="Smooth")
def smooth_pop():
    return _smooth_smooth_pop()


_smooth_smooth_pop = Smooth(
    lambda: pop_variation_by_scen(),
    lambda: 4,
    lambda: pop_variation_by_scen(),
    lambda: 2,
    "_smooth_smooth_pop",
)


@component.add(
    name="smooth probe",
    units="people/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def smooth_probe():
    return if_then_else(
        time() < p_customized_year_pop_evolution(),
        lambda: pop_variation_by_scen(),
        lambda: smooth_pop(),
    )


@component.add(name="T asymptote pop", comp_type="Auxiliary", comp_subtype="Normal")
def t_asymptote_pop():
    return (target_year_pop_asymptote() - p_customized_year_pop_evolution()) / 3


@component.add(
    name="Target year pop asymptote",
    units="Year",
    comp_type="Constant",
    comp_subtype="External",
)
def target_year_pop_asymptote():
    """
    Year when population target reaches around 95% of the target population (asymptote).
    """
    return _ext_constant_target_year_pop_asymptote()


_ext_constant_target_year_pop_asymptote = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "target_year_asymptote_pop",
    {},
    _root,
    {},
    "_ext_constant_target_year_pop_asymptote",
)


@component.add(
    name="variation historic pop",
    units="people/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
)
def variation_input_pop():
    return if_then_else(
        time() < 2010,
        lambda: 0,
        lambda: -1 + input_population(time() + 1) / input_population(time()),
    )
