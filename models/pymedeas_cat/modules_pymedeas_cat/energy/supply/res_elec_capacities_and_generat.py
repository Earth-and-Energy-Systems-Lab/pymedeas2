"""
Module energy.supply.res_elec_capacities_and_generat
Translated using PySD version 3.14.2
"""

@component.add(
    name="abundance_RES_elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_fe_elec_demand_after_priorities": 4,
        "fe_real_tot_generation_res_elec": 2,
    },
)
def abundance_res_elec():
    """
    The parameter abundance varies between (1;0). The closest to 1 indicates that electricity generation from RES is far to cover to whole electricity demand, if "abundance RES elec"=0 it means that RES elec cover the whole electricity demand.
    """
    return if_then_else(
        total_fe_elec_demand_after_priorities() == 0,
        lambda: 0,
        lambda: if_then_else(
            total_fe_elec_demand_after_priorities() > fe_real_tot_generation_res_elec(),
            lambda: (
                total_fe_elec_demand_after_priorities()
                - fe_real_tot_generation_res_elec()
            )
            / total_fe_elec_demand_after_priorities(),
            lambda: 0,
        ),
    )


@component.add(
    name="Cp_baseload_reduction",
    units="Dmnl",
    subscripts=["RES_elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"cp_res_elec": 1, "cpini_res_elec": 1},
)
def cp_baseload_reduction():
    return zidz(cp_res_elec(), cpini_res_elec())


@component.add(
    name="Cp_RES_elec",
    units="Dmnl",
    subscripts=["RES_elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "min_cp_baseload_res": 1,
        "cpini_res_elec": 1,
        "shortage_bioe_for_elec": 1,
    },
)
def cp_res_elec():
    """
    Capacity factor of RES technologies (after accounting for the overcapacities required to manage the intermittency of RES elec variables).
    """
    return np.maximum(
        min_cp_baseload_res(), cpini_res_elec() * shortage_bioe_for_elec()
    )


@component.add(
    name='"Cp-ini_RES_elec"',
    units="Dmnl",
    subscripts=["RES_elec"],
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
    r"../energy.xlsx",
    "Catalonia",
    "cp_initial_res_elec*",
    {"RES_elec": _subscript_dict["RES_elec"]},
    _root,
    {"RES_elec": _subscript_dict["RES_elec"]},
    "_ext_constant_cpini_res_elec",
)


@component.add(
    name="curtailment_and_storage_share_variable_RES",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_curtailment_and_storage_share_variable_res",
        "__lookup__": "_ext_lookup_curtailment_and_storage_share_variable_res",
    },
)
def curtailment_and_storage_share_variable_res(x, final_subs=None):
    """
    Share of curtailment and storage of variable RES
    """
    return _ext_lookup_curtailment_and_storage_share_variable_res(x, final_subs)


_ext_lookup_curtailment_and_storage_share_variable_res = ExtLookup(
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "year_RES_power",
    "share_curtailment",
    {},
    _root,
    {},
    "_ext_lookup_curtailment_and_storage_share_variable_res",
)


@component.add(
    name="curtailment_RES",
    units="Dmnl",
    subscripts=["RES_elec"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={"time": 4, "curtailment_and_storage_share_variable_res": 4},
)
def curtailment_res():
    value = xr.DataArray(
        np.nan, {"RES_elec": _subscript_dict["RES_elec"]}, ["RES_elec"]
    )
    value.loc[["hydro"]] = 0
    value.loc[["geot_elec"]] = 0
    value.loc[["solid_bioE_elec"]] = 0
    value.loc[["oceanic"]] = 0
    value.loc[["wind_onshore"]] = curtailment_and_storage_share_variable_res(time())
    value.loc[["wind_offshore"]] = curtailment_and_storage_share_variable_res(time())
    value.loc[["solar_PV"]] = curtailment_and_storage_share_variable_res(time())
    value.loc[["CSP"]] = curtailment_and_storage_share_variable_res(time())
    return value


@component.add(
    name="end_hist_data",
    units="year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_end_hist_data"},
)
def end_hist_data():
    return _ext_constant_end_hist_data()


_ext_constant_end_hist_data = ExtConstant(
    r"../energy.xlsx",
    "Catalonia",
    "end_hist_data",
    {},
    _root,
    {},
    "_ext_constant_end_hist_data",
)


@component.add(
    name="FE_real_tot_generation_RES_elec",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_fe_elec_demand_after_priorities": 1,
        "potential_tot_generation_after_curtailment_res_elec_twh": 1,
    },
)
def fe_real_tot_generation_res_elec():
    return float(
        np.minimum(
            float(np.maximum(total_fe_elec_demand_after_priorities(), 0)),
            potential_tot_generation_after_curtailment_res_elec_twh(),
        )
    )


@component.add(
    name="initial_instal_cap_RES_elec",
    units="TW",
    subscripts=["RES_elec"],
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
    r"../energy.xlsx",
    "Catalonia",
    "initial_installed_capacity_res_for_electricity*",
    {"RES_elec": _subscript_dict["RES_elec"]},
    _root,
    {"RES_elec": _subscript_dict["RES_elec"]},
    "_ext_constant_initial_instal_cap_res_elec",
)


@component.add(
    name="installed_capacity_RES_elec",
    units="TW",
    subscripts=["RES_elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"installed_capacity_res_elec_policies": 2, "max_res_elec_twe": 2},
)
def installed_capacity_res_elec():
    return if_then_else(
        installed_capacity_res_elec_policies() >= max_res_elec_twe(),
        lambda: max_res_elec_twe(),
        lambda: installed_capacity_res_elec_policies(),
    )


@component.add(
    name="Installed_capacity_RES_elec_delayed",
    units="TW",
    subscripts=["RES_elec"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_installed_capacity_res_elec_delayed": 1},
    other_deps={
        "_delayfixed_installed_capacity_res_elec_delayed": {
            "initial": {"table_hist_capacity_res_elec": 1, "time_step": 1},
            "step": {"installed_capacity_res_elec": 1},
        }
    },
)
def installed_capacity_res_elec_delayed():
    return _delayfixed_installed_capacity_res_elec_delayed()


_delayfixed_installed_capacity_res_elec_delayed = DelayFixed(
    lambda: installed_capacity_res_elec(),
    lambda: time_step(),
    lambda: table_hist_capacity_res_elec(1995),
    time_step,
    "_delayfixed_installed_capacity_res_elec_delayed",
)


@component.add(
    name="Installed_capacity_RES_elec_policies",
    units="TW",
    subscripts=["RES_elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "end_hist_data": 5,
        "table_hist_capacity_res_elec": 3,
        "start_year_p_growth_res_elec": 3,
        "p_power": 2,
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
    name="lifetime_RES_elec",
    units="Years",
    subscripts=["RES_elec"],
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
    r"../energy.xlsx",
    "Global",
    "lifetime_res_elec*",
    {"RES_elec": _subscript_dict["RES_elec"]},
    _root,
    {"RES_elec": _subscript_dict["RES_elec"]},
    "_ext_constant_lifetime_res_elec",
)


@component.add(
    name="min_Cp_baseload_RES",
    units="Dmnl",
    subscripts=["RES_elec"],
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
    r"../energy.xlsx",
    "Catalonia",
    "minimum_cp_baseload_res*",
    {"RES_elec": _subscript_dict["RES_elec"]},
    _root,
    {"RES_elec": _subscript_dict["RES_elec"]},
    "_ext_constant_min_cp_baseload_res",
)


@component.add(
    name="new_RES_installed_capacity",
    units="TW/year",
    subscripts=["RES_elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "res_installed_capacity_year_delayed": 1,
        "installed_capacity_res_elec": 1,
        "nvs_1_year": 1,
    },
)
def new_res_installed_capacity():
    return (
        if_then_else(
            time() > 1995,
            lambda: installed_capacity_res_elec()
            - res_installed_capacity_year_delayed(),
            lambda: xr.DataArray(
                0, {"RES_elec": _subscript_dict["RES_elec"]}, ["RES_elec"]
            ),
        )
        / nvs_1_year()
    )


@component.add(
    name="P_power",
    units="TW",
    subscripts=["RES_elec"],
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
    r"../../scenarios/scen_cat.xlsx",
    "NZP",
    "year_RES_power",
    "p_RES_power",
    {"RES_elec": _subscript_dict["RES_elec"]},
    _root,
    {"RES_elec": _subscript_dict["RES_elec"]},
    "_ext_lookup_p_power",
)


@component.add(
    name="potential_generation_RES_elec_TWh",
    units="TWh/year",
    subscripts=["RES_elec"],
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
    name="potential_RES_elec_after_intermitt_TWh",
    units="TWh/year",
    subscripts=["RES_elec"],
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
    name="potential_tot_generation_after_curtailment_RES_elec_TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_tot_generation_res_elec_twh": 1,
        "time": 1,
        "curtailment_and_storage_share_variable_res": 1,
    },
)
def potential_tot_generation_after_curtailment_res_elec_twh():
    return potential_tot_generation_res_elec_twh() * (
        1 - curtailment_and_storage_share_variable_res(time())
    )


@component.add(
    name="potential_tot_generation_RES_elec_TWh",
    units="TWh/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_generation_res_elec_twh": 1},
)
def potential_tot_generation_res_elec_twh():
    """
    Total potential generation of electricity from RES given the installed capacity.
    """
    return sum(
        potential_generation_res_elec_twh().rename({"RES_elec": "RES_elec!"}),
        dim=["RES_elec!"],
    )


@component.add(
    name="real_Cp_RES_elec",
    units="Dmnl",
    subscripts=["RES_elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "cp_res_elec": 1,
        "replaced_capacity_res_elec_tw": 2,
        "real_generation_res_elec_twh": 1,
        "twe_per_twh": 1,
    },
)
def real_cp_res_elec():
    return if_then_else(
        time() < 2015,
        lambda: cp_res_elec(),
        lambda: if_then_else(
            replaced_capacity_res_elec_tw() == 0,
            lambda: xr.DataArray(
                0, {"RES_elec": _subscript_dict["RES_elec"]}, ["RES_elec"]
            ),
            lambda: real_generation_res_elec_twh()
            * twe_per_twh()
            / replaced_capacity_res_elec_tw(),
        ),
    )


@component.add(
    name="real_generation_RES_elec_TWh",
    units="TWh/year",
    subscripts=["RES_elec"],
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
        * zidz(1, 1 + res_elec_tot_overcapacity())
        * shortage_bioe_for_elec()
    )


@component.add(
    name="remaining_potential_RES_elec_after_intermitt",
    units="Dmnl",
    subscripts=["RES_elec"],
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
            0, {"RES_elec": _subscript_dict["RES_elec"]}, ["RES_elec"]
        ),
    )


@component.add(
    name="replaced_capacity_RES_elec_TW",
    units="TW",
    subscripts=["RES_elec"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_replaced_capacity_res_elec_tw": 1},
    other_deps={
        "_integ_replaced_capacity_res_elec_tw": {
            "initial": {"initial_instal_cap_res_elec": 1},
            "step": {"res_elec_capacity_under_construction_tw": 1, "wear_res_elec": 1},
        }
    },
)
def replaced_capacity_res_elec_tw():
    """
    Annual installed capacity of RES elec technologies for electricity generation.
    """
    return _integ_replaced_capacity_res_elec_tw()


_integ_replaced_capacity_res_elec_tw = Integ(
    lambda: res_elec_capacity_under_construction_tw() - wear_res_elec(),
    lambda: initial_instal_cap_res_elec(),
    "_integ_replaced_capacity_res_elec_tw",
)


@component.add(
    name="replacement_capacity_RES_elec",
    units="TW/year",
    subscripts=["RES_elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "res_elec_tot_overcapacity": 1,
        "wear_res_elec": 1,
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
                0, {"RES_elec": _subscript_dict["RES_elec"]}, ["RES_elec"]
            ),
            lambda: wear_res_elec() * (1 - res_elec_tot_overcapacity()),
        )
        * shortage_bioe_for_elec() ** 2
    )


@component.add(
    name="RES_elec_capacity_under_construction_TW",
    units="TW/year",
    subscripts=["RES_elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"new_res_installed_capacity": 1},
)
def res_elec_capacity_under_construction_tw():
    """
    RES infraestructure for electricity generation capacity under construction.
    """
    return new_res_installed_capacity()


@component.add(
    name="RES_elec_planned_capacity_TW",
    units="TW",
    subscripts=["RES_elec"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_res_elec_planned_capacity_tw": 1},
    other_deps={
        "_integ_res_elec_planned_capacity_tw": {
            "initial": {},
            "step": {
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
    lambda: replacement_capacity_res_elec() - res_elec_capacity_under_construction_tw(),
    lambda: xr.DataArray(0, {"RES_elec": _subscript_dict["RES_elec"]}, ["RES_elec"]),
    "_integ_res_elec_planned_capacity_tw",
)


@component.add(
    name="RES_elec_tot_overcapacity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_tot_generation_after_curtailment_res_elec_twh": 1,
        "fe_real_tot_generation_res_elec": 1,
    },
)
def res_elec_tot_overcapacity():
    """
    Overcapacity for each technology RES for electricity taking into account the installed capacity and the real generation.
    """
    return (
        zidz(
            potential_tot_generation_after_curtailment_res_elec_twh(),
            fe_real_tot_generation_res_elec(),
        )
        - 1
    )


@component.add(
    name="RES_installed_capacity_year_delayed",
    units="TW",
    subscripts=["RES_elec"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_res_installed_capacity_year_delayed": 1},
    other_deps={
        "_delayfixed_res_installed_capacity_year_delayed": {
            "initial": {},
            "step": {"installed_capacity_res_elec": 1},
        }
    },
)
def res_installed_capacity_year_delayed():
    return _delayfixed_res_installed_capacity_year_delayed()


_delayfixed_res_installed_capacity_year_delayed = DelayFixed(
    lambda: installed_capacity_res_elec(),
    lambda: 1,
    lambda: xr.DataArray(0, {"RES_elec": _subscript_dict["RES_elec"]}, ["RES_elec"]),
    time_step,
    "_delayfixed_res_installed_capacity_year_delayed",
)


@component.add(
    name="table_hist_capacity_RES_elec",
    units="TW",
    subscripts=["RES_elec"],
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
    r"../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_installed_capacity_res_for_electricity",
    {"RES_elec": _subscript_dict["RES_elec"]},
    _root,
    {"RES_elec": _subscript_dict["RES_elec"]},
    "_ext_lookup_table_hist_capacity_res_elec",
)


@component.add(
    name="threshold_remaining_potential_new_capacity",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def threshold_remaining_potential_new_capacity():
    """
    This threshold represents the level of the remaining potential that starts to affects the planification of new RES elec capacity (decreasing returns). Avoid problems of (erroneously) affecting past historical growth trends.
    """
    return 0.5


@component.add(
    name="time_construction_RES_elec",
    units="year",
    subscripts=["RES_elec"],
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
    r"../energy.xlsx",
    "Global",
    "construction_time_res_elec*",
    {"RES_elec": _subscript_dict["RES_elec"]},
    _root,
    {"RES_elec": _subscript_dict["RES_elec"]},
    "_ext_constant_time_construction_res_elec",
)


@component.add(
    name="time_planification_RES_elec",
    units="year",
    subscripts=["RES_elec"],
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
    r"../energy.xlsx",
    "Global",
    "planning_time_res_elec*",
    {"RES_elec": _subscript_dict["RES_elec"]},
    _root,
    {"RES_elec": _subscript_dict["RES_elec"]},
    "_ext_constant_time_planification_res_elec",
)


@component.add(
    name='"total_time_plan+constr_RES_elec"',
    units="year",
    subscripts=["RES_elec"],
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
    name="wear_RES_elec",
    units="TW/year",
    subscripts=["RES_elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "replaced_capacity_res_elec_tw": 1, "lifetime_res_elec": 1},
)
def wear_res_elec():
    """
    Depreciation of RES infraestructures.
    """
    return if_then_else(
        time() < 2015,
        lambda: xr.DataArray(
            0, {"RES_elec": _subscript_dict["RES_elec"]}, ["RES_elec"]
        ),
        lambda: replaced_capacity_res_elec_tw() / lifetime_res_elec(),
    )
