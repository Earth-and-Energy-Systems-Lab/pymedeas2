"""
Module res_pes
Translated using PySD version 2.2.0
"""


def share_res_for_elec_vs_tpe_res():
    """
    Real Name: share RES for Elec vs TPE RES
    Original Eqn: PE Elec generation from RES EJ/("PE supply RES non-Elec EJ"+PE Elec generation from RES EJ)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of RES for electricity in relation to TPE RES.
    """
    return pe_elec_generation_from_res_ej() / (
        pe_supply_res_nonelec_ej() + pe_elec_generation_from_res_ej()
    )


def tpe_from_res_ej():
    """
    Real Name: TPE from RES EJ
    Original Eqn: PE Elec generation from RES EJ+"PE supply RES non-Elec EJ"
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Total primary energy supply from all RES.
    """
    return pe_elec_generation_from_res_ej() + pe_supply_res_nonelec_ej()


def tpe_from_res_mtoe():
    """
    Real Name: TPE from RES Mtoe
    Original Eqn: TPE from RES EJ*MToe per EJ
    Units: MToe/year
    Limits: (None, None)
    Type: component
    Subs: None

    Total primary energy supply from all RES.
    """
    return tpe_from_res_ej() * mtoe_per_ej()
