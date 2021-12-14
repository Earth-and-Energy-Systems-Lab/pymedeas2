"""
Module capacities__generation__ehr
Translated using PySD version 2.1.0
"""


def abundance_res_heatcom():
    """
    Real Name: "abundance RES heat-com"
    Original Eqn: IF THEN ELSE("FED Heat-com after priorities EJ"=0,0, ZIDZ( ("FED Heat-com after priorities EJ"-"FE real supply RES for heat-com tot EJ"), "FED Heat-com after priorities EJ"))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    The parameter abundance varies between (1;0). The closest to 1 indicates that heat
        generation from RES is far to cover to whole heat demand, if "abundance
        RES heat"=0 it means that RES heat cover the whole heat demand.                IF THEN ELSE(Total FED Heat EJ delayed 1yr=0,0,        IF THEN ELSE(Total FED Heat EJ delayed 1yr > FE real supply RES for heat tot EJ,        (Total FED Heat EJ delayed 1yr-FE real supply RES for heat tot EJ)/Total
        FED Heat EJ delayed 1yr, 0))
    """
    return if_then_else(
        fed_heatcom_after_priorities_ej() == 0,
        lambda: 0,
        lambda: zidz(
            (
                fed_heatcom_after_priorities_ej()
                - fe_real_supply_res_for_heatcom_tot_ej()
            ),
            fed_heatcom_after_priorities_ej(),
        ),
    )


def abundance_res_heatcom2():
    """
    Real Name: "abundance RES heat-com2"
    Original Eqn: SQRT ("abundance RES heat-com")
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Adaptation of the parameter abundance for better behaviour of the model.
    """
    return np.sqrt(abundance_res_heatcom())


@subs(["RES heat"], _subscript_dict)
def adapt_growth_res_for_heatcom():
    """
    Real Name: "adapt growth RES for heat-com"
    Original Eqn: IF THEN ELSE(Time<2014, "past RES growth for heat-com"[RES heat], IF THEN ELSE(Time<Start year P growth RES heat, "past RES growth for heat-com"[RES heat], IF THEN ELSE(Time<Target year P growth RES heat, "past RES growth for heat-com"[RES heat]+(P RES for heat[RES heat]-"past RES growth for heat-com"[RES heat])*(Time-Start year P growth RES heat)/(Target year P growth RES heat-Start year P growth RES heat), P RES for heat[RES heat] )))
    Units: 1/Year
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']

    Modeling of a soft transition from current historic annual growth to reach
        the policy-objective in the target year.
    """
    return if_then_else(
        time() < 2014,
        lambda: past_res_growth_for_heatcom(),
        lambda: if_then_else(
            time() < start_year_p_growth_res_heat(),
            lambda: past_res_growth_for_heatcom(),
            lambda: if_then_else(
                time() < target_year_p_growth_res_heat(),
                lambda: past_res_growth_for_heatcom()
                + (p_res_for_heat() - past_res_growth_for_heatcom())
                * (time() - start_year_p_growth_res_heat())
                / (target_year_p_growth_res_heat() - start_year_p_growth_res_heat()),
                lambda: p_res_for_heat(),
            ),
        ),
    )


def efficiency_conversion_bioe_plants_to_heat():
    """
    Real Name: Efficiency conversion BioE plants to heat
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'efficiency_conversion_bioe_plants_to_heat')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Efficiency of the transformation from bioenergy to heat in heat and CHP
        plants (aggregated). Efficiency of the transformation from bioenergy to
        electricity (estimation for 2014 from the IEA balances.
    """
    return _ext_constant_efficiency_conversion_bioe_plants_to_heat()


def efficiency_geothermal_for_heat():
    """
    Real Name: Efficiency geothermal for heat
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'efficiency_geothermal_for_heat')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return _ext_constant_efficiency_geothermal_for_heat()


@subs(["RES heat"], _subscript_dict)
def efficiency_res_heat():
    """
    Real Name: Efficiency RES heat
    Original Eqn:
      f1 solar panels for heat*Losses solar for heat
      Efficiency geothermal for heat
      Efficiency conversion BioE plants to heat
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']

    Efficiency of RES technologies for heat.
    """
    return xrmerge(
        rearrange(
            f1_solar_panels_for_heat() * losses_solar_for_heat(),
            ["RES heat"],
            {"RES heat": ["solar heat"]},
        ),
        rearrange(
            efficiency_geothermal_for_heat(), ["RES heat"], {"RES heat": ["geot heat"]}
        ),
        rearrange(
            efficiency_conversion_bioe_plants_to_heat(),
            ["RES heat"],
            {"RES heat": ["solid bioE heat"]},
        ),
    )


def f1_solar_panels_for_heat():
    """
    Real Name: f1 solar panels for heat
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'efficiency_solar_panels_for_heat')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Efficiency solar panels for heat.
    """
    return _ext_constant_f1_solar_panels_for_heat()


@subs(["RES heat"], _subscript_dict)
def fe_real_generation_res_heatcom_ej():
    """
    Real Name: "FE real generation RES heat-com EJ"
    Original Eqn: "potential FES RES for heat-com EJ"[RES heat]*(1-"RES heat-com tot overcapacity")
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']

    Commercial heat generation by RES technology.
    """
    return potential_fes_res_for_heatcom_ej() * (1 - res_heatcom_tot_overcapacity())


def fe_real_supply_res_for_heatcom_tot_ej():
    """
    Real Name: "FE real supply RES for heat-com tot EJ"
    Original Eqn: MIN(MAX("FED Heat-com after priorities EJ", 0), "potential FES tot RES for heat-com EJ")
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total final energy supply delivered by RES for commercial heat.
    """
    return np.minimum(
        np.maximum(fed_heatcom_after_priorities_ej(), 0),
        potential_fes_tot_res_for_heatcom_ej(),
    )


def historic_res_capacity_for_heatcom(x):
    """
    Real Name: "Historic RES capacity for heat-com"
    Original Eqn: ( GET DIRECT LOOKUPS('../energy.xlsx', 'Austria', 'time_historic_data', 'historic_res_capacity_for_heat_commercial'))
    Units: TW
    Limits: (None, None)
    Type: lookup
    Subs: ['RES heat']

    Historic installed capacity of RES technologies for commercial heat
        generation.
    """
    return _ext_lookup_historic_res_capacity_for_heatcom(x)


@subs(["RES heat"], _subscript_dict)
def initial_value_res_for_heatcom():
    """
    Real Name: "initial value RES for heat-com"
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'initial_res_capacity_for_heat_commercial*')
    Units: TW
    Limits: (None, None)
    Type: constant
    Subs: ['RES heat']

    RES supply by technology for commercial heat in the year 1995.
    """
    return _ext_constant_initial_value_res_for_heatcom()


@subs(["RES heat"], _subscript_dict)
def installed_capacity_res_heatcom_tw():
    """
    Real Name: "installed capacity RES heat-com TW"
    Original Eqn: INTEG ( "new RES capacity for heat-com TW"[RES heat]+"replacement RES for heat-com TW"[RES heat]-"wear RES capacity for heat-com TW"[RES heat], "initial value RES for heat-com"[RES heat])
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']

    Installed capacity of RES for commercial heat.
    """
    return _integ_installed_capacity_res_heatcom_tw()


@subs(["RES heat"], _subscript_dict)
def life_time_res_for_heat():
    """
    Real Name: life time RES for heat
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'lifetime_res_for_heat*')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: ['RES heat']

    Lifetime RES thermal technologies and plants.
    """
    return _ext_constant_life_time_res_for_heat()


def losses_solar_for_heat():
    """
    Real Name: Losses solar for heat
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'losses_solar_for_heat')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Losses (pipelina and storage) of solar for heat.
    """
    return _ext_constant_losses_solar_for_heat()


@subs(["RES heat"], _subscript_dict)
def new_res_capacity_for_heatcom_tw():
    """
    Real Name: "new RES capacity for heat-com TW"
    Original Eqn: IF THEN ELSE(Time<2013, "Historic RES capacity for heat-com"[RES heat](INTEGER(Time+1))-"Historic RES capacity for heat-com"[RES heat](INTEGER(Time)), "adapt growth RES for heat-com"[RES heat]*"installed capacity RES heat-com TW"[RES heat]*remaining potential constraint on new RES heat capacity [RES heat])*"abundance RES heat-com2"
    Units: TW/Year
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']

    New annual installed capacity of RES technologies for commercial heat.
    """
    return (
        if_then_else(
            time() < 2013,
            lambda: historic_res_capacity_for_heatcom(integer(time() + 1))
            - historic_res_capacity_for_heatcom(integer(time())),
            lambda: adapt_growth_res_for_heatcom()
            * installed_capacity_res_heatcom_tw()
            * remaining_potential_constraint_on_new_res_heat_capacity(),
        )
        * abundance_res_heatcom2()
    )


def p_geothermal_for_heat():
    """
    Real Name: P geothermal for heat
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'C61')
    Units: 1/Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual growth in relation to the existing installed capacity.
    """
    return _ext_constant_p_geothermal_for_heat()


@subs(["RES heat"], _subscript_dict)
def p_res_for_heat():
    """
    Real Name: P RES for heat
    Original Eqn:
      P solar for heat
      P geothermal for heat
      P solid bioE for heat
    Units: 1/Year
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']

    Annual growth in RES supply for heat depending on the policy of the
        scenario.
    """
    return xrmerge(
        rearrange(p_solar_for_heat(), ["RES heat"], {"RES heat": ["solar heat"]}),
        rearrange(p_geothermal_for_heat(), ["RES heat"], {"RES heat": ["geot heat"]}),
        rearrange(
            p_solid_bioe_for_heat(), ["RES heat"], {"RES heat": ["solid bioE heat"]}
        ),
    )


def p_solar_for_heat():
    """
    Real Name: P solar for heat
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'C60')
    Units: 1/Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual growth in relation to the existing installed capacity.
    """
    return _ext_constant_p_solar_for_heat()


def p_solid_bioe_for_heat():
    """
    Real Name: P solid bioE for heat
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'C62')
    Units: 1/Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual growth in relation to the existing installed capacity.
    """
    return _ext_constant_p_solid_bioe_for_heat()


@subs(["RES heat"], _subscript_dict)
def past_res_growth_for_heatcom():
    """
    Real Name: "past RES growth for heat-com"
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'historic_growth_res_for_heat_com*')
    Units: 1/Year
    Limits: (None, None)
    Type: constant
    Subs: ['RES heat']

    Historic annual average growth.
    """
    return _ext_constant_past_res_growth_for_heatcom()


@subs(["RES heat"], _subscript_dict)
def pes_dem_res_for_heatcom_by_techn():
    """
    Real Name: "PES DEM RES for heat-com by techn"
    Original Eqn:
      "FE real generation RES heat-com EJ"[geot heat]
      "FE real generation RES heat-com EJ"[solar heat]
      "FE real generation RES heat-com EJ"[solid bioE heat]/Efficiency RES heat[solid bioE heat]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']

    Primary energy supply of RES technologies for commercial heat (Direct
        Energy Method convention of accounting for primary energy).
    """
    return xrmerge(
        rearrange(
            float(fe_real_generation_res_heatcom_ej().loc["geot heat"]),
            ["RES heat"],
            {"RES heat": ["geot heat"]},
        ),
        rearrange(
            float(fe_real_generation_res_heatcom_ej().loc["solar heat"]),
            ["RES heat"],
            {"RES heat": ["solar heat"]},
        ),
        rearrange(
            float(fe_real_generation_res_heatcom_ej().loc["solid bioE heat"])
            / float(efficiency_res_heat().loc["solid bioE heat"]),
            ["RES heat"],
            {"RES heat": ["solid bioE heat"]},
        ),
    )


@subs(["RES heat"], _subscript_dict)
def pes_res_for_heatcom_by_techn():
    """
    Real Name: "PES RES for heat-com by techn"
    Original Eqn: "FE real generation RES heat-com EJ"[RES heat]/Efficiency RES heat[RES heat]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']

    Primary energy supply of RES technologies for commercial heat.
    """
    return fe_real_generation_res_heatcom_ej() / efficiency_res_heat()


@subs(["RES heat"], _subscript_dict)
def potential_fes_res_for_heatcom_ej():
    """
    Real Name: "potential FES RES for heat-com EJ"
    Original Eqn: "potential FES RES for heat-com TWh"[RES heat]*EJ per TWh
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']

    Potential final energy supply renewables for commercial heat given the
        installed capacity.
    """
    return potential_fes_res_for_heatcom_twh() * ej_per_twh()


@subs(["RES heat"], _subscript_dict)
def potential_fes_res_for_heatcom_twh():
    """
    Real Name: "potential FES RES for heat-com TWh"
    Original Eqn: "installed capacity RES heat-com TW"[RES heat]*Efficiency RES heat[RES heat]*Cp RES for heat[RES heat] /TWe per TWh
    Units: TWh
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']

    Potential final energy supply renewables for commercial heat given the
        installed capacity.
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
    Original Eqn: SUM("potential FES RES for heat-com EJ"[RES heat!])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Potential total final energy supply renewables for commercial heat given
        the installed capacity.
    """
    return sum(potential_fes_res_for_heatcom_ej(), dim=("RES heat",))


@subs(["RES heat"], _subscript_dict)
def remaining_potential_constraint_on_new_res_heat_capacity():
    """
    Real Name: remaining potential constraint on new RES heat capacity
    Original Eqn: IF THEN ELSE(remaining potential RES for heat[RES heat]>threshold remaining potential new capacity,1,remaining potential RES for heat[RES heat]*(1/threshold remaining potential new capacity))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']

    Constraint of remaining potential on new RES elec capacity.        Another alternative: SQRT(remaining potential RES elec after intermitt[RES
        elec])
    """
    return if_then_else(
        remaining_potential_res_for_heat()
        > threshold_remaining_potential_new_capacity(),
        lambda: 1,
        lambda: remaining_potential_res_for_heat()
        * (1 / threshold_remaining_potential_new_capacity()),
    )


@subs(["RES heat"], _subscript_dict)
def remaining_potential_res_for_heat():
    """
    Real Name: remaining potential RES for heat
    Original Eqn: ZIDZ( (MAX(0, Max FE RES for heat[RES heat]-"potential FES RES for heat-com EJ"[RES heat]-"potential FES RES for heat-nc EJ"[RES heat])), Max FE RES for heat[RES heat] )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']

    Remaining potential available as given as a fraction of unity.
    """
    return zidz(
        (
            np.maximum(
                0,
                max_fe_res_for_heat()
                - potential_fes_res_for_heatcom_ej()
                - potential_fes_res_for_heatnc_ej(),
            )
        ),
        max_fe_res_for_heat(),
    )


@subs(["RES heat"], _subscript_dict)
def replacement_res_for_heatcom_tw():
    """
    Real Name: "replacement RES for heat-com TW"
    Original Eqn: "wear RES capacity for heat-com TW"[RES heat]*"replacement RES for heat-com"[RES heat]*(1-"RES heat-com tot overcapacity" )*shortage BioE for heat[RES heat]^2
    Units: TW/Year
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']

    Annual replacement of RES for commercial heat by technology.
    """
    return (
        wear_res_capacity_for_heatcom_tw()
        * replacement_res_for_heatcom()
        * (1 - res_heatcom_tot_overcapacity())
        * shortage_bioe_for_heat() ** 2
    )


@subs(["RES heat"], _subscript_dict)
def replacement_res_for_heatcom():
    """
    Real Name: "replacement RES for heat-com"
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'replacement_rate_res_for_heat*')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['RES heat']

    If =1, we asume that all the power that reaches the end of its lifetime is
        replaced.
    """
    return _ext_constant_replacement_res_for_heatcom()


def res_heatcom_tot_overcapacity():
    """
    Real Name: "RES heat-com tot overcapacity"
    Original Eqn: IF THEN ELSE("potential FES tot RES for heat-com EJ"=0,0, ("potential FES tot RES for heat-com EJ"-"FE real supply RES for heat-com tot EJ")/"potential FES tot RES for heat-com EJ" )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Overcapacity for each technology RES for heat-com taking into account the
        installed capacity and the real generation.
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
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'C58')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Start year of the policy growth of RES technologies for generating heat.
    """
    return _ext_constant_start_year_p_growth_res_heat()


def target_year_p_growth_res_heat():
    """
    Real Name: Target year P growth RES heat
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'C59')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Target year of the policy growth of RES technologies for generating heat.
    """
    return _ext_constant_target_year_p_growth_res_heat()


@subs(["RES heat"], _subscript_dict)
def wear_res_capacity_for_heatcom_tw():
    """
    Real Name: "wear RES capacity for heat-com TW"
    Original Eqn: "installed capacity RES heat-com TW"[RES heat]/life time RES for heat[RES heat]
    Units: TW/Year
    Limits: (None, None)
    Type: component
    Subs: ['RES heat']

    Decommission of the capacity that reachs the end of its lifetime.
    """
    return installed_capacity_res_heatcom_tw() / life_time_res_for_heat()


_ext_constant_efficiency_conversion_bioe_plants_to_heat = ExtConstant(
    "../energy.xlsx",
    "Global",
    "efficiency_conversion_bioe_plants_to_heat",
    {},
    _root,
    "_ext_constant_efficiency_conversion_bioe_plants_to_heat",
)


_ext_constant_efficiency_geothermal_for_heat = ExtConstant(
    "../energy.xlsx",
    "Global",
    "efficiency_geothermal_for_heat",
    {},
    _root,
    "_ext_constant_efficiency_geothermal_for_heat",
)


_ext_constant_f1_solar_panels_for_heat = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "efficiency_solar_panels_for_heat",
    {},
    _root,
    "_ext_constant_f1_solar_panels_for_heat",
)


_ext_lookup_historic_res_capacity_for_heatcom = ExtLookup(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_res_capacity_for_heat_commercial",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    "_ext_lookup_historic_res_capacity_for_heatcom",
)


_ext_constant_initial_value_res_for_heatcom = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "initial_res_capacity_for_heat_commercial*",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    "_ext_constant_initial_value_res_for_heatcom",
)


@subs(["RES heat"], _subscript_dict)
def _integ_init_installed_capacity_res_heatcom_tw():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for installed_capacity_res_heatcom_tw
    Limits: None
    Type: setup
    Subs: ['RES heat']

    Provides initial conditions for installed_capacity_res_heatcom_tw function
    """
    return initial_value_res_for_heatcom()


@subs(["RES heat"], _subscript_dict)
def _integ_input_installed_capacity_res_heatcom_tw():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for installed_capacity_res_heatcom_tw
    Limits: None
    Type: component
    Subs: ['RES heat']

    Provides derivative for installed_capacity_res_heatcom_tw function
    """
    return (
        new_res_capacity_for_heatcom_tw()
        + replacement_res_for_heatcom_tw()
        - wear_res_capacity_for_heatcom_tw()
    )


_integ_installed_capacity_res_heatcom_tw = Integ(
    _integ_input_installed_capacity_res_heatcom_tw,
    _integ_init_installed_capacity_res_heatcom_tw,
    "_integ_installed_capacity_res_heatcom_tw",
)


_ext_constant_life_time_res_for_heat = ExtConstant(
    "../energy.xlsx",
    "Global",
    "lifetime_res_for_heat*",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    "_ext_constant_life_time_res_for_heat",
)


_ext_constant_losses_solar_for_heat = ExtConstant(
    "../energy.xlsx",
    "Global",
    "losses_solar_for_heat",
    {},
    _root,
    "_ext_constant_losses_solar_for_heat",
)


_ext_constant_p_geothermal_for_heat = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "C61",
    {},
    _root,
    "_ext_constant_p_geothermal_for_heat",
)


_ext_constant_p_solar_for_heat = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "C60",
    {},
    _root,
    "_ext_constant_p_solar_for_heat",
)


_ext_constant_p_solid_bioe_for_heat = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "C62",
    {},
    _root,
    "_ext_constant_p_solid_bioe_for_heat",
)


_ext_constant_past_res_growth_for_heatcom = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "historic_growth_res_for_heat_com*",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    "_ext_constant_past_res_growth_for_heatcom",
)


_ext_constant_replacement_res_for_heatcom = ExtConstant(
    "../energy.xlsx",
    "Global",
    "replacement_rate_res_for_heat*",
    {"RES heat": _subscript_dict["RES heat"]},
    _root,
    "_ext_constant_replacement_res_for_heatcom",
)


_ext_constant_start_year_p_growth_res_heat = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "C58",
    {},
    _root,
    "_ext_constant_start_year_p_growth_res_heat",
)


_ext_constant_target_year_p_growth_res_heat = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "C59",
    {},
    _root,
    "_ext_constant_target_year_p_growth_res_heat",
)
