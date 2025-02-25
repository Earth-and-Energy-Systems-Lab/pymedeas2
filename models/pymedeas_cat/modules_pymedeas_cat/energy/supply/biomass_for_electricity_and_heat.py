"""
Module energy.supply.biomass_for_electricity_and_heat
Translated using PySD version 3.14.0
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
    return np.maximum(
        0,
        total_pe_solid_bioe_potential_heatelec()
        - float(pes_res_for_heat_by_techn().loc["solid_bioE_heat"]),
    )


@component.add(
    name="available_max_PE_solid_bioE_for_heat_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_pe_solid_bioe_potential_heatelec": 1,
        "pe_real_generation_res_elec": 1,
    },
)
def available_max_pe_solid_bioe_for_heat_ej():
    """
    Maximum available (primary energy) solid bioenergy for heat.
    """
    return np.maximum(
        0,
        total_pe_solid_bioe_potential_heatelec()
        - float(pe_real_generation_res_elec().loc["solid_bioE_elec"]),
    )


@component.add(
    name="FES_biomass",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "end_hist_data": 5,
        "historic_biomass_fec": 3,
        "policy_solid_bioe": 2,
    },
)
def fes_biomass():
    """
    Final energy supply of biomass, biomass used for electricity generation is obtained from scenarios RES energy capacity development.
    """
    return if_then_else(
        time() < end_hist_data(),
        lambda: historic_biomass_fec(time()),
        lambda: if_then_else(
            time() < 2020,
            lambda: historic_biomass_fec(end_hist_data())
            + (policy_solid_bioe(2020) - historic_biomass_fec(end_hist_data()))
            / (2020 - end_hist_data())
            * (time() - end_hist_data()),
            lambda: policy_solid_bioe(time()),
        ),
    )


@component.add(
    name="FES_biomass_sectors",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fes_biomass": 1, "modern_solids_bioe_demand_households": 1},
)
def fes_biomass_sectors():
    return fes_biomass() - modern_solids_bioe_demand_households()


@component.add(
    name="historic_biomass_FEC",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_biomass_fec",
        "__lookup__": "_ext_lookup_historic_biomass_fec",
    },
)
def historic_biomass_fec(x, final_subs=None):
    return _ext_lookup_historic_biomass_fec(x, final_subs)


_ext_lookup_historic_biomass_fec = ExtLookup(
    "../energy.xlsx",
    "Catalonia",
    "time_efficiencies",
    "historic_final_energy_consumption_biomass",
    {},
    _root,
    {},
    "_ext_lookup_historic_biomass_fec",
)


@component.add(
    name="max_PE_potential_solid_bioE_for_elec_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_pe_solid_bioe_potential_heatelec": 1,
        "share_solids_bioe_for_elec_vs_heat": 1,
    },
)
def max_pe_potential_solid_bioe_for_elec_ej():
    """
    Maximum potential (primary energy) of solid bioenergy for generating electricity.
    """
    return (
        total_pe_solid_bioe_potential_heatelec() * share_solids_bioe_for_elec_vs_heat()
    )


@component.add(
    name="max_PE_potential_solid_bioE_for_heat_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_pe_solid_bioe_potential_heatelec": 1,
        "share_solids_bioe_for_elec_vs_heat": 1,
    },
)
def max_pe_potential_solid_bioe_for_heat_ej():
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
    "../energy.xlsx",
    "Catalonia",
    "max_pot_NPP_bioe_conv",
    {},
    _root,
    {},
    "_ext_constant_max_potential_npp_bioe_conventional_for_heatelec",
)


@component.add(
    name="policy_solid_bioE",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_policy_solid_bioe",
        "__lookup__": "_ext_lookup_policy_solid_bioe",
    },
)
def policy_solid_bioe(x, final_subs=None):
    return _ext_lookup_policy_solid_bioe(x, final_subs)


_ext_lookup_policy_solid_bioe = ExtLookup(
    "../../scenarios/scen_cat.xlsx",
    "NZP",
    "year_RES_power",
    "p_solid_bioE",
    {},
    _root,
    {},
    "_ext_lookup_policy_solid_bioe",
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
    name="Total_PE_solid_bioE_potential_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_potential_npp_bioe_conventional_for_heatelec": 1,
        "pe_bioe_residues_nonbiofuels_ej": 1,
    },
)
def total_pe_solid_bioe_potential_ej():
    """
    If switch land 1 =1 the land restrictions are used, otherwise a fixed potential is used
    """
    return (
        max_potential_npp_bioe_conventional_for_heatelec()
        + pe_bioe_residues_nonbiofuels_ej()
    )


@component.add(
    name='"Total_PE_solid_bioE_potential_heat+elec"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_pe_solid_bioe_potential_ej": 1,
        "modern_solids_bioe_demand_households": 1,
    },
)
def total_pe_solid_bioe_potential_heatelec():
    return np.maximum(
        total_pe_solid_bioe_potential_ej() - modern_solids_bioe_demand_households(), 0
    )
