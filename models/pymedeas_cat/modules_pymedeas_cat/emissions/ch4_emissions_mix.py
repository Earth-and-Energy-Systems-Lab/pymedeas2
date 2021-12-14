"""
Module ch4_emissions_mix
Translated using PySD version 2.1.0
"""


def ch4_emissions_coal_test():
    """
    Real Name: CH4 emissions COAL test
    Original Eqn: CH4 emissions coal without CTL+CH4 emissions CTL
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return ch4_emissions_coal_without_ctl() + ch4_emissions_ctl()


def ch4_emissions_extraction_coal():
    """
    Real Name: CH4 emissions extraction coal
    Original Eqn: (Coal in FEC AUT+PE demand coal Elec plants EJ+PED coal for CHP plants EJ+PED coal for CTL EJ +PED coal for Heat plants EJ+"PED coal Heat-nc")*MJ per EJ*gCH4 per MJ coal/g per Mt
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        (
            coal_in_fec_aut()
            + pe_demand_coal_elec_plants_ej()
            + ped_coal_for_chp_plants_ej()
            + ped_coal_for_ctl_ej()
            + ped_coal_for_heat_plants_ej()
            + ped_coal_heatnc()
        )
        * mj_per_ej()
        * gch4_per_mj_coal()
        / g_per_mt()
    )


def ch4_emissions_extraction_gas():
    """
    Real Name: CH4 emissions extraction gas
    Original Eqn: (FE nat gas consumption+PE demand gas Elec plants EJ+PED gas for CHP plants EJ+"PED gas Heat-nc" +PED gases for Heat plants EJ+"PED nat. gas for GTL EJ" )*(1-share unconv tot gas )*MJ per EJ*gCH4 per MJ conv gas/g per Mt+ (FE nat gas consumption+PE demand gas Elec plants EJ+PED gas for CHP plants EJ+"PED gas Heat-nc" +PED gases for Heat plants EJ+"PED nat. gas for GTL EJ" )*share unconv tot gas *gCH4 per MJ unconv gas*MJ per EJ/g per Mt
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        fe_nat_gas_consumption()
        + pe_demand_gas_elec_plants_ej()
        + ped_gas_for_chp_plants_ej()
        + ped_gas_heatnc()
        + ped_gases_for_heat_plants_ej()
        + ped_nat_gas_for_gtl_ej()
    ) * (
        1 - share_unconv_tot_gas()
    ) * mj_per_ej() * gch4_per_mj_conv_gas() / g_per_mt() + (
        fe_nat_gas_consumption()
        + pe_demand_gas_elec_plants_ej()
        + ped_gas_for_chp_plants_ej()
        + ped_gas_heatnc()
        + ped_gases_for_heat_plants_ej()
        + ped_nat_gas_for_gtl_ej()
    ) * share_unconv_tot_gas() * gch4_per_mj_unconv_gas() * mj_per_ej() / g_per_mt()


def ch4_emissions_extraction_oil():
    """
    Real Name: CH4 emissions extraction OIL
    Original Eqn: (FED oil+PE demand oil Elec plants EJ+"PED liquids Heat-nc" +PED oil for CHP plants EJ +PED oil for Heat plants EJ)*MJ per EJ*gCH4 per MJ oil/g per Mt
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        (
            fed_oil()
            + pe_demand_oil_elec_plants_ej()
            + ped_liquids_heatnc()
            + ped_oil_for_chp_plants_ej()
            + ped_oil_for_heat_plants_ej()
        )
        * mj_per_ej()
        * gch4_per_mj_oil()
        / g_per_mt()
    )


def ch4_emissions_gas_test():
    """
    Real Name: CH4 emissions GAS test
    Original Eqn: CH4 emissions conv gas without GTL+CH4 emissions GTL+CH4 emissions unconv gas
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        ch4_emissions_conv_gas_without_gtl()
        + ch4_emissions_gtl()
        + ch4_emissions_unconv_gas()
    )


def ch4_emissions_oil_test():
    """
    Real Name: CH4 emissions OIL test
    Original Eqn: CH4 emissions oil
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return ch4_emissions_oil()


def check_hist_ch4_emissions():
    """
    Real Name: check hist CH4 emissions
    Original Eqn: IF THEN ELSE(Time<2012, (Total FE CH4 emissions-Total CH4 emissions fossil fuels )*100/Total CH4 emissions fossil fuels, 0)
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return if_then_else(
        time() < 2012,
        lambda: (total_fe_ch4_emissions() - total_ch4_emissions_fossil_fuels())
        * 100
        / total_ch4_emissions_fossil_fuels(),
        lambda: 0,
    )


def coal_for_elec_ch4_emissions():
    """
    Real Name: Coal for Elec CH4 emissions
    Original Eqn: (PE demand coal Elec plants EJ+PED coal for CHP plants EJ)*MJ per EJ*gCH4 per MJ coal/g per Mt
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        (pe_demand_coal_elec_plants_ej() + ped_coal_for_chp_plants_ej())
        * mj_per_ej()
        * gch4_per_mj_coal()
        / g_per_mt()
    )


def coal_for_heat_ch4_emissions():
    """
    Real Name: Coal for Heat CH4 emissions
    Original Eqn: ("PED coal Heat-nc"+PED coal for Heat plants EJ)*MJ per EJ*gCH4 per MJ coal/g per Mt
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        (ped_coal_heatnc() + ped_coal_for_heat_plants_ej())
        * mj_per_ej()
        * gch4_per_mj_coal()
        / g_per_mt()
    )


def fe_nat_gas_consumption():
    """
    Real Name: FE nat gas consumption
    Original Eqn: (1-share Biogas total PES Gases AUT)*real FE consumption gases EJ
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (1 - share_biogas_total_pes_gases_aut()) * real_fe_consumption_gases_ej()


def fec_oil_2():
    """
    Real Name: FEC oil 2
    Original Eqn: real FE consumption liquids EJ-FES total biofuels production EJ
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return real_fe_consumption_liquids_ej() - fes_total_biofuels_production_ej()


def fed_oil():
    """
    Real Name: FED oil
    Original Eqn: PEC total oil-total demand oil other FED
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return pec_total_oil() - total_demand_oil_other_fed()


def gas_for_elec_ch4_emissions():
    """
    Real Name: Gas for Elec CH4 emissions
    Original Eqn: (PE demand gas Elec plants EJ+PED gas for CHP plants EJ)*MJ per EJ*gCH4 per MJ conv gas/g per Mt
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        (pe_demand_gas_elec_plants_ej() + ped_gas_for_chp_plants_ej())
        * mj_per_ej()
        * gch4_per_mj_conv_gas()
        / g_per_mt()
    )


def gas_for_heat_ch4_emissions():
    """
    Real Name: Gas for Heat CH4 emissions
    Original Eqn: (PED gases for Heat plants EJ+"PED gas Heat-nc")*MJ per EJ*gCH4 per MJ conv gas/g per Mt
    Units: GtCO2/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        (ped_gases_for_heat_plants_ej() + ped_gas_heatnc())
        * mj_per_ej()
        * gch4_per_mj_conv_gas()
        / g_per_mt()
    )


def gases_fe_ch4_emission():
    """
    Real Name: Gases FE CH4 emission
    Original Eqn: FE nat gas consumption*MJ per EJ*gCH4 per MJ conv gas/g per Mt
    Units: GtCO2/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return fe_nat_gas_consumption() * mj_per_ej() * gch4_per_mj_conv_gas() / g_per_mt()


def liquids_fe_ch4_emissions():
    """
    Real Name: Liquids FE CH4 emissions
    Original Eqn: FED oil*MJ per EJ*gCH4 per MJ oil/g per Mt+ PED coal for CTL EJ*MJ per EJ*gCH4 per MJ CTL/g per Mt+ "PED nat. gas for GTL EJ"*MJ per EJ*gCH4 per MJ GTL/g per Mt
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        fed_oil() * mj_per_ej() * gch4_per_mj_oil() / g_per_mt()
        + ped_coal_for_ctl_ej() * mj_per_ej() * gch4_per_mj_ctl() / g_per_mt()
        + ped_nat_gas_for_gtl_ej() * mj_per_ej() * gch4_per_mj_gtl() / g_per_mt()
    )


def oil_for_elec_ch4_emissions():
    """
    Real Name: Oil for Elec CH4 emissions
    Original Eqn: (PE demand oil Elec plants EJ+PED oil for CHP plants EJ)*MJ per EJ*gCH4 per MJ oil/g per Mt
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        (pe_demand_oil_elec_plants_ej() + ped_oil_for_chp_plants_ej())
        * mj_per_ej()
        * gch4_per_mj_oil()
        / g_per_mt()
    )


def oil_for_heat_ch4_emissions():
    """
    Real Name: Oil for Heat CH4 emissions
    Original Eqn: (PED oil for Heat plants EJ+"PED liquids Heat-nc")*MJ per EJ*gCH4 per MJ oil/g per Mt
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        (ped_oil_for_heat_plants_ej() + ped_liquids_heatnc())
        * mj_per_ej()
        * gch4_per_mj_oil()
        / g_per_mt()
    )


def pes_oil_2():
    """
    Real Name: PES oil 2
    Original Eqn: PED NRE Liquids-Other liquids required EJ-PE demand oil Elec plants EJ-"PED liquids Heat-nc" -PED oil for CHP plants EJ-PED oil for Heat plants EJ
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        ped_nre_liquids()
        - other_liquids_required_ej()
        - pe_demand_oil_elec_plants_ej()
        - ped_liquids_heatnc()
        - ped_oil_for_chp_plants_ej()
        - ped_oil_for_heat_plants_ej()
    )


def ratio_elec_ch4_emissions():
    """
    Real Name: ratio Elec CH4 emissions
    Original Eqn: ZIDZ(Total Elec NRES CH4 emissions, Total FE Elec consumption EJ )
    Units: MtCH4/EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(total_elec_nres_ch4_emissions(), total_fe_elec_consumption_ej())


def ratio_gases_ch4_emissions():
    """
    Real Name: ratio Gases CH4 emissions
    Original Eqn: ZIDZ(Gases FE CH4 emission, real FE consumption gases EJ )
    Units: MtCH4/EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(gases_fe_ch4_emission(), real_fe_consumption_gases_ej())


def ratio_heat_ch4_emissions():
    """
    Real Name: ratio Heat CH4 emissions
    Original Eqn: ZIDZ(Total Heat CH4 emissions, Total FED Heat EJ )
    Units: MtCH4/EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(total_heat_ch4_emissions(), total_fed_heat_ej())


def ratio_liquids_ch4_emissions():
    """
    Real Name: ratio Liquids CH4 emissions
    Original Eqn: ZIDZ(Liquids FE CH4 emissions, Total FEC liquids )
    Units: MtCH4/EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(liquids_fe_ch4_emissions(), total_fec_liquids())


def ratio_solids_ch4_emissions():
    """
    Real Name: ratio Solids CH4 emissions
    Original Eqn: ZIDZ(Solids FE CH4 emissions, Required FED solids )
    Units: MtCH4/EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(solids_fe_ch4_emissions(), required_fed_solids())


def share_coal_for_elec_ch4_emissions():
    """
    Real Name: share coal for Elec CH4 emissions
    Original Eqn: ZIDZ( Coal for Elec CH4 emissions,Total Elec NRES CH4 emissions )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(coal_for_elec_ch4_emissions(), total_elec_nres_ch4_emissions())


def share_gas_for_elec_ch4_emissions():
    """
    Real Name: share gas for Elec CH4 emissions
    Original Eqn: ZIDZ( Gas for Elec CH4 emissions,Total Elec NRES CH4 emissions)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(gas_for_elec_ch4_emissions(), total_elec_nres_ch4_emissions())


def share_oil_for_elec_ch4_emissions():
    """
    Real Name: share oil for Elec CH4 emissions
    Original Eqn: ZIDZ( Oil for Elec CH4 emissions,Total Elec NRES CH4 emissions)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(oil_for_elec_ch4_emissions(), total_elec_nres_ch4_emissions())


def solids_fe_ch4_emissions():
    """
    Real Name: Solids FE CH4 emissions
    Original Eqn: Coal in FEC AUT*MJ per EJ*gCH4 per MJ coal/g per Mt
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return coal_in_fec_aut() * mj_per_ej() * gch4_per_mj_coal() / g_per_mt()


def total_ch4_emission_sper_sector():
    """
    Real Name: Total CH4 emission sper sector
    Original Eqn: CH4 emissions extraction coal+CH4 emissions extraction gas+CH4 emissions extraction OIL
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        ch4_emissions_extraction_coal()
        + ch4_emissions_extraction_gas()
        + ch4_emissions_extraction_oil()
    )


def total_ch4_emissions():
    """
    Real Name: Total CH4 emissions
    Original Eqn: CH4 emissions COAL test+CH4 emissions GAS test+CH4 emissions OIL test
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        ch4_emissions_coal_test() + ch4_emissions_gas_test() + ch4_emissions_oil_test()
    )


def total_demand_oil_other_fed():
    """
    Real Name: total demand oil other FED
    Original Eqn: PE demand oil Elec plants EJ+PED oil for CHP plants EJ+PED oil for Heat plants EJ+"PED liquids Heat-nc"
    Units: EJ/Year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        pe_demand_oil_elec_plants_ej()
        + ped_oil_for_chp_plants_ej()
        + ped_oil_for_heat_plants_ej()
        + ped_liquids_heatnc()
    )


def total_elec_nres_ch4_emissions():
    """
    Real Name: Total Elec NRES CH4 emissions
    Original Eqn: Coal for Elec CH4 emissions+Gas for Elec CH4 emissions+Oil for Elec CH4 emissions
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        coal_for_elec_ch4_emissions()
        + gas_for_elec_ch4_emissions()
        + oil_for_elec_ch4_emissions()
    )


def total_fe_ch4_emissions():
    """
    Real Name: Total FE CH4 emissions
    Original Eqn: SUM(Total per FE CH4 emissions[final sources!])
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return sum(total_per_fe_ch4_emissions(), dim=("final sources",))


def total_heat_ch4_emissions():
    """
    Real Name: Total Heat CH4 emissions
    Original Eqn: Coal for Heat CH4 emissions+Gas for Heat CH4 emissions+Oil for Heat CH4 emissions
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        coal_for_heat_ch4_emissions()
        + gas_for_heat_ch4_emissions()
        + oil_for_heat_ch4_emissions()
    )


@subs(["final sources"], _subscript_dict)
def total_per_fe_ch4_emissions():
    """
    Real Name: Total per FE CH4 emissions
    Original Eqn:
      Total Elec NRES CH4 emissions
      Total Heat CH4 emissions
      Liquids FE CH4 emissions
      Gases FE CH4 emission
      Solids FE CH4 emissions
    Units: MtCH4
    Limits: (None, None)
    Type: component
    Subs: ['final sources']


    """
    return xrmerge(
        rearrange(
            total_elec_nres_ch4_emissions(),
            ["final sources"],
            {"final sources": ["electricity"]},
        ),
        rearrange(
            total_heat_ch4_emissions(), ["final sources"], {"final sources": ["heat"]}
        ),
        rearrange(
            liquids_fe_ch4_emissions(),
            ["final sources"],
            {"final sources": ["liquids"]},
        ),
        rearrange(
            gases_fe_ch4_emission(), ["final sources"], {"final sources": ["gases"]}
        ),
        rearrange(
            solids_fe_ch4_emissions(), ["final sources"], {"final sources": ["solids"]}
        ),
    )
