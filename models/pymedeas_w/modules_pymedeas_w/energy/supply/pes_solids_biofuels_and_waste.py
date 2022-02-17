"""
Module pes_solids_biofuels_and_waste
Translated using PySD version 2.2.1
"""


def losses_in_charcoal_plants_ej():
    """
    Real Name: Losses in charcoal plants EJ
    Original Eqn: GET DIRECT DATA('../energy.xlsx', 'World', 'time_efficiencies', 'historic_losses_charcoal_plants')
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
    Original Eqn: Losses in charcoal plants EJ+PE real generation RES elec[solid bioE elec]+PE traditional biomass EJ delayed 1yr +"PES RES for heat-com by techn"[solid bioE heat]+"PES RES for heat-nc by techn"[solid bioE heat]
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Total biomass supply.It aggregates supply for electricity, heat and
        traditional biomass.
    """
    return (
        losses_in_charcoal_plants_ej()
        + float(pe_real_generation_res_elec().loc["solid bioE elec"])
        + pe_traditional_biomass_ej_delayed_1yr()
        + float(pes_res_for_heatcom_by_techn().loc["solid bioE heat"])
        + float(pes_res_for_heatnc_by_techn().loc["solid bioE heat"])
    )


def solid_biofuels_emissions_relevant_ej():
    """
    Real Name: solid biofuels emissions relevant EJ
    Original Eqn: PE real generation RES elec[solid bioE elec]+"PES RES for heat-com by techn"[solid bioE heat]+"PES RES for heat-nc by techn"[solid bioE heat]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Solids biofuels primary energy supply for estimating the CO2 emissions (we
        assume the XO2 emissions from traditional biomass are already included in
        land-use change emissions).
    """
    return (
        float(pe_real_generation_res_elec().loc["solid bioE elec"])
        + float(pes_res_for_heatcom_by_techn().loc["solid bioE heat"])
        + float(pes_res_for_heatnc_by_techn().loc["solid bioE heat"])
    )


_ext_data_losses_in_charcoal_plants_ej = ExtData(
    "../energy.xlsx",
    "World",
    "time_efficiencies",
    "historic_losses_charcoal_plants",
    "interpolate",
    {},
    _root,
    "_ext_data_losses_in_charcoal_plants_ej",
)
