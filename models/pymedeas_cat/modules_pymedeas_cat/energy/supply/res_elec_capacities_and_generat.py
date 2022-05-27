"""
Module res_elec_capacities_and_generat
Translated using PySD version 3.0.1
"""


@component.add(
    name="abundance RES elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_fe_elec_demand_after_priorities_twh": 4,
        "fe_real_tot_generation_res_elec_twh": 2,
    },
)
def abundance_res_elec():
    """
    The parameter abundance varies between (1;0). The closest to 1 indicates that electricity generation from RES is far to cover to whole electricity demand, if "abundance RES elec"=0 it means that RES elec cover the whole electricity demand.
    """
    return if_then_else(
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


@component.add(
    name="activate EROI allocation rule",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def activate_eroi_allocation_rule():
    """
    Activate/Deactivate EROI allocation rule for the RES elec technologies: 1. Activated 0. Deactivated
    """
    return 1


@component.add(
    name="adapt growth RES elec",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "past_res_growth": 1,
        "table_hist_capacity_res_elec": 1,
        "start_year_p_growth_res_elec": 3,
        "p_power": 4,
    },
)
def adapt_growth_res_elec():
    return if_then_else(
        time() < 2015,
        lambda: past_res_growth(),
        lambda: if_then_else(
            time() < start_year_p_growth_res_elec() + 1,
            lambda: zidz(
                p_power(start_year_p_growth_res_elec()),
                table_hist_capacity_res_elec(2015),
            )
            ** (1 / (start_year_p_growth_res_elec() - 2015)),
            lambda: zidz(p_power(time()) - p_power(time() - 1), p_power(time() - 1)),
        ),
    )


@component.add(
    name="adapt growth RES elec after allocation",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "activate_eroi_allocation_rule": 1,
        "adapt_growth_res_elec": 2,
        "eroi_allocation_rule_per_res_elec": 1,
        "constraint_elec_storage_availability": 1,
    },
)
def adapt_growth_res_elec_after_allocation():
    """
    Annual growth per RES elec technology after accounting for the allocation rule.
    """
    return (
        if_then_else(
            activate_eroi_allocation_rule() == 0,
            lambda: adapt_growth_res_elec(),
            lambda: adapt_growth_res_elec() * eroi_allocation_rule_per_res_elec(),
        )
        * constraint_elec_storage_availability()
    )


@component.add(
    name="Cp RES elec",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "min_cp_baseload_res": 1,
        "cpini_res_elec": 1,
        "shortage_bioe_for_elec": 1,
        "cp_exogenous_res_elec_reduction": 1,
    },
)
def cp_res_elec():
    """
    Capacity factor of RES technologies (after accounting for the overcapacities required to manage the intermittency of RES elec variables).
    """
    return np.maximum(
        min_cp_baseload_res(),
        cpini_res_elec() * cp_exogenous_res_elec_reduction() * shortage_bioe_for_elec(),
    )


@component.add(
    name="FE real tot generation RES elec TWh",
    units="TWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_fe_elec_demand_after_priorities_twh": 1,
        "potential_tot_generation_res_elec_twh": 1,
    },
)
def fe_real_tot_generation_res_elec_twh():
    return np.minimum(
        np.maximum(total_fe_elec_demand_after_priorities_twh(), 0),
        potential_tot_generation_res_elec_twh(),
    )


@component.add(
    name="Cp baseload reduction",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"cp_res_elec": 1, "cpini_res_elec": 1},
)
def cp_baseload_reduction():
    return cp_res_elec() / cpini_res_elec()


@component.add(
    name='"Cp-ini RES elec"',
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_cpini_res_elec"},
)
def cpini_res_elec():
    """
    Initial capacity factor (before accounting for the reduction of Cp of the base-load plants with the penetration of the intermittent RES (solar and wind) in the electricity generation mix).
    """
    return _ext_constant_cpini_res_elec()


_ext_constant_cpini_res_elec = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "cp_initial_res_elec*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    {"RES elec": _subscript_dict["RES elec"]},
    "_ext_constant_cpini_res_elec",
)


@component.add(
    name="Historic new required capacity RES elec",
    units="TW",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "total_time_planconstr_res_elec": 2,
        "table_hist_capacity_res_elec": 2,
    },
)
def historic_new_required_capacity_res_elec():
    """
    (Assuming 100% of planned was planned and constructed).
    """
    return table_hist_capacity_res_elec(
        integer(time() + 1) + total_time_planconstr_res_elec(),
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
        integer(time()) + total_time_planconstr_res_elec(),
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
    depends_on={"initial_required_capacity_res_elec": 1},
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
    depends_on={"__external__": "_ext_constant_initial_instal_cap_res_elec"},
)
def initial_instal_cap_res_elec():
    """
    Installed capacity per RES elec by technology in the initial year 1995.
    """
    return _ext_constant_initial_instal_cap_res_elec()


_ext_constant_initial_instal_cap_res_elec = ExtConstant(
    "../energy.xlsx",
    "Austria",
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
    depends_on={"table_hist_capacity_res_elec": 2},
)
def initial_required_capacity_res_elec():
    """
    Initial required capacity of RES by technology (year 1995). We assume that it is the same than the additional installed capacity between 1995 and 1996.
    """
    return table_hist_capacity_res_elec(1996) - table_hist_capacity_res_elec(1995)


@component.add(
    name="installed capacity delayed",
    units="TW",
    subscripts=["RES elec"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_installed_capacity_delayed": 1},
    other_deps={
        "_delayfixed_installed_capacity_delayed": {
            "initial": {},
            "step": {"installed_capacity_res_elec_tw": 1},
        }
    },
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
    name="installed capacity RES elec delayed 1yr",
    units="TW",
    subscripts=["RES elec"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_installed_capacity_res_elec_delayed_1yr": 1},
    other_deps={
        "_delayfixed_installed_capacity_res_elec_delayed_1yr": {
            "initial": {},
            "step": {"installed_capacity_res_elec_tw": 1},
        }
    },
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
    name="installed capacity RES elec TW",
    units="TW",
    subscripts=["RES elec"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_installed_capacity_res_elec_tw": 1},
    other_deps={
        "_integ_installed_capacity_res_elec_tw": {
            "initial": {"initial_instal_cap_res_elec": 1},
            "step": {"res_elec_capacity_under_construction_tw": 1, "wear_res_elec": 1},
        }
    },
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
    name="lifetime RES elec",
    units="Years",
    subscripts=["RES elec"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_lifetime_res_elec"},
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
    depends_on={"__external__": "_ext_constant_min_cp_baseload_res"},
)
def min_cp_baseload_res():
    """
    Assumption of minimum Cp for baseload RES plants.
    """
    return _ext_constant_min_cp_baseload_res()


_ext_constant_min_cp_baseload_res = ExtConstant(
    "../energy.xlsx",
    "Austria",
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
    depends_on={
        "installed_capacity_res_elec_tw": 1,
        "installed_capacity_res_elec_delayed_1yr": 1,
    },
)
def new_capacity_installed_growth_rate_res_elec():
    """
    Annual RES elec capacity installed growth rate.
    """
    return -1 + zidz(
        installed_capacity_res_elec_tw(), installed_capacity_res_elec_delayed_1yr()
    )


@component.add(
    name="new required capacity RES elec",
    units="TW",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "total_time_planconstr_res_elec": 1,
        "historic_new_required_capacity_res_elec": 1,
        "installed_capacity_res_elec_tw": 1,
        "adapt_growth_res_elec": 1,
        "p_power": 1,
        "max_res_elec_twe": 1,
    },
)
def new_required_capacity_res_elec():
    """
    New required capacity of RES technologies for electricity generation. We assume 100% of the required infraestructure is planned and constructed.
    """
    return if_then_else(
        time() < 2014 - total_time_planconstr_res_elec(),
        lambda: historic_new_required_capacity_res_elec(),
        lambda: if_then_else(
            max_res_elec_twe() > installed_capacity_res_elec_tw(),
            lambda: p_power(time() - 1) * adapt_growth_res_elec(),
            lambda: xr.DataArray(
                0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
            ),
        ),
    )


@component.add(
    name="new RES elec capacity under planning",
    units="TW/Year",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_capacity_res_elec_tw": 1,
        "time_step": 1,
        "time_planification_res_elec": 1,
    },
)
def new_res_elec_capacity_under_planning():
    """
    New RES infraestructure for electricity generation capacity under planning.
    """
    return np.maximum(
        0,
        required_capacity_res_elec_tw()
        / np.maximum(time_planification_res_elec(), time_step()),
    )


@component.add(
    name="P power",
    units="TW",
    subscripts=["RES elec"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_p_power",
        "__lookup__": "_ext_lookup_p_power",
    },
)
def p_power(x, final_subs=None):
    return _ext_lookup_p_power(x, final_subs)


_ext_lookup_p_power = ExtLookup(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "year_RES_power",
    "p_RES_power",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    {"RES elec": _subscript_dict["RES elec"]},
    "_ext_lookup_p_power",
)


@component.add(
    name="past RES growth",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 3, "table_hist_capacity_res_elec": 3},
)
def past_res_growth():
    return zidz(
        table_hist_capacity_res_elec(time()) - table_hist_capacity_res_elec(time() - 1),
        table_hist_capacity_res_elec(time() - 1),
    )


@component.add(
    name="potential generation RES elec TWh",
    units="TWh",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "installed_capacity_res_elec_tw": 1,
        "cp_res_elec": 1,
        "twe_per_twh": 1,
    },
)
def potential_generation_res_elec_twh():
    """
    Potential generation of electricity by RES technology given the installed capacity.
    """
    return installed_capacity_res_elec_tw() * cp_res_elec() / twe_per_twh()


@component.add(
    name="potential RES elec after intermitt TWh",
    units="TWh",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_res_elec_twe": 1, "cp_baseload_reduction": 1, "twe_per_twh": 1},
)
def potential_res_elec_after_intermitt_twh():
    """
    Potential of RES for electricity per technology after accounting for the reduction of the maximal potential given the reduction of the Cp.
    """
    return max_res_elec_twe() * cp_baseload_reduction() / twe_per_twh()


@component.add(
    name="potential tot generation RES elec TWh",
    units="TWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_generation_res_elec_twh": 1},
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
    name="potential tot RES elec after intermitt",
    units="TWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_res_elec_after_intermitt_twh": 1},
)
def potential_tot_res_elec_after_intermitt():
    """
    Total potential of RES for electricity after accounting for the reduction of the maximal potential given the reduction of the Cp.
    """
    return sum(
        potential_res_elec_after_intermitt_twh().rename({"RES elec": "RES elec!"}),
        dim=["RES elec!"],
    )


@component.add(
    name="real Cp RES elec",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "cp_res_elec": 1,
        "installed_capacity_res_elec_tw": 2,
        "real_generation_res_elec_twh": 1,
        "twe_per_twh": 1,
    },
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
    depends_on={
        "potential_generation_res_elec_twh": 1,
        "res_elec_tot_overcapacity": 1,
        "shortage_bioe_for_elec": 1,
    },
)
def real_generation_res_elec_twh():
    """
    Electricity generation by RES technology.
    """
    return (
        potential_generation_res_elec_twh()
        * (1 - res_elec_tot_overcapacity())
        * shortage_bioe_for_elec()
    )


@component.add(
    name="remaining potential constraint on new RES elec capacity",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "remaining_potential_res_elec_after_intermitt": 2,
        "threshold_remaining_potential_new_capacity": 2,
    },
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
    name="remaining potential RES elec after intermitt",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_res_elec_after_intermitt_twh": 3,
        "potential_generation_res_elec_twh": 2,
    },
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
    name="remaining potential tot RES elec after intermitt",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_tot_res_elec_after_intermitt": 3,
        "fe_real_tot_generation_res_elec_twh": 2,
    },
)
def remaining_potential_tot_res_elec_after_intermitt():
    return if_then_else(
        potential_tot_res_elec_after_intermitt()
        > fe_real_tot_generation_res_elec_twh(),
        lambda: (
            potential_tot_res_elec_after_intermitt()
            - fe_real_tot_generation_res_elec_twh()
        )
        / potential_tot_res_elec_after_intermitt(),
        lambda: 0,
    )


@component.add(
    name="replacement capacity RES elec",
    units="TW/Year",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "replacement_rate_res_elec": 1,
        "res_elec_tot_overcapacity": 1,
        "wear_res_elec": 1,
        "constraint_elec_storage_availability": 1,
        "shortage_bioe_for_elec": 1,
    },
)
def replacement_capacity_res_elec():
    """
    Annual replacement of RES infrastructure for electricity generation by technology. It is assumed that the step of planning the replaced infrastructure can be done while the infraestructure to be replaced is still under operation. For replaced infraestructures, the construction time should be smaller than for new infaestructures, however we compensate for this assuming that the demantling time is included in onstruction time for replaced infrastructure.
    """
    return (
        if_then_else(
            time() < 2015,
            lambda: xr.DataArray(
                0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
            ),
            lambda: replacement_rate_res_elec()
            * wear_res_elec()
            * (1 - res_elec_tot_overcapacity()),
        )
        * constraint_elec_storage_availability()
        * shortage_bioe_for_elec() ** 2
    )


@component.add(
    name="replacement rate RES elec",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_generation_res_elec_twh": 1,
        "potential_res_elec_after_intermitt_twh": 1,
    },
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
    depends_on={"_integ_required_capacity_res_elec_tw": 1},
    other_deps={
        "_integ_required_capacity_res_elec_tw": {
            "initial": {"initial_required_capacity_res_elec": 1},
            "step": {
                "new_required_capacity_res_elec": 1,
                "new_res_elec_capacity_under_planning": 1,
            },
        }
    },
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
    name="RES elec capacity under construction TW",
    units="TW/Year",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "installed_capacity_delayed": 1,
        "max_res_elec_twe": 1,
        "res_elec_planned_capacity_tw": 1,
        "time_construction_res_elec": 1,
    },
)
def res_elec_capacity_under_construction_tw():
    """
    RES infraestructure for electricity generation capacity under construction.
    """
    return if_then_else(
        installed_capacity_delayed() < max_res_elec_twe(),
        lambda: res_elec_planned_capacity_tw() / time_construction_res_elec(),
        lambda: xr.DataArray(
            0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
        ),
    )


@component.add(
    name="RES elec planned capacity TW",
    units="TW",
    subscripts=["RES elec"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_res_elec_planned_capacity_tw": 1},
    other_deps={
        "_integ_res_elec_planned_capacity_tw": {
            "initial": {"initial_capacity_in_construction_res_elec": 1},
            "step": {
                "new_res_elec_capacity_under_planning": 1,
                "replacement_capacity_res_elec": 1,
                "res_elec_capacity_under_construction_tw": 1,
            },
        }
    },
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
    depends_on={
        "potential_tot_generation_res_elec_twh": 3,
        "fe_real_tot_generation_res_elec_twh": 1,
    },
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
    name="table hist capacity RES elec",
    units="TW/Year",
    subscripts=["RES elec"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_table_hist_capacity_res_elec",
        "__lookup__": "_ext_lookup_table_hist_capacity_res_elec",
    },
)
def table_hist_capacity_res_elec(x, final_subs=None):
    return _ext_lookup_table_hist_capacity_res_elec(x, final_subs)


_ext_lookup_table_hist_capacity_res_elec = ExtLookup(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_installed_capacity_res_for_electricity",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    {"RES elec": _subscript_dict["RES elec"]},
    "_ext_lookup_table_hist_capacity_res_elec",
)


@component.add(
    name="threshold remaining potential new capacity",
    comp_type="Constant",
    comp_subtype="Normal",
)
def threshold_remaining_potential_new_capacity():
    """
    This threshold represents the level of the remaining potential that starts to affects the planification of new RES elec capacity (decreasing returns). Avoid problems of (erroneously) affecting past historical growth trends.
    """
    return 0.5


@component.add(
    name="Time 95pc TS potential RES elec",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"remaining_potential_res_elec_after_intermitt": 1, "time": 1},
)
def time_95pc_ts_potential_res_elec():
    """
    Time when the remaining resource availability falls bellow 5% of the techno-ecological potential, i.e. when the 95% of the techno-ecological potential is reached.
    """
    return if_then_else(
        remaining_potential_res_elec_after_intermitt() > 0.05,
        lambda: xr.DataArray(
            0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
        ),
        lambda: xr.DataArray(
            time(), {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
        ),
    )


@component.add(
    name="time construction RES elec",
    units="Year",
    subscripts=["RES elec"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_time_construction_res_elec"},
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
    units="Year",
    subscripts=["RES elec"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_time_planification_res_elec"},
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
    units="Year",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time_construction_res_elec": 1,
        "time_step": 2,
        "time_planification_res_elec": 1,
    },
)
def total_time_planconstr_res_elec():
    return np.maximum(time_construction_res_elec(), time_step()) + np.maximum(
        time_planification_res_elec(), time_step()
    )


@component.add(
    name="wear RES elec",
    units="TW/Year",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "installed_capacity_res_elec_tw": 1, "lifetime_res_elec": 1},
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
