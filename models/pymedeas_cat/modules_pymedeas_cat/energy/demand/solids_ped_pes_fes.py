"""
Module energy.demand.solids_ped_pes_fes
Translated using PySD version 3.10.0
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
    name="Energy losses from solids",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_distr_losses_ff_ej": 1, "transformation_ff_losses_ej": 1},
)
def energy_losses_from_solids():
    """
    Solids-related distribution and transformation losses.
    """
    return float(energy_distr_losses_ff_ej().loc["solids"]) + float(
        transformation_ff_losses_ej().loc["solids"]
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
    name="PEC coal",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"imports_cat_coal_from_row_ej": 1, "extraction_coal_cat": 1},
)
def pec_coal():
    return imports_cat_coal_from_row_ej() + extraction_coal_cat()


@component.add(
    name="PEC coal for conversion",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pec_coal": 1, "share_coal_for_conversion": 1},
)
def pec_coal_for_conversion():
    return pec_coal() * share_coal_for_conversion()


@component.add(
    name="PEC waste for conversion",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_waste_for_chp_plants": 1,
        "pes_waste_for_elec_plants": 1,
        "pes_waste_for_heatcom_plants": 1,
    },
)
def pec_waste_for_conversion():
    """
    Primary energy consumption of waste to convert it into electricity and heat. Waste is converted to the aforemnetioned in waste valorization facilities.
    """
    return (
        pes_waste_for_chp_plants()
        + pes_waste_for_elec_plants()
        + pes_waste_for_heatcom_plants()
    )


@component.add(
    name="PED coal EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_coal_for_conversion": 1,
        "fes_biomass": 1,
        "pes_waste": 1,
        "pe_traditional_biomass_ej_delayed_1yr": 1,
        "ped_solids": 1,
        "losses_in_charcoal_plants_ej": 1,
        "pes_peat_ej": 1,
    },
)
def ped_coal_ej():
    return np.maximum(
        ped_coal_for_conversion(),
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
    name="PED coal for conversion",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_coal_elec_plants_ej": 1,
        "ped_coal_for_chp_plants_ej": 1,
        "ped_coal_for_heat_plants_ej": 1,
        "ped_coal_heatnc": 1,
        "ped_coal_for_ctl_ej": 1,
    },
)
def ped_coal_for_conversion():
    """
    Primary energy demand of coal to convert it into heat and electricity.
    """
    return (
        ped_coal_elec_plants_ej()
        + ped_coal_for_chp_plants_ej()
        + ped_coal_for_heat_plants_ej()
        + ped_coal_heatnc()
        + ped_coal_for_ctl_ej()
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
        "ped_coal_for_conversion": 1,
        "pec_waste_for_conversion": 1,
        "energy_losses_from_solids": 1,
        "nonenergy_use_demand_by_final_fuel_ej": 1,
    },
)
def ped_solids():
    """
    Primary energy demand of solids.
    """
    return np.maximum(
        0,
        required_fed_by_solids()
        + ped_coal_for_conversion()
        + pec_waste_for_conversion()
        + energy_losses_from_solids()
        + float(nonenergy_use_demand_by_final_fuel_ej().loc["solids"]),
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
    units="EJ/Year",
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
        "required_fed_by_solids": 1,
        "pes_solids": 1,
        "energy_losses_from_solids": 1,
        "share_solids_for_final_energy": 1,
    },
)
def real_fe_consumption_solids_ej():
    """
    Real final energy consumption by solids after accounting for energy availability.
    """
    return np.minimum(
        required_fed_by_solids(),
        (pes_solids() - energy_losses_from_solids()) * share_solids_for_final_energy(),
    )


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
    name="share coal for conversion",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_for_conversion": 1, "ped_coal_ej": 1},
)
def share_coal_for_conversion():
    return zidz(ped_coal_for_conversion(), ped_coal_ej())


@component.add(
    name='"share fed vs non-energy solids"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_solids": 2,
        "nonenergy_use_demand_by_final_fuel_ej": 1,
    },
)
def share_fed_vs_nonenergy_solids():
    return zidz(
        required_fed_by_solids(),
        float(nonenergy_use_demand_by_final_fuel_ej().loc["solids"])
        + required_fed_by_solids(),
    )


@component.add(
    name="share solids for final energy",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_solids": 1,
        "energy_losses_from_solids": 1,
        "ped_solids": 1,
    },
)
def share_solids_for_final_energy():
    """
    Share of final energy vs primary energy for solids.
    """
    return zidz(required_fed_by_solids(), ped_solids() - energy_losses_from_solids())


@component.add(
    name='"share solids for non-energy uses"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nonenergy_use_demand_by_final_fuel_ej": 1,
        "energy_losses_from_solids": 1,
        "ped_solids": 1,
    },
)
def share_solids_for_nonenergy_uses():
    return zidz(
        float(nonenergy_use_demand_by_final_fuel_ej().loc["solids"]),
        ped_solids() - energy_losses_from_solids(),
    )
