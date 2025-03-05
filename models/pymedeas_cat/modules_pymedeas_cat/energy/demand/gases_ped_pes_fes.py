"""
Module energy.demand.gases_ped_pes_fes
Translated using PySD version 3.14.2
"""

@component.add(
    name="abundance_gases",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_gases": 3, "pes_gases": 2},
)
def abundance_gases():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        ped_gases() < pes_gases(),
        lambda: 1,
        lambda: 1 - zidz(ped_gases() - pes_gases(), ped_gases()),
    )


@component.add(
    name="check_gases",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_gases": 1, "pes_gases": 2},
)
def check_gases():
    """
    Variable to avoid energy oversupply caused by exogenously driven policies.
    """
    return zidz(ped_gases() - pes_gases(), pes_gases())


@component.add(
    name='"constrain_gas_exogenous_growth?"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"check_gases": 2},
)
def constrain_gas_exogenous_growth():
    """
    If negative, there is oversupply of gas. This variable is used to constrain the exogenous growth of exogenously-driven policies.
    """
    return if_then_else(check_gases() > -0.01, lambda: 1, lambda: check_gases())


@component.add(
    name="FES_total_biogas",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"share_biogas_in_pes": 1, "real_fe_consumption_gases_ej": 1},
)
def fes_total_biogas():
    return share_biogas_in_pes() * real_fe_consumption_gases_ej()


@component.add(
    name='"Historic_conv_nat._gas_domestic_CAT_extracted_EJ"',
    units="EJ/year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_conv_nat_gas_domestic_cat_extracted_ej",
        "__data__": "_ext_data_historic_conv_nat_gas_domestic_cat_extracted_ej",
        "time": 1,
    },
)
def historic_conv_nat_gas_domestic_cat_extracted_ej():
    return _ext_data_historic_conv_nat_gas_domestic_cat_extracted_ej(time())


_ext_data_historic_conv_nat_gas_domestic_cat_extracted_ej = ExtData(
    r"../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_domestic_natural_gas_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_conv_nat_gas_domestic_cat_extracted_ej",
)


@component.add(
    name='"Historic_net_imports_nat._gas_CAT_"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_nat_gas_ej": 1,
        "historic_conv_nat_gas_domestic_cat_extracted_ej": 1,
        "historic_unconv_nat_gas_domestic_cat_extracted_ej": 1,
    },
)
def historic_net_imports_nat_gas_cat_():
    return (
        ped_nat_gas_ej()
        - historic_conv_nat_gas_domestic_cat_extracted_ej()
        - historic_unconv_nat_gas_domestic_cat_extracted_ej()
    )


@component.add(
    name='"Historic_share_conv._nat_gas_domestic_CAT_extraction"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "historic_conv_nat_gas_domestic_cat_extracted_ej": 1,
        "ped_nat_gas_ej": 1,
    },
)
def historic_share_conv_nat_gas_domestic_cat_extraction():
    return zidz(historic_conv_nat_gas_domestic_cat_extracted_ej(), ped_nat_gas_ej())


@component.add(
    name='"Historic_share_conv._nat_gas_domestic_CAT_extraction\\"_until_2016"',
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={
        "_sampleiftrue_historic_share_conv_nat_gas_domestic_cat_extraction_until_2016": 1
    },
    other_deps={
        "_sampleiftrue_historic_share_conv_nat_gas_domestic_cat_extraction_until_2016": {
            "initial": {"historic_share_conv_nat_gas_domestic_cat_extraction": 1},
            "step": {
                "time": 1,
                "historic_share_conv_nat_gas_domestic_cat_extraction": 1,
            },
        }
    },
)
def historic_share_conv_nat_gas_domestic_cat_extraction_until_2016():
    return (
        _sampleiftrue_historic_share_conv_nat_gas_domestic_cat_extraction_until_2016()
    )


_sampleiftrue_historic_share_conv_nat_gas_domestic_cat_extraction_until_2016 = (
    SampleIfTrue(
        lambda: time() < 2016,
        lambda: historic_share_conv_nat_gas_domestic_cat_extraction(),
        lambda: historic_share_conv_nat_gas_domestic_cat_extraction(),
        "_sampleiftrue_historic_share_conv_nat_gas_domestic_cat_extraction_until_2016",
    )
)


@component.add(
    name='"Historic_share_net_imports_nat._gas_until_2016"',
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_historic_share_net_imports_nat_gas_until_2016": 1},
    other_deps={
        "_sampleiftrue_historic_share_net_imports_nat_gas_until_2016": {
            "initial": {
                "historic_net_imports_nat_gas_cat_": 1,
                "extraction_nat_gas_ej_world": 1,
            },
            "step": {
                "time": 1,
                "historic_net_imports_nat_gas_cat_": 1,
                "extraction_nat_gas_ej_world": 1,
            },
        }
    },
)
def historic_share_net_imports_nat_gas_until_2016():
    return _sampleiftrue_historic_share_net_imports_nat_gas_until_2016()


_sampleiftrue_historic_share_net_imports_nat_gas_until_2016 = SampleIfTrue(
    lambda: time() < 2016,
    lambda: zidz(historic_net_imports_nat_gas_cat_(), extraction_nat_gas_ej_world()),
    lambda: zidz(historic_net_imports_nat_gas_cat_(), extraction_nat_gas_ej_world()),
    "_sampleiftrue_historic_share_net_imports_nat_gas_until_2016",
)


@component.add(
    name='"Historic_share_unconv._nat._gas_domestric_CAT_extraction"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "historic_unconv_nat_gas_domestic_cat_extracted_ej": 1,
        "ped_nat_gas_ej": 1,
    },
)
def historic_share_unconv_nat_gas_domestric_cat_extraction():
    return zidz(historic_unconv_nat_gas_domestic_cat_extracted_ej(), ped_nat_gas_ej())


@component.add(
    name='"Historic_share_unconv._nat._gas_domestric_CAT_extraction_until_2016"',
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={
        "_sampleiftrue_historic_share_unconv_nat_gas_domestric_cat_extraction_until_2016": 1
    },
    other_deps={
        "_sampleiftrue_historic_share_unconv_nat_gas_domestric_cat_extraction_until_2016": {
            "initial": {"historic_share_unconv_nat_gas_domestric_cat_extraction": 1},
            "step": {
                "time": 1,
                "historic_share_unconv_nat_gas_domestric_cat_extraction": 1,
            },
        }
    },
)
def historic_share_unconv_nat_gas_domestric_cat_extraction_until_2016():
    return (
        _sampleiftrue_historic_share_unconv_nat_gas_domestric_cat_extraction_until_2016()
    )


_sampleiftrue_historic_share_unconv_nat_gas_domestric_cat_extraction_until_2016 = SampleIfTrue(
    lambda: time() < 2016,
    lambda: historic_share_unconv_nat_gas_domestric_cat_extraction(),
    lambda: historic_share_unconv_nat_gas_domestric_cat_extraction(),
    "_sampleiftrue_historic_share_unconv_nat_gas_domestric_cat_extraction_until_2016",
)


@component.add(
    name='"Historic_unconv_nat._gas_domestic_CAT_extracted_EJ"',
    units="EJ/year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_unconv_nat_gas_domestic_cat_extracted_ej",
        "__data__": "_ext_data_historic_unconv_nat_gas_domestic_cat_extracted_ej",
        "time": 1,
    },
)
def historic_unconv_nat_gas_domestic_cat_extracted_ej():
    return _ext_data_historic_unconv_nat_gas_domestic_cat_extracted_ej(time())


_ext_data_historic_unconv_nat_gas_domestic_cat_extracted_ej = ExtData(
    r"../energy.xlsx",
    "Catalonia",
    "time_historic_data",
    "historic_domestic_unconventional_natural_gas_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_unconv_nat_gas_domestic_cat_extracted_ej",
)


@component.add(
    name="imports_CAT_conv_gas_from_RoW",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "imports_cat_nat_gas_from_row_ej": 1,
        "share_conv_vs_total_gas_extraction_world": 1,
    },
)
def imports_cat_conv_gas_from_row():
    return (
        imports_cat_nat_gas_from_row_ej() * share_conv_vs_total_gas_extraction_world()
    )


@component.add(
    name='"imports_CAT_nat._gas_from_RoW_EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"net_gas_flux_cat": 1},
)
def imports_cat_nat_gas_from_row_ej():
    return net_gas_flux_cat()


@component.add(
    name="imports_CAT_unconv_gas_from_RoW",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "imports_cat_nat_gas_from_row_ej": 1,
        "share_conv_vs_total_gas_extraction_world": 1,
    },
)
def imports_cat_unconv_gas_from_row():
    return imports_cat_nat_gas_from_row_ej() * (
        1 - share_conv_vs_total_gas_extraction_world()
    )


@component.add(
    name="nat_gas_for_non_energy",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nonenergy_use_demand_by_final_fuel": 1, "share_ff_fs": 1},
)
def nat_gas_for_non_energy():
    return float(nonenergy_use_demand_by_final_fuel().loc["gases"]) * float(
        share_ff_fs().loc["gases"]
    )


@component.add(
    name="nat_gas_TFC",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_ej": 1, "share_nat_gas_for_fc_emissions_relevant": 1},
)
def nat_gas_tfc():
    return ped_nat_gas_ej() * share_nat_gas_for_fc_emissions_relevant()


@component.add(
    name="Other_gases_required",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "transformation_ff_losses_ej": 2,
        "energy_distr_losses_ff": 2,
        "nonenergy_use_demand_by_final_fuel": 2,
    },
)
def other_gases_required():
    return if_then_else(
        float(transformation_ff_losses_ej().loc["gases"])
        + float(energy_distr_losses_ff().loc["gases"])
        + float(nonenergy_use_demand_by_final_fuel().loc["gases"])
        < 0,
        lambda: 0,
        lambda: float(transformation_ff_losses_ej().loc["gases"])
        + float(energy_distr_losses_ff().loc["gases"])
        + float(nonenergy_use_demand_by_final_fuel().loc["gases"]),
    )


@component.add(
    name='"PEC_nat._gas"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_nat_gas_cat_": 1, "imports_cat_nat_gas_from_row_ej": 1},
)
def pec_nat_gas():
    return pes_nat_gas_cat_() + imports_cat_nat_gas_from_row_ej()


@component.add(
    name='"PED_CAT_nat._gas_from_RoW"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_ej": 1, "pes_nat_gas_cat_": 1},
)
def ped_cat_nat_gas_from_row():
    return float(np.maximum(0, ped_nat_gas_ej() - pes_nat_gas_cat_()))


@component.add(
    name='"PED_domestic_CAT_conv._nat._gas_EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_nat_gas_ej": 1,
        "historic_share_conv_nat_gas_domestic_cat_extraction_until_2016": 1,
    },
)
def ped_domestic_cat_conv_nat_gas_ej():
    return (
        ped_nat_gas_ej()
        * historic_share_conv_nat_gas_domestic_cat_extraction_until_2016()
    )


@component.add(
    name='"PED_domestic_CAT_total_nat.gas_EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_ej": 1, "imports_cat_nat_gas_from_row_ej": 1},
)
def ped_domestic_cat_total_natgas_ej():
    """
    "PED nat. gas EJ"*("Historic share conv. nat gas domestic CAT extraction
    " until 2016"+"Historic share unconv. nat. gas domestric CAT extraction until 2016" )
    """
    return float(np.maximum(0, ped_nat_gas_ej() - imports_cat_nat_gas_from_row_ej()))


@component.add(
    name="PED_gases",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_gases": 1,
        "ped_nat_gas_for_gtl_ej": 1,
        "ped_gas_elec_plants_ej": 1,
        "ped_gases_for_heat_plants_ej": 1,
        "ped_gas_for_chp_plants_ej": 1,
        "ped_gas_heatnc": 1,
        "other_gases_required": 1,
        "pes_biogas_for_chp": 1,
        "pes_biogas_for_elec_plants": 1,
        "pes_biogas_for_heatcom_plants": 1,
        "self_consuption_energy_sector": 1,
    },
)
def ped_gases():
    """
    Primary energy demand total gases.
    """
    return float(
        np.maximum(
            0,
            required_fed_by_gases()
            + ped_nat_gas_for_gtl_ej()
            + ped_gas_elec_plants_ej()
            + ped_gases_for_heat_plants_ej()
            + ped_gas_for_chp_plants_ej()
            + ped_gas_heatnc()
            + other_gases_required()
            + pes_biogas_for_chp()
            + pes_biogas_for_elec_plants()
            + pes_biogas_for_heatcom_plants()
            + float(self_consuption_energy_sector().loc["gases"]),
        )
    )


@component.add(
    name='"PED_nat._gas_EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_gas_elec_plants_ej": 1,
        "ped_gas_for_chp_plants_ej": 1,
        "ped_gases_for_heat_plants_ej": 1,
        "synthethic_fuel_generation_delayed": 1,
        "ped_gases": 1,
        "pes_biogas_ej": 1,
    },
)
def ped_nat_gas_ej():
    """
    Primary energy demand of natural (fossil) gas.
    """
    return float(
        np.maximum(
            ped_gas_elec_plants_ej()
            + ped_gas_for_chp_plants_ej()
            + ped_gases_for_heat_plants_ej(),
            ped_gases()
            - pes_biogas_ej()
            - sum(
                synthethic_fuel_generation_delayed()
                .loc[_subscript_dict["ETG"]]
                .rename({"E_to_synthetic": "ETG!"}),
                dim=["ETG!"],
            ),
        )
    )


@component.add(
    name="PES_gases",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pec_nat_gas": 1,
        "pes_biogas_ej": 1,
        "synthethic_fuel_generation_delayed": 1,
    },
)
def pes_gases():
    """
    Primary energy supply gas.
    """
    return (
        pec_nat_gas()
        + pes_biogas_ej()
        + sum(
            synthethic_fuel_generation_delayed()
            .loc[_subscript_dict["ETG"]]
            .rename({"E_to_synthetic": "ETG!"}),
            dim=["ETG!"],
        )
    )


@component.add(
    name="real_FE_consumption_gases_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_gases": 1,
        "ped_nat_gas_for_gtl_ej": 1,
        "other_gases_required": 1,
        "share_gases_for_final_energy": 1,
    },
)
def real_fe_consumption_gases_ej():
    """
    Real final energy consumption by gases after accounting for energy availability.
    """
    return (
        pes_gases() - ped_nat_gas_for_gtl_ej() - other_gases_required()
    ) * share_gases_for_final_energy()


@component.add(
    name="Required_FED_by_gases",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"required_fed_by_fuel": 1},
)
def required_fed_by_gases():
    """
    Required final energy demand by gas.
    """
    return float(required_fed_by_fuel().loc["gases"])


@component.add(
    name="Share_biogas_in_PES",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_biogas_ej": 1, "pes_gases": 1},
)
def share_biogas_in_pes():
    return zidz(pes_biogas_ej(), pes_gases())


@component.add(
    name="share_FF_FS",
    units="1",
    subscripts=["matter_final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_nat_gas_ej": 1,
        "ped_gases": 1,
        "ped_liquids": 1,
        "ped_total_oil_ej": 1,
        "ped_solids": 1,
        "ped_coal_ej": 1,
    },
)
def share_ff_fs():
    value = xr.DataArray(
        np.nan,
        {"matter_final_sources": _subscript_dict["matter_final_sources"]},
        ["matter_final_sources"],
    )
    value.loc[["gases"]] = zidz(ped_nat_gas_ej(), ped_gases())
    value.loc[["liquids"]] = zidz(ped_total_oil_ej(), ped_liquids())
    value.loc[["solids"]] = zidz(ped_coal_ej(), ped_solids())
    return value


@component.add(
    name="share_gas_elec_plants",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_gas_elec_plants_ej": 1, "ped_nat_gas_ej": 1},
)
def share_gas_elec_plants():
    return zidz(ped_gas_elec_plants_ej(), ped_nat_gas_ej())


@component.add(
    name='"share_gases_dem_for_Heat-nc"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_gas_heatnc": 1, "pes_gases": 1, "ped_nat_gas_for_gtl_ej": 1},
)
def share_gases_dem_for_heatnc():
    """
    Share of natural gas demand for non-commercial Heat plants in relation to the demand of natural fossil gas.
    """
    return zidz(ped_gas_heatnc(), pes_gases() - ped_nat_gas_for_gtl_ej())


@component.add(
    name="share_gases_for_final_energy",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_gases": 1,
        "ped_gases": 1,
        "other_gases_required": 1,
        "ped_nat_gas_for_gtl_ej": 1,
    },
)
def share_gases_for_final_energy():
    """
    Share of final energy vs primary energy for gases.
    """
    return zidz(
        required_fed_by_gases(),
        ped_gases() - ped_nat_gas_for_gtl_ej() - other_gases_required(),
    )


@component.add(
    name='"share_nat._gas_dem_for_Elec"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_ej": 2, "ped_gas_elec_plants_ej": 1},
)
def share_nat_gas_dem_for_elec():
    """
    Share of natural gas demand to cover electricity consumption.
    """
    return if_then_else(
        ped_nat_gas_ej() > 0,
        lambda: ped_gas_elec_plants_ej() / ped_nat_gas_ej(),
        lambda: 0,
    )


@component.add(
    name='"share_nat._gas_dem_for_Heat-com"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_ej": 2, "ped_gases_for_heat_plants_ej": 1},
)
def share_nat_gas_dem_for_heatcom():
    """
    Share of natural gas demand for commercial Heat plants in relation to the demand of natural fossil gas.
    """
    return if_then_else(
        ped_nat_gas_ej() > 0,
        lambda: ped_gases_for_heat_plants_ej() / ped_nat_gas_ej(),
        lambda: 0,
    )


@component.add(
    name="share_nat_gas_for_Elec_emissions_relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_gas_elec_plants_ej": 1,
        "ped_gas_for_chp_plants_ej": 1,
        "share_elec_gen_in_chp": 1,
        "self_consuption_energy_sector": 1,
        "ped_nat_gas_ej": 1,
    },
)
def share_nat_gas_for_elec_emissions_relevant():
    return zidz(
        ped_gas_elec_plants_ej()
        + ped_gas_for_chp_plants_ej()
        * float(share_elec_gen_in_chp().loc["natural_gas"]),
        ped_nat_gas_ej() - float(self_consuption_energy_sector().loc["gases"]),
    )


@component.add(
    name="share_nat_gas_for_FC_emissions_relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_nat_gas_for_elec_emissions_relevant": 1,
        "share_nat_gas_for_gtl_emissions_relevant": 1,
        "share_nat_gas_for_heat_emissions_relevant": 1,
    },
)
def share_nat_gas_for_fc_emissions_relevant():
    """
    (1-(ZIDZ("Non-energy_use_demand_by_final_fuel"[gases]*share_FF_FS[gases],PED_gases)+s hare_nat_gas_for_Elec_emissions_relevant +share_nat_gas_for_GTL_emissions_relevant +share_nat_gas_for_Heat_emissions_relevant))
    """
    return 1 - (
        share_nat_gas_for_elec_emissions_relevant()
        + share_nat_gas_for_gtl_emissions_relevant()
        + share_nat_gas_for_heat_emissions_relevant()
    )


@component.add(
    name="share_nat_gas_for_GTL_emissions_relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_for_gtl_ej": 1, "ped_nat_gas_ej": 1, "share_ff_fs": 1},
)
def share_nat_gas_for_gtl_emissions_relevant():
    return zidz(ped_nat_gas_for_gtl_ej(), ped_nat_gas_ej()) * float(
        share_ff_fs().loc["gases"]
    )


@component.add(
    name="share_nat_gas_for_Heat_emissions_relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_gases_for_heat_plants_ej": 1,
        "ped_gas_heatnc": 1,
        "ped_gas_for_chp_plants_ej": 1,
        "share_elec_gen_in_chp": 1,
        "self_consuption_energy_sector": 1,
        "ped_nat_gas_ej": 1,
    },
)
def share_nat_gas_for_heat_emissions_relevant():
    return zidz(
        ped_gases_for_heat_plants_ej()
        + ped_gas_heatnc()
        + ped_gas_for_chp_plants_ej()
        * (1 - float(share_elec_gen_in_chp().loc["natural_gas"])),
        ped_nat_gas_ej() - -float(self_consuption_energy_sector().loc["gases"]),
    )


@component.add(
    name="Year_scarcity_gases",
    units="year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_gases": 1, "time": 1},
)
def year_scarcity_gases():
    """
    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_gases() > 0.95, lambda: 0, lambda: time())
