"""
Module phs
Translated using PySD version 3.0.0
"""


@component.add(
    name="adapt growth PHS",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def adapt_growth_phs():
    """
    Annual growth per RES elec technology. Modeling of a soft transition from current historic annual growth to reach the policy-objective in the target year.
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


@component.add(
    name="Cp PHS", units="Dmnl", comp_type="Constant", comp_subtype="External"
)
def cp_phs():
    """
    Capacity factor of pumped hydro storage (PHS).
    """
    return _ext_constant_cp_phs()


_ext_constant_cp_phs = ExtConstant(
    "../energy.xlsx", "Austria", "cp_phs", {}, _root, {}, "_ext_constant_cp_phs"
)


@component.add(
    name="Historic new required capacity PHS",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def historic_new_required_capacity_phs():
    """
    (Assuming 100% of planned was planned and constructed).
    """
    return table_hist_capacity_phs(
        time() + float(total_time_planconstr_res_elec().loc["hydro"]) + 1
    ) - table_hist_capacity_phs(
        time() + float(total_time_planconstr_res_elec().loc["hydro"])
    )


@component.add(
    name="initial capacity in construction PHS",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def initial_capacity_in_construction_phs():
    """
    Initial capacity of PHS in construction (year 1995). We assume that it is the same than the additional installed capacity between 1995 and 1996.
    """
    return initial_required_capacity_phs()


@component.add(
    name="initial instal cap PHS",
    units="TW",
    comp_type="Constant",
    comp_subtype="External",
)
def initial_instal_cap_phs():
    """
    Installed capacity of PHS in the initial year 1995.
    """
    return _ext_constant_initial_instal_cap_phs()


_ext_constant_initial_instal_cap_phs = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "initial_installed_capacity_phs",
    {},
    _root,
    {},
    "_ext_constant_initial_instal_cap_phs",
)


@component.add(
    name="initial required capacity PHS",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def initial_required_capacity_phs():
    """
    Initial required capacity of PHS (year 1995). We assume that it is the same than the additional installed capacity between 1995 and 1996.
    """
    return table_hist_capacity_phs(1996) - table_hist_capacity_phs(1995)


@component.add(
    name="installed capacity PHS TW",
    units="TW",
    comp_type="Stateful",
    comp_subtype="Integ",
)
def installed_capacity_phs_tw():
    return _integ_installed_capacity_phs_tw()


_integ_installed_capacity_phs_tw = Integ(
    lambda: phs_capacity_under_construction() - wear_phs(),
    lambda: initial_instal_cap_phs(),
    "_integ_installed_capacity_phs_tw",
)


@component.add(
    name="max capacity potential PHS",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def max_capacity_potential_phs():
    """
    Maximum capacity potential of PHS.
    """
    return max_potential_phs_twe() / cp_phs()


@component.add(
    name="max potential PHS TWe",
    units="TWe",
    comp_type="Constant",
    comp_subtype="External",
)
def max_potential_phs_twe():
    """
    Maximum potential for PHS.
    """
    return _ext_constant_max_potential_phs_twe()


_ext_constant_max_potential_phs_twe = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "max_PHS_potential",
    {},
    _root,
    {},
    "_ext_constant_max_potential_phs_twe",
)


@component.add(
    name="max potential PHS TWh",
    units="TWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def max_potential_phs_twh():
    return max_capacity_potential_phs() * cp_phs() / twe_per_twh()


@component.add(
    name="new PHS capacity under planning",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def new_phs_capacity_under_planning():
    return required_capacity_phs() / float(time_planification_res_elec().loc["hydro"])


@component.add(
    name="new required PHS capacity",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def new_required_phs_capacity():
    """
    IF THEN ELSE(Time<(2014-"total time plan+constr RES elec"[RES elec]), Historic new required capacity RES elec[RES elec],installed capacity RES elec TW[RES elec]*adapt growth RES elec after allocation[RES elec]*remaining potential constraint on new RES elec capacity[RES elec]*abundance RES elec2) 0.9*installed capacity PHS TW*(1-(installed capacity PHS TW/demand storage capacity))
    """
    return if_then_else(
        time() < 2014 - float(total_time_planconstr_res_elec().loc["hydro"]),
        lambda: historic_new_required_capacity_phs(),
        lambda: installed_capacity_phs_tw()
        * adapt_growth_phs()
        * remaining_potential_constraint_on_new_phs_capacity(),
    )


@component.add(
    name="output PHS over lifetime",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def output_phs_over_lifetime():
    """
    Total electricity output generated over the full operation of the infrastructure of the new capacity installed.
    """
    return (
        cp_phs()
        * phs_capacity_under_construction()
        * (1 / twe_per_twh())
        * float(lifetime_res_elec().loc["hydro"])
        * ej_per_twh()
    )


@component.add(
    name="P PHS growth", units="Dmnl", comp_type="Constant", comp_subtype="External"
)
def p_phs_growth():
    """
    Annual growth in relation to the existing installed capacity.
    """
    return _ext_constant_p_phs_growth()


_ext_constant_p_phs_growth = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "p_PHS_growth",
    {},
    _root,
    {},
    "_ext_constant_p_phs_growth",
)


@component.add(
    name="past PHS capacity growth",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="External",
)
def past_phs_capacity_growth():
    """
    Current growth levels.
    """
    return _ext_constant_past_phs_capacity_growth()


_ext_constant_past_phs_capacity_growth = ExtConstant(
    "../energy.xlsx",
    "Austria",
    "historic_growth_phs_capacity",
    {},
    _root,
    {},
    "_ext_constant_past_phs_capacity_growth",
)


@component.add(
    name="PHS capacity under construction",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def phs_capacity_under_construction():
    return phs_planned_capacity() / float(time_construction_res_elec().loc["hydro"])


@component.add(
    name="PHS planned capacity", units="TW", comp_type="Stateful", comp_subtype="Integ"
)
def phs_planned_capacity():
    return _integ_phs_planned_capacity()


_integ_phs_planned_capacity = Integ(
    lambda: new_phs_capacity_under_planning()
    + replacement_capacity_phs()
    - phs_capacity_under_construction(),
    lambda: initial_capacity_in_construction_phs(),
    "_integ_phs_planned_capacity",
)


@component.add(
    name="real FE elec stored PHS TWh",
    units="TWh",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def real_fe_elec_stored_phs_twh():
    """
    Electricity stored in pumped hydro storage plants. It does not add up to the electricity generation of other sources since this electricity has already been accounted for! (stored).
    """
    return installed_capacity_phs_tw() * cp_phs() / twe_per_twh()


@component.add(
    name="remaining potential constraint on new PHS capacity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def remaining_potential_constraint_on_new_phs_capacity():
    return if_then_else(
        remaining_potential_phs() > threshold_remaining_potential_new_capacity(),
        lambda: 1,
        lambda: remaining_potential_phs()
        * (1 / threshold_remaining_potential_new_capacity()),
    )


@component.add(
    name="remaining potential PHS",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def remaining_potential_phs():
    return if_then_else(
        max_capacity_potential_phs() > installed_capacity_phs_tw(),
        lambda: (max_capacity_potential_phs() - installed_capacity_phs_tw())
        / max_capacity_potential_phs(),
        lambda: 0,
    )


@component.add(
    name="replacement capacity PHS",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def replacement_capacity_phs():
    """
    IF THEN ELSE(Time<2015,0,replacement rate PHS*wear PHS*(1-RES elec tot overcapacity))*remaining potential elec storage by RES techn2[RES elec]
    """
    return if_then_else(
        time() < 2015, lambda: 0, lambda: replacement_rate_phs() * wear_phs()
    )


@component.add(
    name="replacement rate PHS",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def replacement_rate_phs():
    """
    Replacement rate of PHS infrastructure: by default all decommissioned capacity is replaced (=1). In the case of overcapacity in relation to the potential, we reduce the annual replacement rate to 0.8.
    """
    return if_then_else(
        real_fe_elec_stored_phs_twh() < max_potential_phs_twh(), lambda: 1, lambda: 0.8
    )


@component.add(
    name="required capacity PHS", units="TW", comp_type="Stateful", comp_subtype="Integ"
)
def required_capacity_phs():
    return _integ_required_capacity_phs()


_integ_required_capacity_phs = Integ(
    lambda: new_required_phs_capacity() - new_phs_capacity_under_planning(),
    lambda: initial_required_capacity_phs(),
    "_integ_required_capacity_phs",
)


@component.add(
    name="table hist capacity PHS",
    units="TW/Year",
    comp_type="Lookup",
    comp_subtype="External",
)
def table_hist_capacity_phs(x, final_subs=None):
    return _ext_lookup_table_hist_capacity_phs(x, final_subs)


_ext_lookup_table_hist_capacity_phs = ExtLookup(
    "../energy.xlsx",
    "Austria",
    "time_historic_data",
    "historic_installed_capacity_phs",
    {},
    _root,
    {},
    "_ext_lookup_table_hist_capacity_phs",
)


@component.add(
    name="wear PHS", units="TW", comp_type="Auxiliary", comp_subtype="Normal"
)
def wear_phs():
    return if_then_else(
        time() < 2015,
        lambda: 0,
        lambda: installed_capacity_phs_tw() / float(lifetime_res_elec().loc["hydro"]),
    )
