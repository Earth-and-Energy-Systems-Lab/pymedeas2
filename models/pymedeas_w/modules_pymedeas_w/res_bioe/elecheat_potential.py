"""
Module elecheat_potential
Translated using PySD version 2.1.0
"""


def available_pe_potential_solid_bioe_for_elec_ej():
    """
    Real Name: available PE potential solid bioE for elec EJ
    Original Eqn: MAX(0, "Total PE solid bioE potential heat+elec EJ"-"PES RES for heat-com by techn"[solid bioE heat]-"PES RES for heat-nc by techn"[solid bioE heat] )
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Available (primary energy) potential solid bioenergy for electricity.
    """
    return np.maximum(
        0,
        total_pe_solid_bioe_potential_heatelec_ej()
        - float(pes_res_for_heatcom_by_techn().loc["solid bioE heat"])
        - float(pes_res_for_heatnc_by_techn().loc["solid bioE heat"]),
    )


def available_pe_potential_solid_bioe_for_heat_ej():
    """
    Real Name: available PE potential solid bioE for heat EJ
    Original Eqn: MAX(0, "Total PE solid bioE potential heat+elec EJ"-PE bioE for Elec generation EJ)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Available (primary energy) potential solid bioenergy for heat.
    """
    return np.maximum(
        0,
        total_pe_solid_bioe_potential_heatelec_ej() - pe_bioe_for_elec_generation_ej(),
    )


def available_potential_fe_solid_bioe_for_elec_ej():
    """
    Real Name: available potential FE solid bioE for elec EJ
    Original Eqn: available PE potential solid bioE for elec EJ*efficiency conversion bioE to Elec
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Available (final energy) potential solid bioenergy for electricity.
    """
    return (
        available_pe_potential_solid_bioe_for_elec_ej()
        * efficiency_conversion_bioe_to_elec()
    )


def max_potential_npp_bioe_conventional_for_heatelec():
    """
    Real Name: "Max potential NPP bioE conventional for heat+elec"
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'G42')
    Units: EJ/year
    Limits: (None, None)
    Type: constant
    Subs: None

    Sustainable potential NPP of conventional bioenergy for heat and
        electricity. Source: Technical Report.
    """
    return _ext_constant_max_potential_npp_bioe_conventional_for_heatelec()


def total_pe_solid_bioe_potential_heatelec_ej():
    """
    Real Name: "Total PE solid bioE potential heat+elec EJ"
    Original Eqn: "Max potential NPP bioE conventional for heat+elec"+"PE bioE residues for heat+elec EJ"
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    If switch land 1 =1 the land restrictions are used, otherwise a fixed
        potential is used
    """
    return (
        max_potential_npp_bioe_conventional_for_heatelec()
        + pe_bioe_residues_for_heatelec_ej()
    )


_ext_constant_max_potential_npp_bioe_conventional_for_heatelec = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "G42",
    {},
    _root,
    "_ext_constant_max_potential_npp_bioe_conventional_for_heatelec",
)
