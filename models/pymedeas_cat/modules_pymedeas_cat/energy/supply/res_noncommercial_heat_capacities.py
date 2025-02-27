"""
Module energy.supply.res_noncommercial_heat_capacities
Translated using PySD version 3.14.2
"""

@component.add(
    name='"abundance_RES_heat-nc"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fed_heatnc_ej": 3, "fe_real_supply_res_for_heatnc_tot_ej": 1},
)
def abundance_res_heatnc():
    """
    The parameter abundance varies between (1;0). The closest to 1 indicates that heat generation from RES is far to cover to whole heat demand, if "abundance RES heat"=0 it means that RES heat cover the whole heat demand. IF THEN ELSE(Total FED Heat EJ delayed 1yr=0,0, IF THEN ELSE(Total FED Heat EJ delayed 1yr > FE real supply RES for heat tot EJ, (Total FED Heat EJ delayed 1yr-FE real supply RES for heat tot EJ)/Total FED Heat EJ delayed 1yr, 0))
    """
    return if_then_else(
        total_fed_heatnc_ej() == 0,
        lambda: 0,
        lambda: zidz(
            total_fed_heatnc_ej() - fe_real_supply_res_for_heatnc_tot_ej(),
            total_fed_heatnc_ej(),
        ),
    )


@component.add(
    name='"abundance_RES_heat-nc2"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_res_heatnc": 1},
)
def abundance_res_heatnc2():
    """
    Adaptation of the parameter abundance for better behaviour of the model.
    """
    return float(np.sqrt(abundance_res_heatnc()))


@component.add(
    name='"adapt_growth_RES_for_heat-nc"',
    units="1/year",
    subscripts=["RES_heat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 4,
        "past_res_growth_for_heatnc": 4,
        "start_year_p_growth_res_heat": 3,
        "p_res_for_heat": 2,
        "target_year_p_growth_res_heat": 2,
    },
)
def adapt_growth_res_for_heatnc():
    """
    Modeling of a soft transition from current historic annual growth to reach the policy-objective in the target yeat.
    """
    return if_then_else(
        time() < 2014,
        lambda: past_res_growth_for_heatnc(),
        lambda: if_then_else(
            time() < start_year_p_growth_res_heat(),
            lambda: past_res_growth_for_heatnc(),
            lambda: if_then_else(
                time() < target_year_p_growth_res_heat(),
                lambda: past_res_growth_for_heatnc()
                + (p_res_for_heat() - past_res_growth_for_heatnc())
                * (time() - start_year_p_growth_res_heat())
                / (target_year_p_growth_res_heat() - start_year_p_growth_res_heat()),
                lambda: p_res_for_heat(),
            ),
        ),
    )


@component.add(
    name="Cp_RES_for_heat",
    units="Dmnl",
    subscripts=["RES_heat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"cpini_res_for_heat": 1, "shortage_bioe_for_heat": 1},
)
def cp_res_for_heat():
    return cpini_res_for_heat() * shortage_bioe_for_heat()


@component.add(
    name='"Cp-ini_RES_for_heat"',
    units="Dmnl",
    subscripts=["RES_heat"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_cpini_res_for_heat"},
)
def cpini_res_for_heat():
    return _ext_constant_cpini_res_for_heat()


_ext_constant_cpini_res_for_heat = ExtConstant(
    r"../energy.xlsx",
    "Catalonia",
    "cp_initial_res_heat*",
    {"RES_heat": _subscript_dict["RES_heat"]},
    _root,
    {"RES_heat": _subscript_dict["RES_heat"]},
    "_ext_constant_cpini_res_for_heat",
)


@component.add(
    name='"FE_real_generation_RES_heat-nc"',
    units="EJ/year",
    subscripts=["RES_heat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_fes_res_for_heatnc_ej": 1, "res_heatnc_tot_overcapacity": 1},
)
def fe_real_generation_res_heatnc():
    """
    Non-commercial heat generation by RES technology.
    """
    return potential_fes_res_for_heatnc_ej() * (1 - res_heatnc_tot_overcapacity())


@component.add(
    name='"FE_real_supply_RES_for_heat-nc_tot_EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fed_heatnc_ej": 1, "potential_fes_tot_res_for_heatnc_ej": 1},
)
def fe_real_supply_res_for_heatnc_tot_ej():
    """
    Total final energy supply delivered by RES for non-commercial heat.
    """
    return float(
        np.minimum(
            float(np.maximum(total_fed_heatnc_ej(), 0)),
            potential_fes_tot_res_for_heatnc_ej(),
        )
    )


@component.add(
    name='"Historic_RES_capacity_for_heat-nc"',
    units="TW",
    subscripts=["RES_heat"],
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_res_capacity_for_heatnc",
        "__lookup__": "_ext_lookup_historic_res_capacity_for_heatnc",
    },
)
def historic_res_capacity_for_heatnc(x, final_subs=None):
    """
    Historic installed capacity of RES technologies for non-commercial heat generation.
    """
    return _ext_lookup_historic_res_capacity_for_heatnc(x, final_subs)


_ext_lookup_historic_res_capacity_for_heatnc = ExtLookup(
    r"../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_res_capacity_for_heat_non_commercial",
    {"RES_heat": _subscript_dict["RES_heat"]},
    _root,
    {"RES_heat": _subscript_dict["RES_heat"]},
    "_ext_lookup_historic_res_capacity_for_heatnc",
)


@component.add(
    name='"initial_value_RES_for_heat-nc"',
    units="TW",
    subscripts=["RES_heat"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_initial_value_res_for_heatnc"},
)
def initial_value_res_for_heatnc():
    """
    RES supply by technology for non-commercial heat in the year 1995.
    """
    return _ext_constant_initial_value_res_for_heatnc()


_ext_constant_initial_value_res_for_heatnc = ExtConstant(
    r"../energy.xlsx",
    "Catalonia",
    "initial_res_capacity_for_heat_non_commercial*",
    {"RES_heat": _subscript_dict["RES_heat"]},
    _root,
    {"RES_heat": _subscript_dict["RES_heat"]},
    "_ext_constant_initial_value_res_for_heatnc",
)


@component.add(
    name='"installed_capacity_RES_heat-nc_TW"',
    units="TW",
    subscripts=["RES_heat"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_installed_capacity_res_heatnc_tw": 1},
    other_deps={
        "_integ_installed_capacity_res_heatnc_tw": {
            "initial": {"initial_value_res_for_heatnc": 1},
            "step": {
                "new_res_capacity_for_heatnc_tw": 1,
                "replacement_res_for_heatnc_tw": 1,
                "wear_res_capacity_for_heatnc_tw": 1,
            },
        }
    },
)
def installed_capacity_res_heatnc_tw():
    """
    Installed capacity of RES for non-commercial heat.
    """
    return _integ_installed_capacity_res_heatnc_tw()


_integ_installed_capacity_res_heatnc_tw = Integ(
    lambda: new_res_capacity_for_heatnc_tw()
    + replacement_res_for_heatnc_tw()
    - wear_res_capacity_for_heatnc_tw(),
    lambda: initial_value_res_for_heatnc(),
    "_integ_installed_capacity_res_heatnc_tw",
)


@component.add(
    name='"new_RES_capacity_for_heat-nc_TW"',
    units="TW/year",
    subscripts=["RES_heat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "historic_res_capacity_for_heatnc": 2,
        "time_step": 2,
        "adapt_growth_res_for_heatnc": 1,
        "remaining_potential_constraint_on_new_res_heat_capacity": 1,
        "installed_capacity_res_heatnc_tw": 1,
        "abundance_res_heatnc2": 1,
    },
)
def new_res_capacity_for_heatnc_tw():
    """
    New annual installed capacity of RES technologies for non-commercial heat.
    """
    return (
        if_then_else(
            time() < 2013,
            lambda: (
                historic_res_capacity_for_heatnc(time() + time_step())
                - historic_res_capacity_for_heatnc(time())
            )
            / time_step(),
            lambda: adapt_growth_res_for_heatnc()
            * installed_capacity_res_heatnc_tw()
            * remaining_potential_constraint_on_new_res_heat_capacity(),
        )
        * abundance_res_heatnc2()
    )


@component.add(
    name='"past_RES_growth_for_heat-nc"',
    units="1/year",
    subscripts=["RES_heat"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_past_res_growth_for_heatnc"},
)
def past_res_growth_for_heatnc():
    """
    Historic annual average growth.
    """
    return _ext_constant_past_res_growth_for_heatnc()


_ext_constant_past_res_growth_for_heatnc = ExtConstant(
    r"../energy.xlsx",
    "Catalonia",
    "historic_growth_res_for_heat_nc*",
    {"RES_heat": _subscript_dict["RES_heat"]},
    _root,
    {"RES_heat": _subscript_dict["RES_heat"]},
    "_ext_constant_past_res_growth_for_heatnc",
)


@component.add(
    name='"PES_DEM_RES_for_heat-nc_by_techn"',
    units="EJ/year",
    subscripts=["RES_heat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fe_real_generation_res_heatnc": 3, "efficiency_res_heat": 1},
)
def pes_dem_res_for_heatnc_by_techn():
    """
    Primary energy supply of RES technologies for non-commercial heat (Direct Energy Method convention of accounting for primary energy).
    """
    value = xr.DataArray(
        np.nan, {"RES_heat": _subscript_dict["RES_heat"]}, ["RES_heat"]
    )
    value.loc[["geot_heat"]] = float(fe_real_generation_res_heatnc().loc["geot_heat"])
    value.loc[["solar_heat"]] = float(fe_real_generation_res_heatnc().loc["solar_heat"])
    value.loc[["solid_bioE_heat"]] = float(
        fe_real_generation_res_heatnc().loc["solid_bioE_heat"]
    ) / float(efficiency_res_heat().loc["solid_bioE_heat"])
    return value


@component.add(
    name='"PES_RES_for_heat-nc_by_techn"',
    units="EJ/year",
    subscripts=["RES_heat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fe_real_generation_res_heatnc": 1, "efficiency_res_heat": 1},
)
def pes_res_for_heatnc_by_techn():
    """
    Primary energy supply of RES technologies for non-commercial heat.
    """
    return fe_real_generation_res_heatnc() / efficiency_res_heat()


@component.add(
    name='"potential_FES_RES_for_heat-nc_EJ"',
    units="EJ/year",
    subscripts=["RES_heat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_fes_res_for_heatnc_twh": 1, "ej_per_twh": 1},
)
def potential_fes_res_for_heatnc_ej():
    """
    Potential final energy supply renewables for non-commercial heat given the installed capacity.
    """
    return potential_fes_res_for_heatnc_twh() * ej_per_twh()


@component.add(
    name='"potential_FES_RES_for_heat-nc_TWh"',
    units="TWh/year",
    subscripts=["RES_heat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "installed_capacity_res_heatnc_tw": 1,
        "efficiency_res_heat": 1,
        "cp_res_for_heat": 1,
        "twe_per_twh": 1,
    },
)
def potential_fes_res_for_heatnc_twh():
    """
    Potential final energy supply renewables for non-commercial heat given the installed capacity.
    """
    return (
        installed_capacity_res_heatnc_tw()
        * efficiency_res_heat()
        * cp_res_for_heat()
        / twe_per_twh()
    )


@component.add(
    name='"potential_FES_tot_RES_for_heat-nc_EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_fes_res_for_heatnc_ej": 1},
)
def potential_fes_tot_res_for_heatnc_ej():
    """
    Potential total final energy supply renewables for non-commercial heat given the installed capacity.
    """
    return sum(
        potential_fes_res_for_heatnc_ej().rename({"RES_heat": "RES_heat!"}),
        dim=["RES_heat!"],
    )


@component.add(
    name='"replacement_RES_for_heat-nc"',
    units="Dmnl",
    subscripts=["RES_heat"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_replacement_res_for_heatnc"},
)
def replacement_res_for_heatnc():
    """
    If =1, we asume that all the power that reaches the end of its lifetime is replaced.
    """
    return _ext_constant_replacement_res_for_heatnc()


_ext_constant_replacement_res_for_heatnc = ExtConstant(
    r"../energy.xlsx",
    "Global",
    "replacement_rate_res_for_heat*",
    {"RES_heat": _subscript_dict["RES_heat"]},
    _root,
    {"RES_heat": _subscript_dict["RES_heat"]},
    "_ext_constant_replacement_res_for_heatnc",
)


@component.add(
    name='"replacement_RES_for_heat-nc_TW"',
    units="TW/year",
    subscripts=["RES_heat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "wear_res_capacity_for_heatnc_tw": 1,
        "replacement_res_for_heatnc": 1,
        "res_heatnc_tot_overcapacity": 1,
        "shortage_bioe_for_heat": 1,
    },
)
def replacement_res_for_heatnc_tw():
    """
    Annual replacement of RES for non-commercial heat by technology.
    """
    return (
        wear_res_capacity_for_heatnc_tw()
        * replacement_res_for_heatnc()
        * (1 - res_heatnc_tot_overcapacity())
        * shortage_bioe_for_heat() ** 2
    )


@component.add(
    name='"RES_heat-nc_tot_overcapacity"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_fes_tot_res_for_heatnc_ej": 3,
        "fe_real_supply_res_for_heatnc_tot_ej": 1,
    },
)
def res_heatnc_tot_overcapacity():
    """
    Overcapacity for each technology RES for heat-nc taking into account the installed capacity and the real generation.
    """
    return if_then_else(
        potential_fes_tot_res_for_heatnc_ej() == 0,
        lambda: 0,
        lambda: (
            potential_fes_tot_res_for_heatnc_ej()
            - fe_real_supply_res_for_heatnc_tot_ej()
        )
        / potential_fes_tot_res_for_heatnc_ej(),
    )


@component.add(
    name='"wear_RES_capacity_for_heat-nc_TW"',
    units="TW/year",
    subscripts=["RES_heat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"installed_capacity_res_heatnc_tw": 1, "life_time_res_for_heat": 1},
)
def wear_res_capacity_for_heatnc_tw():
    """
    Decommission of the capacity that reachs the end of its lifetime.
    """
    return installed_capacity_res_heatnc_tw() / life_time_res_for_heat()
