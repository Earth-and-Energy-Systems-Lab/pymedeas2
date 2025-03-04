"""
Module energy.demand.solids_ped_pes_fes
Translated using PySD version 3.14.2
"""

@component.add(
    name="abundance_solids",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_solids": 2, "ped_solids": 3},
)
def abundance_solids():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        pes_solids() > ped_solids(),
        lambda: 1,
        lambda: 1 - zidz(ped_solids() - pes_solids(), ped_solids()),
    )


@component.add(
    name="historic_coal_extraction",
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_coal_extraction",
        "__lookup__": "_ext_lookup_historic_coal_extraction",
    },
)
def historic_coal_extraction(x, final_subs=None):
    return _ext_lookup_historic_coal_extraction(x, final_subs)


_ext_lookup_historic_coal_extraction = ExtLookup(
    r"../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_domestic_coal_extraction",
    {},
    _root,
    {},
    "_ext_lookup_historic_coal_extraction",
)


@component.add(
    name="historic_PEC_coal",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "historic_coal_extraction": 1,
        "imports_cat_coal_from_row_ej": 1,
        "extraction_coal_cat": 1,
    },
)
def historic_pec_coal():
    return if_then_else(
        time() < 2019,
        lambda: historic_coal_extraction(time()) + imports_cat_coal_from_row_ej(),
        lambda: extraction_coal_cat(),
    )


@component.add(
    name="Historic_PES_peat_EJ",
    units="EJ/year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_pes_peat_ej",
        "__data__": "_ext_data_historic_pes_peat_ej",
        "time": 1,
    },
)
def historic_pes_peat_ej():
    """
    Historic primary energy supply of peat.
    """
    return _ext_data_historic_pes_peat_ej(time())


_ext_data_historic_pes_peat_ej = ExtData(
    r"../energy.xlsx",
    "Catalonia",
    "time_efficiencies",
    "historic_primary_energy_supply_peat",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_pes_peat_ej",
)


@component.add(
    name="imports_CAT_coal_from_RoW_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"net_coal_flux_cat": 1},
)
def imports_cat_coal_from_row_ej():
    return net_coal_flux_cat()


@component.add(
    name="Other_solids_required",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "transformation_ff_losses_ej": 1,
        "energy_distr_losses_ff": 1,
        "nonenergy_use_demand_by_final_fuel": 1,
    },
)
def other_solids_required():
    return (
        float(transformation_ff_losses_ej().loc["solids"])
        + float(energy_distr_losses_ff().loc["solids"])
        + float(nonenergy_use_demand_by_final_fuel().loc["solids"])
    )


@component.add(
    name="PEC_coal",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"imports_cat_coal_from_row_ej": 1, "extraction_coal_cat": 1},
)
def pec_coal():
    return imports_cat_coal_from_row_ej() + extraction_coal_cat()


@component.add(
    name="PED_coal_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_ff_for_heat_plants": 1,
        "ped_coal_heatnc": 1,
        "ped_coal_elec_plants_ej": 1,
        "ped_coal_for_chp_plants_ej": 1,
        "pes_peat": 1,
        "ped_solids": 1,
        "pes_waste": 1,
        "losses_in_charcoal_plants_ej": 1,
        "pe_traditional_biomass_ej_delayed_1yr": 1,
        "fes_biomass": 1,
    },
)
def ped_coal_ej():
    return float(
        np.maximum(
            float(ped_ff_for_heat_plants().loc["solids"])
            + ped_coal_heatnc()
            + ped_coal_elec_plants_ej()
            + ped_coal_for_chp_plants_ej(),
            ped_solids()
            - (
                pe_traditional_biomass_ej_delayed_1yr()
                + pes_peat()
                + losses_in_charcoal_plants_ej()
                + pes_waste()
                + fes_biomass()
            ),
        )
    )


@component.add(
    name="PED_domestic_CAT_coal_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_ej": 1, "imports_cat_coal_from_row_ej": 1},
)
def ped_domestic_cat_coal_ej():
    """
    PED coal EJ*Historic share coal domestic CAT extraction until 2016
    """
    return float(np.maximum(0, ped_coal_ej() - imports_cat_coal_from_row_ej()))


@component.add(
    name="PED_solids",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_solids": 1,
        "ped_coal_for_ctl": 1,
        "ped_coal_elec_plants_ej": 1,
        "ped_ff_for_heat_plants": 1,
        "ped_coal_for_chp_plants_ej": 1,
        "ped_coal_heatnc": 1,
        "other_solids_required": 1,
        "pes_waste_for_chp_plants": 1,
        "pes_waste_for_elec_plants": 1,
        "pes_waste_for_heatcom_plants": 1,
    },
)
def ped_solids():
    """
    Primary energy demand of solids.
    """
    return float(
        np.maximum(
            0,
            required_fed_by_solids()
            + ped_coal_for_ctl()
            + ped_coal_elec_plants_ej()
            + float(ped_ff_for_heat_plants().loc["solids"])
            + ped_coal_for_chp_plants_ej()
            + ped_coal_heatnc()
            + other_solids_required()
            + pes_waste_for_chp_plants()
            + pes_waste_for_elec_plants()
            + pes_waste_for_heatcom_plants(),
        )
    )


@component.add(
    name="PES_peat",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_pes_peat_ej": 1},
)
def pes_peat():
    return historic_pes_peat_ej()


@component.add(
    name="PES_solids",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pec_coal": 1,
        "pe_traditional_biomass_ej_delayed_1yr": 1,
        "pes_peat": 1,
        "pes_waste": 1,
        "losses_in_charcoal_plants_ej": 1,
        "fes_biomass": 1,
    },
)
def pes_solids():
    """
    Primary energy supply solids.
    """
    return (
        pec_coal()
        + pe_traditional_biomass_ej_delayed_1yr()
        + pes_peat()
        + pes_waste()
        + losses_in_charcoal_plants_ej()
        + fes_biomass()
    )


@component.add(
    name="real_FE_consumption_solids_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_solids": 1,
        "ped_coal_for_ctl": 1,
        "other_solids_required": 1,
        "share_solids_for_final_energy": 1,
        "required_fed_by_solids": 1,
    },
)
def real_fe_consumption_solids_ej():
    """
    Real final energy consumption by solids after accounting for energy availability.
    """
    return float(
        np.minimum(
            (pes_solids() - ped_coal_for_ctl() - other_solids_required())
            * share_solids_for_final_energy(),
            required_fed_by_solids(),
        )
    )


@component.add(
    name="Required_FED_by_solids",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fuel": 1},
)
def required_fed_by_solids():
    """
    Required final energy demand solids.
    """
    return float(required_fed_by_fuel().loc["solids"])


@component.add(
    name="share_biomass_in_PES",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fes_biomass": 1,
        "pe_traditional_biomass_ej_delayed_1yr": 1,
        "pes_solids": 1,
    },
)
def share_biomass_in_pes():
    return zidz(fes_biomass() + pe_traditional_biomass_ej_delayed_1yr(), pes_solids())


@component.add(
    name='"share_coal_dem_for_Heat-com"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_ej": 2, "ped_ff_for_heat_plants": 1},
)
def share_coal_dem_for_heatcom():
    """
    Share of coal demand to cover commercial heat consumption in Heat plants.
    """
    return if_then_else(
        ped_coal_ej() > 0,
        lambda: float(ped_ff_for_heat_plants().loc["solids"]) / ped_coal_ej(),
        lambda: 0,
    )


@component.add(
    name='"share_coal_dem_for_Heat-nc"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_heatnc": 1, "ped_coal_ej": 1},
)
def share_coal_dem_for_heatnc():
    """
    Share of coal demand to cover non-commercial heat consumption in Heat plants.
    """
    return zidz(ped_coal_heatnc(), ped_coal_ej())


@component.add(
    name="share_coal_elec_plants",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_elec_plants_ej": 1, "ped_coal_ej": 1},
)
def share_coal_elec_plants():
    return zidz(ped_coal_elec_plants_ej(), ped_coal_ej())


@component.add(
    name="share_coal_for_CTL_emissions_relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_for_ctl": 1, "ped_coal_ej": 1},
)
def share_coal_for_ctl_emissions_relevant():
    return zidz(ped_coal_for_ctl(), ped_coal_ej())


@component.add(
    name="share_coal_for_Elec_emissions_relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_coal_elec_plants_ej": 1,
        "ped_coal_for_chp_plants_ej": 1,
        "share_elec_gen_in_chp": 1,
        "ped_coal_ej": 1,
    },
)
def share_coal_for_elec_emissions_relevant():
    return zidz(
        ped_coal_elec_plants_ej()
        + ped_coal_for_chp_plants_ej() * float(share_elec_gen_in_chp().loc["coal"]),
        ped_coal_ej(),
    )


@component.add(
    name="share_coal_for_FC_emissions_relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nonenergy_use_demand_by_final_fuel": 1,
        "ped_solids": 1,
        "share_coal_for_ctl_emissions_relevant": 1,
        "share_coal_for_elec_emissions_relevant": 1,
        "share_coal_for_heat_emissions_relevant": 1,
    },
)
def share_coal_for_fc_emissions_relevant():
    return (
        1
        - zidz(float(nonenergy_use_demand_by_final_fuel().loc["solids"]), ped_solids())
        - share_coal_for_ctl_emissions_relevant()
        - share_coal_for_elec_emissions_relevant()
        - share_coal_for_heat_emissions_relevant()
    )


@component.add(
    name="share_coal_for_Heat_emissions_relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_ff_for_heat_plants": 1,
        "ped_coal_heatnc": 1,
        "ped_coal_for_chp_plants_ej": 1,
        "share_elec_gen_in_chp": 1,
        "ped_coal_ej": 1,
    },
)
def share_coal_for_heat_emissions_relevant():
    return zidz(
        float(ped_ff_for_heat_plants().loc["solids"])
        + ped_coal_heatnc()
        + ped_coal_for_chp_plants_ej()
        * (1 - float(share_elec_gen_in_chp().loc["coal"])),
        ped_coal_ej(),
    )


@component.add(
    name="share_solids_for_final_energy",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_solids": 1,
        "other_solids_required": 1,
        "ped_coal_for_ctl": 1,
        "ped_solids": 1,
    },
)
def share_solids_for_final_energy():
    """
    Share of final energy vs primary energy for solids.
    """
    return zidz(
        required_fed_by_solids(),
        ped_solids() - ped_coal_for_ctl() - other_solids_required(),
    )
