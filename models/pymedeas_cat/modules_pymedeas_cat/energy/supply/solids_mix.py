"""
Module solids_mix
Translated using PySD version 3.0.0
"""


@component.add(
    name="Coal in FEC AUT",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def coal_in_fec_aut():
    return pec_coal() - total_coal_consumption()


@component.add(
    name="PED totat solids",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ped_totat_solids():
    return (
        other_solids_required()
        + pe_demand_coal_elec_plants_ej()
        + ped_coal_for_chp_plants_ej()
        + ped_coal_for_ctl_ej()
        + ped_coal_for_heat_plants_ej()
        + ped_coal_heatnc()
        + required_fed_solids()
    )


@component.add(
    name="share coal total FED",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_coal_total_fed():
    return zidz(pec_coal(), total_solids_ej())


@component.add(
    name="share modern solids BioE demand households",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_modern_solids_bioe_demand_households():
    return zidz(modern_solids_bioe_demand_households(), total_solids_ej())


@component.add(
    name="share traditional biomass",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_traditional_biomass():
    return zidz(pe_traditional_biomass_ej_delayed_1yr(), total_solids_ej())


@component.add(
    name="Solids CO2 emissions",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def solids_co2_emissions():
    return required_fed_solids() * gco2_per_mj_coal() * mj_per_ej() / g_per_gt()


@component.add(
    name="Total coal consumption",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_coal_consumption():
    return (
        pe_demand_coal_elec_plants_ej()
        + ped_coal_for_chp_plants_ej()
        + ped_coal_for_ctl_ej()
        + ped_coal_for_heat_plants_ej()
        + ped_coal_heatnc()
        + other_solids_required()
    )


@component.add(
    name="Total solids EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_solids_ej():
    return (
        pes_waste_for_tfc()
        + pes_peat_ej()
        + pec_coal()
        + pe_traditional_biomass_ej_delayed_1yr()
        + modern_solids_bioe_demand_households()
        + losses_in_charcoal_plants_ej()
    )


@component.add(
    name="Total solids FEC",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_solids_fec():
    return (
        modern_solids_bioe_demand_households()
        + coal_in_fec_aut()
        + losses_in_charcoal_plants_ej()
        + pes_peat_ej()
        + pes_waste_for_tfc()
    )
