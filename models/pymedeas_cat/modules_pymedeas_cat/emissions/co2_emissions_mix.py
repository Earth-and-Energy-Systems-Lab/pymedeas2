"""
Module co2_emissions_mix
Translated using PySD version 2.1.0
"""


def check_historic_co2_emissions():
    """
    Real Name: check historic CO2 emissions
    Original Eqn: IF THEN ELSE(Time<2015, (Total FE CO2 emissions-Total CO2 emissions all fuels )*100/CO2 fossil fuel emissions, 0)
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        time() < 2015,
        lambda: (total_fe_co2_emissions() - total_co2_emissions_all_fuels())
        * 100
        / co2_fossil_fuel_emissions(),
        lambda: 0,
    )


def co2_emissions_coal():
    """
    Real Name: CO2 emissions COAL
    Original Eqn: modern solids BioE demand households*gCO2 per MJ conv gas*MJ per EJ/g per Gt+ Coal for Elec CO2 emissions+ Coal for Heat CO2 emissions
    Units: GtCO2
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        modern_solids_bioe_demand_households()
        * gco2_per_mj_conv_gas()
        * mj_per_ej()
        / g_per_gt()
        + coal_for_elec_co2_emissions()
        + coal_for_heat_co2_emissions()
    )


def co2_emissions_liquids():
    """
    Real Name: CO2 emissions liquids
    Original Eqn: FEC oil EJ*share conv oil vs tot agg*MJ per EJ*gCO2 per MJ conv oil/g per Gt+ FEC oil EJ*(1-share conv oil vs tot agg)*MJ per EJ*gCO2 per MJ unconv oil/g per Gt+ Oil for Elec CO2 emissions+ Oil for Heat CO2 emissions+ Oil liquids saved by biofuels EJ*MJ per EJ*gCO2 per MJ conv gas/g per Gt
    Units: GtCO2
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        fec_oil_ej()
        * share_conv_oil_vs_tot_agg()
        * mj_per_ej()
        * gco2_per_mj_conv_oil()
        / g_per_gt()
        + fec_oil_ej()
        * (1 - share_conv_oil_vs_tot_agg())
        * mj_per_ej()
        * gco2_per_mj_unconv_oil()
        / g_per_gt()
        + oil_for_elec_co2_emissions()
        + oil_for_heat_co2_emissions()
        + oil_liquids_saved_by_biofuels_ej()
        * mj_per_ej()
        * gco2_per_mj_conv_gas()
        / g_per_gt()
    )


def co2_emissions_oil_test():
    """
    Real Name: CO2 emissions OIL test
    Original Eqn: CO2 emissions conv oil+CO2 emissions unconv oil
    Units: GtCO2
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return co2_emissions_conv_oil() + co2_emissions_unconv_oil()


def coal_for_elec_co2_emissions():
    """
    Real Name: Coal for Elec CO2 emissions
    Original Eqn: (PE demand coal Elec plants EJ*MJ per EJ*gCO2 per MJ coal/g per Gt)+ (PED coal for CHP plants EJ*MJ per EJ*gCO2 per MJ coal/g per Gt)
    Units: GtCO2/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        pe_demand_coal_elec_plants_ej() * mj_per_ej() * gco2_per_mj_coal() / g_per_gt()
    ) + (ped_coal_for_chp_plants_ej() * mj_per_ej() * gco2_per_mj_coal() / g_per_gt())


def coal_for_heat_co2_emissions():
    """
    Real Name: Coal for Heat CO2 emissions
    Original Eqn: ("PED coal Heat-nc"+PED coal for Heat plants EJ)*MJ per EJ*gCO2 per MJ coal/g per Gt
    Units: GtCO2/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        (ped_coal_heatnc() + ped_coal_for_heat_plants_ej())
        * mj_per_ej()
        * gco2_per_mj_coal()
        / g_per_gt()
    )


def fec_oil_ej():
    """
    Real Name: FEC oil EJ
    Original Eqn: share PED NRE liquids*real FE consumption liquids EJ
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return share_ped_nre_liquids() * real_fe_consumption_liquids_ej()


def fes_coal():
    """
    Real Name: FES coal
    Original Eqn: PEC coal-PED coal total primary uses
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pec_coal() - ped_coal_total_primary_uses()


def gas_for_elec_co2_emissions():
    """
    Real Name: Gas for Elec CO2 emissions
    Original Eqn: (PE demand gas Elec plants EJ+PED gas for CHP plants EJ)*gCO2 per MJ conv gas*MJ per EJ/g per Gt+ (PE demand gas Elec plants EJ+PED gas for CHP plants EJ)*(1-share conv vs total gas extraction EU )*gCO2 per MJ unconv gas*MJ per EJ/g per Gt
    Units: GtCO2/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        pe_demand_gas_elec_plants_ej() + ped_gas_for_chp_plants_ej()
    ) * gco2_per_mj_conv_gas() * mj_per_ej() / g_per_gt() + (
        pe_demand_gas_elec_plants_ej() + ped_gas_for_chp_plants_ej()
    ) * (
        1 - share_conv_vs_total_gas_extraction_eu()
    ) * gco2_per_mj_unconv_gas() * mj_per_ej() / g_per_gt()


def gas_for_heat_co2_emissions():
    """
    Real Name: Gas for Heat CO2 emissions
    Original Eqn: (PED gases for Heat plants EJ+"PED gas Heat-nc")*MJ per EJ*gCO2 per MJ conv gas/g per Gt
    Units: GtCO2/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        (ped_gases_for_heat_plants_ej() + ped_gas_heatnc())
        * mj_per_ej()
        * gco2_per_mj_conv_gas()
        / g_per_gt()
    )


def gases_fe_co2_emission():
    """
    Real Name: Gases FE CO2 emission
    Original Eqn: (real FE consumption gases EJ-non energy use gas demand)*MJ per EJ*gCO2 per MJ conv gas/g per Gt
    Units: GtCO2/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        (real_fe_consumption_gases_ej() - non_energy_use_gas_demand())
        * mj_per_ej()
        * gco2_per_mj_conv_gas()
        / g_per_gt()
    )


def liquids_fe_co2_emissions():
    """
    Real Name: Liquids FE CO2 emissions
    Original Eqn: FEC oil EJ*share conv vs total oil extraction EU*MJ per EJ*gCO2 per MJ conv oil/g per Gt+ FEC oil EJ*(1-share conv vs total oil extraction EU)*MJ per EJ*gCO2 per MJ unconv oil/g per Gt+ CTL production*MJ per EJ*gCO2 per MJ CTL/g per Gt+ GTL production*MJ per EJ*gCO2 per MJ GTL/g per Gt+ Oil liquids saved by biofuels EJ*MJ per EJ*gCO2 per MJ conv gas/g per Gt
    Units: GtCO2/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        fec_oil_ej()
        * share_conv_vs_total_oil_extraction_eu()
        * mj_per_ej()
        * gco2_per_mj_conv_oil()
        / g_per_gt()
        + fec_oil_ej()
        * (1 - share_conv_vs_total_oil_extraction_eu())
        * mj_per_ej()
        * gco2_per_mj_unconv_oil()
        / g_per_gt()
        + ctl_production() * mj_per_ej() * gco2_per_mj_ctl() / g_per_gt()
        + gtl_production() * mj_per_ej() * gco2_per_mj_gtl() / g_per_gt()
        + oil_liquids_saved_by_biofuels_ej()
        * mj_per_ej()
        * gco2_per_mj_conv_gas()
        / g_per_gt()
    )


def non_energy_use_gas_demand():
    """
    Real Name: non energy use gas demand
    Original Eqn: "Non-energy use demand by final fuel EJ"[gases]
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"])


def oil_for_elec_co2_emissions():
    """
    Real Name: Oil for Elec CO2 emissions
    Original Eqn: (PE demand oil Elec plants EJ+PED oil for CHP plants EJ)*share conv vs total oil extraction EU *MJ per EJ *gCO2 per MJ conv oil/g per Gt+ (PE demand oil Elec plants EJ+PED oil for CHP plants EJ)*(1-share conv vs total oil extraction EU ) *MJ per EJ*gCO2 per MJ unconv oil/g per Gt
    Units: GtCO2/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        pe_demand_oil_elec_plants_ej() + ped_oil_for_chp_plants_ej()
    ) * share_conv_vs_total_oil_extraction_eu() * mj_per_ej() * gco2_per_mj_conv_oil() / g_per_gt() + (
        pe_demand_oil_elec_plants_ej() + ped_oil_for_chp_plants_ej()
    ) * (
        1 - share_conv_vs_total_oil_extraction_eu()
    ) * mj_per_ej() * gco2_per_mj_unconv_oil() / g_per_gt()


def oil_for_heat_co2_emissions():
    """
    Real Name: Oil for Heat CO2 emissions
    Original Eqn: (PED oil for Heat plants EJ+"PED liquids Heat-nc")*share conv vs total oil extraction EU*MJ per EJ*gCO2 per MJ conv oil/g per Gt+ (PED oil for Heat plants EJ+"PED liquids Heat-nc")*(1-share conv vs total oil extraction EU)*MJ per EJ*gCO2 per MJ unconv oil/g per Gt
    Units: GtCO2/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        ped_oil_for_heat_plants_ej() + ped_liquids_heatnc()
    ) * share_conv_vs_total_oil_extraction_eu() * mj_per_ej() * gco2_per_mj_conv_oil() / g_per_gt() + (
        ped_oil_for_heat_plants_ej() + ped_liquids_heatnc()
    ) * (
        1 - share_conv_vs_total_oil_extraction_eu()
    ) * mj_per_ej() * gco2_per_mj_unconv_oil() / g_per_gt()


def ped_coal_total_primary_uses():
    """
    Real Name: PED coal total primary uses
    Original Eqn: PE demand coal Elec plants EJ+PED coal for CHP plants EJ+PED coal for CTL EJ+PED coal for Heat plants EJ +"PED coal Heat-nc"
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        pe_demand_coal_elec_plants_ej()
        + ped_coal_for_chp_plants_ej()
        + ped_coal_for_ctl_ej()
        + ped_coal_for_heat_plants_ej()
        + ped_coal_heatnc()
    )


def pes_solids_bioe_for_heat():
    """
    Real Name: PES solids BioE for heat
    Original Eqn: PES RES for heat by techn[solid bioE heat]
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return float(pes_res_for_heat_by_techn().loc["solid bioE heat"])


def ratio_elec_co2_emissions():
    """
    Real Name: ratio Elec CO2 emissions
    Original Eqn: ZIDZ(Total Elec CO2 emissions, Total FE Elec consumption EJ )
    Units: GtCO2/EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(total_elec_co2_emissions(), total_fe_elec_consumption_ej())


def ratio_gases_co2_emissions():
    """
    Real Name: ratio Gases CO2 emissions
    Original Eqn: ZIDZ(Gases FE CO2 emission, real FE consumption gases EJ )
    Units: GtCO2/EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(gases_fe_co2_emission(), real_fe_consumption_gases_ej())


def ratio_heat_co2_emissions():
    """
    Real Name: ratio Heat CO2 emissions
    Original Eqn: ZIDZ(Total Heat CO2 emissions, Total FED Heat EJ )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(total_heat_co2_emissions(), total_fed_heat_ej())


def ratio_liquids_co2_emissions():
    """
    Real Name: ratio Liquids CO2 emissions
    Original Eqn: ZIDZ(Liquids FE CO2 emissions, Total FEC liquids AUT )
    Units: GtCO2/EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(liquids_fe_co2_emissions(), total_fec_liquids_aut())


def ratio_solids_co2_emissions():
    """
    Real Name: ratio Solids CO2 emissions
    Original Eqn: ZIDZ(Solids FE CO2 emissions, Required FED solids )
    Units: GtCO2/EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(solids_fe_co2_emissions(), required_fed_solids())


def share_coal_for_elec_co2_emissions():
    """
    Real Name: share coal for Elec CO2 emissions
    Original Eqn: ZIDZ( Coal for Elec CO2 emissions,Total Elec NRES CO2 emisions)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(coal_for_elec_co2_emissions(), total_elec_nres_co2_emisions())


def share_gas_for_elec_co2_emissions():
    """
    Real Name: share gas for Elec CO2 emissions
    Original Eqn: ZIDZ( Gas for Elec CO2 emissions,Total Elec NRES CO2 emisions)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(gas_for_elec_co2_emissions(), total_elec_nres_co2_emisions())


def share_oil_for_elec_co2_emissions():
    """
    Real Name: share oil for Elec CO2 emissions
    Original Eqn: ZIDZ( Oil for Elec CO2 emissions,Total Elec NRES CO2 emisions)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(oil_for_elec_co2_emissions(), total_elec_nres_co2_emisions())


def share_ped_nre_liquids():
    """
    Real Name: share PED NRE liquids
    Original Eqn: 1-(ZIDZ(FES total biofuels production EJ, PED liquids EJ ))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return 1 - (zidz(fes_total_biofuels_production_ej(), ped_liquids_ej()))


def share_res():
    """
    Real Name: share RES
    Original Eqn: 1-(Total PED Elec/Total FE Elec generation EJ)
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return 1 - (total_ped_elec() / total_fe_elec_generation_ej())


def solids_fe_co2_emissions():
    """
    Real Name: Solids FE CO2 emissions
    Original Eqn: Coal in FEC AUT*MJ per EJ*gCO2 per MJ coal/g per Gt+ CO2 emissions peat+ modern solids BioE demand households*gCO2 per MJ conv gas*MJ per EJ/g per Gt
    Units: GtCO2/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        coal_in_fec_aut() * mj_per_ej() * gco2_per_mj_coal() / g_per_gt()
        + co2_emissions_peat()
        + modern_solids_bioe_demand_households()
        * gco2_per_mj_conv_gas()
        * mj_per_ej()
        / g_per_gt()
    )


def total_co2_emissions_all_fuels():
    """
    Real Name: Total CO2 emissions all fuels
    Original Eqn: CO2 fossil fuel emissions+ (Oil liquids saved by biofuels EJ+"PES tot biogas for heat-com" +solid bioE emissions relevant EJ )*MJ per EJ*gCO2 per MJ conv gas/g per Gt+ CO2 emissions peat
    Units: GtCO2/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        co2_fossil_fuel_emissions()
        + (
            oil_liquids_saved_by_biofuels_ej()
            + pes_tot_biogas_for_heatcom()
            + solid_bioe_emissions_relevant_ej()
        )
        * mj_per_ej()
        * gco2_per_mj_conv_gas()
        / g_per_gt()
        + co2_emissions_peat()
    )


def total_co2_emissions_nat_gas():
    """
    Real Name: TOTAL CO2 emissions nat gas
    Original Eqn: CO2 emissions conv gas without GTL+CO2 emissions unconv gas
    Units: GtCO2/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return co2_emissions_conv_gas_without_gtl() + co2_emissions_unconv_gas()


def total_co2_gases_emissoin_test():
    """
    Real Name: TOTAL CO2 gases emissoin test
    Original Eqn: Gas for Elec CO2 emissions+Gas for Heat CO2 emissions+Gases FE CO2 emission
    Units: GtCO2/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        gas_for_elec_co2_emissions()
        + gas_for_heat_co2_emissions()
        + gases_fe_co2_emission()
    )


def total_elec_co2_emissions():
    """
    Real Name: Total Elec CO2 emissions
    Original Eqn: Total Elec NRES CO2 emisions+ PE bioE for Elec generation EJ*MJ per EJ*gCO2 per MJ conv gas/g per Gt
    Units: GtCO2/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        total_elec_nres_co2_emisions()
        + pe_bioe_for_elec_generation_ej()
        * mj_per_ej()
        * gco2_per_mj_conv_gas()
        / g_per_gt()
    )


def total_elec_nres_co2_emisions():
    """
    Real Name: Total Elec NRES CO2 emisions
    Original Eqn: Coal for Elec CO2 emissions+Gas for Elec CO2 emissions+Oil for Elec CO2 emissions
    Units: GtCO2/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        coal_for_elec_co2_emissions()
        + gas_for_elec_co2_emissions()
        + oil_for_elec_co2_emissions()
    )


def total_fe_co2_emissions():
    """
    Real Name: Total FE CO2 emissions
    Original Eqn: SUM(Total per FE CO2 emissions[final sources!])
    Units: GtCO2/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return sum(total_per_fe_co2_emissions(), dim=("final sources",))


def total_fe_elec_generation_ej():
    """
    Real Name: Total FE Elec generation EJ
    Original Eqn: Total FE Elec generation TWh AUT*EJ per TWh
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return total_fe_elec_generation_twh_aut() * ej_per_twh()


def total_fec_liquids_aut():
    """
    Real Name: Total FEC liquids AUT
    Original Eqn: real FE consumption liquids EJ+GTL production+CTL production
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return real_fe_consumption_liquids_ej() + gtl_production() + ctl_production()


def total_fed_solids_ej():
    """
    Real Name: Total FED solids EJ
    Original Eqn: FES coal+modern solids BioE demand households
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return fes_coal() + modern_solids_bioe_demand_households()


def total_heat_co2_emissions():
    """
    Real Name: Total Heat CO2 emissions
    Original Eqn: Coal for Heat CO2 emissions+Gas for Heat CO2 emissions+Oil for Heat CO2 emissions+ PES solids BioE for heat*MJ per EJ*gCO2 per MJ conv gas/g per Gt
    Units: GtCO2/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        coal_for_heat_co2_emissions()
        + gas_for_heat_co2_emissions()
        + oil_for_heat_co2_emissions()
        + pes_solids_bioe_for_heat() * mj_per_ej() * gco2_per_mj_conv_gas() / g_per_gt()
    )


def total_ped_elec():
    """
    Real Name: Total PED Elec
    Original Eqn: PE demand coal Elec plants EJ+PE demand gas Elec plants EJ+PE demand oil Elec plants EJ +PED coal for CHP plants EJ+PED gas for CHP plants EJ+PED oil for CHP plants EJ
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        pe_demand_coal_elec_plants_ej()
        + pe_demand_gas_elec_plants_ej()
        + pe_demand_oil_elec_plants_ej()
        + ped_coal_for_chp_plants_ej()
        + ped_gas_for_chp_plants_ej()
        + ped_oil_for_chp_plants_ej()
    )


@subs(["final sources"], _subscript_dict)
def total_per_fe_co2_emissions():
    """
    Real Name: Total per FE CO2 emissions
    Original Eqn:
      Total Heat CO2 emissions
      Liquids FE CO2 emissions
      Gases FE CO2 emission
      Solids FE CO2 emissions
      Total Elec CO2 emissions
    Units: GtCO2/Year
    Limits: (None, None)
    Type: component
    Subs: ['final sources']


    """
    return xrmerge(
        rearrange(
            total_heat_co2_emissions(), ["final sources"], {"final sources": ["heat"]}
        ),
        rearrange(
            liquids_fe_co2_emissions(),
            ["final sources"],
            {"final sources": ["liquids"]},
        ),
        rearrange(
            gases_fe_co2_emission(), ["final sources"], {"final sources": ["gases"]}
        ),
        rearrange(
            solids_fe_co2_emissions(), ["final sources"], {"final sources": ["solids"]}
        ),
        rearrange(
            total_elec_co2_emissions(),
            ["final sources"],
            {"final sources": ["electricity"]},
        ),
    )
