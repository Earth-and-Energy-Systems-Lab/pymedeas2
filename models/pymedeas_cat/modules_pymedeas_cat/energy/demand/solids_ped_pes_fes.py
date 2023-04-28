"""
Module energy.demand.solids_ped_pes_fes
Translated using PySD version 3.9.1
"""


@component.add(
    name="abundance solids",
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
    name="DEBUG historic PEC coal",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "debug_historic_coal_extraction": 1,
        "imports_cat_coal_from_row_ej": 1,
        "extraction_coal_cat": 1,
    },
)
def debug_historic_pec_coal():
    return if_then_else(
        time() < 2019,
        lambda: debug_historic_coal_extraction(time()) + imports_cat_coal_from_row_ej(),
        lambda: extraction_coal_cat(),
    )


@component.add(
    name="Historic coal domestic CAT extracted EJ",
    units="EJ",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_coal_domestic_cat_extracted_ej",
        "__data__": "_ext_data_historic_coal_domestic_cat_extracted_ej",
        "time": 1,
    },
)
def historic_coal_domestic_cat_extracted_ej():
    return _ext_data_historic_coal_domestic_cat_extracted_ej(time())


_ext_data_historic_coal_domestic_cat_extracted_ej = ExtData(
    "../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_domestic_coal_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_coal_domestic_cat_extracted_ej",
)


@component.add(
    name="Historic net imports coal CAT",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_ej": 1, "historic_coal_domestic_cat_extracted_ej": 1},
)
def historic_net_imports_coal_cat():
    return ped_coal_ej() - historic_coal_domestic_cat_extracted_ej()


@component.add(
    name="Historic PES peat EJ",
    units="EJ",
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
    "../energy.xlsx",
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
    name="imports CAT coal from RoW EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"net_coal_flux_cat": 1},
)
def imports_cat_coal_from_row_ej():
    return net_coal_flux_cat()


@component.add(
    name="Other solids required",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "transformation_ff_losses_ej": 1,
        "energy_distr_losses_ff_ej": 1,
        "nonenergy_use_demand_by_final_fuel_ej": 1,
    },
)
def other_solids_required():
    return (
        float(transformation_ff_losses_ej().loc["solids"])
        + float(energy_distr_losses_ff_ej().loc["solids"])
        + float(nonenergy_use_demand_by_final_fuel_ej().loc["solids"])
    )


@component.add(
    name="PEC coal",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"imports_cat_coal_from_row_ej": 1, "extraction_coal_cat": 1},
)
def pec_coal():
    return imports_cat_coal_from_row_ej() + extraction_coal_cat()


@component.add(
    name="PED coal EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_coal_for_heat_plants_ej": 1,
        "ped_coal_heatnc": 1,
        "ped_coal_elec_plants_ej": 1,
        "ped_coal_for_chp_plants_ej": 1,
        "pes_waste": 1,
        "ped_solids": 1,
        "fes_biomass": 1,
        "losses_in_charcoal_plants_ej": 1,
        "pe_traditional_biomass_ej_delayed_1yr": 1,
        "pes_peat_ej": 1,
    },
)
def ped_coal_ej():
    return np.maximum(
        ped_coal_for_heat_plants_ej()
        + ped_coal_heatnc()
        + ped_coal_elec_plants_ej()
        + ped_coal_for_chp_plants_ej(),
        ped_solids()
        - (
            pe_traditional_biomass_ej_delayed_1yr()
            + pes_peat_ej()
            + losses_in_charcoal_plants_ej()
            + pes_waste()
            + fes_biomass()
        ),
    )


@component.add(
    name="PED domestic CAT coal EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_ej": 1, "imports_cat_coal_from_row_ej": 1},
)
def ped_domestic_cat_coal_ej():
    """
    PED coal EJ*Historic share coal domestic CAT extraction until 2016
    """
    return np.maximum(0, ped_coal_ej() - imports_cat_coal_from_row_ej())


@component.add(
    name="PED solids",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_solids": 1,
        "ped_coal_for_ctl_ej": 1,
        "ped_coal_elec_plants_ej": 1,
        "ped_coal_for_heat_plants_ej": 1,
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
    return np.maximum(
        0,
        required_fed_by_solids()
        + ped_coal_for_ctl_ej()
        + ped_coal_elec_plants_ej()
        + ped_coal_for_heat_plants_ej()
        + ped_coal_for_chp_plants_ej()
        + ped_coal_heatnc()
        + other_solids_required()
        + pes_waste_for_chp_plants()
        + pes_waste_for_elec_plants()
        + pes_waste_for_heatcom_plants(),
    )


@component.add(
    name="PES peat EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_pes_peat_ej": 1},
)
def pes_peat_ej():
    return historic_pes_peat_ej()


@component.add(
    name="PES solids",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pec_coal": 1,
        "pe_traditional_biomass_ej_delayed_1yr": 1,
        "pes_peat_ej": 1,
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
        + pes_peat_ej()
        + pes_waste()
        + losses_in_charcoal_plants_ej()
        + fes_biomass()
    )


@component.add(
    name="real FE consumption solids EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_coal_cat": 1,
        "imports_cat_coal_from_row_ej": 1,
        "pes_waste": 1,
        "fes_biomass": 1,
        "losses_in_charcoal_plants_ej": 1,
        "pe_traditional_biomass_ej_delayed_1yr": 1,
        "pes_peat_ej": 1,
        "ped_coal_for_ctl_ej": 1,
        "other_solids_required": 1,
        "share_solids_for_final_energy": 1,
    },
)
def real_fe_consumption_solids_ej():
    """
    Real final energy consumption by solids after accounting for energy availability.
    """
    return (
        extraction_coal_cat()
        + imports_cat_coal_from_row_ej()
        + (
            fes_biomass()
            + pe_traditional_biomass_ej_delayed_1yr()
            + pes_peat_ej()
            + losses_in_charcoal_plants_ej()
            + pes_waste()
        )
        - ped_coal_for_ctl_ej()
        - other_solids_required()
    ) * share_solids_for_final_energy()


@component.add(
    name="Required FED by solids",
    units="EJ/Year",
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
    name="share coal dem for Elec",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_ej": 2, "ped_coal_elec_plants_ej": 1},
)
def share_coal_dem_for_elec():
    """
    Share of coal demand to cover electricity consumption in Elec plants.
    """
    return if_then_else(
        ped_coal_ej() > 0, lambda: ped_coal_elec_plants_ej() / ped_coal_ej(), lambda: 0
    )


@component.add(
    name='"share coal dem for Heat-com"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_ej": 2, "ped_coal_for_heat_plants_ej": 1},
)
def share_coal_dem_for_heatcom():
    """
    Share of coal demand to cover commercial heat consumption in Heat plants.
    """
    return if_then_else(
        ped_coal_ej() > 0,
        lambda: ped_coal_for_heat_plants_ej() / ped_coal_ej(),
        lambda: 0,
    )


@component.add(
    name='"share coal dem for Heat-nc"',
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
    name="share coal elec plants",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_elec_plants_ej": 1, "ped_coal_ej": 1},
)
def share_coal_elec_plants():
    return zidz(ped_coal_elec_plants_ej(), ped_coal_ej())


@component.add(
    name="share coal for CTL emissions relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_for_ctl_ej": 1, "ped_coal_ej": 1},
)
def share_coal_for_ctl_emissions_relevant():
    return zidz(ped_coal_for_ctl_ej(), ped_coal_ej())


@component.add(
    name="share coal for Elec emissions relevant",
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
    name="share coal for FC emissions relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nonenergy_use_demand_by_final_fuel_ej": 1,
        "ped_solids": 1,
        "share_coal_for_ctl_emissions_relevant": 1,
        "share_coal_for_elec_emissions_relevant": 1,
        "share_coal_for_heat_emissions_relevant": 1,
    },
)
def share_coal_for_fc_emissions_relevant():
    return (
        1
        - zidz(
            float(nonenergy_use_demand_by_final_fuel_ej().loc["solids"]), ped_solids()
        )
        - share_coal_for_ctl_emissions_relevant()
        - share_coal_for_elec_emissions_relevant()
        - share_coal_for_heat_emissions_relevant()
    )


@component.add(
    name="share coal for Heat emissions relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_coal_for_heat_plants_ej": 1,
        "ped_coal_heatnc": 1,
        "ped_coal_for_chp_plants_ej": 1,
        "share_elec_gen_in_chp": 1,
        "ped_coal_ej": 1,
    },
)
def share_coal_for_heat_emissions_relevant():
    return zidz(
        ped_coal_for_heat_plants_ej()
        + ped_coal_heatnc()
        + ped_coal_for_chp_plants_ej()
        * (1 - float(share_elec_gen_in_chp().loc["coal"])),
        ped_coal_ej(),
    )


@component.add(
    name="share solids for final energy",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_solids": 1,
        "other_solids_required": 1,
        "ped_solids": 1,
        "ped_coal_for_ctl_ej": 1,
    },
)
def share_solids_for_final_energy():
    """
    Share of final energy vs primary energy for solids.
    """
    return zidz(
        required_fed_by_solids(),
        ped_solids() - ped_coal_for_ctl_ej() - other_solids_required(),
    )
