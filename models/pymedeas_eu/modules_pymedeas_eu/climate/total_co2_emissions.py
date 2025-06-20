"""
Module climate.total_co2_emissions
Translated using PySD version 3.14.2
"""

@component.add(
    name="activate_Affores_program",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_activate_affores_program"},
)
def activate_affores_program():
    """
    0. Deactivated. 1. Activated.
    """
    return _ext_constant_activate_affores_program()


_ext_constant_activate_affores_program = ExtConstant(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "activate_afforestation_program",
    {},
    _root,
    {},
    "_ext_constant_activate_affores_program",
)


@component.add(
    name="Adapt_emissions_shale_oil",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 4, "nvs_50_years_ts": 2},
)
def adapt_emissions_shale_oil():
    return if_then_else(
        time() < 2050,
        lambda: 0.001 + (0.15 - 0.001) * (time() - 2000) / nvs_50_years_ts(),
        lambda: if_then_else(
            time() < 2100,
            lambda: 0.15 + (0.72 - 0.15) * (time() - 2050) / nvs_50_years_ts(),
            lambda: 0.72,
        ),
    )


@component.add(
    name="Afforestation_program_2020",
    units="MtC/year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_afforestation_program_2020",
        "__data__": "_ext_data_afforestation_program_2020",
        "time": 1,
    },
)
def afforestation_program_2020():
    """
    Afforestation program from 2024
    """
    return _ext_data_afforestation_program_2020(time())


_ext_data_afforestation_program_2020 = ExtData(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "time_afforestation",
    "afforestation",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_afforestation_program_2020",
)


@component.add(
    name="Afforestation_program_2020_GtCO2",
    units="GtCO2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "afforestation_program_2020": 1,
        "activate_affores_program": 1,
        "mtc_per_gtc": 1,
    },
)
def afforestation_program_2020_gtco2():
    """
    Annual emissions captured by the afforestation program.
    """
    return afforestation_program_2020() * activate_affores_program() / mtc_per_gtc()


@component.add(
    name="Aux_total_CO2_emissions_GTCO2",
    units="GtCO2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_emissions_per_fuel": 1},
)
def aux_total_co2_emissions_gtco2():
    """
    Auxiliary variable to allocate the total annual CO2 emission. Then CCS captured CO2 is substracted to each sector
    """
    return sum(
        co2_emissions_per_fuel().rename({"final_sources": "final_sources!"}),
        dim=["final_sources!"],
    )


@component.add(
    name="CO2_emissions_BioE_and_Waste",
    units="GtCO2/year",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_emissions_biofuels": 1,
        "co2_emissions_biogas": 1,
        "co2_emissions_biomass": 1,
        "co2_emissions_solid_bioe": 1,
        "co2_emissions_waste": 1,
    },
)
def co2_emissions_bioe_and_waste():
    """
    CO2 emissions biofuels[final sources]+CO2 emissions biogas[final sources]+CO2 emissions biomass[final sources]+CO2 emissions solid bioE[final sources]+CO2 emissions waste[final sources]
    """
    return (
        co2_emissions_biofuels()
        + co2_emissions_biogas()
        + co2_emissions_biomass()
        + co2_emissions_solid_bioe()
        + co2_emissions_waste()
    )


@component.add(
    name="CO2_emissions_biofuels",
    units="GtCO2/year",
    subscripts=["final_sources"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={"gtco2_per_ej_biofuels": 1, "oil_liquids_saved_by_biofuels_ej": 1},
)
def co2_emissions_biofuels():
    value = xr.DataArray(
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    except_subs = xr.ones_like(value, dtype=bool)
    except_subs.loc[["liquids"]] = False
    value.values[except_subs.values] = 0
    value.loc[["liquids"]] = (
        gtco2_per_ej_biofuels() * oil_liquids_saved_by_biofuels_ej()
    )
    return value


@component.add(
    name="CO2_emissions_biogas",
    units="GtCO2/year",
    subscripts=["final_sources"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gtco2_per_ej_biogas": 3,
        "pes_tot_biogas_for_elec": 1,
        "pes_tot_biogas_for_heatcom": 1,
        "pes_biogas_for_tfc": 1,
    },
)
def co2_emissions_biogas():
    value = xr.DataArray(
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    value.loc[["electricity"]] = gtco2_per_ej_biogas() * pes_tot_biogas_for_elec()
    value.loc[["heat"]] = gtco2_per_ej_biogas() * pes_tot_biogas_for_heatcom()
    value.loc[["liquids"]] = 0
    value.loc[["gases"]] = gtco2_per_ej_biogas() * pes_biogas_for_tfc()
    value.loc[["solids"]] = 0
    return value


@component.add(
    name="CO2_emissions_biomass",
    units="GtCO2/year",
    subscripts=["final_sources"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gtco2_per_ej_traditional_biomass": 1,
        "pe_traditional_biomass_consum_ej": 1,
    },
)
def co2_emissions_biomass():
    value = xr.DataArray(
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    except_subs = xr.ones_like(value, dtype=bool)
    except_subs.loc[["solids"]] = False
    value.values[except_subs.values] = 0
    value.loc[["solids"]] = (
        gtco2_per_ej_traditional_biomass() * pe_traditional_biomass_consum_ej()
    )
    return value


@component.add(
    name="CO2_emissions_coal",
    units="GtCO2/year",
    subscripts=["final_sources"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gtco2_per_ej_coal": 3,
        "pec_ff": 4,
        "share_ff_for_elec_emissions_relevant": 1,
        "share_ff_for_heat_emissions_relevant": 1,
        "share_coal_for_ctl_emissions_relevant": 1,
        "gtco2_per_ej_ctl": 1,
        "share_ff_for_fc_emission_relevant": 1,
    },
)
def co2_emissions_coal():
    value = xr.DataArray(
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    value.loc[["electricity"]] = (
        gtco2_per_ej_coal()
        * float(pec_ff().loc["solids"])
        * float(share_ff_for_elec_emissions_relevant().loc["solids"])
    )
    value.loc[["heat"]] = (
        gtco2_per_ej_coal()
        * float(pec_ff().loc["solids"])
        * float(share_ff_for_heat_emissions_relevant().loc["solids"])
    )
    value.loc[["liquids"]] = (
        gtco2_per_ej_ctl()
        * float(pec_ff().loc["solids"])
        * share_coal_for_ctl_emissions_relevant()
    )
    value.loc[["gases"]] = 0
    value.loc[["solids"]] = (
        gtco2_per_ej_coal()
        * float(pec_ff().loc["solids"])
        * float(share_ff_for_fc_emission_relevant().loc["solids"])
    )
    return value


@component.add(
    name="CO2_emissions_fossil_fuels",
    units="GtCO2/year",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_emissions_oil": 1,
        "co2_emissions_gas": 1,
        "co2_emissions_coal": 1,
        "co2_emissions_peat": 1,
    },
)
def co2_emissions_fossil_fuels():
    return (
        co2_emissions_oil()
        + co2_emissions_gas()
        + co2_emissions_coal()
        + co2_emissions_peat()
    )


@component.add(
    name="CO2_emissions_gas",
    units="GtCO2/year",
    subscripts=["final_sources"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gtco2_per_ej_gas": 3,
        "pec_ff": 4,
        "share_ff_for_elec_emissions_relevant": 1,
        "share_ff_for_heat_emissions_relevant": 1,
        "gtco2_per_ej_gtl": 1,
        "share_nat_gas_for_gtl_emissions_relevant": 1,
        "share_ff_for_fc_emission_relevant": 1,
    },
)
def co2_emissions_gas():
    value = xr.DataArray(
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    value.loc[["electricity"]] = (
        gtco2_per_ej_gas()
        * float(pec_ff().loc["gases"])
        * float(share_ff_for_elec_emissions_relevant().loc["gases"])
    )
    value.loc[["heat"]] = (
        gtco2_per_ej_gas()
        * float(pec_ff().loc["gases"])
        * float(share_ff_for_heat_emissions_relevant().loc["gases"])
    )
    value.loc[["liquids"]] = (
        gtco2_per_ej_gtl()
        * float(pec_ff().loc["gases"])
        * share_nat_gas_for_gtl_emissions_relevant()
    )
    value.loc[["gases"]] = (
        gtco2_per_ej_gas()
        * float(pec_ff().loc["gases"])
        * float(share_ff_for_fc_emission_relevant().loc["gases"])
    )
    value.loc[["solids"]] = 0
    return value


@component.add(
    name="CO2_emissions_oil",
    units="GtCO2/year",
    subscripts=["final_sources"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gtco2_per_ej_oil": 3,
        "pec_ff": 3,
        "share_ff_for_elec_emissions_relevant": 1,
        "share_ff_for_heat_emissions_relevant": 1,
        "share_ff_for_fc_emission_relevant": 1,
    },
)
def co2_emissions_oil():
    value = xr.DataArray(
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    value.loc[["electricity"]] = (
        gtco2_per_ej_oil()
        * float(pec_ff().loc["liquids"])
        * float(share_ff_for_elec_emissions_relevant().loc["liquids"])
    )
    value.loc[["heat"]] = (
        gtco2_per_ej_oil()
        * float(pec_ff().loc["liquids"])
        * float(share_ff_for_heat_emissions_relevant().loc["liquids"])
    )
    value.loc[["liquids"]] = (
        gtco2_per_ej_oil()
        * float(pec_ff().loc["liquids"])
        * float(share_ff_for_fc_emission_relevant().loc["liquids"])
    )
    value.loc[["gases"]] = 0
    value.loc[["solids"]] = 0
    return value


@component.add(
    name="CO2_emissions_peat",
    units="GtCO2/year",
    subscripts=["final_sources"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={"pes_peat": 1, "gtco2_per_ej_peat": 1},
)
def co2_emissions_peat():
    """
    CO2 emissions from peat.
    """
    value = xr.DataArray(
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    except_subs = xr.ones_like(value, dtype=bool)
    except_subs.loc[["solids"]] = False
    value.values[except_subs.values] = 0
    value.loc[["solids"]] = pes_peat() * gtco2_per_ej_peat()
    return value


@component.add(
    name="CO2_emissions_per_fuel",
    units="GtCO2/year",
    subscripts=["final_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_emissions_fossil_fuels": 1, "co2_emissions_bioe_and_waste": 1},
)
def co2_emissions_per_fuel():
    """
    Total CO2 emissions per each fuel type.
    """
    return co2_emissions_fossil_fuels() + co2_emissions_bioe_and_waste()


@component.add(
    name="CO2_emissions_solid_bioE",
    units="GtCO2/year",
    subscripts=["final_sources"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gtco2_per_ej_solid_bioe": 3,
        "pe_real_generation_res_elec": 1,
        "pes_res_for_heatcom_by_techn": 1,
        "pes_res_for_heatnc_by_techn": 1,
        "modern_bioe_in_households": 1,
    },
)
def co2_emissions_solid_bioe():
    value = xr.DataArray(
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    value.loc[["electricity"]] = gtco2_per_ej_solid_bioe() * float(
        pe_real_generation_res_elec().loc["solid_bioE_elec"]
    )
    value.loc[["heat"]] = gtco2_per_ej_solid_bioe() * (
        float(pes_res_for_heatcom_by_techn().loc["solid_bioE_heat"])
        + float(pes_res_for_heatnc_by_techn().loc["solid_bioE_heat"])
    )
    value.loc[["liquids"]] = 0
    value.loc[["gases"]] = 0
    value.loc[["solids"]] = gtco2_per_ej_solid_bioe() * modern_bioe_in_households()
    return value


@component.add(
    name="CO2_emissions_waste",
    units="GtCO2/year",
    subscripts=["final_sources"],
    comp_type="Constant, Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gtco2_per_ej_waste": 3,
        "pes_tot_waste_for_elec": 1,
        "pes_tot_waste_for_heatcom": 1,
        "pes_waste_for_tfc": 1,
    },
)
def co2_emissions_waste():
    value = xr.DataArray(
        np.nan, {"final_sources": _subscript_dict["final_sources"]}, ["final_sources"]
    )
    value.loc[["electricity"]] = gtco2_per_ej_waste() * pes_tot_waste_for_elec()
    value.loc[["heat"]] = gtco2_per_ej_waste() * pes_tot_waste_for_heatcom()
    value.loc[["liquids"]] = 0
    value.loc[["gases"]] = 0
    value.loc[["solids"]] = gtco2_per_ej_waste() * pes_waste_for_tfc()
    return value


@component.add(
    name='"CO2_land-use_change_emissions_exogenous"',
    units="GtCO2/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_co2_landuse_change_emissions_exogenous",
        "__lookup__": "_ext_lookup_co2_landuse_change_emissions_exogenous",
    },
)
def co2_landuse_change_emissions_exogenous(x, final_subs=None):
    return _ext_lookup_co2_landuse_change_emissions_exogenous(x, final_subs)


_ext_lookup_co2_landuse_change_emissions_exogenous = ExtLookup(
    r"../../scenarios/scen_eu.xlsx",
    "NZP",
    "years_co2_luc",
    "co2_luc",
    {},
    _root,
    {},
    "_ext_lookup_co2_landuse_change_emissions_exogenous",
)


@component.add(
    name="CO2_LULCF",
    units="GtCO2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 5,
        "past_trends_co2_lucf": 3,
        "co2_landuse_change_emissions_exogenous": 2,
    },
)
def co2_lulcf():
    """
    CO2 emissions from Land-Use Change and Forestry.
    """
    return if_then_else(
        time() < 2015,
        lambda: past_trends_co2_lucf(),
        lambda: if_then_else(
            time() < 2020,
            lambda: past_trends_co2_lucf()
            + (co2_landuse_change_emissions_exogenous(time()) - past_trends_co2_lucf())
            / 5
            * (time() - 2015),
            lambda: co2_landuse_change_emissions_exogenous(time()),
        ),
    )


@component.add(
    name='"CO2_soil&LUCF_emissions"',
    units="GtCO2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_lulcf": 1},
)
def co2_soillucf_emissions():
    """
    CO2 emissions associated to soil managemente and land-use change uses and forestry.
    """
    return co2_lulcf()


@component.add(
    name="GtC_per_GtCO2", units="GtC/GtCO2", comp_type="Constant", comp_subtype="Normal"
)
def gtc_per_gtco2():
    """
    1 kg of CO2 contains 3/11 of carbon.
    """
    return 3 / 11


@component.add(
    name="GtCO2_per_EJ_biofuels",
    units="GtCO2/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gtco2_per_ej_biofuels"},
)
def gtco2_per_ej_biofuels():
    return _ext_constant_gtco2_per_ej_biofuels()


_ext_constant_gtco2_per_ej_biofuels = ExtConstant(
    r"../climate.xlsx",
    "Global",
    "co2_biofuels",
    {},
    _root,
    {},
    "_ext_constant_gtco2_per_ej_biofuels",
)


@component.add(
    name="GtCO2_per_EJ_biogas",
    units="GtCO2/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gtco2_per_ej_biogas"},
)
def gtco2_per_ej_biogas():
    return _ext_constant_gtco2_per_ej_biogas()


_ext_constant_gtco2_per_ej_biogas = ExtConstant(
    r"../climate.xlsx",
    "Global",
    "co2_biogas",
    {},
    _root,
    {},
    "_ext_constant_gtco2_per_ej_biogas",
)


@component.add(
    name="GtCO2_per_EJ_coal",
    units="GtCO2/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gtco2_per_ej_coal"},
)
def gtco2_per_ej_coal():
    return _ext_constant_gtco2_per_ej_coal()


_ext_constant_gtco2_per_ej_coal = ExtConstant(
    r"../climate.xlsx",
    "Global",
    "co2_coal",
    {},
    _root,
    {},
    "_ext_constant_gtco2_per_ej_coal",
)


@component.add(
    name="GtCO2_per_EJ_conv_gas",
    units="GtCO2/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gtco2_per_ej_conv_gas"},
)
def gtco2_per_ej_conv_gas():
    return _ext_constant_gtco2_per_ej_conv_gas()


_ext_constant_gtco2_per_ej_conv_gas = ExtConstant(
    r"../climate.xlsx",
    "Global",
    "co2_conv_gas",
    {},
    _root,
    {},
    "_ext_constant_gtco2_per_ej_conv_gas",
)


@component.add(
    name="GtCO2_per_EJ_conv_oil",
    units="GtCO2/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gtco2_per_ej_conv_oil"},
)
def gtco2_per_ej_conv_oil():
    return _ext_constant_gtco2_per_ej_conv_oil()


_ext_constant_gtco2_per_ej_conv_oil = ExtConstant(
    r"../climate.xlsx",
    "Global",
    "co2_conv_oil",
    {},
    _root,
    {},
    "_ext_constant_gtco2_per_ej_conv_oil",
)


@component.add(
    name="GtCO2_per_EJ_CTL",
    units="GtCO2/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gtco2_per_ej_ctl"},
)
def gtco2_per_ej_ctl():
    return _ext_constant_gtco2_per_ej_ctl()


_ext_constant_gtco2_per_ej_ctl = ExtConstant(
    r"../climate.xlsx",
    "Global",
    "co2_ctl",
    {},
    _root,
    {},
    "_ext_constant_gtco2_per_ej_ctl",
)


@component.add(
    name="GtCO2_per_EJ_gas",
    units="GtCO2/EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_conv_vs_total_gas_extraction": 2,
        "gtco2_per_ej_conv_gas": 1,
        "gtco2_per_ej_unconv_gas": 1,
    },
)
def gtco2_per_ej_gas():
    return (
        share_conv_vs_total_gas_extraction() * gtco2_per_ej_conv_gas()
        + (1 - share_conv_vs_total_gas_extraction()) * gtco2_per_ej_unconv_gas()
    )


@component.add(
    name="GtCO2_per_EJ_GTL",
    units="GtCO2/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gtco2_per_ej_gtl"},
)
def gtco2_per_ej_gtl():
    return _ext_constant_gtco2_per_ej_gtl()


_ext_constant_gtco2_per_ej_gtl = ExtConstant(
    r"../climate.xlsx",
    "Global",
    "co2_gtl",
    {},
    _root,
    {},
    "_ext_constant_gtco2_per_ej_gtl",
)


@component.add(
    name="GtCO2_per_EJ_oil",
    units="GtCO2/EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_conv_vs_total_oil_extraction": 2,
        "gtco2_per_ej_conv_oil": 1,
        "adapt_emissions_shale_oil": 1,
        "gtco2_per_ej_unconv_oil": 2,
        "gtco2_per_ej_shale_oil": 1,
    },
)
def gtco2_per_ej_oil():
    return share_conv_vs_total_oil_extraction() * gtco2_per_ej_conv_oil() + (
        1 - share_conv_vs_total_oil_extraction()
    ) * (
        gtco2_per_ej_unconv_oil()
        + (gtco2_per_ej_shale_oil() - gtco2_per_ej_unconv_oil())
        * adapt_emissions_shale_oil()
    )


@component.add(
    name="GtCO2_per_EJ_peat",
    units="GtCO2/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gtco2_per_ej_peat"},
)
def gtco2_per_ej_peat():
    return _ext_constant_gtco2_per_ej_peat()


_ext_constant_gtco2_per_ej_peat = ExtConstant(
    r"../climate.xlsx",
    "Global",
    "co2_peat",
    {},
    _root,
    {},
    "_ext_constant_gtco2_per_ej_peat",
)


@component.add(
    name="GtCO2_per_EJ_shale_oil",
    units="GtCO2/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gtco2_per_ej_shale_oil"},
)
def gtco2_per_ej_shale_oil():
    return _ext_constant_gtco2_per_ej_shale_oil()


_ext_constant_gtco2_per_ej_shale_oil = ExtConstant(
    r"../climate.xlsx",
    "Global",
    "co2_shale_oil",
    {},
    _root,
    {},
    "_ext_constant_gtco2_per_ej_shale_oil",
)


@component.add(
    name="GtCO2_per_EJ_solid_BioE",
    units="GtCO2/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gtco2_per_ej_solid_bioe"},
)
def gtco2_per_ej_solid_bioe():
    return _ext_constant_gtco2_per_ej_solid_bioe()


_ext_constant_gtco2_per_ej_solid_bioe = ExtConstant(
    r"../climate.xlsx",
    "Global",
    "co2_solid_bioe",
    {},
    _root,
    {},
    "_ext_constant_gtco2_per_ej_solid_bioe",
)


@component.add(
    name="GtCO2_per_EJ_traditional_biomass",
    units="GtCO2/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gtco2_per_ej_traditional_biomass"},
)
def gtco2_per_ej_traditional_biomass():
    return _ext_constant_gtco2_per_ej_traditional_biomass()


_ext_constant_gtco2_per_ej_traditional_biomass = ExtConstant(
    r"../climate.xlsx",
    "Global",
    "co2_traditional_biomass",
    {},
    _root,
    {},
    "_ext_constant_gtco2_per_ej_traditional_biomass",
)


@component.add(
    name="GtCO2_per_EJ_unconv_gas",
    units="GtCO2/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gtco2_per_ej_unconv_gas"},
)
def gtco2_per_ej_unconv_gas():
    return _ext_constant_gtco2_per_ej_unconv_gas()


_ext_constant_gtco2_per_ej_unconv_gas = ExtConstant(
    r"../climate.xlsx",
    "Global",
    "co2_unconv_gas",
    {},
    _root,
    {},
    "_ext_constant_gtco2_per_ej_unconv_gas",
)


@component.add(
    name="GtCO2_per_EJ_unconv_oil",
    units="GtCO2/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gtco2_per_ej_unconv_oil"},
)
def gtco2_per_ej_unconv_oil():
    return _ext_constant_gtco2_per_ej_unconv_oil()


_ext_constant_gtco2_per_ej_unconv_oil = ExtConstant(
    r"../climate.xlsx",
    "Global",
    "co2_unconv_oil",
    {},
    _root,
    {},
    "_ext_constant_gtco2_per_ej_unconv_oil",
)


@component.add(
    name="GtCO2_per_EJ_waste",
    units="GtCO2/EJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gtco2_per_ej_waste"},
)
def gtco2_per_ej_waste():
    return _ext_constant_gtco2_per_ej_waste()


_ext_constant_gtco2_per_ej_waste = ExtConstant(
    r"../climate.xlsx",
    "Global",
    "co2_waste",
    {},
    _root,
    {},
    "_ext_constant_gtco2_per_ej_waste",
)


@component.add(
    name="MtC_per_GtC", units="MtC/GtC", comp_type="Constant", comp_subtype="Normal"
)
def mtc_per_gtc():
    return 1000


@component.add(
    name='"50_years_TS"', units="year", comp_type="Constant", comp_subtype="Normal"
)
def nvs_50_years_ts():
    return 50


@component.add(
    name="Past_trends_CO2_LUCF",
    units="GtCO2/year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_past_trends_co2_lucf",
        "__data__": "_ext_data_past_trends_co2_lucf",
        "time": 1,
    },
)
def past_trends_co2_lucf():
    """
    Historic CO2 emissions from Land-Use Change and Forestry.
    """
    return _ext_data_past_trends_co2_lucf(time())


_ext_data_past_trends_co2_lucf = ExtData(
    r"../land.xlsx",
    "Europe",
    "time",
    "historic_co2_emissions_from_land_use_change_and_forestry",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_past_trends_co2_lucf",
)
