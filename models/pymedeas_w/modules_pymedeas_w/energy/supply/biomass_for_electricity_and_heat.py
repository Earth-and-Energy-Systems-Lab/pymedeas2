"""
Module energy.supply.biomass_for_electricity_and_heat
Translated using PySD version 3.14.0
"""

@component.add(
    name="available PE potential solid bioE for elec",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_pe_solid_bioe_potential_heatelec": 1,
        "pes_res_for_heatcom_by_techn": 1,
        "pes_res_for_heatnc_by_techn": 1,
    },
)
def available_pe_potential_solid_bioe_for_elec():
    """
    Available (primary energy) potential solid bioenergy for electricity.
    """
    return np.maximum(
        0,
        total_pe_solid_bioe_potential_heatelec()
        - float(pes_res_for_heatcom_by_techn().loc["solid bioE heat"])
        - float(pes_res_for_heatnc_by_techn().loc["solid bioE heat"]),
    )


@component.add(
    name="available PE potential solid bioE for heat",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_pe_solid_bioe_potential_heatelec": 1,
        "pe_real_generation_res_elec": 1,
    },
)
def available_pe_potential_solid_bioe_for_heat():
    """
    Available (primary energy) potential solid bioenergy for heat.
    """
    return np.maximum(
        0,
        total_pe_solid_bioe_potential_heatelec()
        - float(pe_real_generation_res_elec().loc["solid bioE elec"]),
    )


@component.add(
    name="available potential FE solid bioE for elec",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "available_pe_potential_solid_bioe_for_elec": 1,
        "efficiency_conversion_bioe_to_elec": 1,
    },
)
def available_potential_fe_solid_bioe_for_elec():
    """
    Available (final energy) potential solid bioenergy for electricity.
    """
    return (
        available_pe_potential_solid_bioe_for_elec()
        * efficiency_conversion_bioe_to_elec()
    )


@component.add(
    name='"Max potential NPP bioE conventional for heat+elec"',
    units="EJ/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_max_potential_npp_bioe_conventional_for_heatelec"
    },
)
def max_potential_npp_bioe_conventional_for_heatelec():
    """
    Sustainable potential NPP of conventional bioenergy for heat and electricity. Source: Technical Report.
    """
    return _ext_constant_max_potential_npp_bioe_conventional_for_heatelec()


_ext_constant_max_potential_npp_bioe_conventional_for_heatelec = ExtConstant(
    "../energy.xlsx",
    "World",
    "max_pot_NPP_bioe_conv",
    {},
    _root,
    {},
    "_ext_constant_max_potential_npp_bioe_conventional_for_heatelec",
)


@component.add(
    name='"Total PE solid bioE potential heat+elec"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_potential_npp_bioe_conventional_for_heatelec": 1,
        "pe_bioe_residues_for_heatelec_ej": 1,
    },
)
def total_pe_solid_bioe_potential_heatelec():
    """
    If switch land 1 =1 the land restrictions are used, otherwise a fixed potential is used
    """
    return (
        max_potential_npp_bioe_conventional_for_heatelec()
        + pe_bioe_residues_for_heatelec_ej()
    )
