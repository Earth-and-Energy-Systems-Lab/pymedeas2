"""
Module res_commercial_heat_capacities
Translated using PySD version 2.2.1
"""


def abundance_res_heatcom():
    """
    Real Name: "abundance RES heat-com"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    The parameter abundance varies between (1;0). The closest to 1 indicates that heat generation from RES is far to cover to whole heat demand, if "abundance RES heat"=0 it means that RES heat cover the whole heat demand. IF THEN ELSE(Total FED Heat EJ delayed 1yr=0,0, IF THEN ELSE(Total FED Heat EJ delayed 1yr > FE real supply RES for heat tot EJ, (Total FED Heat EJ delayed 1yr-FE real supply RES for heat tot EJ)/Total FED Heat EJ delayed 1yr, 0))
    """
    return if_then_else(
        fed_heatcom_after_priorities_ej() == 0,
        lambda: 0,
        lambda: zidz(
            fed_heatcom_after_priorities_ej() - fe_real_supply_res_for_heatcom_tot_ej(),
            fed_heatcom_after_priorities_ej(),
        ),
    )


def abundance_res_heatcom2():
    """
    Real Name: "abundance RES heat-com2"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Adaptation of the parameter abundance for better behaviour of the model.
    """
    return np.sqrt(abundance_res_heatcom())


@subs(["RES heat"], _subscript_dict)
def adapt_growth_res_for_heatcom():
    """
    Real Name: "adapt growth RES for heat-com"
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

    Modeling of a soft transition from current historic annual growth to reach the policy-objective 5 years later.
    """
    return if_then_else(
        time() < 2014,
        lambda: past_res_growth_for_heatcom(),
        lambda: if_then_else(
            time() < start_year_p_growth_res_heat(),
            lambda: past_res_growth_for_heatcom()
            + (p_res_for_heat() - past_res_growth_for_heatcom())
            * (time() - 2014)
            / (start_year_p_growth_res_heat() - 2014),
            lambda: p_res_for_heat(),
        ),
    )


def efficiency_conversion_bioe_plants_to_heat():
    """
    Real Name: Efficiency conversion BioE plants to heat
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Efficiency of the transformation from bioenergy to heat in heat and CHP plants (aggregated). Efficiency of the transformation from bioenergy to electricity (estimation for 2014 from the IEA balances.
    """
    return _ext_constant_efficiency_conversion_bioe_plants_to_heat()


_ext_constant_efficiency_conversion_bioe_plants_to_heat = ExtConstant(
    "../energy.xlsx",
    "Global",
    "efficiency_conversion_bioe_plants_to_heat",
    {},
    _root,
    "_ext_constant_efficiency_conversion_bioe_plants_to_heat",
)


def efficiency_geothermal_for_heat():
    """
    Real Name: Efficiency geothermal for heat
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return _ext_constant_efficiency_geothermal_for_heat()


_ext_constant_efficiency_geothermal_for_heat = ExtConstant(
    "../energy.xlsx",
    "Global",
    "efficiency_geothermal_for_heat",
    {},
    _root,
    "_ext_constant_efficiency_geothermal_for_heat",
)


@subs(["RES heat"], _subscript_dict)
def efficiency_res_heat():
    """
    Real Name: Efficiency RES heat
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']


    """
    value = xr.DataArray(
        np.nan, {"RES heat": _subscript_dict["RES heat"]}, ["RES heat"]
    )
    value.loc[{"RES heat": ["solar heat"]}] = (
        efficiency_solar_panels_for_heat() * losses_solar_for_heat()
    )
    value.loc[{"RES heat": ["geot heat"]}] = efficiency_geothermal_for_heat()
    value.loc[
        {"RES heat": ["solid bioE heat"]}
    ] = efficiency_conversion_bioe_plants_to_heat()
    return value


def efficiency_solar_panels_for_heat():
    """
    Real Name: Efficiency solar panels for heat
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return _ext_constant_efficiency_solar_panels_for_heat()


_ext_constant_efficiency_solar_panels_for_heat = ExtConstant(
    "../energy.xlsx",
    "World",
    "efficiency_solar_panels_for_heat",
    {},
    _root,
    "_ext_constant_efficiency_solar_panels_for_heat",
)


@subs(["RES heat"], _subscript_dict)
def fe_real_generation_res_heatcom_ej():
    """
    Real Name: "FE real generation RES heat-com EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

    Commercial heat generation by RES technology.
    """
    return potential_fes_res_for_heatcom_ej() * (1 - res_heatcom_tot_overcapacity())


def fe_real_supply_res_for_heatcom_tot_ej():
    """
    Real Name: "FE real supply RES for heat-com tot EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total final energy supply delivered by RES for commercial heat.
    """
    return np.minimum(
        np.maximum(fed_heatcom_after_priorities_ej(), 0),
        potential_fes_tot_res_for_heatcom_ej(),
    )


@subs(["RES heat"], _subscript_dict)
def historic_res_capacity_for_heatcom(x):
    """
    Real Name: "Historic RES capacity for heat-com"
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Lookup
    Subs: ['RES heat']

    Historic installed capacity of RES technologies for commercial heat generation.
    """
    return _ext_lookup_historic_res_capacity_for_heatcom(x)


_ext_lookup_historic_res_capacity_for_heatcom = ExtLookup(
    "../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_res_capacity_for_heat_commercial",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    "_ext_lookup_historic_res_capacity_for_heatcom",
)


@subs(["RES heat"], _subscript_dict)
def initial_value_res_for_heatcom():
    """
    Real Name: "initial value RES for heat-com"
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Constant
    Subs: ['RES heat']

    RES supply by technology for commercial heat in the year 1995.
    """
    return _ext_constant_initial_value_res_for_heatcom()


_ext_constant_initial_value_res_for_heatcom = ExtConstant(
    "../energy.xlsx",
    "World",
    "initial_res_capacity_for_heat_commercial*",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    "_ext_constant_initial_value_res_for_heatcom",
)


@subs(["RES heat"], _subscript_dict)
def installed_capacity_res_heatcom_tw():
    """
    Real Name: "installed capacity RES heat-com TW"
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Stateful
    Subs: ['RES heat']

    Installed capacity of RES for commercial heat.
    """
    return _integ_installed_capacity_res_heatcom_tw()


_integ_installed_capacity_res_heatcom_tw = Integ(
    lambda: new_res_capacity_for_heatcom_tw()
    + replacement_res_for_heatcom_tw()
    - wear_res_capacity_for_heatcom_tw(),
    lambda: initial_value_res_for_heatcom(),
    "_integ_installed_capacity_res_heatcom_tw",
)


@subs(["RES heat"], _subscript_dict)
def life_time_res_for_heat():
    """
    Real Name: life time RES for heat
    Original Eqn:
    Units: year
    Limits: (None, None)
    Type: Constant
    Subs: ['RES heat']

    Lifetime RES thermal technologies and plants.
    """
    return _ext_constant_life_time_res_for_heat()


_ext_constant_life_time_res_for_heat = ExtConstant(
    "../energy.xlsx",
    "Global",
    "lifetime_res_for_heat*",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    "_ext_constant_life_time_res_for_heat",
)


def losses_solar_for_heat():
    """
    Real Name: Losses solar for heat
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []


    """
    return _ext_constant_losses_solar_for_heat()


_ext_constant_losses_solar_for_heat = ExtConstant(
    "../energy.xlsx",
    "Global",
    "losses_solar_for_heat",
    {},
    _root,
    "_ext_constant_losses_solar_for_heat",
)


@subs(["RES heat"], _subscript_dict)
def new_res_capacity_for_heatcom_tw():
    """
    Real Name: "new RES capacity for heat-com TW"
    Original Eqn:
    Units: TW/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

    New annual installed capacity of RES technologies for commercial heat.
    """
    return (
        if_then_else(
            time() < 2013,
            lambda: historic_res_capacity_for_heatcom(time() + 1)
            - historic_res_capacity_for_heatcom(time()),
            lambda: adapt_growth_res_for_heatcom()
            * installed_capacity_res_heatcom_tw()
            * remaining_potential_constraint_on_new_res_heat_capacity(),
        )
        * abundance_res_heatcom2()
    )


def p_geothermal_for_heat():
    """
    Real Name: P geothermal for heat
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Annual growth in relation to the existing installed capacity.
    """
    return _ext_constant_p_geothermal_for_heat()


_ext_constant_p_geothermal_for_heat = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "p_geothermal_heat_growth",
    {},
    _root,
    "_ext_constant_p_geothermal_for_heat",
)


@subs(["RES heat"], _subscript_dict)
def p_res_for_heat():
    """
    Real Name: P RES for heat
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

    Annual growth in RES supply for heat depending on the policy of the scenario.
    """
    value = xr.DataArray(
        np.nan, {"RES heat": _subscript_dict["RES heat"]}, ["RES heat"]
    )
    value.loc[{"RES heat": ["solar heat"]}] = p_solar_for_heat()
    value.loc[{"RES heat": ["geot heat"]}] = p_geothermal_for_heat()
    value.loc[{"RES heat": ["solid bioE heat"]}] = p_solid_bioe_for_heat()
    return value


def p_solar_for_heat():
    """
    Real Name: P solar for heat
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Annual growth in relation to the existing installed capacity.
    """
    return _ext_constant_p_solar_for_heat()


_ext_constant_p_solar_for_heat = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "p_solar_heat_growth",
    {},
    _root,
    "_ext_constant_p_solar_for_heat",
)


def p_solid_bioe_for_heat():
    """
    Real Name: P solid bioE for heat
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Annual growth in relation to the existing installed capacity.
    """
    return _ext_constant_p_solid_bioe_for_heat()


_ext_constant_p_solid_bioe_for_heat = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "p_solid_bioe_heat_growth",
    {},
    _root,
    "_ext_constant_p_solid_bioe_for_heat",
)


@subs(["RES heat"], _subscript_dict)
def past_res_growth_for_heatcom():
    """
    Real Name: "past RES growth for heat-com"
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Constant
    Subs: ['RES heat']

    Historic annual average growth.
    """
    return _ext_constant_past_res_growth_for_heatcom()


_ext_constant_past_res_growth_for_heatcom = ExtConstant(
    "../energy.xlsx",
    "World",
    "historic_growth_res_for_heat_com*",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    "_ext_constant_past_res_growth_for_heatcom",
)


@subs(["RES heat"], _subscript_dict)
def pes_res_for_heatcom_by_techn():
    """
    Real Name: "PES RES for heat-com by techn"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

    Primary energy supply of RES technologies for commercial heat.
    """
    value = xr.DataArray(
        np.nan, {"RES heat": _subscript_dict["RES heat"]}, ["RES heat"]
    )
    value.loc[{"RES heat": ["geot heat"]}] = float(
        fe_real_generation_res_heatcom_ej().loc["geot heat"]
    ) / float(efficiency_res_heat().loc["geot heat"])
    value.loc[{"RES heat": ["solar heat"]}] = (
        float(fe_real_generation_res_heatcom_ej().loc["solar heat"])
        * efficiency_solar_panels_for_heat()
        / float(efficiency_res_heat().loc["solar heat"])
    )
    value.loc[{"RES heat": ["solid bioE heat"]}] = float(
        fe_real_generation_res_heatcom_ej().loc["solid bioE heat"]
    ) / float(efficiency_res_heat().loc["solid bioE heat"])
    return value


@subs(["RES heat"], _subscript_dict)
def potential_fes_res_for_heatcom_ej():
    """
    Real Name: "potential FES RES for heat-com EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

    Potential final energy supply renewables for commercial heat given the installed capacity.
    """
    return potential_fes_res_for_heatcom_twh() * ej_per_twh()


@subs(["RES heat"], _subscript_dict)
def potential_fes_res_for_heatcom_twh():
    """
    Real Name: "potential FES RES for heat-com TWh"
    Original Eqn:
    Units: TWh
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

    Potential final energy supply renewables for commercial heat given the installed capacity.
    """
    return (
        installed_capacity_res_heatcom_tw()
        * efficiency_res_heat()
        * cp_res_for_heat()
        / twe_per_twh()
    )


def potential_fes_tot_res_for_heatcom_ej():
    """
    Real Name: "potential FES tot RES for heat-com EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Potential total final energy supply renewables for commercial heat given the installed capacity.
    """
    return sum(
        potential_fes_res_for_heatcom_ej().rename({"RES heat": "RES heat!"}),
        dim=["RES heat!"],
    )


@subs(["RES heat"], _subscript_dict)
def remaining_potential_constraint_on_new_res_heat_capacity():
    """
    Real Name: remaining potential constraint on new RES heat capacity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

    Constraint of remaining potential on new RES elec capacity. Another alternative: SQRT(remaining potential RES elec after intermitt[RES elec])
    """
    return if_then_else(
        remaining_potential_res_for_heat()
        > threshold_remaining_potential_new_capacity(),
        lambda: xr.DataArray(
            1, {"RES heat": _subscript_dict["RES heat"]}, ["RES heat"]
        ),
        lambda: remaining_potential_res_for_heat()
        * (1 / threshold_remaining_potential_new_capacity()),
    )


@subs(["RES heat"], _subscript_dict)
def remaining_potential_res_for_heat():
    """
    Real Name: remaining potential RES for heat
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

    Remaining potential available as given as a fraction of unity.
    """
    return zidz(
        np.maximum(
            0,
            max_fe_potential_res_for_heat()
            - potential_fes_res_for_heatcom_ej()
            - potential_fes_res_for_heatnc_ej(),
        ),
        max_fe_potential_res_for_heat(),
    )


@subs(["RES heat"], _subscript_dict)
def replacement_res_for_heatcom_tw():
    """
    Real Name: "replacement RES for heat-com TW"
    Original Eqn:
    Units: TW/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

    Annual replacement of RES for commercial heat by technology.
    """
    return (
        wear_res_capacity_for_heatcom_tw()
        * replacement_res_for_heatcom()
        * (1 - res_heatcom_tot_overcapacity())
    )


@subs(["RES heat"], _subscript_dict)
def replacement_res_for_heatcom():
    """
    Real Name: "replacement RES for heat-com"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: ['RES heat']

    If =1, we asume that all the power that reaches the end of its lifetime is replaced.
    """
    return _ext_constant_replacement_res_for_heatcom()


_ext_constant_replacement_res_for_heatcom = ExtConstant(
    "../energy.xlsx",
    "Global",
    "replacement_rate_res_for_heat*",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    "_ext_constant_replacement_res_for_heatcom",
)


def res_heatcom_tot_overcapacity():
    """
    Real Name: "RES heat-com tot overcapacity"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Overcapacity for each technology RES for heat-com taking into account the installed capacity and the real generation.
    """
    return if_then_else(
        potential_fes_tot_res_for_heatcom_ej() == 0,
        lambda: 0,
        lambda: (
            potential_fes_tot_res_for_heatcom_ej()
            - fe_real_supply_res_for_heatcom_tot_ej()
        )
        / potential_fes_tot_res_for_heatcom_ej(),
    )


def start_year_p_growth_res_heat():
    """
    Real Name: Start year P growth RES heat
    Original Eqn:
    Units: year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Start year of the policy growth of RES technologies for generating heat.
    """
    return _ext_constant_start_year_p_growth_res_heat()


_ext_constant_start_year_p_growth_res_heat = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "start_year_P_growth_RES_heat",
    {},
    _root,
    "_ext_constant_start_year_p_growth_res_heat",
)


@subs(["RES heat"], _subscript_dict)
def wear_res_capacity_for_heatcom_tw():
    """
    Real Name: "wear RES capacity for heat-com TW"
    Original Eqn:
    Units: TW/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

    Decommission of the capacity that reachs the end of its lifetime.
    """
    return installed_capacity_res_heatcom_tw() / life_time_res_for_heat()
