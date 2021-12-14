"""
Module ped_from_nonelectric_res
Translated using PySD version 2.1.0
"""


def max_potential_pe_nonelectric_res():
    """
    Real Name: "Max potential PE non-electric RES"
    Original Eqn: max PE potential tot RES heat EJ+Max PEavail biofuels potential
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Techno-ecological sustainable potential (primary energy) of non-electric
        RES.
    """
    return max_pe_potential_tot_res_heat_ej() + max_peavail_biofuels_potential()


def pe_supply_from_res_nonelec_without_trad_bioe_ej():
    """
    Real Name: "PE supply from RES non-elec without trad bioE EJ"
    Original Eqn: PES tot RES for heat+FES total biofuels production EJ+PES biogas for TFC
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy (non electric) supply from RES without traditional biomass.
    """
    return (
        pes_tot_res_for_heat()
        + fes_total_biofuels_production_ej()
        + pes_biogas_for_tfc()
    )


def pe_supply_res_nonelec_ej():
    """
    Real Name: "PE supply RES non-Elec EJ"
    Original Eqn: "PE supply from RES non-elec without trad bioE EJ"+PE traditional biomass EJ delayed 1yr+Losses in charcoal plants EJ
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Primary energy (non electricity) from RES, including traditional biomass.
    """
    return (
        pe_supply_from_res_nonelec_without_trad_bioe_ej()
        + pe_traditional_biomass_ej_delayed_1yr()
        + losses_in_charcoal_plants_ej()
    )
