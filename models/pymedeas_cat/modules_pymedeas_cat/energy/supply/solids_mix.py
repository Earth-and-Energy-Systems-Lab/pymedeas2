"""
Module solids_mix
Translated using PySD version 2.2.1
"""


def coal_in_fec_aut():
    """
    Real Name: Coal in FEC AUT
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return pec_coal() - total_coal_consumption()


def ped_totat_solids():
    """
    Real Name: PED totat solids
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        other_solids_required()
        + pe_demand_coal_elec_plants_ej()
        + ped_coal_for_chp_plants_ej()
        + ped_coal_for_ctl_ej()
        + ped_coal_for_heat_plants_ej()
        + ped_coal_heatnc()
        + required_fed_solids()
    )


def share_coal_total_fed():
    """
    Real Name: share coal total FED
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(pec_coal(), total_solids_ej())


def share_modern_solids_bioe_demand_households():
    """
    Real Name: share modern solids BioE demand households
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(modern_solids_bioe_demand_households(), total_solids_ej())


def share_traditional_biomass():
    """
    Real Name: share traditional biomass
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(pe_traditional_biomass_ej_delayed_1yr(), total_solids_ej())


def solids_co2_emissions():
    """
    Real Name: Solids CO2 emissions
    Original Eqn:
    Units: GtCO2/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return required_fed_solids() * gco2_per_mj_coal() * mj_per_ej() / g_per_gt()


def total_coal_consumption():
    """
    Real Name: Total coal consumption
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        pe_demand_coal_elec_plants_ej()
        + ped_coal_for_chp_plants_ej()
        + ped_coal_for_ctl_ej()
        + ped_coal_for_heat_plants_ej()
        + ped_coal_heatnc()
        + other_solids_required()
    )


def total_solids_ej():
    """
    Real Name: Total solids EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        pes_waste_for_tfc()
        + pes_peat_ej()
        + pec_coal()
        + pe_traditional_biomass_ej_delayed_1yr()
        + modern_solids_bioe_demand_households()
        + losses_in_charcoal_plants_ej()
    )


def total_solids_fec():
    """
    Real Name: Total solids FEC
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        modern_solids_bioe_demand_households()
        + coal_in_fec_aut()
        + losses_in_charcoal_plants_ej()
        + pes_peat_ej()
        + pes_waste_for_tfc()
    )
