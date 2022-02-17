"""
Module total_ghg_emissions
Translated using PySD version 2.2.1
"""


def activate_afforestation_program():
    """
    Real Name: activate afforestation program
    Original Eqn: GET DIRECT CONSTANTS('../../scenarios/scen_w.xlsx', 'BAU', 'afforestation_program')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    1. Activated.        2. No.
    """
    return _ext_constant_activate_afforestation_program()


def adapt_co2_emissions_unconv_gas():
    """
    Real Name: Adapt CO2 emissions unconv gas
    Original Eqn: IF THEN ELSE( Time<2050, 0.01+(0.22-0.01)*(Time-2000)/50, IF THEN ELSE( Time<2100, 0.22+(0.6-0.22)*(Time-2050)/50, 0.6))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Unconventional gas emissions are 3,53 tCO2/toe vs 2,35 for conventional.
        Since we have all natural gas modeled in an aggregated manner, this
        function corrects these emissions assuming that unconventional gas would
        follow the share un relation to natural gas as estimated by
        [Mohr&Evans2011](BG) for 2050 and 2100 (linear interpolation).
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


def adapt_emissions_shale_oil():
    """
    Real Name: Adapt emissions shale oil
    Original Eqn: IF THEN ELSE(Time<2050, 0.001+(0.15-0.001)*(Time-2000)/50, IF THEN ELSE( Time<2100, 0.15+(0.72-0.15)*(Time-2050)/50, 0.72))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Shale oil emissions are 6,14tCO2/toe vs 3,84 for unconventional oil. Since
        we have unconventional oils in an aggregated manner, this functions
        corrects these emissions assuming that shale oil would follow the share in
        relation to the total unconventional oil as estimated by
        [Mohr&Evans2010](Low Case) for 2050 and 2100 (linear interpolation)
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


def afforestation_program_2020():
    """
    Real Name: Afforestation program 2020
    Original Eqn: GET DIRECT DATA('../parameters.xlsx', 'World', 'time_afforestation', 'afforestation')
    Units: MtC/year
    Limits: (None, None)
    Type: component_ext_data
    Subs: None

    Afforestation program from 2020 following [Nilsson 1995] (time to inverse
        the deforestation trend).
    """
    return _ext_data_afforestation_program_2020(time())


def afforestation_program_2020_gtco2():
    """
    Real Name: Afforestation program 2020 GtCO2
    Original Eqn: Afforestation program 2020*activate afforestation program/(C per CO2*Mt per Gt)
    Units: GtCO2/year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual emissions captured by the afforestation program.
    """
    return (
        afforestation_program_2020()
        * activate_afforestation_program()
        / (c_per_co2() * mt_per_gt())
    )


def bioe_co2_emissions():
    """
    Real Name: BioE CO2 emissions
    Original Eqn: gCO2 per MJ conv gas*(Oil liquids saved by biofuels EJ+solid biofuels emissions relevant EJ+"PES tot biogas for heat-com")*MJ per EJ/g per Gt
    Units: GtCO2/year
    Limits: (None, None)
    Type: component
    Subs: None

    CO2 emissions from biomass. We assume that biofuels have an emission
        intensity similar to natural gas (due to ILUCs, see Technical Report), and
        for the rest (traditional biomass, biomass for electricity and biomass for
        heat) we asssume that the carbon balance is null.
    """
    return (
        gco2_per_mj_conv_gas()
        * (
            oil_liquids_saved_by_biofuels_ej()
            + solid_biofuels_emissions_relevant_ej()
            + pes_tot_biogas_for_heatcom()
        )
        * mj_per_ej()
        / g_per_gt()
    )


def c_per_co2():
    """
    Real Name: C per CO2
    Original Eqn: 3/11
    Units: GtC/GTCO2e
    Limits: (None, None)
    Type: constant
    Subs: None

    1 kg of CO2 contains 3/11 of carbon.
    """
    return 3 / 11


def carbon_emissions_gtc():
    """
    Real Name: Carbon emissions GtC
    Original Eqn: Total CO2 emissions GTCO2*C per CO2
    Units: GtC/year
    Limits: (None, None)
    Type: component
    Subs: None

    Total anual carbon emissions.
    """
    return total_co2_emissions_gtco2() * c_per_co2()


def ch4_emissions_coal_without_ctl():
    """
    Real Name: CH4 emissions coal without CTL
    Original Eqn: extraction coal emissions relevant EJ*gCH4 per MJ coal*MJ per EJ/g per Mt
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None

    CH4 emissions coal.
    """
    return (
        extraction_coal_emissions_relevant_ej()
        * gch4_per_mj_coal()
        * mj_per_ej()
        / g_per_mt()
    )


def ch4_emissions_conv_gas_without_gtl():
    """
    Real Name: CH4 emissions conv gas without GTL
    Original Eqn: (real extraction conv gas EJ-"PED nat. gas for GTL EJ"*share conv vs total gas extraction)*gCH4 per MJ conv gas*MJ per EJ/g per Mt
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None

    CH4 emissions conventional gas.
    """
    return (
        (
            real_extraction_conv_gas_ej()
            - ped_nat_gas_for_gtl_ej() * share_conv_vs_total_gas_extraction()
        )
        * gch4_per_mj_conv_gas()
        * mj_per_ej()
        / g_per_mt()
    )


def ch4_emissions_ctl():
    """
    Real Name: CH4 emissions CTL
    Original Eqn: extraction coal for CTL EJ*gCH4 per MJ CTL*MJ per EJ/g per Mt
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None

    CH4 emissions CTL.
    """
    return extraction_coal_for_ctl_ej() * gch4_per_mj_ctl() * mj_per_ej() / g_per_mt()


def ch4_emissions_gtl():
    """
    Real Name: CH4 emissions GTL
    Original Eqn: "PED nat. gas for GTL EJ"*gCH4 per MJ GTL*MJ per EJ/g per Mt
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None

    CH4 emissions GTL.
    """
    return ped_nat_gas_for_gtl_ej() * gch4_per_mj_gtl() * mj_per_ej() / g_per_mt()


def ch4_emissions_oil():
    """
    Real Name: CH4 emissions oil
    Original Eqn: PES oil EJ*gCH4 per MJ oil*MJ per EJ/g per Mt
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None

    CH4 emissions oil.
    """
    return pes_oil_ej() * gch4_per_mj_oil() * mj_per_ej() / g_per_mt()


def ch4_emissions_unconv_gas():
    """
    Real Name: CH4 emissions unconv gas
    Original Eqn: (real extraction unconv gas EJ-"PED nat. gas for GTL EJ"*(1-share conv vs total gas extraction))*gCH4 per MJ unconv gas*MJ per EJ/g per Mt
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None

    CH4 emissions unconventional gas.
    """
    return (
        (
            real_extraction_unconv_gas_ej()
            - ped_nat_gas_for_gtl_ej() * (1 - share_conv_vs_total_gas_extraction())
        )
        * gch4_per_mj_unconv_gas()
        * mj_per_ej()
        / g_per_mt()
    )


def co2_emissions_coal_without_ctl():
    """
    Real Name: CO2 emissions coal without CTL
    Original Eqn: extraction coal emissions relevant EJ*gCO2 per MJ coal*MJ per EJ/g per Gt
    Units: GtCO2/year
    Limits: (None, None)
    Type: component
    Subs: None

    Emissions from coal withoug accounting for CTL-related emissions.
    """
    return (
        extraction_coal_emissions_relevant_ej()
        * gco2_per_mj_coal()
        * mj_per_ej()
        / g_per_gt()
    )


def co2_emissions_conv_gas_without_gtl():
    """
    Real Name: CO2 emissions conv gas without GTL
    Original Eqn: real extraction conv gas emissions relevant EJ*gCO2 per MJ conv gas*MJ per EJ/g per Gt
    Units: GtCO2/year
    Limits: (None, None)
    Type: component
    Subs: None

    CO2 emissions from conventional gas (withouth GTL) when the gas extraction
        is disaggregated in conventional and unconventional resource, and CO2
        emissions from total gas when the extraction is aggregated.
    """
    return (
        real_extraction_conv_gas_emissions_relevant_ej()
        * gco2_per_mj_conv_gas()
        * mj_per_ej()
        / g_per_gt()
    )


def co2_emissions_conv_oil():
    """
    Real Name: CO2 emissions conv oil
    Original Eqn: real extraction conv oil emissions relevant EJ*gCO2 per MJ conv oil*MJ per EJ/g per Gt
    Units: GtCO2/year
    Limits: (None, None)
    Type: component
    Subs: None

    CO2 emissions from conventional oil.
    """
    return (
        real_extraction_conv_oil_emissions_relevant_ej()
        * gco2_per_mj_conv_oil()
        * mj_per_ej()
        / g_per_gt()
    )


def co2_emissions_ctl():
    """
    Real Name: CO2 emissions CTL
    Original Eqn: gCO2 per MJ CTL*extraction coal for CTL EJ*MJ per EJ/g per Gt
    Units: GtCO2/year
    Limits: (None, None)
    Type: component
    Subs: None

    CO2 emissions associated to CTL production.
    """
    return gco2_per_mj_ctl() * extraction_coal_for_ctl_ej() * mj_per_ej() / g_per_gt()


def co2_emissions_gtl():
    """
    Real Name: CO2 emissions GTL
    Original Eqn: "PED nat. gas for GTL EJ"*gCO2 per MJ GTL*MJ per EJ/g per Gt
    Units: GtCO2/year
    Limits: (None, None)
    Type: component
    Subs: None

    CO2 emissions associated to GTL production.
    """
    return ped_nat_gas_for_gtl_ej() * gco2_per_mj_gtl() * mj_per_ej() / g_per_gt()


def co2_emissions_peat():
    """
    Real Name: CO2 emissions peat
    Original Eqn: PES peat EJ*gCO2 per MJ shale oil*MJ per EJ/g per Gt
    Units: GtCO2/year
    Limits: (None, None)
    Type: component
    Subs: None

    CO2 emissions from peat.
    """
    return pes_peat_ej() * gco2_per_mj_shale_oil() * mj_per_ej() / g_per_gt()


def co2_emissions_unconv_gas():
    """
    Real Name: CO2 emissions unconv gas
    Original Eqn: real extraction unconv gas emissions relevant EJ*gCO2 per MJ unconv gas*MJ per EJ/g per Gt
    Units: GtCO2/year
    Limits: (None, None)
    Type: component
    Subs: None

    CO2 emissions from unconventional gas.
    """
    return (
        real_extraction_unconv_gas_emissions_relevant_ej()
        * gco2_per_mj_unconv_gas()
        * mj_per_ej()
        / g_per_gt()
    )


def co2_emissions_unconv_oil():
    """
    Real Name: CO2 emissions unconv oil
    Original Eqn: (real extraction unconv oil emissions relevant EJ*(gCO2 per MJ unconv oil+(gCO2 per MJ shale oil-gCO2 per MJ unconv oil )*Adapt emissions shale oil))*MJ per EJ/g per Gt
    Units: GtCO2/year
    Limits: (None, None)
    Type: component
    Subs: None

    CO2 emissions from unconventional oil.
    """
    return (
        (
            real_extraction_unconv_oil_emissions_relevant_ej()
            * (
                gco2_per_mj_unconv_oil()
                + (gco2_per_mj_shale_oil() - gco2_per_mj_unconv_oil())
                * adapt_emissions_shale_oil()
            )
        )
        * mj_per_ej()
        / g_per_gt()
    )


def co2_fossil_fuel_emissions():
    """
    Real Name: CO2 fossil fuel emissions
    Original Eqn: CO2 emissions conv gas without GTL+CO2 emissions unconv gas+CO2 emissions GTL+CO2 emissions conv oil+CO2 emissions unconv oil+CO2 emissions coal without CTL+CO2 emissions CTL
    Units: GtCO2/year
    Limits: (None, None)
    Type: component
    Subs: None

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


def co2_landuse_change_emissions_exogenous():
    """
    Real Name: "CO2 land-use change emissions exogenous"
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'World', 'co2_luc')
    Units: GtCO2/year
    Limits: (None, None)
    Type: constant
    Subs: None

    [DICE-2013R] Land-use change emissions. Cte at 2010 level for the period
        1990-2100 as first approximation.
    """
    return _ext_constant_co2_landuse_change_emissions_exogenous()


def co2_soilluc_emissions():
    """
    Real Name: "CO2 soil&LUC emissions"
    Original Eqn: "CO2 land-use change emissions exogenous"
    Units: GtCO2/year
    Limits: (None, None)
    Type: component
    Subs: None

    CO2 emissions associated to soil managemente and land-use change uses.
    """
    return co2_landuse_change_emissions_exogenous()


def correction_factor_all_ghgs():
    """
    Real Name: correction factor all GHGs
    Original Eqn: 1.22
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Taking as reference data for 2012 (comparing MEDEAS outputs and CAT from
        INSTM report).
    """
    return 1.22


def cumulative_co2e_ghg_emissions():
    """
    Real Name: Cumulative CO2e GHG emissions
    Original Eqn: INTEG ( Total Ce all GHG, 0)
    Units: GTCO2e/year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_cumulative_co2e_ghg_emissions()


def cumulative_emissions_to_1995():
    """
    Real Name: Cumulative emissions to 1995
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'World', 'cumulative_emissions_to_1995')
    Units: GtC
    Limits: (None, None)
    Type: constant
    Subs: None

    Cumulative emissions 1751-1995 due to carbon emissions from fossil fuel
        consumption, cement production and land-use changes. Data from CDIAC and
        World Resources Institute.
    """
    return _ext_constant_cumulative_emissions_to_1995()


def g_per_gt():
    """
    Real Name: g per Gt
    Original Eqn: 1e+15
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Unit conversion.
    """
    return 1e15


def g_per_mt():
    """
    Real Name: g per Mt
    Original Eqn: 1e+12
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    1e12 grams = 1 Mtonne.
    """
    return 1e12


def gch4_per_mj_coal():
    """
    Real Name: gCH4 per MJ coal
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'gch4_coal')
    Units: GtCO2/MToe
    Limits: (None, None)
    Type: constant
    Subs: None

    CH4 emissions associated to the extraction of coal. Ref: Fig. 2 Howarth
        (2015).
    """
    return _ext_constant_gch4_per_mj_coal()


def gch4_per_mj_conv_gas():
    """
    Real Name: gCH4 per MJ conv gas
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'gch4_conv_gas')
    Units: GtCO2/MToe
    Limits: (None, None)
    Type: constant
    Subs: None

    CH4 emissions associated to the extraction of conventional gas. Ref: Fig.
        2 Howarth (2015).
    """
    return _ext_constant_gch4_per_mj_conv_gas()


def gch4_per_mj_ctl():
    """
    Real Name: gCH4 per MJ CTL
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'gch4_ctl')
    Units: GtCO2/MToe
    Limits: (None, None)
    Type: constant
    Subs: None

    CH4 emission factor of CTL.
    """
    return _ext_constant_gch4_per_mj_ctl()


def gch4_per_mj_gtl():
    """
    Real Name: gCH4 per MJ GTL
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'gch4_gtl')
    Units: GtCO2/MToe
    Limits: (None, None)
    Type: constant
    Subs: None

    CH4 emission factor of GTL.
    """
    return _ext_constant_gch4_per_mj_gtl()


def gch4_per_mj_oil():
    """
    Real Name: gCH4 per MJ oil
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'gch4_oil')
    Units: GtCO2/MToe
    Limits: (None, None)
    Type: constant
    Subs: None

    CH4 emissions associated to the extraction of oil. Ref: Fig. 2 Howarth
        (2015).
    """
    return _ext_constant_gch4_per_mj_oil()


def gch4_per_mj_unconv_gas():
    """
    Real Name: gCH4 per MJ unconv gas
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'gch4_unconventional_gas')
    Units: GtCO2/MToe
    Limits: (None, None)
    Type: constant
    Subs: None

    CH4 emissions associated to the extraction of unconventional gas (shale
        gas). Ref: Fig. 2 Howarth (2015).
    """
    return _ext_constant_gch4_per_mj_unconv_gas()


def gco2_per_mj_coal():
    """
    Real Name: gCO2 per MJ coal
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'gco2_coal')
    Units: gCO2/MJ
    Limits: (None, None)
    Type: constant
    Subs: None

    CO2 emission factor coal.
    """
    return _ext_constant_gco2_per_mj_coal()


def gco2_per_mj_conv_gas():
    """
    Real Name: gCO2 per MJ conv gas
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'gco2_conventional_gas')
    Units: gCO2/MJ
    Limits: (None, None)
    Type: constant
    Subs: None

    CO2 emission factor conventional natural gas.
    """
    return _ext_constant_gco2_per_mj_conv_gas()


def gco2_per_mj_conv_oil():
    """
    Real Name: gCO2 per MJ conv oil
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'gco2_conventional_oil')
    Units: gCO2/MJ
    Limits: (None, None)
    Type: constant
    Subs: None

    CO2 emission factor conventional oil.
    """
    return _ext_constant_gco2_per_mj_conv_oil()


def gco2_per_mj_ctl():
    """
    Real Name: gCO2 per MJ CTL
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'gco2_ctl')
    Units: gCO2/MJ
    Limits: (None, None)
    Type: constant
    Subs: None

    CO2 emissions coefficient of CTL.
    """
    return _ext_constant_gco2_per_mj_ctl()


def gco2_per_mj_gtl():
    """
    Real Name: gCO2 per MJ GTL
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'gco2_gtl')
    Units: gCO2/MJ
    Limits: (None, None)
    Type: constant
    Subs: None

    CO2 emissions coefficient of GTL.
    """
    return _ext_constant_gco2_per_mj_gtl()


def gco2_per_mj_shale_oil():
    """
    Real Name: gCO2 per MJ shale oil
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'gco2_shale_oil')
    Units: gCO2/MJ
    Limits: (None, None)
    Type: constant
    Subs: None

    CO2 emission factor shale oil.
    """
    return _ext_constant_gco2_per_mj_shale_oil()


def gco2_per_mj_unconv_gas():
    """
    Real Name: gCO2 per MJ unconv gas
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'gco2_unconventional_gas')
    Units: gCO2/MJ
    Limits: (None, None)
    Type: constant
    Subs: None

    CO2 emission factor of unconventional gas.
    """
    return _ext_constant_gco2_per_mj_unconv_gas()


def gco2_per_mj_unconv_oil():
    """
    Real Name: gCO2 per MJ unconv oil
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'Global', 'gco2_unconventional_oil')
    Units: gCO2/MJ
    Limits: (None, None)
    Type: constant
    Subs: None

    Emission factor unconventional oil (tar sands/extra heavy oil).
    """
    return _ext_constant_gco2_per_mj_unconv_oil()


def gwp_100_years_ch4():
    """
    Real Name: GWP 100 years CH4
    Original Eqn: 34
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 34


def mt_per_gt():
    """
    Real Name: Mt per Gt
    Original Eqn: 1000
    Units: Mt/Gt
    Limits: (None, None)
    Type: constant
    Subs: None

    Converts megatonnes to gigatonnes.
    """
    return 1000


def new_c_gtc():
    """
    Real Name: new C GtC
    Original Eqn: Carbon emissions GtC
    Units: GtC/year
    Limits: (None, None)
    Type: component
    Subs: None

    Annual carbon emissions.
    """
    return carbon_emissions_gtc()


def total_ce_all_ghg():
    """
    Real Name: Total Ce all GHG
    Original Eqn: "Total CO2e [GWP=100 years]"*correction factor all GHGs*C per CO2
    Units: GTCe/year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return total_co2e_gwp100_years() * correction_factor_all_ghgs() * c_per_co2()


def total_ch4_emissions_fossil_fuels():
    """
    Real Name: Total CH4 emissions fossil fuels
    Original Eqn: CH4 emissions conv gas without GTL+CH4 emissions unconv gas+CH4 emissions coal without CTL +CH4 emissions oil+CH4 emissions CTL+CH4 emissions GTL
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None

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


def total_co2_emissions_gtco2():
    """
    Real Name: Total CO2 emissions GTCO2
    Original Eqn: CO2 fossil fuel emissions+"CO2 soil&LUC emissions"+BioE CO2 emissions+CO2 emissions peat-Afforestation program 2020 GtCO2
    Units: GtCO2/year
    Limits: (None, None)
    Type: component
    Subs: None

    Total annual CO2 emissions. Original unit: "mill Tn CO2"
    """
    return (
        co2_fossil_fuel_emissions()
        + co2_soilluc_emissions()
        + bioe_co2_emissions()
        + co2_emissions_peat()
        - afforestation_program_2020_gtco2()
    )


def total_co2e_gwp100_years():
    """
    Real Name: "Total CO2e [GWP=100 years]"
    Original Eqn: Total CH4 emissions fossil fuels*GWP 100 years CH4/1000+Total CO2 emissions GTCO2
    Units: GTCO2e/year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        total_ch4_emissions_fossil_fuels() * gwp_100_years_ch4() / 1000
        + total_co2_emissions_gtco2()
    )


def total_co2e_all_ghg():
    """
    Real Name: Total CO2e all GHG
    Original Eqn: "Total CO2e [GWP=100 years]"*correction factor all GHGs
    Units: GTCO2e/year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return total_co2e_gwp100_years() * correction_factor_all_ghgs()


def total_cumulative_emissions_gtc():
    """
    Real Name: Total cumulative emissions GtC
    Original Eqn: INTEG ( new C GtC, Cumulative emissions to 1995)
    Units: GtC
    Limits: (None, None)
    Type: component
    Subs: None

    Total cumulative emissions.
    """
    return _integ_total_cumulative_emissions_gtc()


def total_cumulative_emissions_gtco2():
    """
    Real Name: Total cumulative emissions GtCO2
    Original Eqn: Total cumulative emissions GtC/C per CO2
    Units: GtCO2
    Limits: (None, None)
    Type: component
    Subs: None

    Total cumulative emissions.
    """
    return total_cumulative_emissions_gtc() / c_per_co2()


_ext_constant_activate_afforestation_program = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "afforestation_program",
    {},
    _root,
    "_ext_constant_activate_afforestation_program",
)


_ext_data_afforestation_program_2020 = ExtData(
    "../parameters.xlsx",
    "World",
    "time_afforestation",
    "afforestation",
    "interpolate",
    {},
    _root,
    "_ext_data_afforestation_program_2020",
)


_ext_constant_co2_landuse_change_emissions_exogenous = ExtConstant(
    "../parameters.xlsx",
    "World",
    "co2_luc",
    {},
    _root,
    "_ext_constant_co2_landuse_change_emissions_exogenous",
)


_integ_cumulative_co2e_ghg_emissions = Integ(
    lambda: total_ce_all_ghg(), lambda: 0, "_integ_cumulative_co2e_ghg_emissions"
)


_ext_constant_cumulative_emissions_to_1995 = ExtConstant(
    "../parameters.xlsx",
    "World",
    "cumulative_emissions_to_1995",
    {},
    _root,
    "_ext_constant_cumulative_emissions_to_1995",
)


_ext_constant_gch4_per_mj_coal = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gch4_coal",
    {},
    _root,
    "_ext_constant_gch4_per_mj_coal",
)


_ext_constant_gch4_per_mj_conv_gas = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gch4_conv_gas",
    {},
    _root,
    "_ext_constant_gch4_per_mj_conv_gas",
)


_ext_constant_gch4_per_mj_ctl = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gch4_ctl",
    {},
    _root,
    "_ext_constant_gch4_per_mj_ctl",
)


_ext_constant_gch4_per_mj_gtl = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gch4_gtl",
    {},
    _root,
    "_ext_constant_gch4_per_mj_gtl",
)


_ext_constant_gch4_per_mj_oil = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gch4_oil",
    {},
    _root,
    "_ext_constant_gch4_per_mj_oil",
)


_ext_constant_gch4_per_mj_unconv_gas = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gch4_unconventional_gas",
    {},
    _root,
    "_ext_constant_gch4_per_mj_unconv_gas",
)


_ext_constant_gco2_per_mj_coal = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_coal",
    {},
    _root,
    "_ext_constant_gco2_per_mj_coal",
)


_ext_constant_gco2_per_mj_conv_gas = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_conventional_gas",
    {},
    _root,
    "_ext_constant_gco2_per_mj_conv_gas",
)


_ext_constant_gco2_per_mj_conv_oil = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_conventional_oil",
    {},
    _root,
    "_ext_constant_gco2_per_mj_conv_oil",
)


_ext_constant_gco2_per_mj_ctl = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_ctl",
    {},
    _root,
    "_ext_constant_gco2_per_mj_ctl",
)


_ext_constant_gco2_per_mj_gtl = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_gtl",
    {},
    _root,
    "_ext_constant_gco2_per_mj_gtl",
)


_ext_constant_gco2_per_mj_shale_oil = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_shale_oil",
    {},
    _root,
    "_ext_constant_gco2_per_mj_shale_oil",
)


_ext_constant_gco2_per_mj_unconv_gas = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_unconventional_gas",
    {},
    _root,
    "_ext_constant_gco2_per_mj_unconv_gas",
)


_ext_constant_gco2_per_mj_unconv_oil = ExtConstant(
    "../parameters.xlsx",
    "Global",
    "gco2_unconventional_oil",
    {},
    _root,
    "_ext_constant_gco2_per_mj_unconv_oil",
)


_integ_total_cumulative_emissions_gtc = Integ(
    lambda: new_c_gtc(),
    lambda: cumulative_emissions_to_1995(),
    "_integ_total_cumulative_emissions_gtc",
)
