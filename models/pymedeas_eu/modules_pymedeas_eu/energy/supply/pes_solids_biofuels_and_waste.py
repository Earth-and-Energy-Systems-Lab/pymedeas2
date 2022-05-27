"""
Module pes_solids_biofuels_and_waste
Translated using PySD version 3.0.1
"""


@component.add(
    name="Losses in charcoal plants EJ",
    units="EJ",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_losses_in_charcoal_plants_ej",
        "__data__": "_ext_data_losses_in_charcoal_plants_ej",
        "time": 1,
    },
)
def losses_in_charcoal_plants_ej():
    """
    Losses of energy (EJ) produced in charcoal plants.
    """
    return _ext_data_losses_in_charcoal_plants_ej(time())


_ext_data_losses_in_charcoal_plants_ej = ExtData(
    "../energy.xlsx",
    "Europe",
    "time_efficiencies",
    "historic_losses_charcoal_plants",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_losses_in_charcoal_plants_ej",
)


@component.add(
    name='"PES solids bioE & waste EJ"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_solids_bioe_ej": 1, "pes_waste_ej": 1},
)
def pes_solids_bioe_waste_ej():
    """
    Total primary energy supply solids biofuels and waste.
    """
    return pes_solids_bioe_ej() - pes_waste_ej()


@component.add(
    name="PES solids bioE EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "losses_in_charcoal_plants_ej": 1,
        "pe_real_generation_res_elec": 1,
        "pe_traditional_biomass_ej_delayed_1yr": 1,
        "modern_solids_bioe_demand_households": 1,
        "pes_res_for_heat_by_techn": 1,
    },
)
def pes_solids_bioe_ej():
    """
    Total biomass supply.It aggregates supply for electricity, heat and solids (both modern and traditional biomass).
    """
    return (
        losses_in_charcoal_plants_ej()
        + float(pe_real_generation_res_elec().loc["solid bioE elec"])
        + pe_traditional_biomass_ej_delayed_1yr()
        + modern_solids_bioe_demand_households()
        + float(pes_res_for_heat_by_techn().loc["solid bioE heat"])
    )


@component.add(
    name="solid bioE emissions relevant EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pe_real_generation_res_elec": 1,
        "pes_res_for_heat_by_techn": 1,
        "modern_solids_bioe_demand_households": 1,
    },
)
def solid_bioe_emissions_relevant_ej():
    """
    Solids bioenergy primary energy supply for estimating the CO2 emissions (we assume the CO2 emissions from traditional biomass are already included in land-use change emissions).
    """
    return (
        float(pe_real_generation_res_elec().loc["solid bioE elec"])
        + float(pes_res_for_heat_by_techn().loc["solid bioE heat"])
        + modern_solids_bioe_demand_households()
    )
