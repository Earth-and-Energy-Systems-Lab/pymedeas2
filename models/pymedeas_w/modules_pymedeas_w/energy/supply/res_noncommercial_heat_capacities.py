"""
Module res_noncommercial_heat_capacities
Translated using PySD version 3.0.0-dev
"""


@component.add(
    name='"abundance RES heat-nc"',
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
    name='"abundance RES heat-nc2"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_res_heatnc": 1},
)
def abundance_res_heatnc2():
    """
    Adaptation of the parameter abundance for better behaviour of the model.
    """
    return np.sqrt(abundance_res_heatnc())


@component.add(
    name='"adapt growth RES for heat-nc"',
    units="1/year",
    subscripts=["RES heat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "past_res_growth_for_heatnc": 3,
        "start_year_p_growth_res_heat": 2,
        "p_res_for_heat": 2,
    },
)
def adapt_growth_res_for_heatnc():
    """
    Modeling of a soft transition from current historic annual growth to reach the policy-objective 5 years later.
    """
    return if_then_else(
        time() < 2014,
        lambda: past_res_growth_for_heatnc(),
        lambda: if_then_else(
            time() < start_year_p_growth_res_heat(),
            lambda: past_res_growth_for_heatnc()
            + (p_res_for_heat() - past_res_growth_for_heatnc())
            * (time() - 2014)
            / (start_year_p_growth_res_heat() - 2014),
            lambda: p_res_for_heat(),
        ),
    )


@component.add(
    name="Cp RES for heat",
    units="Dmnl",
    subscripts=["RES heat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"cpini_res_for_heat": 1},
)
def cp_res_for_heat():
    return cpini_res_for_heat()


@component.add(
    name='"Cp-ini RES for heat"',
    units="Dmnl",
    subscripts=["RES heat"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_cpini_res_for_heat"},
)
def cpini_res_for_heat():
    return _ext_constant_cpini_res_for_heat()


_ext_constant_cpini_res_for_heat = ExtConstant(
    "../energy.xlsx",
    "World",
    "cp_initial_res_heat*",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    {"RES heat": _subscript_dict["RES heat"]},
    "_ext_constant_cpini_res_for_heat",
)


@component.add(
    name='"FE real generation RES heat-nc EJ"',
    units="EJ",
    subscripts=["RES heat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_fes_res_for_heatnc_ej": 1, "res_heatnc_tot_overcapacity": 1},
)
def fe_real_generation_res_heatnc_ej():
    """
    Non-commercial heat generation by RES technology.
    """
    return potential_fes_res_for_heatnc_ej() * (1 - res_heatnc_tot_overcapacity())


@component.add(
    name='"FE real supply RES for heat-nc tot EJ"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fed_heatnc_ej": 1, "potential_fes_tot_res_for_heatnc_ej": 1},
)
def fe_real_supply_res_for_heatnc_tot_ej():
    """
    Total final energy supply delivered by RES for non-commercial heat.
    """
    return np.minimum(
        np.maximum(total_fed_heatnc_ej(), 0), potential_fes_tot_res_for_heatnc_ej()
    )


@component.add(
    name='"Historic RES capacity for heat-nc"',
    units="TW",
    subscripts=["RES heat"],
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
    "../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_res_capacity_for_heat_non_commercial",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    {"RES heat": _subscript_dict["RES heat"]},
    "_ext_lookup_historic_res_capacity_for_heatnc",
)


@component.add(
    name='"initial value RES for heat-nc"',
    units="TW",
    subscripts=["RES heat"],
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
    "../energy.xlsx",
    "World",
    "initial_res_capacity_for_heat_non_commercial*",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    {"RES heat": _subscript_dict["RES heat"]},
    "_ext_constant_initial_value_res_for_heatnc",
)


@component.add(
    name='"installed capacity RES heat-nc TW"',
    units="TW",
    subscripts=["RES heat"],
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
    name='"new RES capacity for heat-nc TW"',
    units="TW/year",
    subscripts=["RES heat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 3,
        "historic_res_capacity_for_heatnc": 2,
        "installed_capacity_res_heatnc_tw": 1,
        "adapt_growth_res_for_heatnc": 1,
        "remaining_potential_constraint_on_new_res_heat_capacity": 1,
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
            lambda: historic_res_capacity_for_heatnc(time() + 1)
            - historic_res_capacity_for_heatnc(time()),
            lambda: adapt_growth_res_for_heatnc()
            * installed_capacity_res_heatnc_tw()
            * remaining_potential_constraint_on_new_res_heat_capacity(),
        )
        * abundance_res_heatnc2()
    )


@component.add(
    name='"past RES growth for heat-nc"',
    units="1/year",
    subscripts=["RES heat"],
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
    "../energy.xlsx",
    "World",
    "historic_growth_res_for_heat_nc*",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    {"RES heat": _subscript_dict["RES heat"]},
    "_ext_constant_past_res_growth_for_heatnc",
)


@component.add(
    name='"PES RES for heat-nc by techn"',
    units="EJ",
    subscripts=["RES heat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_real_generation_res_heatnc_ej": 3,
        "efficiency_res_heat": 3,
        "efficiency_solar_panels_for_heat": 1,
    },
)
def pes_res_for_heatnc_by_techn():
    """
    Primary energy supply of RES technologies for non-commercial heat.
    """
    value = xr.DataArray(
        np.nan, {"RES heat": _subscript_dict["RES heat"]}, ["RES heat"]
    )
    value.loc[["geot heat"]] = float(
        fe_real_generation_res_heatnc_ej().loc["geot heat"]
    ) / float(efficiency_res_heat().loc["geot heat"])
    value.loc[["solar heat"]] = (
        float(fe_real_generation_res_heatnc_ej().loc["solar heat"])
        * efficiency_solar_panels_for_heat()
        / float(efficiency_res_heat().loc["solar heat"])
    )
    value.loc[["solid bioE heat"]] = float(
        fe_real_generation_res_heatnc_ej().loc["solid bioE heat"]
    ) / float(efficiency_res_heat().loc["solid bioE heat"])
    return value


@component.add(
    name='"potential FES RES for heat-nc EJ"',
    units="EJ",
    subscripts=["RES heat"],
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
    name='"potential FES RES for heat-nc TWh"',
    units="TWh",
    subscripts=["RES heat"],
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
    name='"potential FES tot RES for heat-nc EJ"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_fes_res_for_heatnc_ej": 1},
)
def potential_fes_tot_res_for_heatnc_ej():
    """
    Potential total final energy supply renewables for non-commercial heat given the installed capacity.
    """
    return sum(
        potential_fes_res_for_heatnc_ej().rename({"RES heat": "RES heat!"}),
        dim=["RES heat!"],
    )


@component.add(
    name='"replacement RES for heat-nc TW"',
    units="TW/year",
    subscripts=["RES heat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "wear_res_capacity_for_heatnc_tw": 1,
        "replacement_res_for_heatnc": 1,
        "res_heatnc_tot_overcapacity": 1,
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
    )


@component.add(
    name='"replacement RES for heat-nc"',
    units="Dmnl",
    subscripts=["RES heat"],
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
    "../energy.xlsx",
    "Global",
    "replacement_rate_res_for_heat*",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    {"RES heat": _subscript_dict["RES heat"]},
    "_ext_constant_replacement_res_for_heatnc",
)


@component.add(
    name='"RES heat-nc tot overcapacity"',
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
    name='"wear RES capacity for heat-nc TW"',
    units="TW",
    subscripts=["RES heat"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"installed_capacity_res_heatnc_tw": 1, "life_time_res_for_heat": 1},
)
def wear_res_capacity_for_heatnc_tw():
    """
    Decommission of the capacity that reachs the end of its lifetime.
    """
    return installed_capacity_res_heatnc_tw() / life_time_res_for_heat()
