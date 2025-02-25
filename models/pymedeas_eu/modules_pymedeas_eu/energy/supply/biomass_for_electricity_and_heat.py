"""
Module energy.supply.biomass_for_electricity_and_heat
Translated using PySD version 3.14.2
"""

@component.add(
    name="available_max_PE_solid_bioE_for_elec",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_pe_solid_bioe_potential_heatelec": 1,
        "pes_res_for_heat_by_techn": 1,
    },
)
def available_max_pe_solid_bioe_for_elec():
    """
    Maximum available (primary energy) solid bioenergy for electricity.
    """
    return float(
        np.maximum(
            0,
            total_pe_solid_bioe_potential_heatelec()
            - float(pes_res_for_heat_by_techn().loc["solid_bioE_heat"]),
        )
    )


@component.add(
    name="available_max_PE_solid_bioE_for_heat",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_pe_solid_bioe_potential_heatelec": 1,
        "pe_real_generation_res_elec": 1,
    },
)
def available_max_pe_solid_bioe_for_heat():
    """
    Maximum available (primary energy) solid bioenergy for heat.
    """
    return float(
        np.maximum(
            0,
            total_pe_solid_bioe_potential_heatelec()
            - float(pe_real_generation_res_elec().loc["solid_bioE_elec"]),
        )
    )


@component.add(
    name="max_PE_potential_solid_bioE_for_elec",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_pe_solid_bioe_potential_heatelec": 1,
        "share_solids_bioe_for_elec_vs_heat": 1,
    },
)
def max_pe_potential_solid_bioe_for_elec():
    """
    Maximum potential (primary energy) of solid bioenergy for generating electricity.
    """
    return (
        total_pe_solid_bioe_potential_heatelec() * share_solids_bioe_for_elec_vs_heat()
    )


@component.add(
    name="max_PE_potential_solid_bioE_for_heat",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_pe_solid_bioe_potential_heatelec": 1,
        "share_solids_bioe_for_elec_vs_heat": 1,
    },
)
def max_pe_potential_solid_bioe_for_heat():
    """
    Maximum potential (primary energy) of solid bioenergy for generating heat.
    """
    return total_pe_solid_bioe_potential_heatelec() * (
        1 - share_solids_bioe_for_elec_vs_heat()
    )


@component.add(
    name='"Max_potential_NPP_bioE_conventional_for_heat+elec"',
    units="EJ/year",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_constant_max_potential_npp_bioe_conventional_for_heatelec"
    },
)
def max_potential_npp_bioe_conventional_for_heatelec():
    return _ext_constant_max_potential_npp_bioe_conventional_for_heatelec()


_ext_constant_max_potential_npp_bioe_conventional_for_heatelec = ExtConstant(
    r"../energy.xlsx",
    "Europe",
    "max_pot_NPP_bioe_conv",
    {},
    _root,
    {},
    "_ext_constant_max_potential_npp_bioe_conventional_for_heatelec",
)


@component.add(
    name="share_solids_bioE_for_elec_vs_heat",
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
        float(pe_real_generation_res_elec().loc["solid_bioE_elec"]),
        float(pe_real_generation_res_elec().loc["solid_bioE_elec"])
        + float(pes_res_for_heat_by_techn().loc["solid_bioE_heat"]),
    )


@component.add(
    name="Total_PE_solid_bioE_potential",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_potential_npp_bioe_conventional_for_heatelec": 1,
        "pe_bioe_residues_nonbiofuels": 1,
    },
)
def total_pe_solid_bioe_potential():
    """
    If switch land 1 =1 the land restrictions are used, otherwise a fixed potential is used
    """
    return (
        max_potential_npp_bioe_conventional_for_heatelec()
        + pe_bioe_residues_nonbiofuels()
    )


@component.add(
    name='"Total_PE_solid_bioE_potential_heat+elec"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_pe_solid_bioe_potential": 1,
        "modern_solids_bioe_demand_households": 1,
    },
)
def total_pe_solid_bioe_potential_heatelec():
    return float(
        np.maximum(
            total_pe_solid_bioe_potential() - modern_solids_bioe_demand_households(), 0
        )
    )
