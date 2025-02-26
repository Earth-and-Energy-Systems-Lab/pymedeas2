"""
Module energy.demand.ff_ped_pes_fes
Translated using PySD version 3.14.2
"""

@component.add(
    name="a_lin_reg_peat",
    units="EJ/(year*year)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def a_lin_reg_peat():
    return -0.0125


@component.add(
    name="abundance_FS",
    units="Dmnl",
    subscripts=["matter_final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_fs": 3, "pes_fs": 2},
)
def abundance_fs():
    return if_then_else(
        ped_fs() < pes_fs(),
        lambda: xr.DataArray(
            1,
            {"matter_final_sources": _subscript_dict["matter_final_sources"]},
            ["matter_final_sources"],
        ),
        lambda: 1 - zidz(ped_fs() - pes_fs(), ped_fs()),
    )


@component.add(
    name="b_lin_reg_peat", units="EJ/year", comp_type="Constant", comp_subtype="Normal"
)
def b_lin_reg_peat():
    return 25.3125


@component.add(
    name='"Historic_conv_nat._gas_domestic_EU_extracted_EJ"',
    units="EJ/year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_conv_nat_gas_domestic_eu_extracted_ej",
        "__data__": "_ext_data_historic_conv_nat_gas_domestic_eu_extracted_ej",
        "time": 1,
    },
)
def historic_conv_nat_gas_domestic_eu_extracted_ej():
    return _ext_data_historic_conv_nat_gas_domestic_eu_extracted_ej(time())


_ext_data_historic_conv_nat_gas_domestic_eu_extracted_ej = ExtData(
    r"../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_domestic_natural_gas_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_conv_nat_gas_domestic_eu_extracted_ej",
)


@component.add(
    name="Historic_conv_oil_domestic_EU_extracted",
    units="EJ/year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_conv_oil_domestic_eu_extracted",
        "__data__": "_ext_data_historic_conv_oil_domestic_eu_extracted",
        "time": 1,
    },
)
def historic_conv_oil_domestic_eu_extracted():
    return _ext_data_historic_conv_oil_domestic_eu_extracted(time())


_ext_data_historic_conv_oil_domestic_eu_extracted = ExtData(
    r"../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_domestic_conventional_oil_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_conv_oil_domestic_eu_extracted",
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
    "Europe",
    "time_efficiencies",
    "historic_primary_energy_supply_peat",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_pes_peat_ej",
)


@component.add(
    name='"Historic_share_conv._nat_gas_domestic_EU_extraction"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "historic_conv_nat_gas_domestic_eu_extracted_ej": 2,
        "historic_unconv_nat_gas_domestic_eu_extracted_ej": 1,
    },
)
def historic_share_conv_nat_gas_domestic_eu_extraction():
    return zidz(
        historic_conv_nat_gas_domestic_eu_extracted_ej(),
        historic_conv_nat_gas_domestic_eu_extracted_ej()
        + historic_unconv_nat_gas_domestic_eu_extracted_ej(),
    )


@component.add(
    name='"Historic_share_conv._nat_gas_domestic_EU_extraction_until_2016"',
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={
        "_sampleiftrue_historic_share_conv_nat_gas_domestic_eu_extraction_until_2016": 1
    },
    other_deps={
        "_sampleiftrue_historic_share_conv_nat_gas_domestic_eu_extraction_until_2016": {
            "initial": {"historic_share_conv_nat_gas_domestic_eu_extraction": 1},
            "step": {
                "time": 1,
                "historic_share_conv_nat_gas_domestic_eu_extraction": 1,
            },
        }
    },
)
def historic_share_conv_nat_gas_domestic_eu_extraction_until_2016():
    return _sampleiftrue_historic_share_conv_nat_gas_domestic_eu_extraction_until_2016()


_sampleiftrue_historic_share_conv_nat_gas_domestic_eu_extraction_until_2016 = (
    SampleIfTrue(
        lambda: time() < 2016,
        lambda: historic_share_conv_nat_gas_domestic_eu_extraction(),
        lambda: historic_share_conv_nat_gas_domestic_eu_extraction(),
        "_sampleiftrue_historic_share_conv_nat_gas_domestic_eu_extraction_until_2016",
    )
)


@component.add(
    name='"Historic_share_conv._oil_domestic_EU_extraction"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "historic_conv_oil_domestic_eu_extracted": 2,
        "historic_unconv_oil_domestic_eu_extracted": 1,
    },
)
def historic_share_conv_oil_domestic_eu_extraction():
    return zidz(
        historic_conv_oil_domestic_eu_extracted(),
        historic_conv_oil_domestic_eu_extracted()
        + historic_unconv_oil_domestic_eu_extracted(),
    )


@component.add(
    name='"Historic_share_conv._oil_domestic_EU_extraction\\"_until_2016"',
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={
        "_sampleiftrue_historic_share_conv_oil_domestic_eu_extraction_until_2016": 1
    },
    other_deps={
        "_sampleiftrue_historic_share_conv_oil_domestic_eu_extraction_until_2016": {
            "initial": {"historic_share_conv_oil_domestic_eu_extraction": 1},
            "step": {"time": 1, "historic_share_conv_oil_domestic_eu_extraction": 1},
        }
    },
)
def historic_share_conv_oil_domestic_eu_extraction_until_2016():
    return _sampleiftrue_historic_share_conv_oil_domestic_eu_extraction_until_2016()


_sampleiftrue_historic_share_conv_oil_domestic_eu_extraction_until_2016 = SampleIfTrue(
    lambda: time() < 2016,
    lambda: historic_share_conv_oil_domestic_eu_extraction(),
    lambda: historic_share_conv_oil_domestic_eu_extraction(),
    "_sampleiftrue_historic_share_conv_oil_domestic_eu_extraction_until_2016",
)


@component.add(
    name='"Historic_unconv_nat._gas_domestic_EU_extracted_EJ"',
    units="EJ/year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_unconv_nat_gas_domestic_eu_extracted_ej",
        "__data__": "_ext_data_historic_unconv_nat_gas_domestic_eu_extracted_ej",
        "time": 1,
    },
)
def historic_unconv_nat_gas_domestic_eu_extracted_ej():
    return _ext_data_historic_unconv_nat_gas_domestic_eu_extracted_ej(time())


_ext_data_historic_unconv_nat_gas_domestic_eu_extracted_ej = ExtData(
    r"../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_domestic_unconventional_natural_gas_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_unconv_nat_gas_domestic_eu_extracted_ej",
)


@component.add(
    name="Historic_unconv_oil_domestic_EU_extracted",
    units="EJ/year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_historic_unconv_oil_domestic_eu_extracted",
        "__data__": "_ext_data_historic_unconv_oil_domestic_eu_extracted",
        "time": 1,
    },
)
def historic_unconv_oil_domestic_eu_extracted():
    """
    Historic unconventional extraction from Mohr et al (2015).
    """
    return _ext_data_historic_unconv_oil_domestic_eu_extracted(time())


_ext_data_historic_unconv_oil_domestic_eu_extracted = ExtData(
    r"../energy.xlsx",
    "Europe",
    "time_historic_data",
    "historic_unconventional_oil_extraction",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_historic_unconv_oil_domestic_eu_extracted",
)


@component.add(
    name="imports_EU_coal_from_RoW_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"net_coal_flux_eu": 1},
)
def imports_eu_coal_from_row_ej():
    """
    ** Name should be changed as well, because the name does not make evident that we are talking about net imports. net coal flux EU IF THEN ELSE(Time<2016, PED EU coal from RoW, IF THEN ELSE(limit coal imports from RoW=1, PED EU coal from RoW , IF THEN ELSE (limit coal imports from RoW=2, MIN(PED EU coal from RoW,Historic share net imports coal EU until 2016 *extraction coal EJ World), IF THEN ELSE(limit coal imports from RoW=3, MIN(PED EU coal from RoW, adapt max share imports coal*extraction coal EJ World ), PED EU coal from RoW))))
    """
    return net_coal_flux_eu()


@component.add(
    name="imports_EU_conv_oil_from_RoW_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "imports_eu_total_oil_from_row_ej": 1,
        "share_conv_vs_total_oil_extraction_world": 1,
    },
)
def imports_eu_conv_oil_from_row_ej():
    return (
        imports_eu_total_oil_from_row_ej() * share_conv_vs_total_oil_extraction_world()
    )


@component.add(
    name='"imports_EU_nat._gas_from_RoW_EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"net_gas_flux_eu": 1},
)
def imports_eu_nat_gas_from_row_ej():
    """
    ** Name should be changed as well, because the name does not make evident that we are talking about net imports. net gas flux EU IF THEN ELSE(Time<2016, "PED EU nat. gas from RoW", IF THEN ELSE(limit nat gas imports from RoW=1, "PED EU nat. gas from RoW", IF THEN ELSE (limit nat gas imports from RoW=2, MIN("PED EU nat. gas from RoW","Historic share net imports nat. gas until 2016" *"extraction nat. gas EJ World"), IF THEN ELSE(limit nat gas imports from RoW=3, MIN("PED EU nat. gas from RoW",adapt max share imports nat gas*"extraction nat. gas EJ World"), "PED EU nat. gas from RoW"))))
    """
    return net_gas_flux_eu()


@component.add(
    name="imports_EU_total_oil_from_RoW_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"net_oil_flux_eu": 1},
)
def imports_eu_total_oil_from_row_ej():
    """
    ** Name should be changed as well, because the name does not make evident that we are talking about net imports. net oil flux EU IF THEN ELSE(Time<2016, PED EU total oil from RoW, IF THEN ELSE(limit oil imports from RoW=1, PED EU total oil from RoW, IF THEN ELSE (limit oil imports from RoW=2, MIN(PED EU total oil from RoW,Historic share net imports oil until 2016 *Extraction oil EJ World), IF THEN ELSE(limit oil imports from RoW=3, MIN(PED EU total oil from RoW,adapt max share imports oil*Extraction oil EJ World ), PED EU total oil from RoW))))
    """
    return net_oil_flux_eu()


@component.add(
    name="imports_EU_unconv_oil_from_RoW_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "imports_eu_total_oil_from_row_ej": 1,
        "share_conv_vs_total_oil_extraction_world": 1,
    },
)
def imports_eu_unconv_oil_from_row_ej():
    return imports_eu_total_oil_from_row_ej() * (
        1 - share_conv_vs_total_oil_extraction_world()
    )


@component.add(
    name='"Non-energy_use_consumption"',
    units="EJ/year",
    subscripts=["matter_final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_ff_for_nonenergy_use": 1,
        "energy_distr_losses_ff": 1,
        "transformation_ff_losses": 1,
        "pes_fs": 1,
    },
)
def nonenergy_use_consumption():
    return share_ff_for_nonenergy_use() * (
        pes_fs()
        - transformation_ff_losses()
        .loc[_subscript_dict["matter_final_sources"]]
        .rename({"final_sources": "matter_final_sources"})
        - energy_distr_losses_ff()
        .loc[_subscript_dict["matter_final_sources"]]
        .rename({"final_sources": "matter_final_sources"})
    )


@component.add(
    name="other_FF_required",
    units="EJ/year",
    subscripts=["matter_final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "energy_distr_losses_ff": 2,
        "transformation_ff_losses": 2,
        "ped_coal_for_ctl": 1,
        "other_ff_required_liquids": 1,
        "ped_nat_gas_for_gtl_ej": 1,
    },
)
def other_ff_required():
    value = xr.DataArray(
        np.nan,
        {"matter_final_sources": _subscript_dict["matter_final_sources"]},
        ["matter_final_sources"],
    )
    value.loc[["solids"]] = (
        float(energy_distr_losses_ff().loc["solids"])
        + float(transformation_ff_losses().loc["solids"])
        + ped_coal_for_ctl()
    )
    value.loc[["liquids"]] = other_ff_required_liquids()
    value.loc[["gases"]] = (
        float(energy_distr_losses_ff().loc["gases"])
        + float(transformation_ff_losses().loc["gases"])
        + ped_nat_gas_for_gtl_ej()
    )
    return value


@component.add(
    name="other_FF_required_liquids",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_distr_losses_ff": 1, "transformation_ff_losses": 1},
)
def other_ff_required_liquids():
    """
    Other liquids required, comming from transformation and energy distribution losses
    """
    return float(energy_distr_losses_ff().loc["liquids"]) + float(
        transformation_ff_losses().loc["liquids"]
    )


@component.add(
    name="Other_FS_demands",
    units="EJ/year",
    subscripts=["matter_final_sources"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_biogas_ej": 1, "pes_biogas_for_tfc": 1},
)
def other_fs_demands():
    value = xr.DataArray(
        np.nan,
        {"matter_final_sources": _subscript_dict["matter_final_sources"]},
        ["matter_final_sources"],
    )
    value.loc[["gases"]] = pes_biogas_ej() - pes_biogas_for_tfc()
    value.loc[["liquids"]] = 0
    value.loc[["solids"]] = 0
    return value


@component.add(
    name="Other_liquids_supply_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "oil_refinery_gains_ej": 1,
        "fes_ctlgtl_ej": 1,
        "fes_total_biofuels_production_ej": 1,
        "synthethic_fuel_generation_delayed": 1,
    },
)
def other_liquids_supply_ej():
    """
    Other liquids refer to: refinery gains, CTL, GTL and biofuels.
    """
    return (
        oil_refinery_gains_ej()
        + fes_ctlgtl_ej()
        + fes_total_biofuels_production_ej()
        + sum(
            synthethic_fuel_generation_delayed()
            .loc[_subscript_dict["ETL"]]
            .rename({"E_to_synthetic": "ETL!"}),
            dim=["ETL!"],
        )
    )


@component.add(
    name="PEC_FF",
    units="EJ/year",
    subscripts=["matter_final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_coal_eu": 1,
        "imports_eu_coal_from_row_ej": 1,
        "pes_nat_gas_eu": 1,
        "imports_eu_nat_gas_from_row_ej": 1,
        "pes_total_oil_ej_eu": 1,
        "imports_eu_total_oil_from_row_ej": 1,
        "fes_ctlgtl_ej": 1,
    },
)
def pec_ff():
    value = xr.DataArray(
        np.nan,
        {"matter_final_sources": _subscript_dict["matter_final_sources"]},
        ["matter_final_sources"],
    )
    value.loc[["solids"]] = extraction_coal_eu() + imports_eu_coal_from_row_ej()
    value.loc[["gases"]] = pes_nat_gas_eu() + imports_eu_nat_gas_from_row_ej()
    value.loc[["liquids"]] = (
        pes_total_oil_ej_eu() + imports_eu_total_oil_from_row_ej() + fes_ctlgtl_ej()
    )
    return value


@component.add(
    name='"PED_domestic_EU_conv._FF"',
    units="EJ/year",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_domestic_ff": 2,
        "historic_share_conv_nat_gas_domestic_eu_extraction_until_2016": 1,
        "historic_share_conv_oil_domestic_eu_extraction_until_2016": 1,
    },
)
def ped_domestic_eu_conv_ff():
    value = xr.DataArray(
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    value.loc[["gases"]] = (
        float(ped_domestic_ff().loc["gases"])
        * historic_share_conv_nat_gas_domestic_eu_extraction_until_2016()
    )
    value.loc[["liquids"]] = (
        float(ped_domestic_ff().loc["liquids"])
        * historic_share_conv_oil_domestic_eu_extraction_until_2016()
    )
    return value


@component.add(
    name="PED_domestic_FF",
    units="EJ/year",
    subscripts=["matter_final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_nre_fs": 2,
        "imports_eu_coal_from_row_ej": 1,
        "imports_eu_nat_gas_from_row_ej": 1,
        "ped_total_oil_ej": 1,
        "imports_eu_total_oil_from_row_ej": 1,
    },
)
def ped_domestic_ff():
    value = xr.DataArray(
        np.nan,
        {"matter_final_sources": _subscript_dict["matter_final_sources"]},
        ["matter_final_sources"],
    )
    value.loc[["solids"]] = float(
        np.maximum(0, float(ped_nre_fs().loc["solids"]) - imports_eu_coal_from_row_ej())
    )
    value.loc[["gases"]] = float(
        np.maximum(
            0, float(ped_nre_fs().loc["gases"]) - imports_eu_nat_gas_from_row_ej()
        )
    )
    value.loc[["liquids"]] = float(
        np.maximum(0, ped_total_oil_ej() - imports_eu_total_oil_from_row_ej())
    )
    return value


@component.add(
    name="PED_FS",
    units="EJ/year",
    subscripts=["matter_final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_fuel": 1,
        "nonenergy_use_demand_by_final_fuel": 1,
        "other_ff_required": 1,
        "ped_ff_elec_plants": 1,
        "ped_ff_for_heat_plants": 1,
        "ped_ff_for_chp_plants": 1,
        "ped_ff_heatnc": 1,
        "other_fs_demands": 1,
    },
)
def ped_fs():
    return np.maximum(
        0,
        required_fed_by_fuel()
        .loc[_subscript_dict["matter_final_sources"]]
        .rename({"final_sources": "matter_final_sources"})
        + nonenergy_use_demand_by_final_fuel()
        .loc[_subscript_dict["matter_final_sources"]]
        .rename({"final_sources": "matter_final_sources"})
        + other_ff_required()
        + ped_ff_elec_plants()
        + ped_ff_for_heat_plants()
        + ped_ff_for_chp_plants()
        + ped_ff_heatnc()
        + other_fs_demands(),
    )


@component.add(
    name="PED_FS_liquids",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_fuel": 1,
        "nonenergy_use_demand_by_final_fuel": 1,
        "other_ff_required_liquids": 1,
        "ped_ff_elec_plants": 1,
        "ped_ff_for_heat_plants": 1,
        "ped_ff_for_chp_plants": 1,
        "ped_ff_heatnc": 1,
    },
)
def ped_fs_liquids():
    """
    Primary Energy Demand of liquids
    """
    return float(
        np.maximum(
            0,
            float(required_fed_by_fuel().loc["liquids"])
            + float(nonenergy_use_demand_by_final_fuel().loc["liquids"])
            + other_ff_required_liquids()
            + float(ped_ff_elec_plants().loc["liquids"])
            + float(ped_ff_for_heat_plants().loc["liquids"])
            + float(ped_ff_for_chp_plants().loc["liquids"])
            + float(ped_ff_heatnc().loc["liquids"]),
        )
    )


@component.add(
    name='"PED_nat._gas_EJ"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_fs": 1, "pes_biogas_for_tfc": 1},
)
def ped_nat_gas_ej():
    """
    Primary energy demand of natural (fossil) gas.
    """
    return float(np.maximum(0, float(ped_fs().loc["gases"]) - pes_biogas_for_tfc()))


@component.add(
    name="PED_NRE_FS",
    units="EJ/year",
    subscripts=["matter_final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_nre_fs_liquids": 1,
        "synthethic_fuel_generation_delayed": 2,
        "ped_fs": 2,
        "pes_biogas_ej": 1,
        "modern_solids_bioe_demand_households": 1,
        "pe_traditional_biomass_ej_delayed_1yr": 1,
        "pes_waste_for_tfc": 1,
        "losses_in_charcoal_plants": 1,
        "pes_peat": 1,
    },
)
def ped_nre_fs():
    """
    non-renewable final sources demand
    """
    value = xr.DataArray(
        np.nan,
        {"matter_final_sources": _subscript_dict["matter_final_sources"]},
        ["matter_final_sources"],
    )
    value.loc[["liquids"]] = float(
        np.maximum(
            0,
            ped_nre_fs_liquids()
            - sum(
                synthethic_fuel_generation_delayed()
                .loc[_subscript_dict["ETL"]]
                .rename({"E_to_synthetic": "ETL!"}),
                dim=["ETL!"],
            ),
        )
    )
    value.loc[["gases"]] = (
        float(ped_fs().loc["gases"])
        - pes_biogas_ej()
        - sum(
            synthethic_fuel_generation_delayed()
            .loc[_subscript_dict["ETG"]]
            .rename({"E_to_synthetic": "ETG!"}),
            dim=["ETG!"],
        )
    )
    value.loc[["solids"]] = (
        float(ped_fs().loc["solids"])
        - pe_traditional_biomass_ej_delayed_1yr()
        - pes_waste_for_tfc()
        - modern_solids_bioe_demand_households()
        - pes_peat()
        - losses_in_charcoal_plants()
    )
    return value


@component.add(
    name="PED_NRE_FS_liquids",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_fs_liquids": 1, "fes_total_biofuels_production_ej": 1},
)
def ped_nre_fs_liquids():
    """
    Liquids demand from non-renewable sources (oil)
    """
    return ped_fs_liquids() - fes_total_biofuels_production_ej()


@component.add(
    name="PED_total_oil_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nre_fs": 1, "fes_ctlgtl_ej": 1, "oil_refinery_gains_ej": 1},
)
def ped_total_oil_ej():
    """
    Primary energy demand of total oil (conventional and unconventional).
    """
    return float(
        np.maximum(
            0,
            float(ped_nre_fs().loc["liquids"])
            - fes_ctlgtl_ej()
            - oil_refinery_gains_ej(),
        )
    )


@component.add(
    name="PES_FS",
    units="EJ/year",
    subscripts=["matter_final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pec_ff": 3,
        "pes_waste_for_tfc": 1,
        "pes_peat": 1,
        "pe_traditional_biomass_ej_delayed_1yr": 1,
        "modern_solids_bioe_demand_households": 1,
        "losses_in_charcoal_plants": 1,
        "other_liquids_supply_ej": 1,
        "pes_biogas_for_tfc": 1,
        "synthethic_fuel_generation_delayed": 1,
        "pes_biogas_ej": 1,
    },
)
def pes_fs():
    value = xr.DataArray(
        np.nan,
        {"matter_final_sources": _subscript_dict["matter_final_sources"]},
        ["matter_final_sources"],
    )
    value.loc[["solids"]] = (
        float(pec_ff().loc["solids"])
        + pes_waste_for_tfc()
        + pes_peat()
        + pe_traditional_biomass_ej_delayed_1yr()
        + modern_solids_bioe_demand_households()
        + losses_in_charcoal_plants()
    )
    value.loc[["liquids"]] = float(pec_ff().loc["liquids"]) + other_liquids_supply_ej()
    value.loc[["gases"]] = (
        float(pec_ff().loc["gases"])
        + pes_biogas_for_tfc()
        + sum(
            synthethic_fuel_generation_delayed()
            .loc[_subscript_dict["ETG"]]
            .rename({"E_to_synthetic": "ETG!"}),
            dim=["ETG!"],
        )
        + pes_biogas_ej()
    )
    return value


@component.add(
    name="PES_peat",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "a_lin_reg_peat": 1,
        "b_lin_reg_peat": 1,
        "historic_pes_peat_ej": 1,
    },
)
def pes_peat():
    return float(
        np.maximum(
            if_then_else(
                time() > 2014,
                lambda: a_lin_reg_peat() * time() + b_lin_reg_peat(),
                lambda: historic_pes_peat_ej(),
            ),
            0,
        )
    )


@component.add(
    name="real_FE_consumption_FS",
    units="EJ/year",
    subscripts=["matter_final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_fs": 1,
        "transformation_ff_losses": 1,
        "energy_distr_losses_ff": 1,
        "share_ff_for_final_energy": 1,
    },
)
def real_fe_consumption_fs():
    return (
        pes_fs()
        - transformation_ff_losses()
        .loc[_subscript_dict["matter_final_sources"]]
        .rename({"final_sources": "matter_final_sources"})
        - energy_distr_losses_ff()
        .loc[_subscript_dict["matter_final_sources"]]
        .rename({"final_sources": "matter_final_sources"})
    ) * share_ff_for_final_energy()


@component.add(
    name="share_coal_for_CTL_emissions_relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_coal_for_ctl": 1, "ped_nre_fs": 1},
)
def share_coal_for_ctl_emissions_relevant():
    return zidz(ped_coal_for_ctl(), float(ped_nre_fs().loc["solids"]))


@component.add(
    name='"share_FF_dem_for_Heat-com"',
    units="Dmnl",
    subscripts=["matter_final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_ff_for_heat_plants": 1, "ped_nre_fs": 1},
)
def share_ff_dem_for_heatcom():
    return zidz(ped_ff_for_heat_plants(), ped_nre_fs())


@component.add(
    name="share_FF_for_elec_emissions_relevant",
    units="Dmnl",
    subscripts=["matter_final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_ff_elec_plants": 1,
        "ped_ff_for_chp_plants": 1,
        "share_elec_gen_in_chp": 1,
        "ped_nre_fs": 1,
    },
)
def share_ff_for_elec_emissions_relevant():
    return zidz(
        ped_ff_elec_plants() + ped_ff_for_chp_plants() * share_elec_gen_in_chp(),
        ped_nre_fs(),
    )


@component.add(
    name="share_FF_for_electricity",
    units="Dmnl",
    subscripts=["matter_final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_ff_elec_plants": 1, "ped_nre_fs": 1},
)
def share_ff_for_electricity():
    return zidz(ped_ff_elec_plants(), ped_nre_fs())


@component.add(
    name="share_FF_for_FC_emission_relevant",
    units="Dmnl",
    subscripts=["matter_final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nonenergy_use_demand_by_final_fuel": 3,
        "ped_nre_fs": 2,
        "share_ff_for_elec_emissions_relevant": 3,
        "share_ff_for_heat_emissions_relevant": 3,
        "share_coal_for_ctl_emissions_relevant": 1,
        "ped_fs": 1,
    },
)
def share_ff_for_fc_emission_relevant():
    value = xr.DataArray(
        np.nan,
        {"matter_final_sources": _subscript_dict["matter_final_sources"]},
        ["matter_final_sources"],
    )
    value.loc[["solids"]] = (
        1
        - zidz(
            float(nonenergy_use_demand_by_final_fuel().loc["solids"]),
            float(ped_nre_fs().loc["solids"]),
        )
        - float(share_ff_for_elec_emissions_relevant().loc["solids"])
        - float(share_ff_for_heat_emissions_relevant().loc["solids"])
        - share_coal_for_ctl_emissions_relevant()
    )
    value.loc[["liquids"]] = (
        1
        - zidz(
            float(nonenergy_use_demand_by_final_fuel().loc["liquids"]),
            float(ped_nre_fs().loc["liquids"]),
        )
        - float(share_ff_for_elec_emissions_relevant().loc["liquids"])
        - float(share_ff_for_heat_emissions_relevant().loc["liquids"])
    )
    value.loc[["gases"]] = (
        1
        - zidz(
            float(nonenergy_use_demand_by_final_fuel().loc["gases"]),
            float(ped_fs().loc["gases"]),
        )
        - float(share_ff_for_elec_emissions_relevant().loc["gases"])
        - float(share_ff_for_heat_emissions_relevant().loc["gases"])
    )
    return value


@component.add(
    name="share_FF_for_final_energy",
    units="Dmnl",
    subscripts=["matter_final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_fed_by_fuel": 1,
        "energy_distr_losses_ff": 1,
        "transformation_ff_losses": 1,
        "ped_fs": 1,
    },
)
def share_ff_for_final_energy():
    return zidz(
        required_fed_by_fuel()
        .loc[_subscript_dict["matter_final_sources"]]
        .rename({"final_sources": "matter_final_sources"}),
        ped_fs()
        - transformation_ff_losses()
        .loc[_subscript_dict["matter_final_sources"]]
        .rename({"final_sources": "matter_final_sources"})
        - energy_distr_losses_ff()
        .loc[_subscript_dict["matter_final_sources"]]
        .rename({"final_sources": "matter_final_sources"}),
    )


@component.add(
    name="share_FF_for_heat_emissions_relevant",
    units="Dmnl",
    subscripts=["matter_final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_ff_for_heat_plants": 1,
        "ped_ff_heatnc": 1,
        "ped_ff_for_chp_plants": 1,
        "share_elec_gen_in_chp": 1,
        "ped_nre_fs": 1,
    },
)
def share_ff_for_heat_emissions_relevant():
    return zidz(
        ped_ff_for_heat_plants()
        + ped_ff_heatnc()
        + ped_ff_for_chp_plants() * (1 - share_elec_gen_in_chp()),
        ped_nre_fs(),
    )


@component.add(
    name='"share_FF_for_Heat-nc"',
    units="Dmnl",
    subscripts=["matter_final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_ff_heatnc": 1, "ped_nre_fs": 1},
)
def share_ff_for_heatnc():
    return zidz(ped_ff_heatnc(), ped_nre_fs())


@component.add(
    name='"share_FF_for_non-energy_use"',
    units="Dmnl",
    subscripts=["matter_final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nonenergy_use_demand_by_final_fuel": 1,
        "energy_distr_losses_ff": 1,
        "transformation_ff_losses": 1,
        "ped_fs": 1,
    },
)
def share_ff_for_nonenergy_use():
    return zidz(
        nonenergy_use_demand_by_final_fuel()
        .loc[_subscript_dict["matter_final_sources"]]
        .rename({"final_sources": "matter_final_sources"}),
        ped_fs()
        - transformation_ff_losses()
        .loc[_subscript_dict["matter_final_sources"]]
        .rename({"final_sources": "matter_final_sources"})
        - energy_distr_losses_ff()
        .loc[_subscript_dict["matter_final_sources"]]
        .rename({"final_sources": "matter_final_sources"}),
    )


@component.add(
    name="share_nat_gas_for_GTL_emissions_relevant",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ped_nat_gas_for_gtl_ej": 1, "ped_nat_gas_ej": 1},
)
def share_nat_gas_for_gtl_emissions_relevant():
    return zidz(ped_nat_gas_for_gtl_ej(), ped_nat_gas_ej())
