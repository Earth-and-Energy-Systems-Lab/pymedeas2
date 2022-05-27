"""
Module biomass_for_electricity_and_heat
Translated using PySD version 3.0.1
"""


@component.add(
    name="available max PE solid bioE for elec EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_pe_solid_bioe_potential_heatelec_ej": 1,
        "pes_res_for_heat_by_techn": 1,
    },
)
def available_max_pe_solid_bioe_for_elec_ej():
    """
    Maximum available (primary energy) solid bioenergy for electricity.
    """
    return np.maximum(
        0,
        total_pe_solid_bioe_potential_heatelec_ej()
        - float(pes_res_for_heat_by_techn().loc["solid bioE heat"]),
    )


@component.add(
    name="available max PE solid bioE for heat EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_pe_solid_bioe_potential_heatelec_ej": 1,
        "pe_real_generation_res_elec": 1,
    },
)
def available_max_pe_solid_bioe_for_heat_ej():
    """
    Maximum available (primary energy) solid bioenergy for heat.
    """
    return np.maximum(
        0,
        total_pe_solid_bioe_potential_heatelec_ej()
        - float(pe_real_generation_res_elec().loc["solid bioE elec"]),
    )


@component.add(
    name="max PE potential solid bioE for elec EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_pe_solid_bioe_potential_heatelec_ej": 1,
        "share_solids_bioe_for_elec_vs_heat": 1,
    },
)
def max_pe_potential_solid_bioe_for_elec_ej():
    """
    Maximum potential (primary energy) of solid bioenergy for generating electricity.
    """
    return (
        total_pe_solid_bioe_potential_heatelec_ej()
        * share_solids_bioe_for_elec_vs_heat()
    )


@component.add(
    name="max PE potential solid bioE for heat EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_pe_solid_bioe_potential_heatelec_ej": 1,
        "share_solids_bioe_for_elec_vs_heat": 1,
    },
)
def max_pe_potential_solid_bioe_for_heat_ej():
    """
    Maximum potential (primary energy) of solid bioenergy for generating heat.
    """
    return total_pe_solid_bioe_potential_heatelec_ej() * (
        1 - share_solids_bioe_for_elec_vs_heat()
    )


@component.add(
    name="share solids bioE for elec vs heat",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pe_real_generation_res_elec": 2, "pes_res_for_heat_by_techn": 1},
)
def share_solids_bioe_for_elec_vs_heat():
    """
    Share of solids bioenergy for electricity vs electricity+heat.
    """
    return zidz(
        float(pe_real_generation_res_elec().loc["solid bioE elec"]),
        float(pe_real_generation_res_elec().loc["solid bioE elec"])
        + float(pes_res_for_heat_by_techn().loc["solid bioE heat"]),
    )


@component.add(
    name="Total PE solid bioE potential EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_e_forest_energy_non_trad": 1},
)
def total_pe_solid_bioe_potential_ej():
    """
    If switch land 1 =1 the land restrictions are used, otherwise a fixed potential is used
    """
    return max_e_forest_energy_non_trad()


@component.add(
    name='"Total PE solid bioE potential heat+elec EJ"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_pe_solid_bioe_potential_ej": 1,
        "modern_solids_bioe_demand_households": 1,
    },
)
def total_pe_solid_bioe_potential_heatelec_ej():
    return np.maximum(
        total_pe_solid_bioe_potential_ej() - modern_solids_bioe_demand_households(), 0
    )
