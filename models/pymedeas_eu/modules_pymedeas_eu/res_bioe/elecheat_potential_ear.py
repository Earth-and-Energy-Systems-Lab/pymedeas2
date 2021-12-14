"""
Module elecheat_potential_ear
Translated using PySD version 2.1.0
"""


def available_max_pe_solid_bioe_for_elec_ej():
    """
    Real Name: available max PE solid bioE for elec EJ
    Original Eqn: MAX(0, "Total PE solid bioE potential heat+elec EJ"-PES RES for heat by techn[solid bioE heat])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

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
    Original Eqn: MAX(0, "Total PE solid bioE potential heat+elec EJ"-PE bioE for Elec generation EJ)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Maximum available (primary energy) solid bioenergy for heat.
    """
    return np.maximum(
        0,
        total_pe_solid_bioe_potential_heatelec_ej() - pe_bioe_for_elec_generation_ej(),
    )


def max_pe_potential_solid_bioe_for_elec_ej():
    """
    Real Name: max PE potential solid bioE for elec EJ
    Original Eqn: "Total PE solid bioE potential heat+elec EJ"*share solids bioE for elec vs heat
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Maximum potential (primary energy) of solid bioenergy for generating
        electricity.
    """
    return (
        total_pe_solid_bioe_potential_heatelec_ej()
        * share_solids_bioe_for_elec_vs_heat()
    )


def max_pe_potential_solid_bioe_for_heat_ej():
    """
    Real Name: max PE potential solid bioE for heat EJ
    Original Eqn: "Total PE solid bioE potential heat+elec EJ"*(1-share solids bioE for elec vs heat)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Maximum potential (primary energy) of solid bioenergy for generating heat.
    """
    return total_pe_solid_bioe_potential_heatelec_ej() * (
        1 - share_solids_bioe_for_elec_vs_heat()
    )


def share_solids_bioe_for_elec_vs_heat():
    """
    Real Name: share solids bioE for elec vs heat
    Original Eqn: ZIDZ( PE bioE for Elec generation EJ, (PE bioE for Elec generation EJ +PES RES for heat by techn[solid bioE heat]) )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of solids bioenergy for electricity vs electricity+heat.
    """
    return zidz(
        pe_bioe_for_elec_generation_ej(),
        (
            pe_bioe_for_elec_generation_ej()
            + float(pes_res_for_heat_by_techn().loc["solid bioE heat"])
        ),
    )


def total_pe_solid_bioe_potential_ej():
    """
    Real Name: Total PE solid bioE potential EJ
    Original Eqn: max E forest energy non trad
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    If switch land 1 =1 the land restrictions are used, otherwise a fixed
        potential is used
    """
    return max_e_forest_energy_non_trad()


def total_pe_solid_bioe_potential_heatelec_ej():
    """
    Real Name: "Total PE solid bioE potential heat+elec EJ"
    Original Eqn: MAX(Total PE solid bioE potential EJ-modern solids BioE demand households, 0)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return np.maximum(
        total_pe_solid_bioe_potential_ej() - modern_solids_bioe_demand_households(), 0
    )
