"""
Module solids_mix
Translated using PySD version 2.2.0
"""


def coal_in_fec_aut():
    """
    Real Name: Coal in FEC AUT
    Original Eqn: PEC coal-Total coal consumption
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pec_coal() - total_coal_consumption()


def ped_totat_solids():
    """
    Real Name: PED totat solids
    Original Eqn: Other solids required+PE demand coal Elec plants EJ+PED coal for CHP plants EJ+PED coal for CTL EJ +PED coal for Heat plants EJ+"PED coal Heat-nc"+Required FED solids
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


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
    Original Eqn: ZIDZ(PEC coal, Total solids EJ )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(pec_coal(), total_solids_ej())


def share_modern_solids_bioe_demand_households():
    """
    Real Name: share modern solids BioE demand households
    Original Eqn: ZIDZ(modern solids BioE demand households, Total solids EJ )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(modern_solids_bioe_demand_households(), total_solids_ej())


def share_traditional_biomass():
    """
    Real Name: share traditional biomass
    Original Eqn: ZIDZ(PE traditional biomass EJ delayed 1yr, Total solids EJ )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(pe_traditional_biomass_ej_delayed_1yr(), total_solids_ej())


def solids_co2_emissions():
    """
    Real Name: Solids CO2 emissions
    Original Eqn: Required FED solids*gCO2 per MJ coal*MJ per EJ/g per Gt
    Units: GtCO2/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return required_fed_solids() * gco2_per_mj_coal() * mj_per_ej() / g_per_gt()


def total_coal_consumption():
    """
    Real Name: Total coal consumption
    Original Eqn: PE demand coal Elec plants EJ+PED coal for CHP plants EJ+PED coal for CTL EJ+PED coal for Heat plants EJ +"PED coal Heat-nc"+Other solids required
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


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
    Original Eqn: PES waste for TFC+PES peat EJ+PEC coal+PE traditional biomass EJ delayed 1yr+modern solids BioE demand households+Losses in charcoal plants EJ
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


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
    Original Eqn: modern solids BioE demand households+Coal in FEC AUT+Losses in charcoal plants EJ+PES peat EJ+PES waste for TFC
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        modern_solids_bioe_demand_households()
        + coal_in_fec_aut()
        + losses_in_charcoal_plants_ej()
        + pes_peat_ej()
        + pes_waste_for_tfc()
    )
