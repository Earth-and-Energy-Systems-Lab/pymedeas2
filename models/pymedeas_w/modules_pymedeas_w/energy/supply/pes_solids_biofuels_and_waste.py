"""
Module pes_solids_biofuels_and_waste
Translated using PySD version 3.2.0
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
    "World",
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
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "losses_in_charcoal_plants_ej": 1,
        "pe_real_generation_res_elec": 1,
        "pe_traditional_biomass_ej_delayed_1yr": 1,
        "pes_res_for_heatcom_by_techn": 1,
        "pes_res_for_heatnc_by_techn": 1,
    },
)
def pes_solids_bioe_ej():
    """
    Total biomass supply.It aggregates supply for electricity, heat and traditional biomass.
    """
    return (
        losses_in_charcoal_plants_ej()
        + float(pe_real_generation_res_elec().loc["solid bioE elec"])
        + pe_traditional_biomass_ej_delayed_1yr()
        + float(pes_res_for_heatcom_by_techn().loc["solid bioE heat"])
        + float(pes_res_for_heatnc_by_techn().loc["solid bioE heat"])
    )


@component.add(
    name="solid biofuels emissions relevant EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pe_real_generation_res_elec": 1,
        "pes_res_for_heatcom_by_techn": 1,
        "pes_res_for_heatnc_by_techn": 1,
    },
)
def solid_biofuels_emissions_relevant_ej():
    """
    Solids biofuels primary energy supply for estimating the CO2 emissions (we assume the XO2 emissions from traditional biomass are already included in land-use change emissions).
    """
    return (
        float(pe_real_generation_res_elec().loc["solid bioE elec"])
        + float(pes_res_for_heatcom_by_techn().loc["solid bioE heat"])
        + float(pes_res_for_heatnc_by_techn().loc["solid bioE heat"])
    )
