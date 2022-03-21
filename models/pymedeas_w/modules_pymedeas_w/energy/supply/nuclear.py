"""
Module nuclear
Translated using PySD version 2.2.3
"""


def cp_limit_nuclear():
    """
    Real Name: Cp limit nuclear
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return if_then_else(cp_nuclear() > min_cp_nuclear(), lambda: 1, lambda: 0)


def cp_nuclear():
    """
    Real Name: Cp nuclear
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Capacity factor of nuclear power centrals.
    """
    return cp_nuclear_initial() * cp_exogenous_res_elec_dispatch_reduction()


def cp_nuclear_initial():
    """
    Real Name: Cp nuclear initial
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Capacity factor of nuclear taking historic data as reference: in 2011, there were 374 GW of nuclear capacity operating that generated 2,507 TWh.
    """
    return _ext_constant_cp_nuclear_initial()


_ext_constant_cp_nuclear_initial = ExtConstant(
    "../energy.xlsx",
    "World",
    "cp_initial_nuclear",
    {},
    _root,
    "_ext_constant_cp_nuclear_initial",
)


def effects_shortage_uranium():
    """
    Real Name: effects shortage uranium
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    The eventual scarcity of coal would likely constrain the development of new nuclear facilities. The proposed relationship avoids an abrupt limitation by introducing a range (1;0.8) in the uranium abundance that constrains the intallation of new nuclear capacity.
    """
    return if_then_else(
        extraction_uranium_ej() == 0,
        lambda: 0,
        lambda: if_then_else(
            abundance_uranium() > 0.8,
            lambda: ((abundance_uranium() - 0.8) * 5) ** 2,
            lambda: 0,
        ),
    )


def efficiency_uranium_for_electricity():
    """
    Real Name: efficiency uranium for electricity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Efficiency of uranium in nuclear power centrals. [IEA Balances].
    """
    return _ext_constant_efficiency_uranium_for_electricity()


_ext_constant_efficiency_uranium_for_electricity = ExtConstant(
    "../energy.xlsx",
    "Global",
    "efficiency_uranium_for_electricity",
    {},
    _root,
    "_ext_constant_efficiency_uranium_for_electricity",
)


def historic_nuclear_generation_twh(x):
    """
    Real Name: Historic nuclear generation TWh
    Original Eqn:
    Units: TWh/year
    Limits: (None, None)
    Type: Lookup
    Subs: []

    Historic data of annual production from nuclear energy in TWh.
    """
    return _ext_lookup_historic_nuclear_generation_twh(x)


_ext_lookup_historic_nuclear_generation_twh = ExtLookup(
    "../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_nuclear_generation",
    {},
    _root,
    "_ext_lookup_historic_nuclear_generation_twh",
)


def initial_capacity_in_construction_nuclear():
    """
    Real Name: initial capacity in construction nuclear
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Constant
    Subs: []

    Initial capacity in construction of nuclear (year 1995).
    """
    return 0


def initial_capacity_installed_nuclear():
    """
    Real Name: initial capacity installed nuclear
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Initial capacity installed of nuclear power.
    """
    return initial_gen_nuclear() * twe_per_twh() / cp_nuclear_initial()


def initial_gen_nuclear():
    """
    Real Name: initial gen nuclear
    Original Eqn:
    Units: TWh
    Limits: (None, None)
    Type: Constant
    Subs: []

    Electric generation from nuclear in the initial year 1995.
    """
    return _ext_constant_initial_gen_nuclear()


_ext_constant_initial_gen_nuclear = ExtConstant(
    "../energy.xlsx",
    "World",
    "initial_nuclear_generation",
    {},
    _root,
    "_ext_constant_initial_gen_nuclear",
)


def initial_required_capacity_nuclear():
    """
    Real Name: initial required capacity nuclear
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Constant
    Subs: []

    Initial required capacity of nuclear (year 1995).
    """
    return 0


def installed_capacity_nuclear_tw():
    """
    Real Name: installed capacity nuclear TW
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Stateful
    Subs: []

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


def invest_cost_nuclear():
    """
    Real Name: invest cost nuclear
    Original Eqn:
    Units: Tdollars/TWe
    Limits: (None, None)
    Type: Data
    Subs: []

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
    "_ext_data_invest_cost_nuclear",
)


def invest_nuclear_tdolar():
    """
    Real Name: invest nuclear Tdolar
    Original Eqn:
    Units: Tdollars/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
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


def life_time_nuclear():
    """
    Real Name: life time nuclear
    Original Eqn:
    Units: year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Lifetime of nuclear.
    """
    return _ext_constant_life_time_nuclear()


_ext_constant_life_time_nuclear = ExtConstant(
    "../energy.xlsx",
    "Global",
    "lifetime_nuclear",
    {},
    _root,
    "_ext_constant_life_time_nuclear",
)


def min_cp_nuclear():
    """
    Real Name: min Cp nuclear
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Assumption of minimum Cp for nuclear given the high inertia of nuclear reactors.
    """
    return _ext_constant_min_cp_nuclear()


_ext_constant_min_cp_nuclear = ExtConstant(
    "../energy.xlsx",
    "World",
    "minimum_cp_nuclear",
    {},
    _root,
    "_ext_constant_min_cp_nuclear",
)


def new_nuclear_capacity_under_planning():
    """
    Real Name: new nuclear capacity under planning
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    New nuclear capacity under planning.
    """
    return np.maximum(0, required_capacity_nuclear_tw() / time_planification_nuclear())


def new_required_capacity_nuclear():
    """
    Real Name: new required capacity nuclear
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    New required capacity of nuclear power plants.
    """
    return (
        np.maximum(
            0,
            if_then_else(
                np.logical_or(time() < 2014, demand_elec_nre_twh() == 0),
                lambda: 0,
                lambda: installed_capacity_nuclear_tw() * p_nuclear_elec_gen(),
            ),
        )
        * effects_shortage_uranium()
        * cp_limit_nuclear()
    )


def nuclear_capacity_phaseout():
    """
    Real Name: "nuclear capacity phase-out"
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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


def nuclear_capacity_under_construction():
    """
    Real Name: Nuclear capacity under construction
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Nuclear capacity under construction.
    """
    return if_then_else(
        time() < 2013,
        lambda: (
            historic_nuclear_generation_twh(time() + 1)
            - historic_nuclear_generation_twh(time())
        )
        * twe_per_twh()
        / cp_nuclear(),
        lambda: planned_nuclear_capacity_tw() / time_construction_nuclear(),
    )


def nuclear_overcapacity():
    """
    Real Name: nuclear overcapacity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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


def p_nuclear_elec_gen():
    """
    Real Name: P nuclear elec gen
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Annual increase of new planned nuclear capacity.
    """
    return if_then_else(
        np.logical_or(
            selection_of_nuclear_scenario() == 1,
            np.logical_or(
                selection_of_nuclear_scenario() == 2,
                selection_of_nuclear_scenario() == 4,
            ),
        ),
        lambda: 0,
        lambda: if_then_else(
            time() < start_year_nuclear_growth_scen34(),
            lambda: 0,
            lambda: p_nuclear_scen34(),
        ),
    )


def p_nuclear_scen34():
    """
    Real Name: "P nuclear scen3-4"
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Annual variation (growth or phase-out) of new nuclear power plants (scenarios 3 and 4 of nuclear evolution) from the year "start year nuclear growth scen3-4".
    """
    return _ext_constant_p_nuclear_scen34()


_ext_constant_p_nuclear_scen34 = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "p_nuclear_variation_scen_3_4",
    {},
    _root,
    "_ext_constant_p_nuclear_scen34",
)


def pe_demand_uranium():
    """
    Real Name: PE demand uranium
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy demand of uranium for nuclear power generation.
    """
    return (
        potential_generation_nuclear_elec_twh()
        * ej_per_twh()
        / efficiency_uranium_for_electricity()
    )


def planned_nuclear_capacity_tw():
    """
    Real Name: Planned nuclear capacity TW
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Stateful
    Subs: []

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


def potential_generation_nuclear_elec_twh():
    """
    Real Name: potential generation nuclear elec TWh
    Original Eqn:
    Units: TWh/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total potential generation of electricity from nuclear power plants given the installed capacity. A minimum function is introduced to assure that no more nuclear than electricity required (after the RES and oil contribution) is produced.
    """
    return np.minimum(
        installed_capacity_nuclear_tw() * cp_nuclear() / twe_per_twh(),
        demand_elec_nre_twh(),
    )


def replacement_nuclear_capacity():
    """
    Real Name: replacement nuclear capacity
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    It is assumed that the step of planning of replaced infraestructure can be done while the infraestructure to be replaced is still under operation.
    """
    return (
        if_then_else(
            time() < 2013,
            lambda: nuclear_capacity_under_construction(),
            lambda: if_then_else(
                np.logical_or(
                    selection_of_nuclear_scenario() == 2,
                    selection_of_nuclear_scenario() == 4,
                ),
                lambda: 0,
                lambda: replacement_rate_nuclear()
                * wear_nuclear()
                * (1 - nuclear_overcapacity()),
            ),
        )
        * cp_limit_nuclear()
    )


def replacement_rate_nuclear():
    """
    Real Name: replacement rate nuclear
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    If =1, we asume that all the power that reaches the end of its lifetime is replaced.
    """
    return _ext_constant_replacement_rate_nuclear()


_ext_constant_replacement_rate_nuclear = ExtConstant(
    "../energy.xlsx",
    "Global",
    "replacement_rate_nuclear",
    {},
    _root,
    "_ext_constant_replacement_rate_nuclear",
)


def required_capacity_nuclear_tw():
    """
    Real Name: required capacity nuclear TW
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Required capacity of nuclear power plants.
    """
    return _integ_required_capacity_nuclear_tw()


_integ_required_capacity_nuclear_tw = Integ(
    lambda: new_required_capacity_nuclear() - new_nuclear_capacity_under_planning(),
    lambda: initial_required_capacity_nuclear(),
    "_integ_required_capacity_nuclear_tw",
)


def selection_of_nuclear_scenario():
    """
    Real Name: selection of nuclear scenario
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    If = 1: Constant power capacity at current levels, If = 2: No more nuclear installed, current capacity depreciates, If = 3: Growth of nuclear power.
    """
    return _ext_constant_selection_of_nuclear_scenario()


_ext_constant_selection_of_nuclear_scenario = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "nuclear_scenario_select",
    {},
    _root,
    "_ext_constant_selection_of_nuclear_scenario",
)


def start_year_nuclear_growth_scen34():
    """
    Real Name: "start year nuclear growth scen3-4"
    Original Eqn:
    Units: year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Start year of increase/phase-out of nuclear power plants (Nuclear scenarios 3 and 4).
    """
    return _ext_constant_start_year_nuclear_growth_scen34()


_ext_constant_start_year_nuclear_growth_scen34 = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "start_year_nuclear_variation_scen3_4",
    {},
    _root,
    "_ext_constant_start_year_nuclear_growth_scen34",
)


def time_construction_nuclear():
    """
    Real Name: time construction nuclear
    Original Eqn:
    Units: Time
    Limits: (None, None)
    Type: Constant
    Subs: []

    Average construction time for nuclear power plants.
    """
    return _ext_constant_time_construction_nuclear()


_ext_constant_time_construction_nuclear = ExtConstant(
    "../energy.xlsx",
    "Global",
    "construction_time_nuclear",
    {},
    _root,
    "_ext_constant_time_construction_nuclear",
)


def time_planification_nuclear():
    """
    Real Name: time planification nuclear
    Original Eqn:
    Units: year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Average planification time for nuclear power plants.
    """
    return _ext_constant_time_planification_nuclear()


_ext_constant_time_planification_nuclear = ExtConstant(
    "../energy.xlsx",
    "Global",
    "planning_time_nuclear",
    {},
    _root,
    "_ext_constant_time_planification_nuclear",
)


def twe_per_twh():
    """
    Real Name: TWe per TWh
    Original Eqn:
    Units: TWe/(TWh/year)
    Limits: (None, None)
    Type: Constant
    Subs: []

    Unit conversion (1 TWe=8760 TWh per year)
    """
    return 0.000114155


def wear_nuclear():
    """
    Real Name: wear nuclear
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Depreciation of nuclear power plants.
    """
    return if_then_else(
        time() < 2012,
        lambda: 0,
        lambda: installed_capacity_nuclear_tw() / life_time_nuclear(),
    )
