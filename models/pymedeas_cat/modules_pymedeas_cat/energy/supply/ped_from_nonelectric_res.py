"""
Module energy.supply.ped_from_nonelectric_res
Translated using PySD version 3.14.1
"""

@component.add(
    name='"Max potential PE non-electric RES"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_pe_potential_tot_res_heat_ej": 1,
        "max_peavail_biofuels_potential": 1,
    },
)
def max_potential_pe_nonelectric_res():
    """
    Techno-ecological sustainable potential (primary energy) of non-electric RES.
    """
    return max_pe_potential_tot_res_heat_ej() + max_peavail_biofuels_potential()


@component.add(
    name='"PE supply from RES non-elec without trad bioE EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_tot_res_for_heat": 1,
        "fes_total_biofuels_ej": 1,
        "pes_biogas_for_tfc": 1,
    },
)
def pe_supply_from_res_nonelec_without_trad_bioe_ej():
    """
    Primary energy (non electric) supply from RES without traditional biomass.
    """
    return pes_tot_res_for_heat() + fes_total_biofuels_ej() + pes_biogas_for_tfc()


@component.add(
    name='"PE supply RES non-Elec EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pe_supply_from_res_nonelec_without_trad_bioe_ej": 1,
        "pe_traditional_biomass_ej_delayed_1yr": 1,
        "losses_in_charcoal_plants_ej": 1,
        "modern_solids_bioe_demand_households": 1,
    },
)
def pe_supply_res_nonelec_ej():
    """
    Primary energy (non electricity) from RES, including traditional biomass.
    """
    return (
        pe_supply_from_res_nonelec_without_trad_bioe_ej()
        + pe_traditional_biomass_ej_delayed_1yr()
        + losses_in_charcoal_plants_ej()
        + modern_solids_bioe_demand_households()
    )
