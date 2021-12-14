"""
Module phs_ee
Translated using PySD version 2.1.0
"""


def adapt_growth_phs():
    """
    Real Name: adapt growth PHS
    Original Eqn: IF THEN ELSE(Time<2015, past PHS capacity growth, IF THEN ELSE(Time<Start year P growth RES elec, past PHS capacity growth, IF THEN ELSE(Time<Target year P growth RES elec, past PHS capacity growth+(P PHS growth-past PHS capacity growth)*(Time-Start year P growth RES elec)/(Target year P growth RES elec-Start year P growth RES elec), P PHS growth)*(1+abundance storage)))
    Units: 1/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual growth per RES elec technology. Modeling of a soft transition from
        current historic annual growth to reach the policy-objective in the target
        year.
    """
    return if_then_else(
        time() < 2015,
        lambda: past_phs_capacity_growth(),
        lambda: if_then_else(
            time() < start_year_p_growth_res_elec(),
            lambda: past_phs_capacity_growth(),
            lambda: if_then_else(
                time() < target_year_p_growth_res_elec(),
                lambda: past_phs_capacity_growth()
                + (p_phs_growth() - past_phs_capacity_growth())
                * (time() - start_year_p_growth_res_elec())
                / (target_year_p_growth_res_elec() - start_year_p_growth_res_elec()),
                lambda: p_phs_growth(),
            )
            * (1 + abundance_storage()),
        ),
    )


def cp_phs():
    """
    Real Name: Cp PHS
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'cp_phs')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Capacity factor of pumped hydro storage (PHS).
    """
    return _ext_constant_cp_phs()


def historic_new_required_capacity_phs():
    """
    Real Name: Historic new required capacity PHS
    Original Eqn: table hist capacity PHS(Time+"total time plan+constr RES elec"[hydro]+1)-table hist capacity PHS(Time+"total time plan+constr RES elec"[hydro])
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None

    (Assuming 100% of planned was planned and constructed).
    """
    return table_hist_capacity_phs(
        time() + float(total_time_planconstr_res_elec().loc["hydro"]) + 1
    ) - table_hist_capacity_phs(
        time() + float(total_time_planconstr_res_elec().loc["hydro"])
    )


def initial_capacity_in_construction_phs():
    """
    Real Name: initial capacity in construction PHS
    Original Eqn: initial required capacity PHS
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None

    Initial capacity of PHS in construction (year 1995). We assume that it is
        the same than the additional installed capacity between 1995 and 1996.
    """
    return initial_required_capacity_phs()


def initial_instal_cap_phs():
    """
    Real Name: initial instal cap PHS
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'initial_installed_capacity_phs')
    Units: TW
    Limits: (None, None)
    Type: constant
    Subs: None

    Installed capacity of PHS in the initial year 1995.
    """
    return _ext_constant_initial_instal_cap_phs()


def initial_required_capacity_phs():
    """
    Real Name: initial required capacity PHS
    Original Eqn: table hist capacity PHS(1996)-table hist capacity PHS(1995)
    Units: TW
    Limits: (None, None)
    Type: constant
    Subs: None

    Initial required capacity of PHS (year 1995). We assume that it is the
        same than the additional installed capacity between 1995 and 1996.
    """
    return table_hist_capacity_phs(1996) - table_hist_capacity_phs(1995)


def installed_capacity_phs_tw():
    """
    Real Name: installed capacity PHS TW
    Original Eqn: INTEG ( PHS capacity under construction-wear PHS, initial instal cap PHS)
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_installed_capacity_phs_tw()


def max_capacity_potential_phs():
    """
    Real Name: max capacity potential PHS
    Original Eqn: max potential PHS TWe/Cp PHS
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None

    Maximum capacity potential of PHS.
    """
    return max_potential_phs_twe() / cp_phs()


def max_potential_phs_twe():
    """
    Real Name: max potential PHS TWe
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'C26')
    Units: TWe
    Limits: (None, None)
    Type: constant
    Subs: None

    Maximum potential for PHS.
    """
    return _ext_constant_max_potential_phs_twe()


def max_potential_phs_twh():
    """
    Real Name: max potential PHS TWh
    Original Eqn: max capacity potential PHS*Cp PHS/TWe per TWh
    Units: TWh
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return max_capacity_potential_phs() * cp_phs() / twe_per_twh()


def new_phs_capacity_under_planning():
    """
    Real Name: new PHS capacity under planning
    Original Eqn: required capacity PHS/time planification RES elec[hydro]
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return required_capacity_phs() / float(time_planification_res_elec().loc["hydro"])


def new_required_phs_capacity():
    """
    Real Name: new required PHS capacity
    Original Eqn: IF THEN ELSE(Time<(2014-"total time plan+constr RES elec"[hydro]), Historic new required capacity PHS, installed capacity PHS TW *adapt growth PHS*remaining potential constraint on new PHS capacity)
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None

    IF THEN ELSE(Time<(2014-"total time plan+constr RES elec"[RES elec]), Historic new
        required capacity RES elec[RES elec],installed capacity RES elec TW[RES
        elec]*adapt growth RES elec after allocation[RES elec]*remaining potential
        constraint on new RES elec capacity[RES elec]*abundance RES elec2)                0.9*installed capacity PHS TW*(1-(installed capacity PHS TW/demand storage
        capacity))
    """
    return if_then_else(
        time() < (2014 - float(total_time_planconstr_res_elec().loc["hydro"])),
        lambda: historic_new_required_capacity_phs(),
        lambda: installed_capacity_phs_tw()
        * adapt_growth_phs()
        * remaining_potential_constraint_on_new_phs_capacity(),
    )


def output_phs_over_lifetime():
    """
    Real Name: output PHS over lifetime
    Original Eqn: Cp PHS*PHS capacity under construction*(1/TWe per TWh)*lifetime RES elec[hydro]*EJ per TWh
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total electricity output generated over the full operation of the
        infrastructure of the new capacity installed.
    """
    return (
        cp_phs()
        * phs_capacity_under_construction()
        * (1 / twe_per_twh())
        * float(lifetime_res_elec().loc["hydro"])
        * ej_per_twh()
    )


def p_phs_growth():
    """
    Real Name: P PHS growth
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_aut.xlsx', 'BAU', 'F37')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Annual growth in relation to the existing installed capacity.
    """
    return _ext_constant_p_phs_growth()


def past_phs_capacity_growth():
    """
    Real Name: past PHS capacity growth
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Austria', 'historic_growth_phs_capacity')
    Units: 1/Year
    Limits: (None, None)
    Type: constant
    Subs: None

    Current growth levels.
    """
    return _ext_constant_past_phs_capacity_growth()


def phs_capacity_under_construction():
    """
    Real Name: PHS capacity under construction
    Original Eqn: PHS planned capacity/time construction RES elec[hydro]
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return phs_planned_capacity() / float(time_construction_res_elec().loc["hydro"])


def phs_planned_capacity():
    """
    Real Name: PHS planned capacity
    Original Eqn: INTEG ( new PHS capacity under planning+replacement capacity PHS-PHS capacity under construction, initial capacity in construction PHS)
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_phs_planned_capacity()


def real_fe_elec_stored_phs_twh():
    """
    Real Name: real FE elec stored PHS TWh
    Original Eqn: installed capacity PHS TW*Cp PHS/TWe per TWh
    Units: TWh
    Limits: (None, None)
    Type: component
    Subs: None

    Electricity stored in pumped hydro storage plants. It does not add up to
        the electricity generation of other sources since this electricity has
        already been accounted for! (stored).
    """
    return installed_capacity_phs_tw() * cp_phs() / twe_per_twh()


def remaining_potential_constraint_on_new_phs_capacity():
    """
    Real Name: remaining potential constraint on new PHS capacity
    Original Eqn: IF THEN ELSE(remaining potential PHS>threshold remaining potential new capacity,1,remaining potential PHS*(1/threshold remaining potential new capacity))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        remaining_potential_phs() > threshold_remaining_potential_new_capacity(),
        lambda: 1,
        lambda: remaining_potential_phs()
        * (1 / threshold_remaining_potential_new_capacity()),
    )


def remaining_potential_phs():
    """
    Real Name: remaining potential PHS
    Original Eqn: IF THEN ELSE(max capacity potential PHS > installed capacity PHS TW , (max capacity potential PHS-installed capacity PHS TW)/max capacity potential PHS,0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        max_capacity_potential_phs() > installed_capacity_phs_tw(),
        lambda: (max_capacity_potential_phs() - installed_capacity_phs_tw())
        / max_capacity_potential_phs(),
        lambda: 0,
    )


def replacement_capacity_phs():
    """
    Real Name: replacement capacity PHS
    Original Eqn: IF THEN ELSE(Time<2015,0,replacement rate PHS*wear PHS)
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None

    IF THEN ELSE(Time<2015,0,replacement rate PHS*wear PHS*(1-RES elec tot
        overcapacity))*remaining potential elec storage by RES techn2[RES elec]
    """
    return if_then_else(
        time() < 2015, lambda: 0, lambda: replacement_rate_phs() * wear_phs()
    )


def replacement_rate_phs():
    """
    Real Name: replacement rate PHS
    Original Eqn: IF THEN ELSE(real FE elec stored PHS TWh<max potential PHS TWh,1,0.8)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Replacement rate of PHS infrastructure: by default all decommissioned
        capacity is replaced (=1). In the case of overcapacity in relation to the
        potential, we reduce the annual replacement rate to 0.8.
    """
    return if_then_else(
        real_fe_elec_stored_phs_twh() < max_potential_phs_twh(), lambda: 1, lambda: 0.8
    )


def required_capacity_phs():
    """
    Real Name: required capacity PHS
    Original Eqn: INTEG ( new required PHS capacity-new PHS capacity under planning, initial required capacity PHS)
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_required_capacity_phs()


def table_hist_capacity_phs(x):
    """
    Real Name: table hist capacity PHS
    Original Eqn: ( GET DIRECT LOOKUPS('../energy.xlsx', 'Austria', 'time_historic_data', 'historic_installed_capacity_phs'))
    Units: TW/Year
    Limits: (None, None)
    Type: lookup
    Subs: None


    """
    return _ext_lookup_table_hist_capacity_phs(x)


def wear_phs():
    """
    Real Name: wear PHS
    Original Eqn: IF THEN ELSE(Time<2015, 0, installed capacity PHS TW/lifetime RES elec[hydro])
    Units: TW
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        time() < 2015,
        lambda: 0,
        lambda: installed_capacity_phs_tw() / float(lifetime_res_elec().loc["hydro"]),
    )


_ext_constant_cp_phs = ExtConstant(
    "../energy.xlsx", "Austria", "cp_phs", {}, _root, "_ext_constant_cp_phs"
)


_ext_constant_initial_instal_cap_phs = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "initial_installed_capacity_phs",
    {},
    _root,
    "_ext_constant_initial_instal_cap_phs",
)


_integ_installed_capacity_phs_tw = Integ(
    lambda: phs_capacity_under_construction() - wear_phs(),
    lambda: initial_instal_cap_phs(),
    "_integ_installed_capacity_phs_tw",
)


_ext_constant_max_potential_phs_twe = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "C26",
    {},
    _root,
    "_ext_constant_max_potential_phs_twe",
)


_ext_constant_p_phs_growth = ExtConstant(
    "../../scenarios/scen_aut.xlsx",
    "BAU",
    "F37",
    {},
    _root,
    "_ext_constant_p_phs_growth",
)


_ext_constant_past_phs_capacity_growth = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "historic_growth_phs_capacity",
    {},
    _root,
    "_ext_constant_past_phs_capacity_growth",
)


_integ_phs_planned_capacity = Integ(
    lambda: new_phs_capacity_under_planning()
    + replacement_capacity_phs()
    - phs_capacity_under_construction(),
    lambda: initial_capacity_in_construction_phs(),
    "_integ_phs_planned_capacity",
)


_integ_required_capacity_phs = Integ(
    lambda: new_required_phs_capacity() - new_phs_capacity_under_planning(),
    lambda: initial_required_capacity_phs(),
    "_integ_required_capacity_phs",
)


_ext_lookup_table_hist_capacity_phs = ExtLookup(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_installed_capacity_phs",
    {},
    _root,
    "_ext_lookup_table_hist_capacity_phs",
)
