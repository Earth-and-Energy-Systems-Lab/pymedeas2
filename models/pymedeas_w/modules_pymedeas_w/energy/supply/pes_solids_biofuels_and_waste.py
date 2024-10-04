"""
Module energy.supply.pes_solids_biofuels_and_waste
Translated using PySD version 3.14.0
"""

@component.add(
    name="Losses in charcoal plants historic",
    units="EJ/year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_losses_in_charcoal_plants_historic",
        "__data__": "_ext_data_losses_in_charcoal_plants_historic",
        "time": 1,
    },
)
def losses_in_charcoal_plants_historic():
    """
    Losses of energy (EJ) produced in charcoal plants.
    """
    return _ext_data_losses_in_charcoal_plants_historic(time())


_ext_data_losses_in_charcoal_plants_historic = ExtData(
    "../energy.xlsx",
    "World",
    "time_efficiencies",
    "historic_losses_charcoal_plants",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_losses_in_charcoal_plants_historic",
)


@component.add(
    name="PES solids bioE EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "losses_in_charcoal_plants_historic": 1,
        "pe_real_generation_res_elec": 1,
        "pe_traditional_biomass_ej_delayed": 1,
        "pes_res_for_heatcom_by_techn": 1,
        "pes_res_for_heatnc_by_techn": 1,
    },
)
def pes_solids_bioe_ej():
    """
    Total biomass supply.It aggregates supply for electricity, heat and traditional biomass.
    """
    return (
        losses_in_charcoal_plants_historic()
        + float(pe_real_generation_res_elec().loc["solid bioE elec"])
        + pe_traditional_biomass_ej_delayed()
        + float(pes_res_for_heatcom_by_techn().loc["solid bioE heat"])
        + float(pes_res_for_heatnc_by_techn().loc["solid bioE heat"])
    )


@component.add(
    name='"PES solids bioE & waste EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_solids_bioe_ej": 1, "pes_waste": 1},
)
def pes_solids_bioe_waste_ej():
    """
    Total primary energy supply solids biofuels and waste.
    """
    return pes_solids_bioe_ej() - pes_waste()
