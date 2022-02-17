"""
Module nuclear
Translated using PySD version 2.2.1
"""


def cp_limit_nuclear():
    """
    Real Name: Cp limit nuclear
    Original Eqn: IF THEN ELSE(Cp nuclear>min Cp nuclear, 1, 0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(cp_nuclear() > min_cp_nuclear(), lambda: 1, lambda: 0)


def cp_nuclear():
    """
    Real Name: Cp nuclear
    Original Eqn: Cp nuclear initial*Cp exogenous RES elec dispatch reduction
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Capacity factor of nuclear power centrals.
    """
    return cp_nuclear_initial() * cp_exogenous_res_elec_dispatch_reduction()


def cp_nuclear_initial():
    """
    Real Name: Cp nuclear initial
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'cp_initial_nuclear')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Capacity factor of nuclear taking historic data as reference: in 2011,
        there were 374 GW of nuclear capacity operating that generated 2,507 TWh.
    """
    return _ext_constant_cp_nuclear_initial()


def effects_shortage_uranium():
    """
    Real Name: effects shortage uranium
    Original Eqn: IF THEN ELSE((extraction uranium EJ EU+extraction uranium RoW)=0, 0, IF THEN ELSE(abundance uranium>0.8, ((abundance uranium-0.8)*5)^2, 0))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    The eventual scarcity of coal would likely constrain the development of
        CTL. The proposed relationship avoids an abrupt limitation by introducing
        a range (1;0.8) in the gas abundance that constrains the development of
        CTL.
    """
    return if_then_else(
        (extraction_uranium_ej_eu() + extraction_uranium_row()) == 0,
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
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'efficiency_uranium_for_electricity')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Efficiency of uranium in nuclear power centrals. [IEA Balances].
    """
    return _ext_constant_efficiency_uranium_for_electricity()


def historic_nuclear_generation_twh(x):
    """
    Real Name: Historic nuclear generation TWh
    Original Eqn: ( GET DIRECT LOOKUPS('../energy.xlsx', 'Europe', 'time_historic_data', 'historic_nuclear_generation'))
    Units: TWh/Year
    Limits: (None, None)
    Type: lookup
    Subs: None

    Historic data of annual production from nuclear energy in TWh.
    """
    return _ext_lookup_historic_nuclear_generation_twh(x)


def initial_capacity_in_construction_nuclear():
    """
    Real Name: initial capacity in construction nuclear
    Original Eqn: 0
    Units: TW
    Limits: (None, None)
    Type: constant
    Subs: None

    Initial capacity in construction of nuclear (year 1995).
    """
    return 0


def initial_capacity_installed_nuclear():
    """
    Real Name: initial capacity installed nuclear
    Original Eqn: initial gen nuclear*TWe per TWh/Cp nuclear initial
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None

    Initial capacity installed of nuclear power.
    """
    return initial_gen_nuclear() * twe_per_twh() / cp_nuclear_initial()


def initial_gen_nuclear():
    """
    Real Name: initial gen nuclear
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'initial_nuclear_generation')
    Units: TWh
    Limits: (None, None)
    Type: constant
    Subs: None

    Electric generation from nuclear in the initial year 1995.
    """
    return _ext_constant_initial_gen_nuclear()


def initial_required_capacity_nuclear():
    """
    Real Name: initial required capacity nuclear
    Original Eqn: 0
    Units: TW
    Limits: (None, None)
    Type: constant
    Subs: None

    Initial required capacity of nuclear (year 1995).
    """
    return 0


def installed_capacity_nuclear_tw():
    """
    Real Name: installed capacity nuclear TW
    Original Eqn: INTEG ( Nuclear capacity under construction-"nuclear capacity phase-out" -wear nuclear, initial capacity installed nuclear)
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None

    Annual installed capacity of nuclear power.
    """
    return _integ_installed_capacity_nuclear_tw()


def invest_cost_nuclear():
    """
    Real Name: invest cost nuclear
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Global', 'Time', 'invest_cost_nuclear')
    Units: Tdollars/TWe
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Investment cost of nuclear power considering that future reactors would
        require the same investment as the recent Hinkley Point C nuclear power
        station in UK of 8,000 US$/kW (5536.71 1995US$/kW).
    """
    return _ext_data_invest_cost_nuclear(time())


def invest_nuclear_tdolar():
    """
    Real Name: invest nuclear Tdolar
    Original Eqn: MAX(0, IF THEN ELSE(Nuclear capacity under construction<0,0,(Nuclear capacity under construction+replacement nuclear capacity)*invest cost nuclear/1000))
    Units: Tdollars/Year
    Limits: (None, None)
    Type: component
    Subs: None


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
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'lifetime_nuclear')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Lifetime of nuclear.
    """
    return _ext_constant_life_time_nuclear()


def min_cp_nuclear():
    """
    Real Name: min Cp nuclear
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Europe', 'minimum_cp_nuclear')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Assumption of minimum Cp for nuclear given the high inertia of nuclear
        reactors.
    """
    return _ext_constant_min_cp_nuclear()


def new_nuclear_capacity_under_planning():
    """
    Real Name: new nuclear capacity under planning
    Original Eqn: MAX(0,required capacity nuclear TW/time planification nuclear)
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None

    New nuclear capacity under planning.
    """
    return np.maximum(0, required_capacity_nuclear_tw() / time_planification_nuclear())


def new_required_capacity_nuclear():
    """
    Real Name: new required capacity nuclear
    Original Eqn: MAX(0, IF THEN ELSE(Time<2015, 0, IF THEN ELSE(Demand Elec NRE TWh=0, 0, installed capacity nuclear TW *P nuclear elec gen)))*effects shortage uranium*Cp limit nuclear
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None

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


def nuclear_capacity_phaseout():
    """
    Real Name: "nuclear capacity phase-out"
    Original Eqn: IF THEN ELSE(selection of nuclear scenario=4, IF THEN ELSE(Time<"start year nuclear growth scen3-4", 0, "P nuclear scen3-4"*installed capacity nuclear TW), 0)
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None

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
    Original Eqn: IF THEN ELSE(Time<2014, (Historic nuclear generation TWh(INTEGER(Time+1))-Historic nuclear generation TWh(INTEGER(Time))) *TWe per TWh/Cp nuclear, Planned nuclear capacity TW/time construction nuclear)
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None

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


def nuclear_overcapacity():
    """
    Real Name: nuclear overcapacity
    Original Eqn: IF THEN ELSE(potential generation nuclear elec TWh=0,0, (potential generation nuclear elec TWh-FE nuclear Elec generation TWh )/potential generation nuclear elec TWh)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Overcapacity of nuclear power taking into account the installed capacity
        and the real generation.
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
    Original Eqn: IF THEN ELSE(selection of nuclear scenario=1, 0, IF THEN ELSE(selection of nuclear scenario=2,0, IF THEN ELSE(selection of nuclear scenario=4,0, IF THEN ELSE(selection of nuclear scenario=3, IF THEN ELSE(Time<"start year nuclear growth scen3-4", 0, "P nuclear scen3-4"), 0))))
    Units: 1/Year
    Limits: (None, None)
    Type: component
    Subs: None

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


def p_nuclear_scen34():
    """
    Real Name: "P nuclear scen3-4"
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'p_nuclear_scen3_4_variation')
    Units: 1/Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual variation (growth or phase-out) of new nuclear power plants
        (scenarios 3 and 4 of nuclear evolution) from the year "start year nuclear
        growth scen3-4".
    """
    return _ext_constant_p_nuclear_scen34()


def pe_demand_uranium_eu_ej():
    """
    Real Name: PE demand uranium EU EJ
    Original Eqn: potential generation nuclear elec TWh*EJ per TWh/efficiency uranium for electricity
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

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
    Original Eqn: INTEG ( new nuclear capacity under planning+replacement nuclear capacity -Nuclear capacity under construction , initial capacity in construction nuclear)
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None

    Planned nuclear capacity.
    """
    return _integ_planned_nuclear_capacity_tw()


def potential_generation_nuclear_elec_twh():
    """
    Real Name: potential generation nuclear elec TWh
    Original Eqn: MIN(installed capacity nuclear TW*Cp nuclear/TWe per TWh, Demand Elec NRE TWh)
    Units: TWh/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Total potential generation of electricity from nuclear power plants given
        the installed capacity. A minimum function is introduced to assure that no
        more nuclear than electricity required (after the RES and oil
        contribution) is produced.
    """
    return np.minimum(
        installed_capacity_nuclear_tw() * cp_nuclear() / twe_per_twh(),
        demand_elec_nre_twh(),
    )


def replacement_nuclear_capacity():
    """
    Real Name: replacement nuclear capacity
    Original Eqn: IF THEN ELSE(Time<2014,Nuclear capacity under construction, IF THEN ELSE(selection of nuclear scenario=2, 0, IF THEN ELSE(selection of nuclear scenario=4, 0, replacement rate nuclear*wear nuclear*(1-nuclear overcapacity))))*Cp limit nuclear
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None

    It is assumed that the step of planning of replaced infraestructure can be
        done while the infraestructure to be replaced is still under operation.
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


def replacement_rate_nuclear():
    """
    Real Name: replacement rate nuclear
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'replacement_rate_nuclear')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    If =1, we asume that all the power that reaches the end of its lifetime is
        replaced.
    """
    return _ext_constant_replacement_rate_nuclear()


def required_capacity_nuclear_tw():
    """
    Real Name: required capacity nuclear TW
    Original Eqn: INTEG ( new required capacity nuclear-new nuclear capacity under planning , initial required capacity nuclear)
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None

    Required capacity of nuclear power plants.
    """
    return _integ_required_capacity_nuclear_tw()


def selection_of_nuclear_scenario():
    """
    Real Name: selection of nuclear scenario
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'select_nuclear_scen')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    If = 1: Constant power capacity at current levels,        If = 2: No more nuclear installed, current capacity depreciates,        If = 3: Growth of nuclear power.
    """
    return _ext_constant_selection_of_nuclear_scenario()


def start_year_nuclear_growth_scen34():
    """
    Real Name: "start year nuclear growth scen3-4"
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_eu.xlsx', 'BAU', 'start_year_nuclear_variation_scen3_4')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Start year of increase/phase-out of nuclear power plants (Nuclear
        scenarios 3 and 4).
    """
    return _ext_constant_start_year_nuclear_growth_scen34()


def time_construction_nuclear():
    """
    Real Name: time construction nuclear
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'construction_time_nuclear')
    Units: Time
    Limits: (None, None)
    Type: constant
    Subs: None

    Average construction time for nuclear power plants.
    """
    return _ext_constant_time_construction_nuclear()


def time_planification_nuclear():
    """
    Real Name: time planification nuclear
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'planning_time_nuclear')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Average planification time for nuclear power plants.
    """
    return _ext_constant_time_planification_nuclear()


def twe_per_twh():
    """
    Real Name: TWe per TWh
    Original Eqn: 0.000114155
    Units: TWe/(TWh/Year)
    Limits: (None, None)
    Type: constant
    Subs: None

    Unit conversion (1 TWe=8760 TWh per year)
    """
    return 0.000114155


def wear_nuclear():
    """
    Real Name: wear nuclear
    Original Eqn: IF THEN ELSE(Time<2014, 0, installed capacity nuclear TW/life time nuclear)
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None

    Depreciation of nuclear power plants.
    """
    return if_then_else(
        time() < 2014,
        lambda: 0,
        lambda: installed_capacity_nuclear_tw() / life_time_nuclear(),
    )


_ext_constant_cp_nuclear_initial = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "cp_initial_nuclear",
    {},
    _root,
    "_ext_constant_cp_nuclear_initial",
)


_ext_constant_efficiency_uranium_for_electricity = ExtConstant(
    "../energy.xlsx",
    "Global",
    "efficiency_uranium_for_electricity",
    {},
    _root,
    "_ext_constant_efficiency_uranium_for_electricity",
)


_ext_lookup_historic_nuclear_generation_twh = ExtLookup(
    "../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_nuclear_generation",
    {},
    _root,
    "_ext_lookup_historic_nuclear_generation_twh",
)


_ext_constant_initial_gen_nuclear = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "initial_nuclear_generation",
    {},
    _root,
    "_ext_constant_initial_gen_nuclear",
)


_integ_installed_capacity_nuclear_tw = Integ(
    lambda: nuclear_capacity_under_construction()
    - nuclear_capacity_phaseout()
    - wear_nuclear(),
    lambda: initial_capacity_installed_nuclear(),
    "_integ_installed_capacity_nuclear_tw",
)


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


_ext_constant_life_time_nuclear = ExtConstant(
    "../energy.xlsx",
    "Global",
    "lifetime_nuclear",
    {},
    _root,
    "_ext_constant_life_time_nuclear",
)


_ext_constant_min_cp_nuclear = ExtConstant(
    "../energy.xlsx",
    "Europe",
    "minimum_cp_nuclear",
    {},
    _root,
    "_ext_constant_min_cp_nuclear",
)


_ext_constant_p_nuclear_scen34 = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "p_nuclear_scen3_4_variation",
    {},
    _root,
    "_ext_constant_p_nuclear_scen34",
)


_integ_planned_nuclear_capacity_tw = Integ(
    lambda: new_nuclear_capacity_under_planning()
    + replacement_nuclear_capacity()
    - nuclear_capacity_under_construction(),
    lambda: initial_capacity_in_construction_nuclear(),
    "_integ_planned_nuclear_capacity_tw",
)


_ext_constant_replacement_rate_nuclear = ExtConstant(
    "../energy.xlsx",
    "Global",
    "replacement_rate_nuclear",
    {},
    _root,
    "_ext_constant_replacement_rate_nuclear",
)


_integ_required_capacity_nuclear_tw = Integ(
    lambda: new_required_capacity_nuclear() - new_nuclear_capacity_under_planning(),
    lambda: initial_required_capacity_nuclear(),
    "_integ_required_capacity_nuclear_tw",
)


_ext_constant_selection_of_nuclear_scenario = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "select_nuclear_scen",
    {},
    _root,
    "_ext_constant_selection_of_nuclear_scenario",
)


_ext_constant_start_year_nuclear_growth_scen34 = ExtConstant(
    "../../scenarios/scen_eu.xlsx",
    "BAU",
    "start_year_nuclear_variation_scen3_4",
    {},
    _root,
    "_ext_constant_start_year_nuclear_growth_scen34",
)


_ext_constant_time_construction_nuclear = ExtConstant(
    "../energy.xlsx",
    "Global",
    "construction_time_nuclear",
    {},
    _root,
    "_ext_constant_time_construction_nuclear",
)


_ext_constant_time_planification_nuclear = ExtConstant(
    "../energy.xlsx",
    "Global",
    "planning_time_nuclear",
    {},
    _root,
    "_ext_constant_time_planification_nuclear",
)
