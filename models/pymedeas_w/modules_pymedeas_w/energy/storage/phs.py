"""
Module phs
Translated using PySD version 2.2.3
"""


def adapt_growth_phs():
    """
    Real Name: adapt growth PHS
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Annual growth per RES elec technology. Modeling of a soft transition from current historic annual growth to reach the policy-objective 5 years later.
    """
    return if_then_else(
        time() < 2015,
        lambda: past_phs_capacity_growth(),
        lambda: if_then_else(
            time() < 2020,
            lambda: past_phs_capacity_growth()
            + (p_phs_growth() - past_phs_capacity_growth()) * (time() - 2015) / 5,
            lambda: p_phs_growth(),
        )
        * (1 + abundance_storage()),
    )


def cp_phs():
    """
    Real Name: Cp PHS
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Capacity factor of pumped hydro storage (PHS).
    """
    return _ext_constant_cp_phs()


_ext_constant_cp_phs = ExtConstant(
    "../energy.xlsx", "World", "cp_phs", {}, _root, "_ext_constant_cp_phs"
)


def historic_new_required_capacity_phs():
    """
    Real Name: Historic new required capacity PHS
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Initial capacity of PHS in construction (year 1995). We assume that it is the same than the additional installed capacity between 1995 and 1996.
    """
    return initial_required_capacity_phs()


def initial_instal_cap_phs():
    """
    Real Name: initial instal cap PHS
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Constant
    Subs: []

    Installed capacity of PHS in the initial year 1995.
    """
    return _ext_constant_initial_instal_cap_phs()


_ext_constant_initial_instal_cap_phs = ExtConstant(
    "../energy.xlsx",
    "World",
    "initial_installed_capacity_phs",
    {},
    _root,
    "_ext_constant_initial_instal_cap_phs",
)


def initial_required_capacity_phs():
    """
    Real Name: initial required capacity PHS
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Initial required capacity of PHS (year 1995). We assume that it is the same than the additional installed capacity between 1995 and 1996.
    """
    return table_hist_capacity_phs(1996) - table_hist_capacity_phs(1995)


def installed_capacity_phs_tw():
    """
    Real Name: installed capacity PHS TW
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _integ_installed_capacity_phs_tw()


_integ_installed_capacity_phs_tw = Integ(
    lambda: phs_capacity_under_construction() - wear_phs(),
    lambda: initial_instal_cap_phs(),
    "_integ_installed_capacity_phs_tw",
)


def max_capacity_potential_phs():
    """
    Real Name: max capacity potential PHS
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Maximum capacity potential of PHS.
    """
    return max_potential_phs_twe() / cp_phs()


def max_potential_phs_twe():
    """
    Real Name: max potential PHS TWe
    Original Eqn:
    Units: TWe
    Limits: (None, None)
    Type: Constant
    Subs: []

    Maximum potential for PHS.
    """
    return _ext_constant_max_potential_phs_twe()


_ext_constant_max_potential_phs_twe = ExtConstant(
    "../energy.xlsx",
    "World",
    "max_PHS_potential",
    {},
    _root,
    "_ext_constant_max_potential_phs_twe",
)


def max_potential_phs_twh():
    """
    Real Name: max potential PHS TWh
    Original Eqn:
    Units: TWh
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return max_capacity_potential_phs() * cp_phs() / twe_per_twh()


def new_phs_capacity_under_planning():
    """
    Real Name: new PHS capacity under planning
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return required_capacity_phs() / float(time_planification_res_elec().loc["hydro"])


def new_required_phs_capacity():
    """
    Real Name: new required PHS capacity
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    IF THEN ELSE(Time<(2014-"total time plan+constr RES elec"[RES elec]), Historic new required capacity RES elec[RES elec],installed capacity RES elec TW[RES elec]*adapt growth RES elec after allocation[RES elec]*remaining potential constraint on new RES elec capacity[RES elec]*abundance RES elec2) 0.9*installed capacity PHS TW*(1-(installed capacity PHS TW/demand storage capacity))
    """
    return if_then_else(
        time() < 2014 - float(total_time_planconstr_res_elec().loc["hydro"]),
        lambda: historic_new_required_capacity_phs(),
        lambda: installed_capacity_phs_tw()
        * adapt_growth_phs()
        * remaining_potential_constraint_on_new_phs_capacity(),
    )


def output_phs_over_lifetime():
    """
    Real Name: output PHS over lifetime
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total electricity output generated over the full operation of the infrastructure of the new capacity installed.
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
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Annual growth in relation to the existing installed capacity.
    """
    return _ext_constant_p_phs_growth()


_ext_constant_p_phs_growth = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "p_phs_growth",
    {},
    _root,
    "_ext_constant_p_phs_growth",
)


def past_phs_capacity_growth():
    """
    Real Name: past PHS capacity growth
    Original Eqn:
    Units: 1/year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Current growth levels.
    """
    return _ext_constant_past_phs_capacity_growth()


_ext_constant_past_phs_capacity_growth = ExtConstant(
    "../energy.xlsx",
    "World",
    "historic_growth_phs_capacity",
    {},
    _root,
    "_ext_constant_past_phs_capacity_growth",
)


def phs_capacity_under_construction():
    """
    Real Name: PHS capacity under construction
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return phs_planned_capacity() / float(time_construction_res_elec().loc["hydro"])


def phs_overcapacity():
    """
    Real Name: PHS overcapacity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Overcapacity of PHS.
    """
    return np.maximum(
        0,
        zidz(
            potential_fe_elec_stored_phs_twh() - real_fe_elec_stored_phs_twh(),
            potential_fe_elec_stored_phs_twh(),
        ),
    )


def phs_planned_capacity():
    """
    Real Name: PHS planned capacity
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _integ_phs_planned_capacity()


_integ_phs_planned_capacity = Integ(
    lambda: new_phs_capacity_under_planning()
    + replacement_capacity_phs()
    - phs_capacity_under_construction(),
    lambda: initial_capacity_in_construction_phs(),
    "_integ_phs_planned_capacity",
)


def potential_fe_elec_stored_phs_twh():
    """
    Real Name: potential FE elec stored PHS TWh
    Original Eqn:
    Units: TWh
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Potential electricity stored in pumped hydro storage plants. It does not add up to the electricity generation of other sources since this electricity has already been accounted for! (stored).
    """
    return installed_capacity_phs_tw() * cp_phs() / twe_per_twh()


def real_fe_elec_stored_phs_twh():
    """
    Real Name: real FE elec stored PHS TWh
    Original Eqn:
    Units: TWh
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Electricity stored in pumped hydro storage plants. It does not add up to the electricity generation of other sources since this electricity has already been accounted for! (stored).
    """
    return np.minimum(max_potential_phs_twh(), potential_fe_elec_stored_phs_twh())


def remaining_potential_constraint_on_new_phs_capacity():
    """
    Real Name: remaining potential constraint on new PHS capacity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


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
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


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
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    IF THEN ELSE(Time<2015,0,replacement rate PHS*wear PHS*(1-RES elec tot overcapacity))*remaining potential elec storage by RES techn2[RES elec]
    """
    return if_then_else(
        time() < 2015,
        lambda: 0,
        lambda: replacement_rate_phs() * wear_phs() * (1 - phs_overcapacity()),
    )


def replacement_rate_phs():
    """
    Real Name: replacement rate PHS
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Replacement rate of PHS infrastructure: by default all decommissioned capacity is replaced (=1). In the case of overcapacity in relation to the potential, we reduce the annual replacement rate to 0.8.
    """
    return if_then_else(
        potential_fe_elec_stored_phs_twh() < max_potential_phs_twh(),
        lambda: 1,
        lambda: 0.8,
    )


def required_capacity_phs():
    """
    Real Name: required capacity PHS
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _integ_required_capacity_phs()


_integ_required_capacity_phs = Integ(
    lambda: new_required_phs_capacity() - new_phs_capacity_under_planning(),
    lambda: initial_required_capacity_phs(),
    "_integ_required_capacity_phs",
)


def table_hist_capacity_phs(x):
    """
    Real Name: table hist capacity PHS
    Original Eqn:
    Units: TW/year
    Limits: (None, None)
    Type: Lookup
    Subs: []


    """
    return _ext_lookup_table_hist_capacity_phs(x)


_ext_lookup_table_hist_capacity_phs = ExtLookup(
    "../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_installed_capacity_phs",
    {},
    _root,
    "_ext_lookup_table_hist_capacity_phs",
)


def wear_phs():
    """
    Real Name: wear PHS
    Original Eqn:
    Units: TW
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return if_then_else(
        time() < 2015,
        lambda: 0,
        lambda: installed_capacity_phs_tw() / float(lifetime_res_elec().loc["hydro"]),
    )
