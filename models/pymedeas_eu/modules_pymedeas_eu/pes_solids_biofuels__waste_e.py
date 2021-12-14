"""
Module pes_solids_biofuels__waste_e
Translated using PySD version 2.1.0
"""


def losses_in_charcoal_plants_ej():
    """
    Real Name: Losses in charcoal plants EJ
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'Europe', 'time_efficiencies', 'historic_losses_charcoal_plants')
    Units: EJ
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Losses of energy (EJ) produced in charcoal plants.
    """
    return _ext_data_losses_in_charcoal_plants_ej(time())


def pes_solids_bioe__waste_ej():
    """
    Real Name: "PES solids bioE & waste EJ"
    Original Eqn: PES solids bioE EJ-PES waste EJ
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total primary energy supply solids biofuels and waste.
    """
    return pes_solids_bioe_ej() - pes_waste_ej()


def pes_solids_bioe_ej():
    """
    Real Name: PES solids bioE EJ
    Original Eqn: Losses in charcoal plants EJ+PE bioE for Elec generation EJ+PE traditional biomass EJ delayed 1yr +modern solids BioE demand households+PES RES for heat by techn[solid bioE heat]
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None

    Total biomass supply.It aggregates supply for electricity, heat and solids
        (both modern and traditional biomass).
    """
    return (
        losses_in_charcoal_plants_ej()
        + pe_bioe_for_elec_generation_ej()
        + pe_traditional_biomass_ej_delayed_1yr()
        + modern_solids_bioe_demand_households()
        + float(pes_res_for_heat_by_techn().loc["solid bioE heat"])
    )


def solid_bioe_emissions_relevant_ej():
    """
    Real Name: solid bioE emissions relevant EJ
    Original Eqn: PE bioE for Elec generation EJ+PES RES for heat by techn[solid bioE heat]+modern solids BioE demand households
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Solids bioenergy primary energy supply for estimating the CO2 emissions
        (we assume the CO2 emissions from traditional biomass are already included
        in land-use change emissions).
    """
    return (
        pe_bioe_for_elec_generation_ej()
        + float(pes_res_for_heat_by_techn().loc["solid bioE heat"])
        + modern_solids_bioe_demand_households()
    )


_ext_data_losses_in_charcoal_plants_ej = ExtData(
    "../energy.xlsx",
    "Europe",
    "time_efficiencies",
    "historic_losses_charcoal_plants",
    "interpolate",
    {},
    _root,
    "_ext_data_losses_in_charcoal_plants_ej",
)
