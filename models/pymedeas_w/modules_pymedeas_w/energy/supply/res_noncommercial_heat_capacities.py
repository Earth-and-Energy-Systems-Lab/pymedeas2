"""
Module res_noncommercial_heat_capacities
Translated using PySD version 2.2.3
"""


def abundance_res_heatnc():
    """
    Real Name: "abundance RES heat-nc"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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


def abundance_res_heatnc2():
    """
    Real Name: "abundance RES heat-nc2"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Adaptation of the parameter abundance for better behaviour of the model.
    """
    return np.sqrt(abundance_res_heatnc())


@subs(["RES heat"], _subscript_dict)
def adapt_growth_res_for_heatnc():
    """
    Real Name: "adapt growth RES for heat-nc"
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

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


@subs(["RES heat"], _subscript_dict)
def cp_res_for_heat():
    """
    Real Name: Cp RES for heat
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']


    """
    return cpini_res_for_heat()


@subs(["RES heat"], _subscript_dict)
def cpini_res_for_heat():
    """
    Real Name: "Cp-ini RES for heat"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: ['RES heat']


    """
    return _ext_constant_cpini_res_for_heat()


_ext_constant_cpini_res_for_heat = ExtConstant(
    "../energy.xlsx",
    "World",
    "cp_initial_res_heat*",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    "_ext_constant_cpini_res_for_heat",
)


@subs(["RES heat"], _subscript_dict)
def fe_real_generation_res_heatnc_ej():
    """
    Real Name: "FE real generation RES heat-nc EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

    Non-commercial heat generation by RES technology.
    """
    return potential_fes_res_for_heatnc_ej() * (1 - res_heatnc_tot_overcapacity())


def fe_real_supply_res_for_heatnc_tot_ej():
    """
    Real Name: "FE real supply RES for heat-nc tot EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total final energy supply delivered by RES for non-commercial heat.
    """
    return np.minimum(
        np.maximum(total_fed_heatnc_ej(), 0), potential_fes_tot_res_for_heatnc_ej()
    )


@subs(["RES heat"], _subscript_dict)
def historic_res_capacity_for_heatnc(x):
    """
    Real Name: "Historic RES capacity for heat-nc"
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Lookup
    Subs: ['RES heat']

    Historic installed capacity of RES technologies for non-commercial heat generation.
    """
    return _ext_lookup_historic_res_capacity_for_heatnc(x)


_ext_lookup_historic_res_capacity_for_heatnc = ExtLookup(
    "../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_res_capacity_for_heat_non_commercial",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    "_ext_lookup_historic_res_capacity_for_heatnc",
)


@subs(["RES heat"], _subscript_dict)
def initial_value_res_for_heatnc():
    """
    Real Name: "initial value RES for heat-nc"
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Constant
    Subs: ['RES heat']

    RES supply by technology for non-commercial heat in the year 1995.
    """
    return _ext_constant_initial_value_res_for_heatnc()


_ext_constant_initial_value_res_for_heatnc = ExtConstant(
    "../energy.xlsx",
    "World",
    "initial_res_capacity_for_heat_non_commercial*",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    "_ext_constant_initial_value_res_for_heatnc",
)


@subs(["RES heat"], _subscript_dict)
def installed_capacity_res_heatnc_tw():
    """
    Real Name: "installed capacity RES heat-nc TW"
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Stateful
    Subs: ['RES heat']

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


@subs(["RES heat"], _subscript_dict)
def new_res_capacity_for_heatnc_tw():
    """
    Real Name: "new RES capacity for heat-nc TW"
    Original Eqn:
    Units: TW/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

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


@subs(["RES heat"], _subscript_dict)
def past_res_growth_for_heatnc():
    """
    Real Name: "past RES growth for heat-nc"
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Constant
    Subs: ['RES heat']

    Historic annual average growth.
    """
    return _ext_constant_past_res_growth_for_heatnc()


_ext_constant_past_res_growth_for_heatnc = ExtConstant(
    "../energy.xlsx",
    "World",
    "historic_growth_res_for_heat_nc*",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    "_ext_constant_past_res_growth_for_heatnc",
)


@subs(["RES heat"], _subscript_dict)
def pes_res_for_heatnc_by_techn():
    """
    Real Name: "PES RES for heat-nc by techn"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

    Primary energy supply of RES technologies for non-commercial heat.
    """
    value = xr.DataArray(
        np.nan, {"RES heat": _subscript_dict["RES heat"]}, ["RES heat"]
    )
    value.loc[{"RES heat": ["geot heat"]}] = float(
        fe_real_generation_res_heatnc_ej().loc["geot heat"]
    ) / float(efficiency_res_heat().loc["geot heat"])
    value.loc[{"RES heat": ["solar heat"]}] = (
        float(fe_real_generation_res_heatnc_ej().loc["solar heat"])
        * efficiency_solar_panels_for_heat()
        / float(efficiency_res_heat().loc["solar heat"])
    )
    value.loc[{"RES heat": ["solid bioE heat"]}] = float(
        fe_real_generation_res_heatnc_ej().loc["solid bioE heat"]
    ) / float(efficiency_res_heat().loc["solid bioE heat"])
    return value


@subs(["RES heat"], _subscript_dict)
def potential_fes_res_for_heatnc_ej():
    """
    Real Name: "potential FES RES for heat-nc EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

    Potential final energy supply renewables for non-commercial heat given the installed capacity.
    """
    return potential_fes_res_for_heatnc_twh() * ej_per_twh()


@subs(["RES heat"], _subscript_dict)
def potential_fes_res_for_heatnc_twh():
    """
    Real Name: "potential FES RES for heat-nc TWh"
    Original Eqn:
    Units: TWh
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

    Potential final energy supply renewables for non-commercial heat given the installed capacity.
    """
    return (
        installed_capacity_res_heatnc_tw()
        * efficiency_res_heat()
        * cp_res_for_heat()
        / twe_per_twh()
    )


def potential_fes_tot_res_for_heatnc_ej():
    """
    Real Name: "potential FES tot RES for heat-nc EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Potential total final energy supply renewables for non-commercial heat given the installed capacity.
    """
    return sum(
        potential_fes_res_for_heatnc_ej().rename({"RES heat": "RES heat!"}),
        dim=["RES heat!"],
    )


@subs(["RES heat"], _subscript_dict)
def replacement_res_for_heatnc_tw():
    """
    Real Name: "replacement RES for heat-nc TW"
    Original Eqn:
    Units: TW/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

    Annual replacement of RES for non-commercial heat by technology.
    """
    return (
        wear_res_capacity_for_heatnc_tw()
        * replacement_res_for_heatnc()
        * (1 - res_heatnc_tot_overcapacity())
    )


@subs(["RES heat"], _subscript_dict)
def replacement_res_for_heatnc():
    """
    Real Name: "replacement RES for heat-nc"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: ['RES heat']

    If =1, we asume that all the power that reaches the end of its lifetime is replaced.
    """
    return _ext_constant_replacement_res_for_heatnc()


_ext_constant_replacement_res_for_heatnc = ExtConstant(
    "../energy.xlsx",
    "Global",
    "replacement_rate_res_for_heat*",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    "_ext_constant_replacement_res_for_heatnc",
)


def res_heatnc_tot_overcapacity():
    """
    Real Name: "RES heat-nc tot overcapacity"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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


@subs(["RES heat"], _subscript_dict)
def wear_res_capacity_for_heatnc_tw():
    """
    Real Name: "wear RES capacity for heat-nc TW"
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

    Decommission of the capacity that reachs the end of its lifetime.
    """
    return installed_capacity_res_heatnc_tw() / life_time_res_for_heat()
