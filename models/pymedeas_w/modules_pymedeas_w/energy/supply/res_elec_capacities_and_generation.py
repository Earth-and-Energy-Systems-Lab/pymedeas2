"""
Module res_elec_capacities_and_generation
Translated using PySD version 3.0.0
"""


@component.add(
    name="past RES growth",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def past_res_growth():
    return (
        table_hist_capacity_res_elec(time()) - table_hist_capacity_res_elec(time() - 1)
    ) / table_hist_capacity_res_elec(time() - 1)


@component.add(
    name="adapt growth RES elec",
    units="1/year",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def adapt_growth_res_elec():
    """
    Annual growth per RES elec technology. Modeling of a soft transition from current historic annual growth to reach the policy-objective 5 years later (2020).
    """
    return if_then_else(
        time() <= 2015,
        lambda: past_res_growth(),
        lambda: if_then_else(
            time() < start_year_p_growth_res_elec() + 1,
            lambda: zidz(
                p_power(start_year_p_growth_res_elec()),
                table_hist_capacity_res_elec(2015),
            )
            ** (1 / (start_year_p_growth_res_elec() - 2015))
            - 1,
            lambda: zidz(p_power(time()) - p_power(time() - 1), p_power(time() - 1)),
        ),
    )


@component.add(
    name="new required capacity RES elec",
    units="TW",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def new_required_capacity_res_elec():
    """
    New required capacity of RES technologies for electricity generation. We assume 100% of the required infraestructure is planned and constructed.
    """
    return if_then_else(
        time() < 2014 - total_time_planconstr_res_elec(),
        lambda: historic_new_required_capacity_res_elec(),
        lambda: if_then_else(
            max_potential_res_elec_twe() > installed_capacity_res_elec_tw(),
            lambda: p_power(time() - 1) * adapt_growth_res_elec(),
            lambda: xr.DataArray(
                0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
            ),
        ),
    )


@component.add(
    name="installed capacity delayed",
    subscripts=["RES elec"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
)
def installed_capacity_delayed():
    return _delayfixed_installed_capacity_delayed()


_delayfixed_installed_capacity_delayed = DelayFixed(
    lambda: installed_capacity_res_elec_tw(),
    lambda: 0.03125,
    lambda: xr.DataArray(0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]),
    time_step,
    "_delayfixed_installed_capacity_delayed",
)


@component.add(
    name="RES elec capacity under construction TW",
    units="TW/year",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def res_elec_capacity_under_construction_tw():
    """
    RES infraestructure for electricity generation capacity under construction.
    """
    return if_then_else(
        installed_capacity_delayed() < max_potential_res_elec_twe(),
        lambda: res_elec_planned_capacity_tw() / time_construction_res_elec(),
        lambda: xr.DataArray(
            0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
        ),
    )


@component.add(
    name="installed capacity RES elec TW",
    units="TW",
    subscripts=["RES elec"],
    comp_type="Stateful",
    comp_subtype="Integ",
)
def installed_capacity_res_elec_tw():
    """
    Annual installed capacity of RES elec technologies for electricity generation.
    """
    return _integ_installed_capacity_res_elec_tw()


_integ_installed_capacity_res_elec_tw = Integ(
    lambda: res_elec_capacity_under_construction_tw() - wear_res_elec(),
    lambda: initial_instal_cap_res_elec(),
    "_integ_installed_capacity_res_elec_tw",
)


@component.add(
    name="P power",
    units="TW",
    subscripts=["RES elec"],
    comp_type="Lookup",
    comp_subtype="External",
)
def p_power(x, final_subs=None):
    """
    Desired installed power (TW)
    """
    return _ext_lookup_p_power(x, final_subs)


_ext_lookup_p_power = ExtLookup(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "year_RES_power",
    "p_RES_power",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    {"RES elec": _subscript_dict["RES elec"]},
    "_ext_lookup_p_power",
)


@component.add(
    name="remaining potential constraint on new RES elec capacity",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def remaining_potential_constraint_on_new_res_elec_capacity():
    """
    Constraint of remaining potential on new RES elec capacity. Another alternative: SQRT(remaining potential RES elec after intermitt[RES elec])
    """
    return if_then_else(
        remaining_potential_res_elec_after_intermitt()
        > threshold_remaining_potential_new_capacity(),
        lambda: xr.DataArray(
            1, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
        ),
        lambda: remaining_potential_res_elec_after_intermitt()
        * (1 / threshold_remaining_potential_new_capacity()),
    )


@component.add(
    name="threshold remaining potential new capacity",
    comp_type="Constant",
    comp_subtype="Normal",
)
def threshold_remaining_potential_new_capacity():
    return 0.5


@component.add(
    name="potential generation RES elec TWh",
    units="TWh",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def potential_generation_res_elec_twh():
    """
    Potential generation of electricity by RES technology given the installed capacity.
    """
    return installed_capacity_res_elec_tw() * cp_res_elec() / twe_per_twh()


@component.add(
    name="abundance RES elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def abundance_res_elec():
    """
    The parameter abundance varies between (1;0). The closest to 1 indicates that electricity generation from RES is far to cover to whole electricity demand, if "abundance RES elec"=0 it means that RES elec cover the whole electricity demand.
    """
    return (
        if_then_else(
            total_fe_elec_demand_after_priorities_twh() == 0,
            lambda: 0,
            lambda: if_then_else(
                total_fe_elec_demand_after_priorities_twh()
                > fe_real_tot_generation_res_elec_twh(),
                lambda: (
                    total_fe_elec_demand_after_priorities_twh()
                    - fe_real_tot_generation_res_elec_twh()
                )
                / total_fe_elec_demand_after_priorities_twh(),
                lambda: 0,
            ),
        )
        * 1.2
    )


@component.add(
    name="activate EROI allocation rule",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def activate_eroi_allocation_rule():
    """
    Activate/Deactivate EROI allocation rule for the RES elec technologies: 1. Activated 0. Deactivated
    """
    return _ext_constant_activate_eroi_allocation_rule()


_ext_constant_activate_eroi_allocation_rule = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "EROI_feedback_flag",
    {},
    _root,
    {},
    "_ext_constant_activate_eroi_allocation_rule",
)


@component.add(
    name="adapt growth RES elec after allocation",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def adapt_growth_res_elec_after_allocation():
    """
    Annual growth per RES elec technology after accounting for the allocation rule.
    """
    return if_then_else(
        activate_eroi_allocation_rule() == 0,
        lambda: adapt_growth_res_elec(),
        lambda: adapt_growth_res_elec() * eroi_allocation_rule_per_res_elec(),
    )


@component.add(
    name="Cp baseload reduction",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def cp_baseload_reduction():
    return cp_res_elec() / cpini_res_elec()


@component.add(
    name="Cp RES elec",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def cp_res_elec():
    """
    Capacity factor of RES technologies (after accounting for the overcapacities required to manage the intermittency of RES elec variables).
    """
    return np.maximum(
        min_cp_baseload_res(), cpini_res_elec() * cp_exogenous_res_elec_reduction()
    )


@component.add(
    name='"Cp-ini RES elec"',
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Constant",
    comp_subtype="External",
)
def cpini_res_elec():
    """
    Initial capacity factor (before accounting for the reduction of Cp of the base-load plants with the penetration of the intermittent RES (solar and wind) in the electricity generation mix).
    """
    return _ext_constant_cpini_res_elec()


_ext_constant_cpini_res_elec = ExtConstant(
    "../energy.xlsx",
    "World",
    "cp_initial_res_elec*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    {"RES elec": _subscript_dict["RES elec"]},
    "_ext_constant_cpini_res_elec",
)


@component.add(
    name="FE real tot generation RES elec TWh",
    units="TWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def fe_real_tot_generation_res_elec_twh():
    return np.minimum(
        np.maximum(total_fe_elec_demand_after_priorities_twh(), 0),
        potential_tot_generation_res_elec_twh(),
    )


@component.add(
    name="Historic new required capacity RES elec",
    units="TW",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def historic_new_required_capacity_res_elec():
    """
    (Assuming 100% of planned was planned and constructed).
    """
    return table_hist_capacity_res_elec(
        time() + total_time_planconstr_res_elec() + 1,
        {
            "RES elec": [
                "hydro",
                "geot elec",
                "solid bioE elec",
                "oceanic",
                "wind onshore",
                "wind offshore",
                "solar PV",
                "CSP",
            ]
        },
    ) - table_hist_capacity_res_elec(
        time() + total_time_planconstr_res_elec(),
        {
            "RES elec": [
                "hydro",
                "geot elec",
                "solid bioE elec",
                "oceanic",
                "wind onshore",
                "wind offshore",
                "solar PV",
                "CSP",
            ]
        },
    )


@component.add(
    name="initial capacity in construction RES elec",
    units="TW",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def initial_capacity_in_construction_res_elec():
    """
    Initial capacity of RES by technology in construction (year 1995). We assume that it is the same than the additional installed capacity between 1995 and 1996.
    """
    return initial_required_capacity_res_elec()


@component.add(
    name="initial instal cap RES elec",
    units="TW",
    subscripts=["RES elec"],
    comp_type="Constant",
    comp_subtype="External",
)
def initial_instal_cap_res_elec():
    """
    Installed capacity per RES elec by technology in the initial year 1995.
    """
    return _ext_constant_initial_instal_cap_res_elec()


_ext_constant_initial_instal_cap_res_elec = ExtConstant(
    "../energy.xlsx",
    "World",
    "initial_installed_capacity_res_for_electricity*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    {"RES elec": _subscript_dict["RES elec"]},
    "_ext_constant_initial_instal_cap_res_elec",
)


@component.add(
    name="initial required capacity RES elec",
    units="TW",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def initial_required_capacity_res_elec():
    """
    Initial required capacity of RES by technology (year 1995). We assume that it is the same than the additional installed capacity between 1995 and 1996.
    """
    return table_hist_capacity_res_elec(1996) - table_hist_capacity_res_elec(1995)


@component.add(
    name="installed capacity RES elec delayed 1yr",
    units="TW",
    subscripts=["RES elec"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
)
def installed_capacity_res_elec_delayed_1yr():
    """
    Annual installed capacity of RES elec technologies for electricity generation delayed 1 year.
    """
    return _delayfixed_installed_capacity_res_elec_delayed_1yr()


_delayfixed_installed_capacity_res_elec_delayed_1yr = DelayFixed(
    lambda: installed_capacity_res_elec_tw(),
    lambda: 1,
    lambda: xr.DataArray(0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]),
    time_step,
    "_delayfixed_installed_capacity_res_elec_delayed_1yr",
)


@component.add(
    name="lifetime RES elec",
    units="years",
    subscripts=["RES elec"],
    comp_type="Constant",
    comp_subtype="External",
)
def lifetime_res_elec():
    """
    Lifetime of each RES technology for electricity generation.
    """
    return _ext_constant_lifetime_res_elec()


_ext_constant_lifetime_res_elec = ExtConstant(
    "../energy.xlsx",
    "Global",
    "lifetime_res_elec*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    {"RES elec": _subscript_dict["RES elec"]},
    "_ext_constant_lifetime_res_elec",
)


@component.add(
    name="min Cp baseload RES",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Constant",
    comp_subtype="External",
)
def min_cp_baseload_res():
    """
    Assumption of minimum Cp for baseload RES plants.
    """
    return _ext_constant_min_cp_baseload_res()


_ext_constant_min_cp_baseload_res = ExtConstant(
    "../energy.xlsx",
    "World",
    "minimum_cp_baseload_res*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    {"RES elec": _subscript_dict["RES elec"]},
    "_ext_constant_min_cp_baseload_res",
)


@component.add(
    name="new capacity installed growth rate RES elec",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def new_capacity_installed_growth_rate_res_elec():
    """
    Annual RES elec capacity installed growth rate.
    """
    return -1 + zidz(
        installed_capacity_res_elec_tw(), installed_capacity_res_elec_delayed_1yr()
    )


@component.add(
    name="new RES elec capacity under planning",
    units="TW/year",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def new_res_elec_capacity_under_planning():
    """
    New RES infraestructure for electricity generation capacity under planning.
    """
    return required_capacity_res_elec_tw() / time_planification_res_elec()


@component.add(
    name="potential RES elec after intermitt TWh",
    units="TWh",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def potential_res_elec_after_intermitt_twh():
    """
    Potential of RES for electricity per technology after accounting for the reduction of the maximal potential given the reduction of the Cp.
    """
    return max_potential_res_elec_twe() * cp_baseload_reduction() / twe_per_twh()


@component.add(
    name="potential tot generation RES elec TWh",
    units="TWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def potential_tot_generation_res_elec_twh():
    """
    Total potential generation of electricity from RES given the installed capacity.
    """
    return sum(
        potential_generation_res_elec_twh().rename({"RES elec": "RES elec!"}),
        dim=["RES elec!"],
    )


@component.add(
    name="real Cp RES elec",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def real_cp_res_elec():
    return if_then_else(
        time() < 2015,
        lambda: cp_res_elec(),
        lambda: if_then_else(
            installed_capacity_res_elec_tw() == 0,
            lambda: xr.DataArray(
                0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
            ),
            lambda: real_generation_res_elec_twh()
            * twe_per_twh()
            / installed_capacity_res_elec_tw(),
        ),
    )


@component.add(
    name="real generation RES elec TWh",
    units="TWh",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def real_generation_res_elec_twh():
    """
    Electricity generation by RES technology.
    """
    return potential_generation_res_elec_twh() * (1 - res_elec_tot_overcapacity())


@component.add(
    name="remaining potential RES elec after intermitt",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def remaining_potential_res_elec_after_intermitt():
    return if_then_else(
        potential_res_elec_after_intermitt_twh() > potential_generation_res_elec_twh(),
        lambda: zidz(
            potential_res_elec_after_intermitt_twh()
            - potential_generation_res_elec_twh(),
            potential_res_elec_after_intermitt_twh(),
        ),
        lambda: xr.DataArray(
            0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
        ),
    )


@component.add(
    name="replacement capacity RES elec",
    units="TW/year",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def replacement_capacity_res_elec():
    """
    Annual replacement of RES infrastructure for electricity generation by technology. It is assumed that the step of planning the replaced infrastructure can be done while the infraestructure to be replaced is still under operation. For replaced infraestructures, the construction time should be smaller than for new infaestructures, however we compensate for this assuming that the demantling time is included in onstruction time for replaced infrastructure.
    """
    return if_then_else(
        time() < 2015,
        lambda: xr.DataArray(
            0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
        ),
        lambda: replacement_rate_res_elec()
        * wear_res_elec()
        * (1 - res_elec_tot_overcapacity()),
    )


@component.add(
    name="replacement rate RES elec",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def replacement_rate_res_elec():
    """
    Replacement rate of RES for electricity: by default all decommissioned capacity is replaced (=1). In the case of overcapacity in relation to the potential after accounting for intermittency, we reduce the annual replacement rate to 0.9.
    """
    return if_then_else(
        potential_generation_res_elec_twh() < potential_res_elec_after_intermitt_twh(),
        lambda: xr.DataArray(
            1, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
        ),
        lambda: xr.DataArray(
            0.9, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
        ),
    )


@component.add(
    name="required capacity RES elec TW",
    units="TW",
    subscripts=["RES elec"],
    comp_type="Stateful",
    comp_subtype="Integ",
)
def required_capacity_res_elec_tw():
    """
    Required capacity of RES technologies for electricity generation.
    """
    return _integ_required_capacity_res_elec_tw()


_integ_required_capacity_res_elec_tw = Integ(
    lambda: new_required_capacity_res_elec() - new_res_elec_capacity_under_planning(),
    lambda: initial_required_capacity_res_elec(),
    "_integ_required_capacity_res_elec_tw",
)


@component.add(
    name="RES elec planned capacity TW",
    units="TW",
    subscripts=["RES elec"],
    comp_type="Stateful",
    comp_subtype="Integ",
)
def res_elec_planned_capacity_tw():
    """
    Planned capacity of RES for electricity.
    """
    return _integ_res_elec_planned_capacity_tw()


_integ_res_elec_planned_capacity_tw = Integ(
    lambda: new_res_elec_capacity_under_planning()
    + replacement_capacity_res_elec()
    - res_elec_capacity_under_construction_tw(),
    lambda: initial_capacity_in_construction_res_elec(),
    "_integ_res_elec_planned_capacity_tw",
)


@component.add(
    name="RES elec tot overcapacity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def res_elec_tot_overcapacity():
    """
    Overcapacity for each technology RES for electricity taking into account the installed capacity and the real generation.
    """
    return if_then_else(
        potential_tot_generation_res_elec_twh() == 0,
        lambda: 0,
        lambda: (
            potential_tot_generation_res_elec_twh()
            - fe_real_tot_generation_res_elec_twh()
        )
        / potential_tot_generation_res_elec_twh(),
    )


@component.add(
    name="Start year P growth RES elec",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
)
def start_year_p_growth_res_elec():
    """
    Start year of the policy growth of RES technologies for generating electricity.
    """
    return _ext_constant_start_year_p_growth_res_elec()


_ext_constant_start_year_p_growth_res_elec = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "start_year_P_growth_RES_elec",
    {},
    _root,
    {},
    "_ext_constant_start_year_p_growth_res_elec",
)


@component.add(
    name="table hist capacity RES elec",
    units="TW/year",
    subscripts=["RES elec"],
    comp_type="Lookup",
    comp_subtype="External",
)
def table_hist_capacity_res_elec(x, final_subs=None):
    return _ext_lookup_table_hist_capacity_res_elec(x, final_subs)


_ext_lookup_table_hist_capacity_res_elec = ExtLookup(
    "../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_installed_capacity_res_for_electricity",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    {"RES elec": _subscript_dict["RES elec"]},
    "_ext_lookup_table_hist_capacity_res_elec",
)


@component.add(
    name="time construction RES elec",
    units="year",
    subscripts=["RES elec"],
    comp_type="Constant",
    comp_subtype="External",
)
def time_construction_res_elec():
    """
    Average construction time for each RES generating electricity. For replaced infraestructures, the construction time should be smaller than for new infaestructures, however we compensate for this assuming that the demantling time is included in onstruction time for replaced infrastructure.
    """
    return _ext_constant_time_construction_res_elec()


_ext_constant_time_construction_res_elec = ExtConstant(
    "../energy.xlsx",
    "Global",
    "construction_time_res_elec*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    {"RES elec": _subscript_dict["RES elec"]},
    "_ext_constant_time_construction_res_elec",
)


@component.add(
    name="time planification RES elec",
    units="year",
    subscripts=["RES elec"],
    comp_type="Constant",
    comp_subtype="External",
)
def time_planification_res_elec():
    """
    Average planification time for each RES generating electricity.
    """
    return _ext_constant_time_planification_res_elec()


_ext_constant_time_planification_res_elec = ExtConstant(
    "../energy.xlsx",
    "Global",
    "planning_time_res_elec*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    {"RES elec": _subscript_dict["RES elec"]},
    "_ext_constant_time_planification_res_elec",
)


@component.add(
    name='"total time plan+constr RES elec"',
    units="year",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_time_planconstr_res_elec():
    return np.maximum(time_construction_res_elec(), time_step()) + np.maximum(
        time_planification_res_elec(), time_step()
    )


@component.add(
    name="wear RES elec",
    units="TW/year",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def wear_res_elec():
    """
    Depreciation of RES infraestructures.
    """
    return if_then_else(
        time() < 2015,
        lambda: xr.DataArray(
            0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
        ),
        lambda: installed_capacity_res_elec_tw() / lifetime_res_elec(),
    )
