"""
Module res_elec_capacities_and_generat
Translated using PySD version 2.2.1
"""


def abundance_res_elec():
    """
    Real Name: abundance RES elec
    Original Eqn: IF THEN ELSE(Total FE Elec demand after priorities TWh=0,0, IF THEN ELSE(Total FE Elec demand after priorities TWh > FE real tot generation RES elec TWh, (Total FE Elec demand after priorities TWh-FE real tot generation RES elec TWh)/Total FE Elec demand after priorities TWh, 0))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    The parameter abundance varies between (1;0). The closest to 1 indicates
        that electricity generation from RES is far to cover to whole electricity
        demand, if "abundance RES elec"=0 it means that RES elec cover the whole
        electricity demand.
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


def abundance_res_elec2():
    """
    Real Name: abundance RES elec2
    Original Eqn: SQRT (abundance RES elec)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Adaptation of the parameter abundance for better behaviour of the model.
    """
    return np.sqrt(abundance_res_elec())


def activate_eroi_allocation_rule():
    """
    Real Name: activate EROI allocation rule
    Original Eqn: 1
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Activate/Deactivate EROI allocation rule for the RES elec technologies:        1. Activated        0. Deactivated
    """
    return 1


@subs(["RES elec"], _subscript_dict)
def adapt_growth_res_elec():
    """
    Real Name: adapt growth RES elec
    Original Eqn:
      IF THEN ELSE(Time<2015, past RES elec capacity growth[hydro], IF THEN ELSE(Time<Start year P growth RES elec, past RES elec capacity growth[hydro], IF THEN ELSE(Time<Target year P growth RES elec, past RES elec capacity growth[hydro]+(P RES elec growth[hydro]-past RES elec capacity growth[hydro])*(Time-Start year P growth RES elec)/(Target year P growth RES elec-Start year P growth RES elec), P RES elec growth[hydro] )))
        .
        .
        .
      IF THEN ELSE(Time<2014, past RES elec capacity growth[CSP], IF THEN ELSE(Time<Start year P growth RES elec, past RES elec capacity growth[CSP], IF THEN ELSE(Time<Target year P growth RES elec, past RES elec capacity growth[CSP]+(P RES elec growth[CSP]-past RES elec capacity growth[CSP])*(Time-Start year P growth RES elec)/(Target year P growth RES elec-Start year P growth RES elec), P RES elec growth[CSP] )))
    Units: 1/Year
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Annual growth per RES elec technology. Modeling of a soft transition from
        current historic annual growth to reach the policy-objective in the target
        year. TODO
    """
    return xrmerge(
        rearrange(
            if_then_else(
                time() < 2015,
                lambda: float(past_res_elec_capacity_growth().loc["hydro"]),
                lambda: if_then_else(
                    time() < start_year_p_growth_res_elec(),
                    lambda: float(past_res_elec_capacity_growth().loc["hydro"]),
                    lambda: if_then_else(
                        time() < target_year_p_growth_res_elec(),
                        lambda: float(past_res_elec_capacity_growth().loc["hydro"])
                        + (
                            float(p_res_elec_growth().loc["hydro"])
                            - float(past_res_elec_capacity_growth().loc["hydro"])
                        )
                        * (time() - start_year_p_growth_res_elec())
                        / (
                            target_year_p_growth_res_elec()
                            - start_year_p_growth_res_elec()
                        ),
                        lambda: float(p_res_elec_growth().loc["hydro"]),
                    ),
                ),
            ),
            ["RES elec"],
            {"RES elec": ["hydro"]},
        ),
        rearrange(
            if_then_else(
                time() < 2013,
                lambda: float(past_res_elec_capacity_growth().loc["geot elec"]),
                lambda: if_then_else(
                    time() < start_year_p_growth_res_elec(),
                    lambda: float(past_res_elec_capacity_growth().loc["geot elec"]),
                    lambda: if_then_else(
                        time() < target_year_p_growth_res_elec(),
                        lambda: float(past_res_elec_capacity_growth().loc["geot elec"])
                        + (
                            float(p_res_elec_growth().loc["geot elec"])
                            - float(past_res_elec_capacity_growth().loc["geot elec"])
                        )
                        * (time() - start_year_p_growth_res_elec())
                        / (
                            target_year_p_growth_res_elec()
                            - start_year_p_growth_res_elec()
                        ),
                        lambda: float(p_res_elec_growth().loc["geot elec"]),
                    ),
                ),
            ),
            ["RES elec"],
            {"RES elec": ["geot elec"]},
        ),
        rearrange(
            if_then_else(
                time() < 2013,
                lambda: float(past_res_elec_capacity_growth().loc["solid bioE elec"]),
                lambda: if_then_else(
                    time() < start_year_p_growth_res_elec(),
                    lambda: float(
                        past_res_elec_capacity_growth().loc["solid bioE elec"]
                    ),
                    lambda: if_then_else(
                        time() < target_year_p_growth_res_elec(),
                        lambda: float(
                            past_res_elec_capacity_growth().loc["solid bioE elec"]
                        )
                        + (
                            float(p_res_elec_growth().loc["solid bioE elec"])
                            - float(
                                past_res_elec_capacity_growth().loc["solid bioE elec"]
                            )
                        )
                        * (time() - start_year_p_growth_res_elec())
                        / (
                            target_year_p_growth_res_elec()
                            - start_year_p_growth_res_elec()
                        ),
                        lambda: float(p_res_elec_growth().loc["solid bioE elec"]),
                    ),
                ),
            ),
            ["RES elec"],
            {"RES elec": ["solid bioE elec"]},
        ),
        rearrange(
            if_then_else(
                time() < 2014,
                lambda: float(past_res_elec_capacity_growth().loc["oceanic"]),
                lambda: if_then_else(
                    time() < start_year_p_growth_res_elec(),
                    lambda: float(past_res_elec_capacity_growth().loc["oceanic"]),
                    lambda: if_then_else(
                        time() < target_year_p_growth_res_elec(),
                        lambda: float(past_res_elec_capacity_growth().loc["oceanic"])
                        + (
                            float(p_res_elec_growth().loc["oceanic"])
                            - float(past_res_elec_capacity_growth().loc["oceanic"])
                        )
                        * (time() - start_year_p_growth_res_elec())
                        / (
                            target_year_p_growth_res_elec()
                            - start_year_p_growth_res_elec()
                        ),
                        lambda: float(p_res_elec_growth().loc["oceanic"]),
                    ),
                ),
            ),
            ["RES elec"],
            {"RES elec": ["oceanic"]},
        ),
        rearrange(
            if_then_else(
                time() < 2015,
                lambda: float(past_res_elec_capacity_growth().loc["wind onshore"]),
                lambda: if_then_else(
                    time() < start_year_p_growth_res_elec(),
                    lambda: float(past_res_elec_capacity_growth().loc["wind onshore"]),
                    lambda: if_then_else(
                        time() < target_year_p_growth_res_elec(),
                        lambda: float(
                            past_res_elec_capacity_growth().loc["wind onshore"]
                        )
                        + (
                            float(p_res_elec_growth().loc["wind onshore"])
                            - float(past_res_elec_capacity_growth().loc["wind onshore"])
                        )
                        * (time() - start_year_p_growth_res_elec())
                        / (
                            target_year_p_growth_res_elec()
                            - start_year_p_growth_res_elec()
                        ),
                        lambda: float(p_res_elec_growth().loc["wind onshore"]),
                    ),
                ),
            ),
            ["RES elec"],
            {"RES elec": ["wind onshore"]},
        ),
        rearrange(
            if_then_else(
                time() < 2014,
                lambda: float(past_res_elec_capacity_growth().loc["wind offshore"]),
                lambda: if_then_else(
                    time() < start_year_p_growth_res_elec(),
                    lambda: float(past_res_elec_capacity_growth().loc["wind offshore"]),
                    lambda: if_then_else(
                        time() < target_year_p_growth_res_elec(),
                        lambda: float(
                            past_res_elec_capacity_growth().loc["wind offshore"]
                        )
                        + (
                            float(p_res_elec_growth().loc["wind offshore"])
                            - float(
                                past_res_elec_capacity_growth().loc["wind offshore"]
                            )
                        )
                        * (time() - start_year_p_growth_res_elec())
                        / (
                            target_year_p_growth_res_elec()
                            - start_year_p_growth_res_elec()
                        ),
                        lambda: float(p_res_elec_growth().loc["wind offshore"]),
                    ),
                ),
            ),
            ["RES elec"],
            {"RES elec": ["wind offshore"]},
        ),
        rearrange(
            if_then_else(
                time() < 2014,
                lambda: float(past_res_elec_capacity_growth().loc["solar PV"]),
                lambda: if_then_else(
                    time() < start_year_p_growth_res_elec(),
                    lambda: float(past_res_elec_capacity_growth().loc["solar PV"]),
                    lambda: if_then_else(
                        time() < target_year_p_growth_res_elec(),
                        lambda: float(past_res_elec_capacity_growth().loc["solar PV"])
                        + (
                            float(p_res_elec_growth().loc["solar PV"])
                            - float(past_res_elec_capacity_growth().loc["solar PV"])
                        )
                        * (time() - start_year_p_growth_res_elec())
                        / (
                            target_year_p_growth_res_elec()
                            - start_year_p_growth_res_elec()
                        ),
                        lambda: float(p_res_elec_growth().loc["solar PV"]),
                    ),
                ),
            ),
            ["RES elec"],
            {"RES elec": ["solar PV"]},
        ),
        rearrange(
            if_then_else(
                time() < 2014,
                lambda: float(past_res_elec_capacity_growth().loc["CSP"]),
                lambda: if_then_else(
                    time() < start_year_p_growth_res_elec(),
                    lambda: float(past_res_elec_capacity_growth().loc["CSP"]),
                    lambda: if_then_else(
                        time() < target_year_p_growth_res_elec(),
                        lambda: float(past_res_elec_capacity_growth().loc["CSP"])
                        + (
                            float(p_res_elec_growth().loc["CSP"])
                            - float(past_res_elec_capacity_growth().loc["CSP"])
                        )
                        * (time() - start_year_p_growth_res_elec())
                        / (
                            target_year_p_growth_res_elec()
                            - start_year_p_growth_res_elec()
                        ),
                        lambda: float(p_res_elec_growth().loc["CSP"]),
                    ),
                ),
            ),
            ["RES elec"],
            {"RES elec": ["CSP"]},
        ),
    )


@subs(["RES elec"], _subscript_dict)
def adapt_growth_res_elec_after_allocation():
    """
    Real Name: adapt growth RES elec after allocation
    Original Eqn: IF THEN ELSE(activate EROI allocation rule=0, adapt growth RES elec[RES elec] , adapt growth RES elec[RES elec]*EROI allocation rule per RES elec[RES elec])*constraint elec storage availability[RES elec]
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Annual growth per RES elec technology after accounting for the allocation
        rule.
    """
    return (
        if_then_else(
            activate_eroi_allocation_rule() == 0,
            lambda: adapt_growth_res_elec(),
            lambda: adapt_growth_res_elec() * eroi_allocation_rule_per_res_elec(),
        )
        * constraint_elec_storage_availability()
    )


@subs(["RES elec"], _subscript_dict)
def cp_baseload_reduction():
    """
    Real Name: Cp baseload reduction
    Original Eqn: Cp RES elec[RES elec]/"Cp-ini RES elec"[RES elec]
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']


    """
    return cp_res_elec() / cpini_res_elec()


@subs(["RES elec"], _subscript_dict)
def cp_res_elec():
    """
    Real Name: Cp RES elec
    Original Eqn: MAX(min Cp baseload RES[RES elec], "Cp-ini RES elec"[RES elec]*Cp exogenous RES elec reduction[RES elec]*shortage BioE for elec[RES elec])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Capacity factor of RES technologies (after accounting for the
        overcapacities required to manage the intermittency of RES elec variables).
    """
    return np.maximum(
        min_cp_baseload_res(),
        cpini_res_elec() * cp_exogenous_res_elec_reduction() * shortage_bioe_for_elec(),
    )


@subs(["RES elec"], _subscript_dict)
def cpini_res_elec():
    """
    Real Name: "Cp-ini RES elec"
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'cp_initial_res_elec*')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['RES elec']

    Initial capacity factor (before accounting for the reduction of Cp of the
        base-load plants with the penetration of the intermittent RES (solar and
        wind) in the electricity generation mix).
    """
    return _ext_constant_cpini_res_elec()


def fe_real_tot_generation_res_elec_twh():
    """
    Real Name: FE real tot generation RES elec TWh
    Original Eqn: MIN(MAX(Total FE Elec demand after priorities TWh, 0), potential tot generation RES elec TWh)
    Units: TWh
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return np.minimum(
        np.maximum(total_fe_elec_demand_after_priorities_twh(), 0),
        potential_tot_generation_res_elec_twh(),
    )


@subs(["RES elec"], _subscript_dict)
def historic_new_required_capacity_res_elec():
    """
    Real Name: Historic new required capacity RES elec
    Original Eqn: table hist capacity RES elec[RES elec]((INTEGER(Time+1))+"total time plan+constr RES elec"[RES elec])-table hist capacity RES elec[RES elec]((INTEGER(Time))+"total time plan+constr RES elec"[RES elec])
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    (Assuming 100% of planned was planned and constructed).
    """
    return table_hist_capacity_res_elec(
        (integer(time() + 1)) + total_time_planconstr_res_elec()
    ) - table_hist_capacity_res_elec(
        (integer(time())) + total_time_planconstr_res_elec()
    )


@subs(["RES elec"], _subscript_dict)
def initial_capacity_in_construction_res_elec():
    """
    Real Name: initial capacity in construction RES elec
    Original Eqn: initial required capacity RES elec[RES elec]
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Initial capacity of RES by technology in construction (year 1995). We
        assume that it is the same than the additional installed capacity between
        1995 and 1996.
    """
    return initial_required_capacity_res_elec()


@subs(["RES elec"], _subscript_dict)
def initial_instal_cap_res_elec():
    """
    Real Name: initial instal cap RES elec
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'initial_installed_capacity_res_for_electricity*')
    Units: TW
    Limits: (None, None)
    Type: constant
    Subs: ['RES elec']

    Installed capacity per RES elec by technology in the initial year 1995.
    """
    return _ext_constant_initial_instal_cap_res_elec()


@subs(["RES elec"], _subscript_dict)
def initial_required_capacity_res_elec():
    """
    Real Name: initial required capacity RES elec
    Original Eqn: table hist capacity RES elec[RES elec](1996)-table hist capacity RES elec[RES elec](1995)
    Units: TW
    Limits: (None, None)
    Type: constant
    Subs: ['RES elec']

    Initial required capacity of RES by technology (year 1995). We assume that
        it is the same than the additional installed capacity between 1995 and
        1996.
    """
    return table_hist_capacity_res_elec(1996) - table_hist_capacity_res_elec(1995)


@subs(["RES elec"], _subscript_dict)
def installed_capacity_res_elec_delayed_1yr():
    """
    Real Name: installed capacity RES elec delayed 1yr
    Original Eqn: DELAY FIXED ( installed capacity RES elec TW[RES elec], 1, 0)
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Annual installed capacity of RES elec technologies for electricity
        generation delayed 1 year.
    """
    return _delayfixed_installed_capacity_res_elec_delayed_1yr()


@subs(["RES elec"], _subscript_dict)
def installed_capacity_res_elec_tw():
    """
    Real Name: installed capacity RES elec TW
    Original Eqn: INTEG ( RES elec capacity under construction TW[RES elec]-wear RES elec[RES elec] , initial instal cap RES elec[RES elec])
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Annual installed capacity of RES elec technologies for electricity
        generation.
    """
    return _integ_installed_capacity_res_elec_tw()


@subs(["RES elec"], _subscript_dict)
def lifetime_res_elec():
    """
    Real Name: lifetime RES elec
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'lifetime_res_elec*')
    Units: Years
    Limits: (None, None)
    Type: constant
    Subs: ['RES elec']

    Lifetime of each RES technology for electricity generation.
    """
    return _ext_constant_lifetime_res_elec()


@subs(["RES elec"], _subscript_dict)
def min_cp_baseload_res():
    """
    Real Name: min Cp baseload RES
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'minimum_cp_baseload_res*')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: ['RES elec']

    Assumption of minimum Cp for baseload RES plants.
    """
    return _ext_constant_min_cp_baseload_res()


@subs(["RES elec"], _subscript_dict)
def new_capacity_installed_growth_rate_res_elec():
    """
    Real Name: new capacity installed growth rate RES elec
    Original Eqn: -1+ZIDZ( installed capacity RES elec TW[RES elec], installed capacity RES elec delayed 1yr[RES elec] )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Annual RES elec capacity installed growth rate.
    """
    return -1 + zidz(
        installed_capacity_res_elec_tw(), installed_capacity_res_elec_delayed_1yr()
    )


@subs(["RES elec"], _subscript_dict)
def new_required_capacity_res_elec():
    """
    Real Name: new required capacity RES elec
    Original Eqn: IF THEN ELSE(Time<(2015-"total time plan+constr RES elec"[RES elec]), Historic new required capacity RES elec[RES elec],installed capacity RES elec TW[RES elec]*adapt growth RES elec after allocation[RES elec]*remaining potential constraint on new RES elec capacity [RES elec]*abundance RES elec2)
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    New required capacity of RES technologies for electricity generation. We
        assume 100% of the required infraestructure is planned and constructed.
    """
    return if_then_else(
        time() < (2015 - total_time_planconstr_res_elec()),
        lambda: historic_new_required_capacity_res_elec(),
        lambda: installed_capacity_res_elec_tw()
        * adapt_growth_res_elec_after_allocation()
        * remaining_potential_constraint_on_new_res_elec_capacity()
        * abundance_res_elec2(),
    )


@subs(["RES elec"], _subscript_dict)
def new_res_elec_capacity_under_planning():
    """
    Real Name: new RES elec capacity under planning
    Original Eqn: MAX(0, required capacity RES elec TW[RES elec]/MAX(time planification RES elec[RES elec],TIME STEP))
    Units: TW/Year
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    New RES infraestructure for electricity generation capacity under planning.
    """
    return np.maximum(
        0,
        required_capacity_res_elec_tw()
        / np.maximum(time_planification_res_elec(), time_step()),
    )


def p_csp_growth():
    """
    Real Name: P CSP growth
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'p_CSP_growth')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual growth in relation to the existing installed capacity.
    """
    return _ext_constant_p_csp_growth()


def p_geot_growth():
    """
    Real Name: P geot growth
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'p_geot_elect_growth')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual growth in relation to the existing installed capacity.
    """
    return _ext_constant_p_geot_growth()


def p_hydro_growth():
    """
    Real Name: P hydro growth
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'p_hydro_growth')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual growth in relation to the existing installed capacity.
    """
    return _ext_constant_p_hydro_growth()


def p_oceanic_growth():
    """
    Real Name: P oceanic growth
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'p_oceanic_growth')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual growth in relation to the existing installed capacity.
    """
    return _ext_constant_p_oceanic_growth()


@subs(["RES elec"], _subscript_dict)
def p_res_elec_growth():
    """
    Real Name: P RES elec growth
    Original Eqn:
      P hydro growth
        .
        .
        .
      P CSP growth
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    For hydro, geot-elec and solid bioenergy this variable represents the
        projected annual growth in relation to past growth trends, for the rest of
        RES elec (oceanic, wind & solar), it represents the annual growth in
        relation to the existing installed capacity.
    """
    return xrmerge(
        rearrange(p_hydro_growth(), ["RES elec"], {"RES elec": ["hydro"]}),
        rearrange(p_geot_growth(), ["RES elec"], {"RES elec": ["geot elec"]}),
        rearrange(
            p_solid_bioeelec_growth(), ["RES elec"], {"RES elec": ["solid bioE elec"]}
        ),
        rearrange(p_oceanic_growth(), ["RES elec"], {"RES elec": ["oceanic"]}),
        rearrange(
            p_wind_onshore_growth(), ["RES elec"], {"RES elec": ["wind onshore"]}
        ),
        rearrange(
            p_wind_offshore_growth(), ["RES elec"], {"RES elec": ["wind offshore"]}
        ),
        rearrange(p_solar_pv_growth(), ["RES elec"], {"RES elec": ["solar PV"]}),
        rearrange(p_csp_growth(), ["RES elec"], {"RES elec": ["CSP"]}),
    )


def p_solar_pv_growth():
    """
    Real Name: P solar PV growth
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'p_solar_PV')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual growth in relation to the existing installed capacity.
    """
    return _ext_constant_p_solar_pv_growth()


def p_solid_bioeelec_growth():
    """
    Real Name: "P solid bioE-elec growth"
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'p_solid_bioe_elect_growth')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual growth in relation to the existing installed capacity.
    """
    return _ext_constant_p_solid_bioeelec_growth()


def p_wind_offshore_growth():
    """
    Real Name: P wind offshore growth
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'p_wind_offshore_growth')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual growth in relation to the existing installed capacity.
    """
    return _ext_constant_p_wind_offshore_growth()


def p_wind_onshore_growth():
    """
    Real Name: P wind onshore growth
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'p_wind_onshore_growth')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual growth in relation to the existing installed capacity.
    """
    return _ext_constant_p_wind_onshore_growth()


@subs(["RES elec"], _subscript_dict)
def past_res_elec_capacity_growth():
    """
    Real Name: past RES elec capacity growth
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'historic_growth_res_for_electricity*')
    Units: 1/Year
    Limits: (None, None)
    Type: constant
    Subs: ['RES elec']

    Current growth levels.
    """
    return _ext_constant_past_res_elec_capacity_growth()


@subs(["RES elec"], _subscript_dict)
def potential_generation_res_elec_twh():
    """
    Real Name: potential generation RES elec TWh
    Original Eqn: installed capacity RES elec TW[RES elec]*Cp RES elec[RES elec]/TWe per TWh
    Units: TWh
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Potential generation of electricity by RES technology given the installed
        capacity.
    """
    return installed_capacity_res_elec_tw() * cp_res_elec() / twe_per_twh()


@subs(["RES elec"], _subscript_dict)
def potential_res_elec_after_intermitt_twh():
    """
    Real Name: potential RES elec after intermitt TWh
    Original Eqn: max RES elec TWe[RES elec]*Cp baseload reduction[RES elec]/TWe per TWh
    Units: TWh
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Potential of RES for electricity per technology after accounting for the
        reduction of the maximal potential given the reduction of the Cp.
    """
    return max_res_elec_twe() * cp_baseload_reduction() / twe_per_twh()


def potential_tot_generation_res_elec_twh():
    """
    Real Name: potential tot generation RES elec TWh
    Original Eqn: SUM(potential generation RES elec TWh[RES elec!])
    Units: TWh
    Limits: (None, None)
    Type: component
    Subs: None

    Total potential generation of electricity from RES given the installed
        capacity.
    """
    return sum(potential_generation_res_elec_twh(), dim=("RES elec",))


def potential_tot_res_elec_after_intermitt():
    """
    Real Name: potential tot RES elec after intermitt
    Original Eqn: SUM(potential RES elec after intermitt TWh[RES elec!])
    Units: TWh
    Limits: (None, None)
    Type: component
    Subs: None

    Total potential of RES for electricity after accounting for the reduction
        of the maximal potential given the reduction of the Cp.
    """
    return sum(potential_res_elec_after_intermitt_twh(), dim=("RES elec",))


@subs(["RES elec"], _subscript_dict)
def real_cp_res_elec():
    """
    Real Name: real Cp RES elec
    Original Eqn: IF THEN ELSE(Time<2015,Cp RES elec[RES elec], IF THEN ELSE(installed capacity RES elec TW[RES elec]=0,0, real generation RES elec TWh[RES elec]*TWe per TWh/installed capacity RES elec TW[RES elec]))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']


    """
    return if_then_else(
        time() < 2015,
        lambda: cp_res_elec(),
        lambda: if_then_else(
            installed_capacity_res_elec_tw() == 0,
            lambda: 0,
            lambda: real_generation_res_elec_twh()
            * twe_per_twh()
            / installed_capacity_res_elec_tw(),
        ),
    )


@subs(["RES elec"], _subscript_dict)
def real_generation_res_elec_twh():
    """
    Real Name: real generation RES elec TWh
    Original Eqn: potential generation RES elec TWh[RES elec]*(1-RES elec tot overcapacity )*shortage BioE for elec[RES elec]
    Units: TWh
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Electricity generation by RES technology.
    """
    return (
        potential_generation_res_elec_twh()
        * (1 - res_elec_tot_overcapacity())
        * shortage_bioe_for_elec()
    )


@subs(["RES elec"], _subscript_dict)
def remaining_potential_constraint_on_new_res_elec_capacity():
    """
    Real Name: remaining potential constraint on new RES elec capacity
    Original Eqn: IF THEN ELSE(remaining potential RES elec after intermitt[RES elec]>threshold remaining potential new capacity,1,remaining potential RES elec after intermitt [RES elec]*(1/threshold remaining potential new capacity))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Constraint of remaining potential on new RES elec capacity.        Another alternative: SQRT(remaining potential RES elec after intermitt[RES
        elec])
    """
    return if_then_else(
        remaining_potential_res_elec_after_intermitt()
        > threshold_remaining_potential_new_capacity(),
        lambda: 1,
        lambda: remaining_potential_res_elec_after_intermitt()
        * (1 / threshold_remaining_potential_new_capacity()),
    )


@subs(["RES elec"], _subscript_dict)
def remaining_potential_res_elec_after_intermitt():
    """
    Real Name: remaining potential RES elec after intermitt
    Original Eqn: IF THEN ELSE(potential RES elec after intermitt TWh[RES elec] > potential generation RES elec TWh[RES elec], ZIDZ( potential RES elec after intermitt TWh[RES elec] -potential generation RES elec TWh[RES elec], potential RES elec after intermitt TWh[RES elec] ), 0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']


    """
    return if_then_else(
        potential_res_elec_after_intermitt_twh() > potential_generation_res_elec_twh(),
        lambda: zidz(
            potential_res_elec_after_intermitt_twh()
            - potential_generation_res_elec_twh(),
            potential_res_elec_after_intermitt_twh(),
        ),
        lambda: 0,
    )


def remaining_potential_tot_res_elec_after_intermitt():
    """
    Real Name: remaining potential tot RES elec after intermitt
    Original Eqn: IF THEN ELSE(potential tot RES elec after intermitt > FE real tot generation RES elec TWh, (potential tot RES elec after intermitt-FE real tot generation RES elec TWh)/potential tot RES elec after intermitt, 0)
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
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


@subs(["RES elec"], _subscript_dict)
def replacement_capacity_res_elec():
    """
    Real Name: replacement capacity RES elec
    Original Eqn: IF THEN ELSE(Time<2015,0,replacement rate RES elec[RES elec]*wear RES elec[RES elec]*(1-RES elec tot overcapacity ))*constraint elec storage availability[RES elec]*shortage BioE for elec[RES elec]^2
    Units: TW/Year
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Annual replacement of RES infrastructure for electricity generation by
        technology. It is assumed that the step of planning the replaced
        infrastructure can be done while the infraestructure to be replaced is
        still under operation. For replaced infraestructures, the construction
        time should be smaller than for new infaestructures, however we compensate
        for this assuming that the demantling time is included in onstruction time
        for replaced infrastructure.
    """
    return (
        if_then_else(
            time() < 2015,
            lambda: 0,
            lambda: replacement_rate_res_elec()
            * wear_res_elec()
            * (1 - res_elec_tot_overcapacity()),
        )
        * constraint_elec_storage_availability()
        * shortage_bioe_for_elec() ** 2
    )


@subs(["RES elec"], _subscript_dict)
def replacement_rate_res_elec():
    """
    Real Name: replacement rate RES elec
    Original Eqn: IF THEN ELSE(potential generation RES elec TWh[RES elec]<potential RES elec after intermitt TWh[RES elec],1,0.9)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Replacement rate of RES for electricity: by default all decommissioned
        capacity is replaced (=1). In the case of overcapacity in relation to the
        potential after accounting for intermittency, we reduce the annual
        replacement rate to 0.9.
    """
    return if_then_else(
        potential_generation_res_elec_twh() < potential_res_elec_after_intermitt_twh(),
        lambda: 1,
        lambda: 0.9,
    )


@subs(["RES elec"], _subscript_dict)
def required_capacity_res_elec_tw():
    """
    Real Name: required capacity RES elec TW
    Original Eqn: INTEG ( new required capacity RES elec[RES elec]-new RES elec capacity under planning[RES elec], initial required capacity RES elec[RES elec])
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Required capacity of RES technologies for electricity generation.
    """
    return _integ_required_capacity_res_elec_tw()


@subs(["RES elec"], _subscript_dict)
def res_elec_capacity_under_construction_tw():
    """
    Real Name: RES elec capacity under construction TW
    Original Eqn: RES elec planned capacity TW[RES elec]/MAX(time construction RES elec[RES elec],TIME STEP)
    Units: TW/Year
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    RES infraestructure for electricity generation capacity under construction.
    """
    return res_elec_planned_capacity_tw() / np.maximum(
        time_construction_res_elec(), time_step()
    )


@subs(["RES elec"], _subscript_dict)
def res_elec_planned_capacity_tw():
    """
    Real Name: RES elec planned capacity TW
    Original Eqn: INTEG ( new RES elec capacity under planning[RES elec]+replacement capacity RES elec[RES elec]-RES elec capacity under construction TW[RES elec], initial capacity in construction RES elec[RES elec])
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Planned capacity of RES for electricity.
    """
    return _integ_res_elec_planned_capacity_tw()


def res_elec_tot_overcapacity():
    """
    Real Name: RES elec tot overcapacity
    Original Eqn: IF THEN ELSE(potential tot generation RES elec TWh=0,0, (potential tot generation RES elec TWh-FE real tot generation RES elec TWh)/potential tot generation RES elec TWh)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Overcapacity for each technology RES for electricity taking into account
        the installed capacity and the real generation.
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


def start_year_p_growth_res_elec():
    """
    Real Name: Start year P growth RES elec
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'start_year_p_growth_RES_elec')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Start year of the policy growth of RES technologies for generating
        electricity.
    """
    return _ext_constant_start_year_p_growth_res_elec()


def table_hist_capacity_res_elec(x):
    """
    Real Name: table hist capacity RES elec
    Original Eqn: ( GET DIRECT LOOKUPS('../energy.xlsx', 'Austria', 'time_historic_data', 'historic_installed_capacity_res_for_electricity'))
    Units: TW/Year
    Limits: (None, None)
    Type: lookup
    Subs: ['RES elec']


    """
    return _ext_lookup_table_hist_capacity_res_elec(x)


def target_year_p_growth_res_elec():
    """
    Real Name: Target year P growth RES elec
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'target_year_p_growth_RES_elec')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Target year of the policy growth of RES technologies for generating
        electricity.
    """
    return _ext_constant_target_year_p_growth_res_elec()


def threshold_remaining_potential_new_capacity():
    """
    Real Name: threshold remaining potential new capacity
    Original Eqn: 0.5
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None

    This threshold represents the level of the remaining potential that starts
        to affects the planification of new RES elec capacity (decreasing
        returns). Avoid problems of (erroneously) affecting past historical growth
        trends.
    """
    return 0.5


@subs(["RES elec"], _subscript_dict)
def time_95pc_ts_potential_res_elec():
    """
    Real Name: Time 95pc TS potential RES elec
    Original Eqn: IF THEN ELSE(remaining potential RES elec after intermitt[RES elec]>0.05, 0, Time)
    Units:
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Time when the remaining resource availability falls bellow 5% of the
        techno-ecological potential, i.e. when the 95% of the techno-ecological
        potential is reached.
    """
    return if_then_else(
        remaining_potential_res_elec_after_intermitt() > 0.05, lambda: 0, lambda: time()
    )


@subs(["RES elec"], _subscript_dict)
def time_construction_res_elec():
    """
    Real Name: time construction RES elec
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'construction_time_res_elec*')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: ['RES elec']

    Average construction time for each RES generating electricity.        For replaced infraestructures, the construction time should be smaller
        than for new infaestructures, however we compensate for this assuming that
        the demantling time is included in onstruction time for replaced
        infrastructure.
    """
    return _ext_constant_time_construction_res_elec()


@subs(["RES elec"], _subscript_dict)
def time_planification_res_elec():
    """
    Real Name: time planification RES elec
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'planning_time_res_elec*')
    Units: Year
    Limits: (None, None)
    Type: constant
    Subs: ['RES elec']

    Average planification time for each RES generating electricity.
    """
    return _ext_constant_time_planification_res_elec()


@subs(["RES elec"], _subscript_dict)
def total_time_planconstr_res_elec():
    """
    Real Name: "total time plan+constr RES elec"
    Original Eqn: MAX(time construction RES elec[RES elec],TIME STEP)+MAX(time planification RES elec[RES elec],TIME STEP)
    Units: Year
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']


    """
    return np.maximum(time_construction_res_elec(), time_step()) + np.maximum(
        time_planification_res_elec(), time_step()
    )


@subs(["RES elec"], _subscript_dict)
def wear_res_elec():
    """
    Real Name: wear RES elec
    Original Eqn: IF THEN ELSE(Time<2015, 0, installed capacity RES elec TW[RES elec]/lifetime RES elec[RES elec])
    Units: TW/Year
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Depreciation of RES infraestructures.
    """
    return if_then_else(
        time() < 2015,
        lambda: 0,
        lambda: installed_capacity_res_elec_tw() / lifetime_res_elec(),
    )


_ext_constant_cpini_res_elec = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "cp_initial_res_elec*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    "_ext_constant_cpini_res_elec",
)


_ext_constant_initial_instal_cap_res_elec = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "initial_installed_capacity_res_for_electricity*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    "_ext_constant_initial_instal_cap_res_elec",
)


_delayfixed_installed_capacity_res_elec_delayed_1yr = DelayFixed(
    lambda: installed_capacity_res_elec_tw(),
    lambda: 1,
    lambda: 0,
    time_step,
    "_delayfixed_installed_capacity_res_elec_delayed_1yr",
)


@subs(["RES elec"], _subscript_dict)
def _integ_init_installed_capacity_res_elec_tw():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for installed_capacity_res_elec_tw
    Limits: None
    Type: setup
    Subs: ['RES elec']

    Provides initial conditions for installed_capacity_res_elec_tw function
    """
    return initial_instal_cap_res_elec()


@subs(["RES elec"], _subscript_dict)
def _integ_input_installed_capacity_res_elec_tw():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for installed_capacity_res_elec_tw
    Limits: None
    Type: component
    Subs: ['RES elec']

    Provides derivative for installed_capacity_res_elec_tw function
    """
    return res_elec_capacity_under_construction_tw() - wear_res_elec()


_integ_installed_capacity_res_elec_tw = Integ(
    _integ_input_installed_capacity_res_elec_tw,
    _integ_init_installed_capacity_res_elec_tw,
    "_integ_installed_capacity_res_elec_tw",
)


_ext_constant_lifetime_res_elec = ExtConstant(
    "../energy.xlsx",
    "Global",
    "lifetime_res_elec*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    "_ext_constant_lifetime_res_elec",
)


_ext_constant_min_cp_baseload_res = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "minimum_cp_baseload_res*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    "_ext_constant_min_cp_baseload_res",
)


_ext_constant_p_csp_growth = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "p_CSP_growth",
    {},
    _root,
    "_ext_constant_p_csp_growth",
)


_ext_constant_p_geot_growth = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "p_geot_elect_growth",
    {},
    _root,
    "_ext_constant_p_geot_growth",
)


_ext_constant_p_hydro_growth = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "p_hydro_growth",
    {},
    _root,
    "_ext_constant_p_hydro_growth",
)


_ext_constant_p_oceanic_growth = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "p_oceanic_growth",
    {},
    _root,
    "_ext_constant_p_oceanic_growth",
)


_ext_constant_p_solar_pv_growth = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "p_solar_PV",
    {},
    _root,
    "_ext_constant_p_solar_pv_growth",
)


_ext_constant_p_solid_bioeelec_growth = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "p_solid_bioe_elect_growth",
    {},
    _root,
    "_ext_constant_p_solid_bioeelec_growth",
)


_ext_constant_p_wind_offshore_growth = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "p_wind_offshore_growth",
    {},
    _root,
    "_ext_constant_p_wind_offshore_growth",
)


_ext_constant_p_wind_onshore_growth = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "p_wind_onshore_growth",
    {},
    _root,
    "_ext_constant_p_wind_onshore_growth",
)


_ext_constant_past_res_elec_capacity_growth = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "historic_growth_res_for_electricity*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    "_ext_constant_past_res_elec_capacity_growth",
)


@subs(["RES elec"], _subscript_dict)
def _integ_init_required_capacity_res_elec_tw():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for required_capacity_res_elec_tw
    Limits: None
    Type: setup
    Subs: ['RES elec']

    Provides initial conditions for required_capacity_res_elec_tw function
    """
    return initial_required_capacity_res_elec()


@subs(["RES elec"], _subscript_dict)
def _integ_input_required_capacity_res_elec_tw():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for required_capacity_res_elec_tw
    Limits: None
    Type: component
    Subs: ['RES elec']

    Provides derivative for required_capacity_res_elec_tw function
    """
    return new_required_capacity_res_elec() - new_res_elec_capacity_under_planning()


_integ_required_capacity_res_elec_tw = Integ(
    _integ_input_required_capacity_res_elec_tw,
    _integ_init_required_capacity_res_elec_tw,
    "_integ_required_capacity_res_elec_tw",
)


@subs(["RES elec"], _subscript_dict)
def _integ_init_res_elec_planned_capacity_tw():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for res_elec_planned_capacity_tw
    Limits: None
    Type: setup
    Subs: ['RES elec']

    Provides initial conditions for res_elec_planned_capacity_tw function
    """
    return initial_capacity_in_construction_res_elec()


@subs(["RES elec"], _subscript_dict)
def _integ_input_res_elec_planned_capacity_tw():
    """
    Real Name: Implicit
    Original Eqn: None
    Units: See docs for res_elec_planned_capacity_tw
    Limits: None
    Type: component
    Subs: ['RES elec']

    Provides derivative for res_elec_planned_capacity_tw function
    """
    return (
        new_res_elec_capacity_under_planning()
        + replacement_capacity_res_elec()
        - res_elec_capacity_under_construction_tw()
    )


_integ_res_elec_planned_capacity_tw = Integ(
    _integ_input_res_elec_planned_capacity_tw,
    _integ_init_res_elec_planned_capacity_tw,
    "_integ_res_elec_planned_capacity_tw",
)


_ext_constant_start_year_p_growth_res_elec = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "start_year_p_growth_RES_elec",
    {},
    _root,
    "_ext_constant_start_year_p_growth_res_elec",
)


_ext_lookup_table_hist_capacity_res_elec = ExtLookup(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_installed_capacity_res_for_electricity",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    "_ext_lookup_table_hist_capacity_res_elec",
)


_ext_constant_target_year_p_growth_res_elec = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "target_year_p_growth_RES_elec",
    {},
    _root,
    "_ext_constant_target_year_p_growth_res_elec",
)


_ext_constant_time_construction_res_elec = ExtConstant(
    "../energy.xlsx",
    "Global",
    "construction_time_res_elec*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    "_ext_constant_time_construction_res_elec",
)


_ext_constant_time_planification_res_elec = ExtConstant(
    "../energy.xlsx",
    "Global",
    "planning_time_res_elec*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    "_ext_constant_time_planification_res_elec",
)
