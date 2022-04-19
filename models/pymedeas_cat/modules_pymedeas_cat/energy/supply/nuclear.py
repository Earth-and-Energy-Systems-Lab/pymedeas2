"""
Module nuclear
Translated using PySD version 3.0.0
"""


@component.add(
    name="Cp limit nuclear", units="Dmnl", comp_type="Auxiliary", comp_subtype="Normal"
)
def cp_limit_nuclear():
    return if_then_else(cp_nuclear() > min_cp_nuclear(), lambda: 1, lambda: 0)


@component.add(
    name="Cp nuclear", units="Dmnl", comp_type="Auxiliary", comp_subtype="Normal"
)
def cp_nuclear():
    """
    Capacity factor of nuclear power centrals.
    """
    return cp_nuclear_initial() * cp_exogenous_res_elec_dispatch_reduction()


@component.add(
    name="Cp nuclear initial",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def cp_nuclear_initial():
    """
    Capacity factor of nuclear taking historic data as reference: in 2011, there were 374 GW of nuclear capacity operating that generated 2,507 TWh.
    """
    return _ext_constant_cp_nuclear_initial()


_ext_constant_cp_nuclear_initial = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "cp_initial_nuclear",
    {},
    _root,
    {},
    "_ext_constant_cp_nuclear_initial",
)


@component.add(
    name="effects shortage uranium",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def effects_shortage_uranium():
    """
    The eventual scarcity of coal would likely constrain the development of CTL. The proposed relationship avoids an abrupt limitation by introducing a range (1;0.8) in the gas abundance that constrains the development of CTL.
    """
    return if_then_else(
        extraction_uranium_ej_aut() + extraction_uranium_row() == 0,
        lambda: 0,
        lambda: if_then_else(
            abundance_uranium() > 0.8,
            lambda: ((abundance_uranium() - 0.8) * 5) ** 2,
            lambda: 0,
        ),
    )


@component.add(
    name="efficiency uranium for electricity",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def efficiency_uranium_for_electricity():
    """
    Efficiency of uranium in nuclear power centrals. [IEA Balances].
    """
    return _ext_constant_efficiency_uranium_for_electricity()


_ext_constant_efficiency_uranium_for_electricity = ExtConstant(
    "../energy.xlsx",
    "Global",
    "efficiency_uranium_for_electricity",
    {},
    _root,
    {},
    "_ext_constant_efficiency_uranium_for_electricity",
)


@component.add(
    name="Historic nuclear generation TWh",
    units="TWh/Year",
    comp_type="Lookup",
    comp_subtype="External",
)
def historic_nuclear_generation_twh(x, final_subs=None):
    """
    Historic data of annual production from nuclear energy in TWh.
    """
    return _ext_lookup_historic_nuclear_generation_twh(x, final_subs)


_ext_lookup_historic_nuclear_generation_twh = ExtLookup(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_nuclear_generation",
    {},
    _root,
    {},
    "_ext_lookup_historic_nuclear_generation_twh",
)


@component.add(
    name="initial capacity in construction nuclear",
    units="TW",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_capacity_in_construction_nuclear():
    """
    Initial capacity in construction of nuclear (year 1995).
    """
    return 0


@component.add(
    name="initial capacity installed nuclear",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def initial_capacity_installed_nuclear():
    """
    Initial capacity installed of nuclear power.
    """
    return initial_gen_nuclear() * twe_per_twh() / cp_nuclear_initial()


@component.add(
    name="initial gen nuclear",
    units="TWh",
    comp_type="Constant",
    comp_subtype="External",
)
def initial_gen_nuclear():
    """
    Electric generation from nuclear in the initial year 1995.
    """
    return _ext_constant_initial_gen_nuclear()


_ext_constant_initial_gen_nuclear = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "initial_nuclear_generation",
    {},
    _root,
    {},
    "_ext_constant_initial_gen_nuclear",
)


@component.add(
    name="initial required capacity nuclear",
    units="TW",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_required_capacity_nuclear():
    """
    Initial required capacity of nuclear (year 1995).
    """
    return 0


@component.add(
    name="installed capacity nuclear TW",
    units="TW",
    comp_type="Stateful",
    comp_subtype="Integ",
)
def installed_capacity_nuclear_tw():
    """
    Annual installed capacity of nuclear power.
    """
    return _integ_installed_capacity_nuclear_tw()


_integ_installed_capacity_nuclear_tw = Integ(
    lambda: nuclear_capacity_under_construction()
    - nuclear_capacity_phaseout()
    - wear_nuclear(),
    lambda: initial_capacity_installed_nuclear(),
    "_integ_installed_capacity_nuclear_tw",
)


@component.add(
    name="invest cost nuclear",
    units="Tdollars/TWe",
    comp_type="Data",
    comp_subtype="External",
)
def invest_cost_nuclear():
    """
    Investment cost of nuclear power considering that future reactors would require the same investment as the recent Hinkley Point C nuclear power station in UK of 8,000 US$/kW (5536.71 1995US$/kW).
    """
    return _ext_data_invest_cost_nuclear(time())


_ext_data_invest_cost_nuclear = ExtData(
    "../energy.xlsx",
    "Global",
    "Time",
    "invest_cost_nuclear",
    None,
    {},
    _root,
    {},
    "_ext_data_invest_cost_nuclear",
)


@component.add(
    name="invest nuclear Tdolar",
    units="Tdollars/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def invest_nuclear_tdolar():
    return np.maximum(
        0,
        if_then_else(
            nuclear_capacity_under_construction() < 0,
            lambda: 0,
            lambda: (
                nuclear_capacity_under_construction() + replacement_nuclear_capacity()
            )
            * invest_cost_nuclear()
            / 1000,
        ),
    )


@component.add(
    name="life time nuclear",
    units="Year",
    comp_type="Constant",
    comp_subtype="External",
)
def life_time_nuclear():
    """
    Lifetime of nuclear.
    """
    return _ext_constant_life_time_nuclear()


_ext_constant_life_time_nuclear = ExtConstant(
    "../energy.xlsx",
    "Global",
    "lifetime_nuclear",
    {},
    _root,
    {},
    "_ext_constant_life_time_nuclear",
)


@component.add(
    name="min Cp nuclear", units="Dmnl", comp_type="Constant", comp_subtype="External"
)
def min_cp_nuclear():
    """
    Assumption of minimum Cp for nuclear given the high inertia of nuclear reactors.
    """
    return _ext_constant_min_cp_nuclear()


_ext_constant_min_cp_nuclear = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "minimum_cp_nuclear",
    {},
    _root,
    {},
    "_ext_constant_min_cp_nuclear",
)


@component.add(
    name="new nuclear capacity under planning",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def new_nuclear_capacity_under_planning():
    """
    New nuclear capacity under planning.
    """
    return np.maximum(0, required_capacity_nuclear_tw() / time_planification_nuclear())


@component.add(
    name="new required capacity nuclear",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def new_required_capacity_nuclear():
    """
    New required capacity of nuclear power plants.
    """
    return (
        np.maximum(
            0,
            if_then_else(
                time() < 2015,
                lambda: 0,
                lambda: if_then_else(
                    demand_elec_nre_twh() == 0,
                    lambda: 0,
                    lambda: installed_capacity_nuclear_tw() * p_nuclear_elec_gen(),
                ),
            ),
        )
        * effects_shortage_uranium()
        * cp_limit_nuclear()
    )


@component.add(
    name='"nuclear capacity phase-out"',
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def nuclear_capacity_phaseout():
    """
    Annual nuclear capacity phase-out (Scenario 4 for nuclear evolution).
    """
    return if_then_else(
        selection_of_nuclear_scenario() == 4,
        lambda: if_then_else(
            time() < start_year_nuclear_growth_scen34(),
            lambda: 0,
            lambda: p_nuclear_scen34() * installed_capacity_nuclear_tw(),
        ),
        lambda: 0,
    )


@component.add(
    name="Nuclear capacity under construction",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def nuclear_capacity_under_construction():
    """
    Nuclear capacity under construction.
    """
    return if_then_else(
        time() < 2014,
        lambda: (
            historic_nuclear_generation_twh(integer(time() + 1))
            - historic_nuclear_generation_twh(integer(time()))
        )
        * twe_per_twh()
        / cp_nuclear(),
        lambda: planned_nuclear_capacity_tw() / time_construction_nuclear(),
    )


@component.add(
    name="nuclear overcapacity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def nuclear_overcapacity():
    """
    Overcapacity of nuclear power taking into account the installed capacity and the real generation.
    """
    return if_then_else(
        potential_generation_nuclear_elec_twh() == 0,
        lambda: 0,
        lambda: (
            potential_generation_nuclear_elec_twh() - fe_nuclear_elec_generation_twh()
        )
        / potential_generation_nuclear_elec_twh(),
    )


@component.add(
    name="P nuclear elec gen",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def p_nuclear_elec_gen():
    """
    Annual increase of new planned nuclear capacity.
    """
    return if_then_else(
        selection_of_nuclear_scenario() == 1,
        lambda: 0,
        lambda: if_then_else(
            selection_of_nuclear_scenario() == 2,
            lambda: 0,
            lambda: if_then_else(
                selection_of_nuclear_scenario() == 4,
                lambda: 0,
                lambda: if_then_else(
                    selection_of_nuclear_scenario() == 3,
                    lambda: if_then_else(
                        time() < start_year_nuclear_growth_scen34(),
                        lambda: 0,
                        lambda: p_nuclear_scen34(),
                    ),
                    lambda: 0,
                ),
            ),
        ),
    )


@component.add(
    name='"P nuclear scen3-4"',
    units="1/Year",
    comp_type="Constant",
    comp_subtype="External",
)
def p_nuclear_scen34():
    """
    Annual variation (growth or phase-out) of new nuclear power plants (scenarios 3 and 4 of nuclear evolution) from the year "start year nuclear growth scen3-4".
    """
    return _ext_constant_p_nuclear_scen34()


_ext_constant_p_nuclear_scen34 = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "p_nuclear_scen3_4_variation",
    {},
    _root,
    {},
    "_ext_constant_p_nuclear_scen34",
)


@component.add(
    name="PE demand uranium AUT EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def pe_demand_uranium_aut_ej():
    """
    Primary energy demand of uranium for nuclear power generation.
    """
    return (
        potential_generation_nuclear_elec_twh()
        * ej_per_twh()
        / efficiency_uranium_for_electricity()
    )


@component.add(
    name="Planned nuclear capacity TW",
    units="TW",
    comp_type="Stateful",
    comp_subtype="Integ",
)
def planned_nuclear_capacity_tw():
    """
    Planned nuclear capacity.
    """
    return _integ_planned_nuclear_capacity_tw()


_integ_planned_nuclear_capacity_tw = Integ(
    lambda: new_nuclear_capacity_under_planning()
    + replacement_nuclear_capacity()
    - nuclear_capacity_under_construction(),
    lambda: initial_capacity_in_construction_nuclear(),
    "_integ_planned_nuclear_capacity_tw",
)


@component.add(
    name="potential generation nuclear elec TWh",
    units="TWh/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def potential_generation_nuclear_elec_twh():
    """
    Total potential generation of electricity from nuclear power plants given the installed capacity. A minimum function is introduced to assure that no more nuclear than electricity required (after the RES and oil contribution) is produced.
    """
    return np.minimum(
        installed_capacity_nuclear_tw() * cp_nuclear() / twe_per_twh(),
        demand_elec_nre_twh(),
    )


@component.add(
    name="replacement nuclear capacity",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def replacement_nuclear_capacity():
    """
    It is assumed that the step of planning of replaced infraestructure can be done while the infraestructure to be replaced is still under operation.
    """
    return (
        if_then_else(
            time() < 2014,
            lambda: nuclear_capacity_under_construction(),
            lambda: if_then_else(
                selection_of_nuclear_scenario() == 2,
                lambda: 0,
                lambda: if_then_else(
                    selection_of_nuclear_scenario() == 4,
                    lambda: 0,
                    lambda: replacement_rate_nuclear()
                    * wear_nuclear()
                    * (1 - nuclear_overcapacity()),
                ),
            ),
        )
        * cp_limit_nuclear()
    )


@component.add(
    name="replacement rate nuclear",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def replacement_rate_nuclear():
    """
    If =1, we asume that all the power that reaches the end of its lifetime is replaced.
    """
    return _ext_constant_replacement_rate_nuclear()


_ext_constant_replacement_rate_nuclear = ExtConstant(
    "../energy.xlsx",
    "Global",
    "replacement_rate_nuclear",
    {},
    _root,
    {},
    "_ext_constant_replacement_rate_nuclear",
)


@component.add(
    name="required capacity nuclear TW",
    units="TW",
    comp_type="Stateful",
    comp_subtype="Integ",
)
def required_capacity_nuclear_tw():
    """
    Required capacity of nuclear power plants.
    """
    return _integ_required_capacity_nuclear_tw()


_integ_required_capacity_nuclear_tw = Integ(
    lambda: new_required_capacity_nuclear() - new_nuclear_capacity_under_planning(),
    lambda: initial_required_capacity_nuclear(),
    "_integ_required_capacity_nuclear_tw",
)


@component.add(
    name="selection of nuclear scenario",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def selection_of_nuclear_scenario():
    """
    If = 1: Constant power capacity at current levels, If = 2: No more nuclear installed, current capacity depreciates, If = 3: Growth of nuclear power.
    """
    return _ext_constant_selection_of_nuclear_scenario()


_ext_constant_selection_of_nuclear_scenario = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "select_nuclear_scen",
    {},
    _root,
    {},
    "_ext_constant_selection_of_nuclear_scenario",
)


@component.add(
    name='"start year nuclear growth scen3-4"',
    units="Year",
    comp_type="Constant",
    comp_subtype="External",
)
def start_year_nuclear_growth_scen34():
    """
    Start year of increase/phase-out of nuclear power plants (Nuclear scenarios 3 and 4).
    """
    return _ext_constant_start_year_nuclear_growth_scen34()


_ext_constant_start_year_nuclear_growth_scen34 = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "start_year_nuclear_variation_scen3_4",
    {},
    _root,
    {},
    "_ext_constant_start_year_nuclear_growth_scen34",
)


@component.add(
    name="time construction nuclear",
    units="Time",
    comp_type="Constant",
    comp_subtype="External",
)
def time_construction_nuclear():
    """
    Average construction time for nuclear power plants.
    """
    return _ext_constant_time_construction_nuclear()


_ext_constant_time_construction_nuclear = ExtConstant(
    "../energy.xlsx",
    "Global",
    "construction_time_nuclear",
    {},
    _root,
    {},
    "_ext_constant_time_construction_nuclear",
)


@component.add(
    name="time planification nuclear",
    units="Year",
    comp_type="Constant",
    comp_subtype="External",
)
def time_planification_nuclear():
    """
    Average planification time for nuclear power plants.
    """
    return _ext_constant_time_planification_nuclear()


_ext_constant_time_planification_nuclear = ExtConstant(
    "../energy.xlsx",
    "Global",
    "planning_time_nuclear",
    {},
    _root,
    {},
    "_ext_constant_time_planification_nuclear",
)


@component.add(
    name="TWe per TWh",
    units="TWe/(TWh/Year)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def twe_per_twh():
    """
    Unit conversion (1 TWe=8760 TWh per year)
    """
    return 0.000114155


@component.add(
    name="wear nuclear", units="TW", comp_type="Auxiliary", comp_subtype="Normal"
)
def wear_nuclear():
    """
    Depreciation of nuclear power plants.
    """
    return if_then_else(
        time() < 2014,
        lambda: 0,
        lambda: installed_capacity_nuclear_tw() / life_time_nuclear(),
    )
