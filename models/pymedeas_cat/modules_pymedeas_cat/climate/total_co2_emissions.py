"""
Module total_co2_emissions
Translated using PySD version 3.2.0
"""


@component.add(name='"1 to G"', comp_type="Constant", comp_subtype="Normal")
def nvs_1_to_g():
    return 1000000000.0


@component.add(
    name="activate Affores program",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_activate_affores_program"},
)
def activate_affores_program():
    """
    1. Activated. 2. No.
    """
    return _ext_constant_activate_affores_program()


_ext_constant_activate_affores_program = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "activate_afforestation_program",
    {},
    _root,
    {},
    "_ext_constant_activate_affores_program",
)


@component.add(
    name="Adapt CO2 emissions unconv gas",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 4},
)
def adapt_co2_emissions_unconv_gas():
    """
    Unconventional gas emissions are 3,53 tCO2/toe vs 2,35 for conventional. Since we have all natural gas modeled in an aggregated manner, this function corrects these emissions assuming that unconventional gas would follow the share un relation to natural gas as estimated by [Mohr&Evans2011](BG) for 2050 and 2100 (linear interpolation).
    """
    return if_then_else(
        time() < 2050,
        lambda: 0.01 + (0.22 - 0.01) * (time() - 2000) / 50,
        lambda: if_then_else(
            time() < 2100,
            lambda: 0.22 + (0.6 - 0.22) * (time() - 2050) / 50,
            lambda: 0.6,
        ),
    )


@component.add(
    name="Adapt emissions shale oil",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 4},
)
def adapt_emissions_shale_oil():
    """
    Shale oil emissions are 6,14tCO2/toe vs 3,84 for unconventional oil. Since we have unconventional oils in an aggregated manner, this functions corrects these emissions assuming that shale oil would follow the share in relation to the total unconventional oil as estimated by [Mohr&Evans2010](Low Case) for 2050 and 2100 (linear interpolation)
    """
    return if_then_else(
        time() < 2050,
        lambda: 0.001 + (0.15 - 0.001) * (time() - 2000) / 50,
        lambda: if_then_else(
            time() < 2100,
            lambda: 0.15 + (0.72 - 0.15) * (time() - 2050) / 50,
            lambda: 0.72,
        ),
    )


@component.add(
    name="Afforestation program 2020",
    units="MtC/Year",
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
    Afforestation program from 2020 following [Nilsson 1995] (time to inverse the deforestation trend).
    """
    return _ext_data_afforestation_program_2020(time())


_ext_data_afforestation_program_2020 = ExtData(
    "../parameters.xlsx",
    "Austria",
    "time_afforestation",
    "afforestation",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_afforestation_program_2020",
)


@component.add(
    name="Afforestation program 2020 GtCO2",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "afforestation_program_2020": 1,
        "activate_affores_program": 1,
        "mt_per_gt": 1,
        "c_per_co2": 1,
    },
)
def afforestation_program_2020_gtco2():
    """
    Annual emissions captured by the afforestation program.
    """
    return (
        afforestation_program_2020()
        * activate_affores_program()
        / (c_per_co2() * mt_per_gt())
    )


@component.add(
    name="BioE CO2 emissions",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gco2_per_mj_conv_gas": 1,
        "pes_tot_biogas_for_heatcom": 1,
        "oil_liquids_saved_by_biofuels_ej": 1,
        "solid_bioe_emissions_relevant_ej": 1,
        "mj_per_ej": 1,
        "g_per_gt": 1,
    },
)
def bioe_co2_emissions():
    """
    CO2 emissions from biomass. We assume that biofuels have an emission intensity similar to natural gas (due to ILUCs, see Technical Report), and for the rest (traditional biomass, biomass for electricity and biomass for heat) we asssume that the carbon balance is null.
    """
    return (
        gco2_per_mj_conv_gas()
        * (
            oil_liquids_saved_by_biofuels_ej()
            + solid_bioe_emissions_relevant_ej()
            + pes_tot_biogas_for_heatcom()
        )
        * mj_per_ej()
        / g_per_gt()
    )


@component.add(
    name="C per CO2", units="GtC/GTCO2e", comp_type="Constant", comp_subtype="Normal"
)
def c_per_co2():
    """
    1 kg of CO2 contains 3/11 of carbon.
    """
    return 3 / 11


@component.add(
    name="Carbon emissions GtC",
    units="GtC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_co2_emissions_gtco2": 1, "c_per_co2": 1},
)
def carbon_emissions_gtc():
    """
    Total anual carbon emissions.
    """
    return total_co2_emissions_gtco2() * c_per_co2()


@component.add(
    name="CH4 emissions coal without CTL",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "consumption_ue_coal_emissions_relevant_ej": 1,
        "gch4_per_mj_coal": 1,
        "mj_per_ej": 1,
        "g_per_mt": 1,
    },
)
def ch4_emissions_coal_without_ctl():
    """
    CH4 emissions coal.
    """
    return (
        consumption_ue_coal_emissions_relevant_ej()
        * gch4_per_mj_coal()
        * mj_per_ej()
        / g_per_mt()
    )


@component.add(
    name="CH4 emissions conv gas without GTL",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pec_conv_gas": 1,
        "share_conv_vs_total_gas_extraction": 1,
        "ped_nat_gas_for_gtl_ej": 1,
        "gch4_per_mj_conv_gas": 1,
        "mj_per_ej": 1,
        "g_per_mt": 1,
    },
)
def ch4_emissions_conv_gas_without_gtl():
    """
    CH4 emissions conventional gas.
    """
    return (
        (
            pec_conv_gas()
            - ped_nat_gas_for_gtl_ej() * share_conv_vs_total_gas_extraction()
        )
        * gch4_per_mj_conv_gas()
        * mj_per_ej()
        / g_per_mt()
    )


@component.add(
    name="CH4 emissions CTL",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_coal_for_ctl": 1,
        "gch4_per_mj_ctl": 1,
        "mj_per_ej": 1,
        "g_per_mt": 1,
    },
)
def ch4_emissions_ctl():
    """
    CH4 emissions CTL.
    """
    return extraction_coal_for_ctl() * gch4_per_mj_ctl() * mj_per_ej() / g_per_mt()


@component.add(
    name="CH4 emissions GTL",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_nat_gas_for_gtl_ej": 1,
        "gch4_per_mj_gtl": 1,
        "mj_per_ej": 1,
        "g_per_mt": 1,
    },
)
def ch4_emissions_gtl():
    """
    CH4 emissions GTL.
    """
    return ped_nat_gas_for_gtl_ej() * gch4_per_mj_gtl() * mj_per_ej() / g_per_mt()


@component.add(
    name="CH4 emissions oil",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pec_total_oil": 1,
        "gch4_per_mj_oil": 1,
        "mj_per_ej": 1,
        "g_per_mt": 1,
    },
)
def ch4_emissions_oil():
    """
    CH4 emissions oil.
    """
    return pec_total_oil() * gch4_per_mj_oil() * mj_per_ej() / g_per_mt()


@component.add(
    name="CH4 emissions unconv gas",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pec_unconv_gas": 1,
        "share_conv_vs_total_gas_extraction": 1,
        "ped_nat_gas_for_gtl_ej": 1,
        "gch4_per_mj_unconv_gas": 1,
        "mj_per_ej": 1,
        "g_per_mt": 1,
    },
)
def ch4_emissions_unconv_gas():
    """
    CH4 emissions unconventional gas.
    """
    return (
        (
            pec_unconv_gas()
            - ped_nat_gas_for_gtl_ej() * (1 - share_conv_vs_total_gas_extraction())
        )
        * gch4_per_mj_unconv_gas()
        * mj_per_ej()
        / g_per_mt()
    )


@component.add(
    name="Choose GWP time frame",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_choose_gwp_time_frame"},
)
def choose_gwp_time_frame():
    return _ext_constant_choose_gwp_time_frame()


_ext_constant_choose_gwp_time_frame = ExtConstant(
    "../../scenarios/scen_cat.xlsx",
    "BAU",
    "GWP_time_frame",
    {},
    _root,
    {},
    "_ext_constant_choose_gwp_time_frame",
)


@component.add(
    name="CO2 emissions coal without CTL",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "consumption_ue_coal_emissions_relevant_ej": 1,
        "gco2_per_mj_coal": 1,
        "mj_per_ej": 1,
        "g_per_gt": 1,
    },
)
def co2_emissions_coal_without_ctl():
    """
    Emissions from coal withoug accounting for CTL-related emissions.
    """
    return (
        consumption_ue_coal_emissions_relevant_ej()
        * gco2_per_mj_coal()
        * mj_per_ej()
        / g_per_gt()
    )


@component.add(
    name="CO2 emissions conv gas without GTL",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_consumption_ue_conv_gas_emissions_relevant_ej": 1,
        "gco2_per_mj_conv_gas": 1,
        "mj_per_ej": 1,
        "g_per_gt": 1,
    },
)
def co2_emissions_conv_gas_without_gtl():
    """
    CO2 emissions from conventional gas (withouth GTL) when the gas extraction is disaggregated in conventional and unconventional resource, and CO2 emissions from total gas when the extraction is aggregated.
    """
    return (
        real_consumption_ue_conv_gas_emissions_relevant_ej()
        * gco2_per_mj_conv_gas()
        * mj_per_ej()
        / g_per_gt()
    )


@component.add(
    name="CO2 emissions conv oil",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_consumption_ue_conv_oil_emissions_relevant_ej": 1,
        "gco2_per_mj_conv_oil": 1,
        "mj_per_ej": 1,
        "g_per_gt": 1,
    },
)
def co2_emissions_conv_oil():
    """
    CO2 emissions from conventional oil.
    """
    return (
        real_consumption_ue_conv_oil_emissions_relevant_ej()
        * gco2_per_mj_conv_oil()
        * mj_per_ej()
        / g_per_gt()
    )


@component.add(
    name="CO2 emissions CTL",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gco2_per_mj_ctl": 1,
        "extraction_coal_for_ctl": 1,
        "mj_per_ej": 1,
        "g_per_gt": 1,
    },
)
def co2_emissions_ctl():
    """
    CO2 emissions associated to CTL production.
    """
    return gco2_per_mj_ctl() * extraction_coal_for_ctl() * mj_per_ej() / g_per_gt()


@component.add(
    name="CO2 emissions GTL",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_nat_gas_for_gtl_ej": 1,
        "gco2_per_mj_gtl": 1,
        "mj_per_ej": 1,
        "g_per_gt": 1,
    },
)
def co2_emissions_gtl():
    """
    CO2 emissions associated to GTL production.
    """
    return ped_nat_gas_for_gtl_ej() * gco2_per_mj_gtl() * mj_per_ej() / g_per_gt()


@component.add(
    name="CO2 emissions peat",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_peat_ej": 1,
        "gco2_per_mj_shale_oil": 1,
        "mj_per_ej": 1,
        "g_per_gt": 1,
    },
)
def co2_emissions_peat():
    """
    CO2 emissions from peat.
    """
    return pes_peat_ej() * gco2_per_mj_shale_oil() * mj_per_ej() / g_per_gt()


@component.add(
    name="CO2 emissions unconv gas",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_consumption_unconv_gas_emissions_relevant_ej": 1,
        "gco2_per_mj_unconv_gas": 1,
        "mj_per_ej": 1,
        "g_per_gt": 1,
    },
)
def co2_emissions_unconv_gas():
    """
    CO2 emissions from unconventional gas.
    """
    return (
        real_consumption_unconv_gas_emissions_relevant_ej()
        * gco2_per_mj_unconv_gas()
        * mj_per_ej()
        / g_per_gt()
    )


@component.add(
    name="CO2 emissions unconv oil",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_consumption_unconv_oil_emissions_relevant_ej": 1,
        "gco2_per_mj_shale_oil": 1,
        "adapt_emissions_shale_oil": 1,
        "gco2_per_mj_unconv_oil": 2,
        "mj_per_ej": 1,
        "g_per_gt": 1,
    },
)
def co2_emissions_unconv_oil():
    """
    CO2 emissions from unconventional oil.
    """
    return (
        (
            real_consumption_unconv_oil_emissions_relevant_ej()
            * (
                gco2_per_mj_unconv_oil()
                + (gco2_per_mj_shale_oil() - gco2_per_mj_unconv_oil())
                * adapt_emissions_shale_oil()
            )
        )
        * mj_per_ej()
        / g_per_gt()
    )


@component.add(
    name="CO2 fossil fuel emissions",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_emissions_conv_gas_without_gtl": 1,
        "co2_emissions_unconv_gas": 1,
        "co2_emissions_gtl": 1,
        "co2_emissions_conv_oil": 1,
        "co2_emissions_unconv_oil": 1,
        "co2_emissions_coal_without_ctl": 1,
        "co2_emissions_ctl": 1,
    },
)
def co2_fossil_fuel_emissions():
    """
    Total CO2 emissions from fossil fuels.
    """
    return (
        co2_emissions_conv_gas_without_gtl()
        + co2_emissions_unconv_gas()
        + co2_emissions_gtl()
        + co2_emissions_conv_oil()
        + co2_emissions_unconv_oil()
        + co2_emissions_coal_without_ctl()
        + co2_emissions_ctl()
    )


@component.add(
    name="CO2 LULCF",
    units="GtCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "past_trends_co2_lucf": 1,
        "variation_co2_landuse_change_emissions_vs_past_trends": 1,
    },
)
def co2_lulcf():
    """
    CO2 emissions from Land-Use Change and Forestry.
    """
    return past_trends_co2_lucf() * (
        1 + variation_co2_landuse_change_emissions_vs_past_trends()
    )


@component.add(
    name='"CO2 soil&LUCF emissions"',
    units="GtCO2/Year",
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
    name="Cumulative CO2e GHG emissions",
    units="GTCO2e/Year",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulative_co2e_ghg_emissions": 1},
    other_deps={
        "_integ_cumulative_co2e_ghg_emissions": {
            "initial": {},
            "step": {"total_co2e_ce": 1},
        }
    },
)
def cumulative_co2e_ghg_emissions():
    return _integ_cumulative_co2e_ghg_emissions()


_integ_cumulative_co2e_ghg_emissions = Integ(
    lambda: total_co2e_ce(), lambda: 0, "_integ_cumulative_co2e_ghg_emissions"
)


@component.add(
    name="Cumulative emissions to 1995",
    units="GtC",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_cumulative_emissions_to_1995"},
)
def cumulative_emissions_to_1995():
    """
    Cumulative emissions 1751-1995 due to carbon emissions from fossil fuel consumption, cement production and land-use changes. Data from CDIAC and World Resources Institute.
    """
    return _ext_constant_cumulative_emissions_to_1995()


_ext_constant_cumulative_emissions_to_1995 = ExtConstant(
    "../parameters.xlsx",
    "Austria",
    "cumulative_emissions_to_1995",
    {},
    _root,
    {},
    "_ext_constant_cumulative_emissions_to_1995",
)


@component.add(
    name="g per Gt", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def g_per_gt():
    """
    Unit conversion.
    """
    return 1000000000000000.0


@component.add(
    name="g per Mt", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def g_per_mt():
    """
    1e12 grams = 1 Mtonne.
    """
    return 1000000000000.0


@component.add(
    name="gCH4 per MJ coal",
    units="GtCO2/MToe",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gch4_per_mj_coal"},
)
def gch4_per_mj_coal():
    """
    CH4 emissions associated to the extraction of coal. Ref: Fig. 2 Howarth (2015).
    """
    return _ext_constant_gch4_per_mj_coal()


_ext_constant_gch4_per_mj_coal = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gch4_coal",
    {},
    _root,
    {},
    "_ext_constant_gch4_per_mj_coal",
)


@component.add(
    name="gCH4 per MJ conv gas",
    units="GtCO2/MToe",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gch4_per_mj_conv_gas"},
)
def gch4_per_mj_conv_gas():
    """
    CH4 emissions associated to the extraction of conventional gas. Ref: Fig. 2 Howarth (2015).
    """
    return _ext_constant_gch4_per_mj_conv_gas()


_ext_constant_gch4_per_mj_conv_gas = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gch4_conv_gas",
    {},
    _root,
    {},
    "_ext_constant_gch4_per_mj_conv_gas",
)


@component.add(
    name="gCH4 per MJ CTL",
    units="GtCO2/MToe",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gch4_per_mj_ctl"},
)
def gch4_per_mj_ctl():
    """
    CH4 emission factor of CTL.
    """
    return _ext_constant_gch4_per_mj_ctl()


_ext_constant_gch4_per_mj_ctl = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gch4_ctl",
    {},
    _root,
    {},
    "_ext_constant_gch4_per_mj_ctl",
)


@component.add(
    name="gCH4 per MJ GTL",
    units="GtCO2/MToe",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gch4_per_mj_gtl"},
)
def gch4_per_mj_gtl():
    """
    CH4 emission factor of GTL.
    """
    return _ext_constant_gch4_per_mj_gtl()


_ext_constant_gch4_per_mj_gtl = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gch4_gtl",
    {},
    _root,
    {},
    "_ext_constant_gch4_per_mj_gtl",
)


@component.add(
    name="gCH4 per MJ oil",
    units="GtCO2/MToe",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gch4_per_mj_oil"},
)
def gch4_per_mj_oil():
    """
    CH4 emissions associated to the extraction of oil. Ref: Fig. 2 Howarth (2015).
    """
    return _ext_constant_gch4_per_mj_oil()


_ext_constant_gch4_per_mj_oil = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gch4_oil",
    {},
    _root,
    {},
    "_ext_constant_gch4_per_mj_oil",
)


@component.add(
    name="gCH4 per MJ unconv gas",
    units="GtCO2/MToe",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gch4_per_mj_unconv_gas"},
)
def gch4_per_mj_unconv_gas():
    """
    CH4 emissions associated to the extraction of unconventional gas (shale gas). Ref: Fig. 2 Howarth (2015).
    """
    return _ext_constant_gch4_per_mj_unconv_gas()


_ext_constant_gch4_per_mj_unconv_gas = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gch4_unconventional_gas",
    {},
    _root,
    {},
    "_ext_constant_gch4_per_mj_unconv_gas",
)


@component.add(
    name="gCO2 per MJ coal",
    units="gCO2/MJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gco2_per_mj_coal"},
)
def gco2_per_mj_coal():
    """
    CO2 emission factor coal.
    """
    return _ext_constant_gco2_per_mj_coal()


_ext_constant_gco2_per_mj_coal = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_coal",
    {},
    _root,
    {},
    "_ext_constant_gco2_per_mj_coal",
)


@component.add(
    name="gCO2 per MJ conv gas",
    units="gCO2/MJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gco2_per_mj_conv_gas"},
)
def gco2_per_mj_conv_gas():
    """
    CO2 emission factor conventional natural gas.
    """
    return _ext_constant_gco2_per_mj_conv_gas()


_ext_constant_gco2_per_mj_conv_gas = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_conventional_gas",
    {},
    _root,
    {},
    "_ext_constant_gco2_per_mj_conv_gas",
)


@component.add(
    name="gCO2 per MJ conv oil",
    units="gCO2/MJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gco2_per_mj_conv_oil"},
)
def gco2_per_mj_conv_oil():
    """
    CO2 emission factor conventional oil.
    """
    return _ext_constant_gco2_per_mj_conv_oil()


_ext_constant_gco2_per_mj_conv_oil = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_conventional_oil",
    {},
    _root,
    {},
    "_ext_constant_gco2_per_mj_conv_oil",
)


@component.add(
    name="gCO2 per MJ CTL",
    units="gCO2/MJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gco2_per_mj_ctl"},
)
def gco2_per_mj_ctl():
    """
    CO2 emissions coefficient of CTL.
    """
    return _ext_constant_gco2_per_mj_ctl()


_ext_constant_gco2_per_mj_ctl = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_ctl",
    {},
    _root,
    {},
    "_ext_constant_gco2_per_mj_ctl",
)


@component.add(
    name="gCO2 per MJ GTL",
    units="gCO2/MJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gco2_per_mj_gtl"},
)
def gco2_per_mj_gtl():
    """
    CO2 emissions coefficient of GTL.
    """
    return _ext_constant_gco2_per_mj_gtl()


_ext_constant_gco2_per_mj_gtl = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_gtl",
    {},
    _root,
    {},
    "_ext_constant_gco2_per_mj_gtl",
)


@component.add(
    name="gCO2 per MJ shale oil",
    units="gCO2/MJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gco2_per_mj_shale_oil"},
)
def gco2_per_mj_shale_oil():
    """
    CO2 emission factor shale oil.
    """
    return _ext_constant_gco2_per_mj_shale_oil()


_ext_constant_gco2_per_mj_shale_oil = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_shale_oil",
    {},
    _root,
    {},
    "_ext_constant_gco2_per_mj_shale_oil",
)


@component.add(
    name="gCO2 per MJ unconv gas",
    units="gCO2/MJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gco2_per_mj_unconv_gas"},
)
def gco2_per_mj_unconv_gas():
    """
    CO2 emission factor of unconventional gas.
    """
    return _ext_constant_gco2_per_mj_unconv_gas()


_ext_constant_gco2_per_mj_unconv_gas = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_unconventional_gas",
    {},
    _root,
    {},
    "_ext_constant_gco2_per_mj_unconv_gas",
)


@component.add(
    name="gCO2 per MJ unconv oil",
    units="gCO2/MJ",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gco2_per_mj_unconv_oil"},
)
def gco2_per_mj_unconv_oil():
    """
    Emission factor unconventional oil (tar sands/extra heavy oil).
    """
    return _ext_constant_gco2_per_mj_unconv_oil()


_ext_constant_gco2_per_mj_unconv_oil = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_unconventional_oil",
    {},
    _root,
    {},
    "_ext_constant_gco2_per_mj_unconv_oil",
)


@component.add(
    name="GWP 100 year",
    subscripts=["GHGs non CO2"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gwp_100_year"},
)
def gwp_100_year():
    return _ext_constant_gwp_100_year()


_ext_constant_gwp_100_year = ExtConstant(
    "../climate.xlsx",
    "Global",
    "GWP_100_year*",
    {"GHGs non CO2": _subscript_dict["GHGs non CO2"]},
    _root,
    {"GHGs non CO2": _subscript_dict["GHGs non CO2"]},
    "_ext_constant_gwp_100_year",
)


@component.add(
    name="GWP 20 year",
    subscripts=["GHGs non CO2"],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_gwp_20_year"},
)
def gwp_20_year():
    return _ext_constant_gwp_20_year()


_ext_constant_gwp_20_year = ExtConstant(
    "../climate.xlsx",
    "Global",
    "GWP_20_year*",
    {"GHGs non CO2": _subscript_dict["GHGs non CO2"]},
    _root,
    {"GHGs non CO2": _subscript_dict["GHGs non CO2"]},
    "_ext_constant_gwp_20_year",
)


@component.add(name="Mt per Gt", comp_type="Constant", comp_subtype="Normal")
def mt_per_gt():
    """
    Conversion from Mega to Giga (1000 M = 1 G).
    """
    return 1000


@component.add(
    name="new C GtC",
    units="GtC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"carbon_emissions_gtc": 1},
)
def new_c_gtc():
    """
    Annual carbon emissions.
    """
    return carbon_emissions_gtc()


@component.add(
    name="Past trends CO2 LUCF",
    units="GtCO2",
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
    "../land.xlsx",
    "Austria",
    "time",
    "historic_co2_emissions_from_land_use_change_and_forestry",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_past_trends_co2_lucf",
)


@component.add(
    name="Total CH4 emissions fossil fuels",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ch4_emissions_conv_gas_without_gtl": 1,
        "ch4_emissions_unconv_gas": 1,
        "ch4_emissions_coal_without_ctl": 1,
        "ch4_emissions_oil": 1,
        "ch4_emissions_ctl": 1,
        "ch4_emissions_gtl": 1,
    },
)
def total_ch4_emissions_fossil_fuels():
    """
    Total CH4 emissions from fossil fuels.
    """
    return (
        ch4_emissions_conv_gas_without_gtl()
        + ch4_emissions_unconv_gas()
        + ch4_emissions_coal_without_ctl()
        + ch4_emissions_oil()
        + ch4_emissions_ctl()
        + ch4_emissions_gtl()
    )


@component.add(
    name="Total CO2 emissions from fossil fuel consumption and cement production",
    units="GtCO2/Year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_total_co2_emissions_from_fossil_fuel_consumption_and_cement_production",
        "__data__": "_ext_data_total_co2_emissions_from_fossil_fuel_consumption_and_cement_production",
        "time": 1,
    },
)
def total_co2_emissions_from_fossil_fuel_consumption_and_cement_production():
    """
    Total CO2 emissions from fossil fuel consumption and cement production (CDIAC).
    """
    return _ext_data_total_co2_emissions_from_fossil_fuel_consumption_and_cement_production(
        time()
    )


_ext_data_total_co2_emissions_from_fossil_fuel_consumption_and_cement_production = ExtData(
    "../climate.xlsx",
    "Austria",
    "time_emissions",
    "historic_co2_emissions_from_fossils_and_cement",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_total_co2_emissions_from_fossil_fuel_consumption_and_cement_production",
)


@component.add(
    name="Total CO2 emissions GTCO2",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_fossil_fuel_emissions": 1,
        "co2_soillucf_emissions": 1,
        "bioe_co2_emissions": 1,
        "co2_emissions_peat": 1,
        "afforestation_program_2020_gtco2": 1,
    },
)
def total_co2_emissions_gtco2():
    """
    Total annual CO2 emissions. Original unit: "mill Tn CO2"
    """
    return (
        co2_fossil_fuel_emissions()
        + co2_soillucf_emissions()
        + bioe_co2_emissions()
        + co2_emissions_peat()
        - afforestation_program_2020_gtco2()
    )


@component.add(
    name="Total CO2e",
    units="GtCO2\u200de/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_co2_emissions_gtco2": 1,
        "mt_per_gt": 2,
        "ch4_anthro_emissions": 1,
        "gwp_20_year": 13,
        "gwp_100_year": 13,
        "choose_gwp_time_frame": 13,
        "n2o_anthro_emissions": 1,
        "pfc_emissions": 1,
        "nvs_1_to_g": 11,
        "sf6_emissions": 1,
        "hfc_emissions": 9,
    },
)
def total_co2e():
    return (
        total_co2_emissions_gtco2()
        + ch4_anthro_emissions()
        * if_then_else(
            choose_gwp_time_frame() == 1,
            lambda: float(gwp_20_year().loc["CH4"]),
            lambda: float(gwp_100_year().loc["CH4"]),
        )
        / mt_per_gt()
        + n2o_anthro_emissions()
        * if_then_else(
            choose_gwp_time_frame() == 1,
            lambda: float(gwp_20_year().loc["N2O"]),
            lambda: float(gwp_100_year().loc["N2O"]),
        )
        / mt_per_gt()
        + pfc_emissions()
        * if_then_else(
            choose_gwp_time_frame() == 1,
            lambda: float(gwp_20_year().loc["PFCs"]),
            lambda: float(gwp_100_year().loc["PFCs"]),
        )
        / nvs_1_to_g()
        + sf6_emissions()
        * if_then_else(
            choose_gwp_time_frame() == 1,
            lambda: float(gwp_20_year().loc["SF6"]),
            lambda: float(gwp_100_year().loc["SF6"]),
        )
        / nvs_1_to_g()
        + float(hfc_emissions().loc["HFC134a"])
        * if_then_else(
            choose_gwp_time_frame() == 1,
            lambda: float(gwp_20_year().loc["HFC134a"]),
            lambda: float(gwp_100_year().loc["HFC134a"]),
        )
        / nvs_1_to_g()
        + float(hfc_emissions().loc["HFC23"])
        * if_then_else(
            choose_gwp_time_frame() == 1,
            lambda: float(gwp_20_year().loc["HFC23"]),
            lambda: float(gwp_100_year().loc["HFC23"]),
        )
        / nvs_1_to_g()
        + float(hfc_emissions().loc["HFC32"])
        * if_then_else(
            choose_gwp_time_frame() == 1,
            lambda: float(gwp_20_year().loc["HFC32"]),
            lambda: float(gwp_100_year().loc["HFC32"]),
        )
        / nvs_1_to_g()
        + float(hfc_emissions().loc["HFC125"])
        * if_then_else(
            choose_gwp_time_frame() == 1,
            lambda: float(gwp_20_year().loc["HFC125"]),
            lambda: float(gwp_100_year().loc["HFC125"]),
        )
        / nvs_1_to_g()
        + float(hfc_emissions().loc["HFC143a"])
        * if_then_else(
            choose_gwp_time_frame() == 1,
            lambda: float(gwp_20_year().loc["HFC143a"]),
            lambda: float(gwp_100_year().loc["HFC143a"]),
        )
        / nvs_1_to_g()
        + float(hfc_emissions().loc["HFC152a"])
        * if_then_else(
            choose_gwp_time_frame() == 1,
            lambda: float(gwp_20_year().loc["HFC152a"]),
            lambda: float(gwp_100_year().loc["HFC152a"]),
        )
        / nvs_1_to_g()
        + float(hfc_emissions().loc["HFC227ea"])
        * if_then_else(
            choose_gwp_time_frame() == 1,
            lambda: float(gwp_20_year().loc["HFC227ea"]),
            lambda: float(gwp_100_year().loc["HFC227ea"]),
        )
        / nvs_1_to_g()
        + float(hfc_emissions().loc["HFC245ca"])
        * if_then_else(
            choose_gwp_time_frame() == 1,
            lambda: float(gwp_20_year().loc["HFC245ca"]),
            lambda: float(gwp_100_year().loc["HFC245ca"]),
        )
        / nvs_1_to_g()
        + float(hfc_emissions().loc["HFC4310mee"])
        * if_then_else(
            choose_gwp_time_frame() == 1,
            lambda: float(gwp_20_year().loc["HFC4310mee"]),
            lambda: float(gwp_100_year().loc["HFC4310mee"]),
        )
        / nvs_1_to_g()
    )


@component.add(
    name="Total CO2e Ce",
    units="GTCe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_co2e": 1, "c_per_co2": 1},
)
def total_co2e_ce():
    return total_co2e() * c_per_co2()


@component.add(
    name="Total cumulative emissions GtC",
    units="GtC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_total_cumulative_emissions_gtc": 1},
    other_deps={
        "_integ_total_cumulative_emissions_gtc": {
            "initial": {"cumulative_emissions_to_1995": 1},
            "step": {"new_c_gtc": 1},
        }
    },
)
def total_cumulative_emissions_gtc():
    """
    Total cumulative emissions.
    """
    return _integ_total_cumulative_emissions_gtc()


_integ_total_cumulative_emissions_gtc = Integ(
    lambda: new_c_gtc(),
    lambda: cumulative_emissions_to_1995(),
    "_integ_total_cumulative_emissions_gtc",
)


@component.add(
    name="Total cumulative emissions GtCO2",
    units="GtCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_cumulative_emissions_gtc": 1, "c_per_co2": 1},
)
def total_cumulative_emissions_gtco2():
    """
    Total cumulative emissions.
    """
    return total_cumulative_emissions_gtc() / c_per_co2()


@component.add(
    name='"Total GHG Emissions Excluding Land-Use Change and Forestry"',
    units="GTCO2e/Year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_total_ghg_emissions_excluding_landuse_change_and_forestry",
        "__data__": "_ext_data_total_ghg_emissions_excluding_landuse_change_and_forestry",
        "time": 1,
    },
)
def total_ghg_emissions_excluding_landuse_change_and_forestry():
    """
    Total GHG Emissions Excluding Land-Use Change and Forestry (CDIAC).
    """
    return _ext_data_total_ghg_emissions_excluding_landuse_change_and_forestry(time())


_ext_data_total_ghg_emissions_excluding_landuse_change_and_forestry = ExtData(
    "../climate.xlsx",
    "Austria",
    "time_emissions",
    "historic_total_ghg_emissions_excluding_land_use_changes_and_forestry",
    None,
    {},
    _root,
    {},
    "_ext_data_total_ghg_emissions_excluding_landuse_change_and_forestry",
)


@component.add(
    name='"Total GHG Emissions Including Land-Use Change and Forestry"',
    units="GtCO2\u200de/Year",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_total_ghg_emissions_including_landuse_change_and_forestry",
        "__data__": "_ext_data_total_ghg_emissions_including_landuse_change_and_forestry",
        "time": 1,
    },
)
def total_ghg_emissions_including_landuse_change_and_forestry():
    """
    Total GHG Emissions Including Land-Use Change and Forestry (CDIAC).
    """
    return _ext_data_total_ghg_emissions_including_landuse_change_and_forestry(time())


_ext_data_total_ghg_emissions_including_landuse_change_and_forestry = ExtData(
    "../climate.xlsx",
    "Austria",
    "time_emissions",
    "historic_total_ghg_emissions_including_land_use_changes_and_forestry",
    None,
    {},
    _root,
    {},
    "_ext_data_total_ghg_emissions_including_landuse_change_and_forestry",
)


@component.add(
    name='"variation CO2 land-use change emissions vs past trends"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def variation_co2_landuse_change_emissions_vs_past_trends():
    return 0
