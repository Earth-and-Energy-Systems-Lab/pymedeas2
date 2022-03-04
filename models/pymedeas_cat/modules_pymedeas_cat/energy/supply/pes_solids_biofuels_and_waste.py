"""
Module pes_solids_biofuels_and_waste
Translated using PySD version 2.2.1
"""


def losses_in_charcoal_plants_ej():
    """
    Real Name: Losses in charcoal plants EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Data
    Subs: []

    Losses of energy (EJ) produced in charcoal plants.
    """
    return _ext_data_losses_in_charcoal_plants_ej(time())


_ext_data_losses_in_charcoal_plants_ej = ExtData(
    "../energy.xlsx",
    "Austria",
    "time_efficiencies",
    "historic_losses_charcoal_plants",
    "interpolate",
    {},
    _root,
    "_ext_data_losses_in_charcoal_plants_ej",
)


def pes_solids_bioe__waste_ej():
    """
    Real Name: "PES solids bioE & waste EJ"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total primary energy supply solids biofuels and waste.
    """
    return pes_solids_bioe_ej() - pes_waste_ej()


def pes_solids_bioe_ej():
    """
    Real Name: PES solids bioE EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total biomass supply.It aggregates supply for electricity, heat and solids (both modern and traditional biomass).
    """
    return (
        losses_in_charcoal_plants_ej()
        + float(pe_real_generation_res_elec().loc["solid bioE elec"])
        + pe_traditional_biomass_ej_delayed_1yr()
        + modern_solids_bioe_demand_households()
        + float(pes_res_for_heat_by_techn().loc["solid bioE heat"])
    )


def solid_bioe_emissions_relevant_ej():
    """
    Real Name: solid bioE emissions relevant EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Solids bioenergy primary energy supply for estimating the CO2 emissions (we assume the CO2 emissions from traditional biomass are already included in land-use change emissions).
    """
    return (
        float(pe_real_generation_res_elec().loc["solid bioE elec"])
        + float(pes_res_for_heat_by_techn().loc["solid bioE heat"])
        + modern_solids_bioe_demand_households()
    )
