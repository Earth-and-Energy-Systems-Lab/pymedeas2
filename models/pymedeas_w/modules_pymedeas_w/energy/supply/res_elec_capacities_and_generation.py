"""
Module energy.supply.res_elec_capacities_and_generation
Translated using PySD version 3.10.0
"""


@component.add(
    name="constructed capacity RES elec TW",
    units="TW",
    subscripts=["RES elec"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_constructed_capacity_res_elec_tw": 1},
    other_deps={
        "_integ_constructed_capacity_res_elec_tw": {
            "initial": {"table_hist_capacity_res_elec": 1},
            "step": {"res_elec_capacity_under_construction_tw": 1, "wear_res_elec": 1},
        }
    },
)
def constructed_capacity_res_elec_tw():
    """
    Annual installed capacity of RES elec technologies for electricity generation.
    """
    return _integ_constructed_capacity_res_elec_tw()


_integ_constructed_capacity_res_elec_tw = Integ(
    lambda: res_elec_capacity_under_construction_tw() - wear_res_elec(),
    lambda: table_hist_capacity_res_elec(1995),
    "_integ_constructed_capacity_res_elec_tw",
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
    name="Cp RES elec",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"min_cp_baseload_res": 1, "cpini_res_elec": 1},
)
def cp_res_elec():
    """
    Capacity factor of RES technologies (after accounting for the overcapacities required to manage the intermittency of RES elec variables). MAX(min Cp baseload RES[RES elec], "Cp-ini RES elec"[RES elec]*Cp exogenous RES elec reduction[RES elec])
    """
    return np.maximum(min_cp_baseload_res(), cpini_res_elec())


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
    "World",
    "cp_initial_res_elec*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    {"RES elec": _subscript_dict["RES elec"]},
    "_ext_constant_cpini_res_elec",
)


@component.add(
    name="curtailment and storage share variable RES",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_curtailment_and_storage_share_variable_res",
        "__lookup__": "_ext_lookup_curtailment_and_storage_share_variable_res",
    },
)
def curtailment_and_storage_share_variable_res(x, final_subs=None):
    return _ext_lookup_curtailment_and_storage_share_variable_res(x, final_subs)


_ext_lookup_curtailment_and_storage_share_variable_res = ExtLookup(
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "year_RES_power",
    "share_curtailment",
    {},
    _root,
    {},
    "_ext_lookup_curtailment_and_storage_share_variable_res",
)


@component.add(
    name="curtailment RES",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={"time": 4, "curtailment_and_storage_share_variable_res": 4},
)
def curtailment_res():
    value = xr.DataArray(
        np.nan, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
    )
    value.loc[["hydro"]] = 0
    value.loc[["geot elec"]] = 0
    value.loc[["solid bioE elec"]] = 0
    value.loc[["oceanic"]] = 0
    value.loc[["wind onshore"]] = curtailment_and_storage_share_variable_res(time())
    value.loc[["wind offshore"]] = curtailment_and_storage_share_variable_res(time())
    value.loc[["solar PV"]] = curtailment_and_storage_share_variable_res(time())
    value.loc[["CSP"]] = curtailment_and_storage_share_variable_res(time())
    return value


@component.add(
    name="end hist data",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_end_hist_data"},
)
def end_hist_data():
    """
    End historical data year
    """
    return _ext_constant_end_hist_data()


_ext_constant_end_hist_data = ExtConstant(
    "../energy.xlsx",
    "World",
    "end_hist_data",
    {},
    _root,
    {},
    "_ext_constant_end_hist_data",
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
    name="Installed capacity RES elec",
    units="TW",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "installed_capacity_res_elec_policies": 2,
        "max_potential_res_elec_twe": 2,
    },
)
def installed_capacity_res_elec():
    """
    Introdue the limitation of the techno-ecological potential
    """
    return if_then_else(
        installed_capacity_res_elec_policies() >= max_potential_res_elec_twe(),
        lambda: max_potential_res_elec_twe(),
        lambda: installed_capacity_res_elec_policies(),
    )


@component.add(
    name="Installed capacity RES elec policies",
    units="TW",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "end_hist_data": 5,
        "table_hist_capacity_res_elec": 3,
        "p_power": 2,
        "start_year_p_growth_res_elec": 3,
    },
)
def installed_capacity_res_elec_policies():
    return if_then_else(
        time() < end_hist_data(),
        lambda: table_hist_capacity_res_elec(time()),
        lambda: if_then_else(
            time() < start_year_p_growth_res_elec(),
            lambda: table_hist_capacity_res_elec(end_hist_data())
            + (
                (
                    p_power(start_year_p_growth_res_elec())
                    - table_hist_capacity_res_elec(end_hist_data())
                )
                / (start_year_p_growth_res_elec() - end_hist_data())
            )
            * (time() - end_hist_data()),
            lambda: p_power(time()),
        ),
    )


@component.add(
    name="lifetime RES elec",
    units="years",
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
    "World",
    "minimum_cp_baseload_res*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    {"RES elec": _subscript_dict["RES elec"]},
    "_ext_constant_min_cp_baseload_res",
)


@component.add(
    name="new RES installed capacity",
    units="TW/year",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "res_installed_capacity_year_delayed": 1,
        "installed_capacity_res_elec": 1,
    },
)
def new_res_installed_capacity():
    return if_then_else(
        time() > 1995,
        lambda: installed_capacity_res_elec() - res_installed_capacity_year_delayed(),
        lambda: xr.DataArray(
            0.1, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
        ),
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
    """
    Desired installed power (TW)
    """
    return _ext_lookup_p_power(x, final_subs)


_ext_lookup_p_power = ExtLookup(
    "../../scenarios/scen_w.xlsx",
    "NZP",
    "year_RES_power",
    "p_RES_power",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    {"RES elec": _subscript_dict["RES elec"]},
    "_ext_lookup_p_power",
)


@component.add(
    name="potential generation RES elec TWh",
    units="TWh",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "installed_capacity_res_elec": 1,
        "cp_res_elec": 1,
        "curtailment_res": 1,
        "twe_per_twh": 1,
    },
)
def potential_generation_res_elec_twh():
    """
    Potential generation of electricity by RES technology given the installed capacity.
    """
    return (
        installed_capacity_res_elec()
        * cp_res_elec()
        * (1 - curtailment_res())
        / twe_per_twh()
    )


@component.add(
    name="potential RES elec after intermitt TWh",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_potential_res_elec_twe": 1,
        "cp_baseload_reduction": 1,
        "twe_per_twh": 1,
    },
)
def potential_res_elec_after_intermitt_twh():
    return max_potential_res_elec_twe() * cp_baseload_reduction() / twe_per_twh()


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
    name="real Cp RES elec",
    units="Dmnl",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "cp_res_elec": 1,
        "real_generation_res_elec_twh": 1,
        "installed_capacity_res_elec": 2,
        "twe_per_twh": 1,
    },
)
def real_cp_res_elec():
    return if_then_else(
        time() < 2015,
        lambda: cp_res_elec(),
        lambda: if_then_else(
            installed_capacity_res_elec() == 0,
            lambda: xr.DataArray(
                0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
            ),
            lambda: real_generation_res_elec_twh()
            * twe_per_twh()
            / installed_capacity_res_elec(),
        ),
    )


@component.add(
    name="real generation RES elec TWh",
    units="TWh",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_generation_res_elec_twh": 1, "res_elec_tot_overcapacity": 1},
)
def real_generation_res_elec_twh():
    """
    Electricity generation by RES technology. potential generation RES elec TWh[RES elec]*(1-RES elec tot overcapacity)
    """
    return potential_generation_res_elec_twh() * zidz(
        1, 1 + res_elec_tot_overcapacity()
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
    name="replacement capacity RES elec",
    units="TW/year",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "wear_res_elec": 1, "res_elec_tot_overcapacity": 1},
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
        lambda: wear_res_elec() * (1 - res_elec_tot_overcapacity()),
    )


@component.add(
    name="RES elec capacity under construction TW",
    units="TW/year",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "res_elec_planned_capacity_replacement": 1,
        "new_res_installed_capacity": 1,
        "time_construction_res_elec": 1,
    },
)
def res_elec_capacity_under_construction_tw():
    """
    RES infraestructure for electricity generation capacity under construction.
    """
    return (
        res_elec_planned_capacity_replacement() + new_res_installed_capacity()
    ) / time_construction_res_elec()


@component.add(
    name="RES elec planned capacity replacement",
    units="TW",
    subscripts=["RES elec"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_res_elec_planned_capacity_replacement": 1},
    other_deps={
        "_integ_res_elec_planned_capacity_replacement": {
            "initial": {},
            "step": {
                "replacement_capacity_res_elec": 1,
                "res_elec_capacity_under_construction_tw": 1,
            },
        }
    },
)
def res_elec_planned_capacity_replacement():
    """
    Planned capacity of RES for electricity.
    """
    return _integ_res_elec_planned_capacity_replacement()


_integ_res_elec_planned_capacity_replacement = Integ(
    lambda: replacement_capacity_res_elec() - res_elec_capacity_under_construction_tw(),
    lambda: xr.DataArray(0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]),
    "_integ_res_elec_planned_capacity_replacement",
)


@component.add(
    name="RES elec tot overcapacity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_tot_generation_res_elec_twh": 1,
        "fe_real_tot_generation_res_elec_twh": 1,
    },
)
def res_elec_tot_overcapacity():
    """
    Overcapacity for each technology RES for electricity taking into account the installed capacity and the real generation.
    """
    return (
        zidz(
            potential_tot_generation_res_elec_twh(),
            fe_real_tot_generation_res_elec_twh(),
        )
        - 1
    )


@component.add(
    name="RES installed capacity delayed",
    units="TW",
    subscripts=["RES elec"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_res_installed_capacity_delayed": 1},
    other_deps={
        "_delayfixed_res_installed_capacity_delayed": {
            "initial": {"table_hist_capacity_res_elec": 1, "time_step": 1},
            "step": {"installed_capacity_res_elec": 1},
        }
    },
)
def res_installed_capacity_delayed():
    return _delayfixed_res_installed_capacity_delayed()


_delayfixed_res_installed_capacity_delayed = DelayFixed(
    lambda: installed_capacity_res_elec(),
    lambda: time_step(),
    lambda: table_hist_capacity_res_elec(1995),
    time_step,
    "_delayfixed_res_installed_capacity_delayed",
)


@component.add(
    name="RES installed capacity year delayed",
    units="TW",
    subscripts=["RES elec"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_res_installed_capacity_year_delayed": 1},
    other_deps={
        "_delayfixed_res_installed_capacity_year_delayed": {
            "initial": {"time": 1},
            "step": {"installed_capacity_res_elec": 1},
        }
    },
)
def res_installed_capacity_year_delayed():
    return _delayfixed_res_installed_capacity_year_delayed()


_delayfixed_res_installed_capacity_year_delayed = DelayFixed(
    lambda: installed_capacity_res_elec(),
    lambda: time(),
    lambda: xr.DataArray(0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]),
    time_step,
    "_delayfixed_res_installed_capacity_year_delayed",
)


@component.add(
    name="Start year P growth RES elec",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_start_year_p_growth_res_elec"},
)
def start_year_p_growth_res_elec():
    """
    Start year of the policy growth of RES technologies for generating electricity.
    """
    return _ext_constant_start_year_p_growth_res_elec()


_ext_constant_start_year_p_growth_res_elec = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "NZP",
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
    depends_on={
        "__external__": "_ext_lookup_table_hist_capacity_res_elec",
        "__lookup__": "_ext_lookup_table_hist_capacity_res_elec",
    },
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
    units="year",
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
    units="year",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time_construction_res_elec": 1,
        "time_step": 1,
        "time": 1,
        "time_planification_res_elec": 1,
    },
)
def total_time_planconstr_res_elec():
    return np.maximum(time_construction_res_elec(), time_step()) + np.maximum(
        time_planification_res_elec(), time()
    )


@component.add(
    name="wear RES elec",
    units="TW/year",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "lifetime_res_elec": 1,
        "constructed_capacity_res_elec_tw": 1,
    },
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
        lambda: constructed_capacity_res_elec_tw() / lifetime_res_elec(),
    )
