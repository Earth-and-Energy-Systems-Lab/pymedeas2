"""
Module biomass_for_electricity_and_heat
Translated using PySD version 2.2.1
"""


def available_max_pe_solid_bioe_for_elec_ej():
    """
    Real Name: available max PE solid bioE for elec EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Maximum available (primary energy) solid bioenergy for electricity.
    """
    return np.maximum(
        0,
        total_pe_solid_bioe_potential_heatelec_ej()
        - float(pes_res_for_heat_by_techn().loc["solid bioE heat"]),
    )


def available_max_pe_solid_bioe_for_heat_ej():
    """
    Real Name: available max PE solid bioE for heat EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Maximum available (primary energy) solid bioenergy for heat.
    """
    return np.maximum(
        0,
        total_pe_solid_bioe_potential_heatelec_ej()
        - float(pe_real_generation_res_elec().loc["solid bioE elec"]),
    )


def max_pe_potential_solid_bioe_for_elec_ej():
    """
    Real Name: max PE potential solid bioE for elec EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Maximum potential (primary energy) of solid bioenergy for generating electricity.
    """
    return (
        total_pe_solid_bioe_potential_heatelec_ej()
        * share_solids_bioe_for_elec_vs_heat()
    )


def max_pe_potential_solid_bioe_for_heat_ej():
    """
    Real Name: max PE potential solid bioE for heat EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Maximum potential (primary energy) of solid bioenergy for generating heat.
    """
    return total_pe_solid_bioe_potential_heatelec_ej() * (
        1 - share_solids_bioe_for_elec_vs_heat()
    )


def share_solids_bioe_for_elec_vs_heat():
    """
    Real Name: share solids bioE for elec vs heat
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of solids bioenergy for electricity vs electricity+heat.
    """
    return zidz(
        float(pe_real_generation_res_elec().loc["solid bioE elec"]),
        float(pe_real_generation_res_elec().loc["solid bioE elec"])
        + float(pes_res_for_heat_by_techn().loc["solid bioE heat"]),
    )


def total_pe_solid_bioe_potential_ej():
    """
    Real Name: Total PE solid bioE potential EJ
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    If switch land 1 =1 the land restrictions are used, otherwise a fixed potential is used
    """
    return max_e_forest_energy_non_trad()


def total_pe_solid_bioe_potential_heatelec_ej():
    """
    Real Name: "Total PE solid bioE potential heat+elec EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return np.maximum(
        total_pe_solid_bioe_potential_ej() - modern_solids_bioe_demand_households(), 0
    )
