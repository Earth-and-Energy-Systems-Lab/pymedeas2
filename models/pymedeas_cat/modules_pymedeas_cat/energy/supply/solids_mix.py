"""
Module energy.supply.solids_mix
Translated using PySD version 3.14.0
"""

@component.add(
    name="Coal_in_FEC_CAT",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pec_coal": 1, "total_coal_consumption": 1},
)
def coal_in_fec_cat():
    return pec_coal() - total_coal_consumption()


@component.add(
    name="PED_totat_solids",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "other_solids_required": 1,
        "ped_coal_elec_plants_ej": 1,
        "ped_coal_for_chp_plants_ej": 1,
        "ped_coal_for_ctl": 1,
        "ped_coal_for_heat_plants_ej": 1,
        "ped_coal_heatnc": 1,
        "required_fed_by_solids": 1,
    },
)
def ped_totat_solids():
    return (
        other_solids_required()
        + ped_coal_elec_plants_ej()
        + ped_coal_for_chp_plants_ej()
        + ped_coal_for_ctl()
        + ped_coal_for_heat_plants_ej()
        + ped_coal_heatnc()
        + required_fed_by_solids()
    )


@component.add(
    name="share_coal_total_FED",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pec_coal": 1, "total_solids_ej": 1},
)
def share_coal_total_fed():
    return zidz(pec_coal(), total_solids_ej())


@component.add(
    name="share_modern_solids_BioE_demand_households",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"modern_solids_bioe_demand_households": 1, "total_solids_ej": 1},
)
def share_modern_solids_bioe_demand_households():
    return zidz(modern_solids_bioe_demand_households(), total_solids_ej())


@component.add(
    name="share_traditional_biomass",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pe_traditional_biomass_ej_delayed_1yr": 1, "total_solids_ej": 1},
)
def share_traditional_biomass():
    return zidz(pe_traditional_biomass_ej_delayed_1yr(), total_solids_ej())


@component.add(
    name="Total_coal_consumption",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_coal_elec_plants_ej": 1,
        "ped_coal_for_chp_plants_ej": 1,
        "ped_coal_for_ctl": 1,
        "ped_coal_for_heat_plants_ej": 1,
        "ped_coal_heatnc": 1,
        "other_solids_required": 1,
    },
)
def total_coal_consumption():
    return (
        ped_coal_elec_plants_ej()
        + ped_coal_for_chp_plants_ej()
        + ped_coal_for_ctl()
        + ped_coal_for_heat_plants_ej()
        + ped_coal_heatnc()
        + other_solids_required()
    )


@component.add(
    name="Total_solids_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_waste_for_tfc": 1,
        "pes_peat": 1,
        "pec_coal": 1,
        "pe_traditional_biomass_ej_delayed_1yr": 1,
        "modern_solids_bioe_demand_households": 1,
        "losses_in_charcoal_plants_ej": 1,
    },
)
def total_solids_ej():
    return (
        pes_waste_for_tfc()
        + pes_peat()
        + pec_coal()
        + pe_traditional_biomass_ej_delayed_1yr()
        + modern_solids_bioe_demand_households()
        + losses_in_charcoal_plants_ej()
    )


@component.add(
    name="Total_solids_FEC",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "modern_solids_bioe_demand_households": 1,
        "coal_in_fec_cat": 1,
        "losses_in_charcoal_plants_ej": 1,
        "pes_peat": 1,
        "pes_waste_for_tfc": 1,
    },
)
def total_solids_fec():
    return (
        modern_solids_bioe_demand_households()
        + coal_in_fec_cat()
        + losses_in_charcoal_plants_ej()
        + pes_peat()
        + pes_waste_for_tfc()
    )
