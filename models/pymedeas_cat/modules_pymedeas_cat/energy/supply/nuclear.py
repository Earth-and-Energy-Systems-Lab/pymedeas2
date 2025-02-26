"""
Module energy.supply.nuclear
Translated using PySD version 3.14.2
"""

@component.add(
    name="Cp_limit_nuclear",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"cp_nuclear": 1, "min_cp_nuclear": 1},
)
def cp_limit_nuclear():
    return if_then_else(cp_nuclear() > min_cp_nuclear(), lambda: 1, lambda: 0)


@component.add(
    name="Cp_nuclear",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"cp_nuclear_initial": 1},
)
def cp_nuclear():
    """
    Capacity factor of nuclear power centrals.Cp nuclear initial*Cp exogenous RES elec dispatch reduction
    """
    return cp_nuclear_initial()


@component.add(
    name="Cp_nuclear_initial",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_cp_nuclear_initial"},
)
def cp_nuclear_initial():
    """
    Capacity factor of nuclear taking historic data as reference: in 2011, there were 374 GW of nuclear capacity operating that generated 2,507 TWh.
    """
    return _ext_constant_cp_nuclear_initial()


_ext_constant_cp_nuclear_initial = ExtConstant(
    r"../energy.xlsx",
    "Catalonia",
    "cp_initial_nuclear",
    {},
    _root,
    {},
    "_ext_constant_cp_nuclear_initial",
)


@component.add(
    name="effects_shortage_uranium",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_uranium_ej_cat": 1,
        "extraction_uranium_row": 1,
        "abundance_uranium": 2,
    },
)
def effects_shortage_uranium():
    """
    The eventual scarcity of coal would likely constrain the development of CTL. The proposed relationship avoids an abrupt limitation by introducing a range (1;0.8) in the gas abundance that constrains the development of CTL.
    """
    return if_then_else(
        extraction_uranium_ej_cat() + extraction_uranium_row() == 0,
        lambda: 0,
        lambda: if_then_else(
            abundance_uranium() > 0.8,
            lambda: ((abundance_uranium() - 0.8) * 5) ** 2,
            lambda: 0,
        ),
    )


@component.add(
    name="efficiency_uranium_for_electricity",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_efficiency_uranium_for_electricity"},
)
def efficiency_uranium_for_electricity():
    """
    Efficiency of uranium in nuclear power centrals. [IEA Balances].
    """
    return _ext_constant_efficiency_uranium_for_electricity()


_ext_constant_efficiency_uranium_for_electricity = ExtConstant(
    r"../energy.xlsx",
    "Global",
    "efficiency_uranium_for_electricity",
    {},
    _root,
    {},
    "_ext_constant_efficiency_uranium_for_electricity",
)


@component.add(
    name="Historic_nuclear_generation_TWh",
    units="TWh/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_nuclear_generation_twh",
        "__lookup__": "_ext_lookup_historic_nuclear_generation_twh",
    },
)
def historic_nuclear_generation_twh(x, final_subs=None):
    """
    Historic data of annual production from nuclear energy in TWh.
    """
    return _ext_lookup_historic_nuclear_generation_twh(x, final_subs)


_ext_lookup_historic_nuclear_generation_twh = ExtLookup(
    r"../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_nuclear_generation",
    {},
    _root,
    {},
    "_ext_lookup_historic_nuclear_generation_twh",
)


@component.add(
    name="initial_capacity_in_construction_nuclear",
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
    name="initial_capacity_installed_nuclear",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"initial_gen_nuclear": 1, "twe_per_twh": 1, "cp_nuclear_initial": 1},
)
def initial_capacity_installed_nuclear():
    """
    Initial capacity installed of nuclear power.
    """
    return initial_gen_nuclear() * twe_per_twh() / cp_nuclear_initial()


@component.add(
    name="initial_gen_nuclear",
    units="TWh/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_gen_nuclear"},
)
def initial_gen_nuclear():
    """
    Electric generation from nuclear in the initial year 1995.
    """
    return _ext_constant_initial_gen_nuclear()


_ext_constant_initial_gen_nuclear = ExtConstant(
    r"../energy.xlsx",
    "Catalonia",
    "initial_nuclear_generation",
    {},
    _root,
    {},
    "_ext_constant_initial_gen_nuclear",
)


@component.add(
    name="initial_required_capacity_nuclear",
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
    name="installed_capacity_nuclear_TW",
    units="TW",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_installed_capacity_nuclear_tw": 1},
    other_deps={
        "_integ_installed_capacity_nuclear_tw": {
            "initial": {"initial_capacity_installed_nuclear": 1},
            "step": {
                "nuclear_capacity_under_construction": 1,
                "nuclear_capacity_phaseout": 1,
                "wear_nuclear": 1,
            },
        }
    },
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
    name="invest_cost_nuclear",
    units="Tdollars/TWe",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_invest_cost_nuclear",
        "__data__": "_ext_data_invest_cost_nuclear",
        "time": 1,
    },
)
def invest_cost_nuclear():
    """
    Investment cost of nuclear power considering that future reactors would require the same investment as the recent Hinkley Point C nuclear power station in UK of 8,000 US$/kW (5536.71 1995US$/kW).
    """
    return _ext_data_invest_cost_nuclear(time())


_ext_data_invest_cost_nuclear = ExtData(
    r"../energy.xlsx",
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
    name="invest_nuclear_Tdolar",
    units="Tdollars/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nuclear_capacity_under_construction": 2,
        "invest_cost_nuclear": 1,
        "replacement_nuclear_capacity": 1,
    },
)
def invest_nuclear_tdolar():
    return float(
        np.maximum(
            0,
            if_then_else(
                nuclear_capacity_under_construction() < 0,
                lambda: 0,
                lambda: (
                    nuclear_capacity_under_construction()
                    + replacement_nuclear_capacity()
                )
                * invest_cost_nuclear()
                / 1000,
            ),
        )
    )


@component.add(
    name="life_time_nuclear",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_life_time_nuclear"},
)
def life_time_nuclear():
    """
    Lifetime of nuclear.
    """
    return _ext_constant_life_time_nuclear()


_ext_constant_life_time_nuclear = ExtConstant(
    r"../energy.xlsx",
    "Global",
    "lifetime_nuclear",
    {},
    _root,
    {},
    "_ext_constant_life_time_nuclear",
)


@component.add(
    name="min_Cp_nuclear",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_min_cp_nuclear"},
)
def min_cp_nuclear():
    """
    Assumption of minimum Cp for nuclear given the high inertia of nuclear reactors.
    """
    return _ext_constant_min_cp_nuclear()


_ext_constant_min_cp_nuclear = ExtConstant(
    r"../energy.xlsx",
    "Catalonia",
    "minimum_cp_nuclear",
    {},
    _root,
    {},
    "_ext_constant_min_cp_nuclear",
)


@component.add(
    name="new_nuclear_capacity_under_planning",
    units="TW/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_capacity_nuclear_tw": 1, "time_planification_nuclear": 1},
)
def new_nuclear_capacity_under_planning():
    """
    New nuclear capacity under planning.
    """
    return float(
        np.maximum(0, required_capacity_nuclear_tw() / time_planification_nuclear())
    )


@component.add(
    name="new_required_capacity_nuclear",
    units="TW/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "demand_elec_nre_twh": 1,
        "installed_capacity_nuclear_tw": 1,
        "p_nuclear_elec_gen": 1,
        "effects_shortage_uranium": 1,
        "cp_limit_nuclear": 1,
    },
)
def new_required_capacity_nuclear():
    """
    New required capacity of nuclear power plants.
    """
    return (
        float(
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
        )
        * effects_shortage_uranium()
        * cp_limit_nuclear()
    )


@component.add(
    name='"nuclear_capacity_phase-out"',
    units="TW/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "selection_of_nuclear_scenario": 1,
        "installed_capacity_nuclear_tw": 1,
        "time": 1,
        "p_nuclear_scen34": 1,
        "start_year_nuclear_growth_scen34": 1,
    },
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
    name="Nuclear_capacity_under_construction",
    units="TW/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "cp_nuclear": 1,
        "time_step": 2,
        "twe_per_twh": 1,
        "historic_nuclear_generation_twh": 2,
        "time_construction_nuclear": 1,
        "planned_nuclear_capacity_tw": 1,
    },
)
def nuclear_capacity_under_construction():
    """
    Nuclear capacity under construction.
    """
    return if_then_else(
        time() < 2014,
        lambda: (
            historic_nuclear_generation_twh(time() + time_step())
            - historic_nuclear_generation_twh(time())
        )
        / time_step()
        * twe_per_twh()
        / cp_nuclear(),
        lambda: planned_nuclear_capacity_tw() / time_construction_nuclear(),
    )


@component.add(
    name="nuclear_overcapacity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_generation_nuclear_elec_twh": 3,
        "fe_nuclear_elec_generation_twh": 1,
    },
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
    name="P_nuclear_elec_gen",
    units="1/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "selection_of_nuclear_scenario": 4,
        "time": 1,
        "p_nuclear_scen34": 1,
        "start_year_nuclear_growth_scen34": 1,
    },
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
    name='"P_nuclear_scen3-4"',
    units="1/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_p_nuclear_scen34"},
)
def p_nuclear_scen34():
    """
    Annual variation (growth or phase-out) of new nuclear power plants (scenarios 3 and 4 of nuclear evolution) from the year "start year nuclear growth scen3-4".
    """
    return _ext_constant_p_nuclear_scen34()


_ext_constant_p_nuclear_scen34 = ExtConstant(
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "p_nuclear_scen3_4_variation",
    {},
    _root,
    {},
    "_ext_constant_p_nuclear_scen34",
)


@component.add(
    name="PE_demand_uranium_CAT_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_generation_nuclear_elec_twh": 1,
        "ej_per_twh": 1,
        "efficiency_uranium_for_electricity": 1,
    },
)
def pe_demand_uranium_cat_ej():
    """
    Primary energy demand of uranium for nuclear power generation.
    """
    return (
        potential_generation_nuclear_elec_twh()
        * ej_per_twh()
        / efficiency_uranium_for_electricity()
    )


@component.add(
    name="Planned_nuclear_capacity_TW",
    units="TW",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_planned_nuclear_capacity_tw": 1},
    other_deps={
        "_integ_planned_nuclear_capacity_tw": {
            "initial": {"initial_capacity_in_construction_nuclear": 1},
            "step": {
                "new_nuclear_capacity_under_planning": 1,
                "replacement_nuclear_capacity": 1,
                "nuclear_capacity_under_construction": 1,
            },
        }
    },
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
    name="potential_generation_nuclear_elec_TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "installed_capacity_nuclear_tw": 1,
        "cp_nuclear": 1,
        "twe_per_twh": 1,
        "demand_elec_nre_twh": 1,
    },
)
def potential_generation_nuclear_elec_twh():
    """
    Total potential generation of electricity from nuclear power plants given the installed capacity. A minimum function is introduced to assure that no more nuclear than electricity required (after the RES and oil contribution) is produced.
    """
    return float(
        np.minimum(
            installed_capacity_nuclear_tw() * cp_nuclear() / twe_per_twh(),
            demand_elec_nre_twh(),
        )
    )


@component.add(
    name="replacement_nuclear_capacity",
    units="TW/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "nuclear_capacity_under_construction": 1,
        "selection_of_nuclear_scenario": 2,
        "replacement_rate_nuclear": 1,
        "wear_nuclear": 1,
        "nuclear_overcapacity": 1,
        "cp_limit_nuclear": 1,
    },
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
    name="replacement_rate_nuclear",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_replacement_rate_nuclear"},
)
def replacement_rate_nuclear():
    """
    If =1, we asume that all the power that reaches the end of its lifetime is replaced.
    """
    return _ext_constant_replacement_rate_nuclear()


_ext_constant_replacement_rate_nuclear = ExtConstant(
    r"../energy.xlsx",
    "Global",
    "replacement_rate_nuclear",
    {},
    _root,
    {},
    "_ext_constant_replacement_rate_nuclear",
)


@component.add(
    name="required_capacity_nuclear_TW",
    units="TW",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_required_capacity_nuclear_tw": 1},
    other_deps={
        "_integ_required_capacity_nuclear_tw": {
            "initial": {"initial_required_capacity_nuclear": 1},
            "step": {
                "new_required_capacity_nuclear": 1,
                "new_nuclear_capacity_under_planning": 1,
            },
        }
    },
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
    name="selection_of_nuclear_scenario",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_selection_of_nuclear_scenario"},
)
def selection_of_nuclear_scenario():
    """
    If = 1: Constant power capacity at current levels, If = 2: No more nuclear installed, current capacity depreciates, If = 3: Growth of nuclear power.
    """
    return _ext_constant_selection_of_nuclear_scenario()


_ext_constant_selection_of_nuclear_scenario = ExtConstant(
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "select_nuclear_scen",
    {},
    _root,
    {},
    "_ext_constant_selection_of_nuclear_scenario",
)


@component.add(
    name='"start_year_nuclear_growth_scen3-4"',
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_start_year_nuclear_growth_scen34"},
)
def start_year_nuclear_growth_scen34():
    """
    Start year of increase/phase-out of nuclear power plants (Nuclear scenarios 3 and 4).
    """
    return _ext_constant_start_year_nuclear_growth_scen34()


_ext_constant_start_year_nuclear_growth_scen34 = ExtConstant(
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "start_year_nuclear_variation_scen3_4",
    {},
    _root,
    {},
    "_ext_constant_start_year_nuclear_growth_scen34",
)


@component.add(
    name="time_construction_nuclear",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_time_construction_nuclear"},
)
def time_construction_nuclear():
    """
    Average construction time for nuclear power plants.
    """
    return _ext_constant_time_construction_nuclear()


_ext_constant_time_construction_nuclear = ExtConstant(
    r"../energy.xlsx",
    "Global",
    "construction_time_nuclear",
    {},
    _root,
    {},
    "_ext_constant_time_construction_nuclear",
)


@component.add(
    name="time_planification_nuclear",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_time_planification_nuclear"},
)
def time_planification_nuclear():
    """
    Average planification time for nuclear power plants.
    """
    return _ext_constant_time_planification_nuclear()


_ext_constant_time_planification_nuclear = ExtConstant(
    r"../energy.xlsx",
    "Global",
    "planning_time_nuclear",
    {},
    _root,
    {},
    "_ext_constant_time_planification_nuclear",
)


@component.add(
    name="TWe_per_TWh",
    units="TWe/(TWh/year)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def twe_per_twh():
    """
    Unit conversion (1 TWe=8760 TWh per year)
    """
    return 0.000114155


@component.add(
    name="wear_nuclear",
    units="TW/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "life_time_nuclear": 1, "installed_capacity_nuclear_tw": 1},
)
def wear_nuclear():
    """
    Depreciation of nuclear power plants.
    """
    return if_then_else(
        time() < 2030,
        lambda: 0,
        lambda: installed_capacity_nuclear_tw() / life_time_nuclear(),
    )
