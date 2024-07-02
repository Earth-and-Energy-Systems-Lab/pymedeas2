"""
Module energy.demand.liquids_ped_pes_fes
Translated using PySD version 3.14.0
"""

@component.add(
    name="abundance_liquids",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_liquids": 3, "pes_liquids": 2},
)
def abundance_liquids():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        ped_liquids() < pes_liquids(),
        lambda: 1,
        lambda: 1 - zidz(ped_liquids() - pes_liquids(), ped_liquids()),
    )


@component.add(
    name="check_liquids",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_liquids": 1, "pes_liquids": 2},
)
def check_liquids():
    """
    If=0, demand=supply. If>0, demand>supply (liquids scarcity). If<0, demand<supply (oversupply). Variable to avoid energy oversupply caused by exogenously driven policies.
    """
    return zidz(ped_liquids() - pes_liquids(), pes_liquids())


@component.add(
    name='"constrain_liquids_exogenous_growth?"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"check_liquids": 2},
)
def constrain_liquids_exogenous_growth():
    """
    If negative, there is oversupply of liquids. This variable is used to constrain the exogenous growth of exogenously-driven policies.
    """
    return if_then_else(check_liquids() > 0, lambda: 1, lambda: check_liquids())


@component.add(
    name="Historic_conv_oil_domestic_CAT_extracted_EJ",
    units="EJ/year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_conv_oil_domestic_cat_extracted_ej",
        "__data__": "_ext_data_historic_conv_oil_domestic_cat_extracted_ej",
        "time": 1,
    },
)
def historic_conv_oil_domestic_cat_extracted_ej():
    return _ext_data_historic_conv_oil_domestic_cat_extracted_ej(time())


_ext_data_historic_conv_oil_domestic_cat_extracted_ej = ExtData(
    "../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_domestic_conventional_oil_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_conv_oil_domestic_cat_extracted_ej",
)


@component.add(
    name="Historic_net_imports_oil_CAT",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_liquids": 1,
        "historic_conv_oil_domestic_cat_extracted_ej": 1,
        "historic_unconv_oil_domestic_cat_extracted_ej": 1,
    },
)
def historic_net_imports_oil_cat():
    return (
        ped_liquids()
        - historic_conv_oil_domestic_cat_extracted_ej()
        - historic_unconv_oil_domestic_cat_extracted_ej()
    )


@component.add(
    name='"Historic_share_conv._oil_domestic_CAT_extraction"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"historic_conv_oil_domestic_cat_extracted_ej": 1, "ped_liquids": 1},
)
def historic_share_conv_oil_domestic_cat_extraction():
    return zidz(historic_conv_oil_domestic_cat_extracted_ej(), ped_liquids())


@component.add(
    name='"Historic_share_conv._oil_domestic_CAT_extraction\\"_until_2016"',
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={
        "_sampleiftrue_historic_share_conv_oil_domestic_cat_extraction_until_2016": 1
    },
    other_deps={
        "_sampleiftrue_historic_share_conv_oil_domestic_cat_extraction_until_2016": {
            "initial": {"historic_share_conv_oil_domestic_cat_extraction": 1},
            "step": {"time": 1, "historic_share_conv_oil_domestic_cat_extraction": 1},
        }
    },
)
def historic_share_conv_oil_domestic_cat_extraction_until_2016():
    return _sampleiftrue_historic_share_conv_oil_domestic_cat_extraction_until_2016()


_sampleiftrue_historic_share_conv_oil_domestic_cat_extraction_until_2016 = SampleIfTrue(
    lambda: time() < 2016,
    lambda: historic_share_conv_oil_domestic_cat_extraction(),
    lambda: historic_share_conv_oil_domestic_cat_extraction(),
    "_sampleiftrue_historic_share_conv_oil_domestic_cat_extraction_until_2016",
)


@component.add(
    name="Historic_unconv_oil_domestic_CAT_extracted_EJ",
    units="EJ/year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_unconv_oil_domestic_cat_extracted_ej",
        "__data__": "_ext_data_historic_unconv_oil_domestic_cat_extracted_ej",
        "time": 1,
    },
)
def historic_unconv_oil_domestic_cat_extracted_ej():
    return _ext_data_historic_unconv_oil_domestic_cat_extracted_ej(time())


_ext_data_historic_unconv_oil_domestic_cat_extracted_ej = ExtData(
    "../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_domestic_unconventional_oil_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_unconv_oil_domestic_cat_extracted_ej",
)


@component.add(
    name="imports_CAT_conv_oil_from_RoW_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "imports_cat_total_oil_from_row_ej": 1,
        "share_conv_vs_total_oil_extraction_world": 1,
    },
)
def imports_cat_conv_oil_from_row_ej():
    return (
        imports_cat_total_oil_from_row_ej() * share_conv_vs_total_oil_extraction_world()
    )


@component.add(
    name="imports_CAT_total_oil_from_RoW_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"net_oil_flux_cat": 1},
)
def imports_cat_total_oil_from_row_ej():
    return net_oil_flux_cat()


@component.add(
    name="imports_CAT_unconv_oil_from_RoW_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "imports_cat_total_oil_from_row_ej": 1,
        "share_conv_vs_total_oil_extraction_world": 1,
    },
)
def imports_cat_unconv_oil_from_row_ej():
    return imports_cat_total_oil_from_row_ej() * (
        1 - share_conv_vs_total_oil_extraction_world()
    )


@component.add(
    name='"Non-energy_use_consumption"',
    units="EJ/year",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_liquids_for_nonenergy_use": 1,
        "pes_liquids": 1,
        "transformation_ff_losses_ej": 1,
        "energy_distr_losses_ff": 1,
    },
)
def nonenergy_use_consumption():
    return xr.DataArray(
        share_liquids_for_nonenergy_use()
        * (
            pes_liquids()
            - float(transformation_ff_losses_ej().loc["liquids"])
            - float(energy_distr_losses_ff().loc["liquids"])
        ),
        {"final_sources": _subscript_dict["final_sources"]},
        ["final_sources"],
    )


@component.add(
    name="oil_TFC",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_liquids": 1, "share_oil_for_fc_emissions_relevant": 1},
)
def oil_tfc():
    return ped_liquids() * share_oil_for_fc_emissions_relevant()


@component.add(
    name="Other_liquids_required_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "energy_distr_losses_ff": 1,
        "transformation_ff_losses_ej": 1,
        "nonenergy_use_demand_by_final_fuel": 1,
    },
)
def other_liquids_required_ej():
    return (
        float(energy_distr_losses_ff().loc["liquids"])
        + float(transformation_ff_losses_ej().loc["liquids"])
        + float(nonenergy_use_demand_by_final_fuel().loc["liquids"])
    )


@component.add(
    name="Other_liquids_supply_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "oil_refinery_gains_ej": 1,
        "fes_ctlgtl_ej": 1,
        "fes_total_biofuels_ej": 1,
    },
)
def other_liquids_supply_ej():
    """
    Other liquids refer to: refinery gains, CTL, GTL and biofuels.
    """
    return oil_refinery_gains_ej() + fes_ctlgtl_ej() + fes_total_biofuels_ej()


@component.add(
    name="PEC_oil_emissions_relevant",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pec_total_oil": 1, "share_liquids_for_nonenergy_use": 1},
)
def pec_oil_emissions_relevant():
    return pec_total_oil() * (1 - share_liquids_for_nonenergy_use())


@component.add(
    name="PEC_total_oil",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_total_oil_ej_cat": 1, "imports_cat_total_oil_from_row_ej": 1},
)
def pec_total_oil():
    """
    There are loses related to oil refinery that reduces final energy consumtion
    """
    return pes_total_oil_ej_cat() + imports_cat_total_oil_from_row_ej()


@component.add(
    name="PED_CAT_total_oil_from_RoW",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_total_oil_ej": 1, "pes_total_oil_ej_cat": 1},
)
def ped_cat_total_oil_from_row():
    return np.maximum(0, ped_total_oil_ej() - pes_total_oil_ej_cat())


@component.add(
    name='"PED_domestic_CAT_conv._oil_EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_total_oil_ej": 1,
        "historic_share_conv_oil_domestic_cat_extraction_until_2016": 1,
    },
)
def ped_domestic_cat_conv_oil_ej():
    return (
        ped_total_oil_ej()
        * historic_share_conv_oil_domestic_cat_extraction_until_2016()
    )


@component.add(
    name="PED_domestic_CAT_total_oil_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_total_oil_ej": 1, "imports_cat_total_oil_from_row_ej": 1},
)
def ped_domestic_cat_total_oil_ej():
    """
    PED total oil EJ*("Historic share conv. oil domestic CAT extraction
    " until 2016"+"Historic share unconv. oil domestric CAT extraction until 2016" )
    """
    return np.maximum(0, ped_total_oil_ej() - imports_cat_total_oil_from_row_ej())


@component.add(
    name="PED_liquids",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_liquids": 1,
        "other_liquids_required_ej": 1,
        "ped_oil_elec_plants_ej": 1,
        "ped_oil_for_heat_plants": 1,
        "ped_oil_for_chp_plants_ej": 1,
        "ped_ff_heatnc": 1,
        "self_consuption_energy_sector": 1,
    },
)
def ped_liquids():
    """
    Primary energy demand of total liquids.
    """
    return np.maximum(
        0,
        required_fed_by_liquids()
        + other_liquids_required_ej()
        + ped_oil_elec_plants_ej()
        + ped_oil_for_heat_plants()
        + ped_oil_for_chp_plants_ej()
        + float(ped_ff_heatnc().loc["liquids"])
        + float(self_consuption_energy_sector().loc["liquids"]),
    )


@component.add(
    name="PED_NRE_Liquids",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_liquids": 1, "fes_total_biofuels_ej": 1},
)
def ped_nre_liquids():
    """
    Primary energy demand of non-renewable energy for the production of liquids.
    """
    return np.maximum(0, ped_liquids() - fes_total_biofuels_ej())


@component.add(
    name="PED_total_oil_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nre_liquids": 1, "fes_ctlgtl_ej": 1, "oil_refinery_gains_ej": 1},
)
def ped_total_oil_ej():
    """
    Primary energy demand of total oil (conventional and unconventional).
    """
    return np.maximum(0, ped_nre_liquids() - fes_ctlgtl_ej() - oil_refinery_gains_ej())


@component.add(
    name="PES_Liquids",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pec_total_oil": 1, "other_liquids_supply_ej": 1},
)
def pes_liquids():
    """
    Total primary supply of liquids.
    """
    return pec_total_oil() + other_liquids_supply_ej()


@component.add(
    name="real_FE_consumption_liquids_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_liquids": 1,
        "transformation_ff_losses_ej": 1,
        "energy_distr_losses_ff": 1,
        "share_liquids_for_final_energy": 1,
    },
)
def real_fe_consumption_liquids_ej():
    """
    Real final energy consumption by liquids after accounting for energy availability.
    """
    return (
        pes_liquids()
        - float(transformation_ff_losses_ej().loc["liquids"])
        - float(energy_distr_losses_ff().loc["liquids"])
    ) * share_liquids_for_final_energy()


@component.add(
    name="Required_FED_by_liquids",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fuel": 1},
)
def required_fed_by_liquids():
    """
    Required final energy demand by liquids.
    """
    return float(required_fed_by_fuel().loc["liquids"])


@component.add(
    name="self_consuption_energy_sector",
    units="EJ/year",
    subscripts=["matter_final_sources"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_liquids": 1, "required_fed_by_gases": 1},
)
def self_consuption_energy_sector():
    value = xr.DataArray(
        np.nan,
        {"matter_final_sources": _subscript_dict["matter_final_sources"]},
        ["matter_final_sources"],
    )
    value.loc[["liquids"]] = 0.164216 * required_fed_by_liquids()
    value.loc[["gases"]] = required_fed_by_gases() * 0.0917106
    value.loc[["solids"]] = 0
    return value


@component.add(
    name="Share_biofuel_in_PES",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fes_total_biofuels_ej": 1, "pes_liquids": 1},
)
def share_biofuel_in_pes():
    return zidz(fes_total_biofuels_ej(), pes_liquids())


@component.add(
    name='"share_liquids_dem_for_Heat-nc"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_ff_heatnc": 1, "pes_liquids": 1},
)
def share_liquids_dem_for_heatnc():
    """
    Share of liquids demand for non-commercial Heat plants in relation to the total demand of liquids.
    """
    return zidz(float(ped_ff_heatnc().loc["liquids"]), pes_liquids())


@component.add(
    name="share_liquids_for_final_energy",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_liquids": 1,
        "transformation_ff_losses_ej": 1,
        "ped_liquids": 1,
        "energy_distr_losses_ff": 1,
    },
)
def share_liquids_for_final_energy():
    """
    Share of final energy vs primary energy for liquids.
    """
    return zidz(
        required_fed_by_liquids(),
        ped_liquids()
        - float(transformation_ff_losses_ej().loc["liquids"])
        - float(energy_distr_losses_ff().loc["liquids"]),
    )


@component.add(
    name='"share_liquids_for_non-energy_use"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nonenergy_use_demand_by_final_fuel": 1,
        "transformation_ff_losses_ej": 1,
        "ped_liquids": 1,
        "energy_distr_losses_ff": 1,
    },
)
def share_liquids_for_nonenergy_use():
    return zidz(
        float(nonenergy_use_demand_by_final_fuel().loc["liquids"]),
        ped_liquids()
        - float(transformation_ff_losses_ej().loc["liquids"])
        - float(energy_distr_losses_ff().loc["liquids"]),
    )


@component.add(
    name='"share_oil_dem_for_Heat-com"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_total_oil_ej": 2, "ped_oil_for_heat_plants": 1},
)
def share_oil_dem_for_heatcom():
    """
    Share of oil demand for commercial Heat plants in relation to the total demand of oil.
    """
    return if_then_else(
        ped_total_oil_ej() > 0,
        lambda: ped_oil_for_heat_plants() / ped_total_oil_ej(),
        lambda: 0,
    )


@component.add(
    name="share_oil_elec_plants",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_oil_elec_plants_ej": 1, "ped_total_oil_ej": 1},
)
def share_oil_elec_plants():
    return zidz(ped_oil_elec_plants_ej(), ped_total_oil_ej())


@component.add(
    name="share_oil_for_Elec_emissions_relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_oil_elec_plants_ej": 1,
        "share_elec_gen_in_chp": 1,
        "ped_oil_for_chp_plants_ej": 1,
        "ped_total_oil_ej": 1,
        "self_consuption_energy_sector": 1,
    },
)
def share_oil_for_elec_emissions_relevant():
    return (
        ped_oil_elec_plants_ej()
        + ped_oil_for_chp_plants_ej() * float(share_elec_gen_in_chp().loc["oil"])
    ) / (ped_total_oil_ej() - float(self_consuption_energy_sector().loc["liquids"]))


@component.add(
    name="share_oil_for_FC_emissions_relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nonenergy_use_demand_by_final_fuel": 1,
        "share_oil_for_elec_emissions_relevant": 1,
        "ped_liquids": 1,
        "share_oil_for_heat_emissions_relevant": 1,
    },
)
def share_oil_for_fc_emissions_relevant():
    return (
        1
        - zidz(
            float(nonenergy_use_demand_by_final_fuel().loc["liquids"]),
            ped_liquids() - share_oil_for_elec_emissions_relevant(),
        )
        - share_oil_for_heat_emissions_relevant()
    )


@component.add(
    name="share_oil_for_heat_CHP_plants",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_oil_for_chp_plants_ej": 1,
        "ped_total_oil_ej": 1,
        "share_elec_gen_in_chp": 1,
    },
)
def share_oil_for_heat_chp_plants():
    return (ped_oil_for_chp_plants_ej() / ped_total_oil_ej()) * (
        1 - float(share_elec_gen_in_chp().loc["oil"])
    )


@component.add(
    name="share_oil_for_Heat_emissions_relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_oil_for_heat_plants": 1,
        "ped_ff_heatnc": 1,
        "share_elec_gen_in_chp": 1,
        "ped_oil_for_chp_plants_ej": 1,
        "ped_total_oil_ej": 1,
        "self_consuption_energy_sector": 1,
    },
)
def share_oil_for_heat_emissions_relevant():
    return (
        ped_oil_for_heat_plants()
        + float(ped_ff_heatnc().loc["liquids"])
        + ped_oil_for_chp_plants_ej() * (1 - float(share_elec_gen_in_chp().loc["oil"]))
    ) / (ped_total_oil_ej() - float(self_consuption_energy_sector().loc["liquids"]))


@component.add(
    name='"Total_demand_liquids_mb/d"',
    units="Mb/d",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_liquids": 1, "mbd_per_ejyear": 1},
)
def total_demand_liquids_mbd():
    """
    Total demand of liquids.
    """
    return ped_liquids() * mbd_per_ejyear()


@component.add(
    name="Year_scarcity_liquids",
    units="year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_liquids": 1, "time": 1},
)
def year_scarcity_liquids():
    """
    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_liquids() > 0.95, lambda: 0, lambda: time())
