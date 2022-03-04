"""
Module co2_emissions_mix
Translated using PySD version 2.2.1
"""


def check_historic_co2_emissions():
    """
    Real Name: check historic CO2 emissions
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


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
    Original Eqn:
    Units: GtCO2
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


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
    Original Eqn:
    Units: GtCO2
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


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
    Original Eqn:
    Units: GtCO2
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return co2_emissions_conv_oil() + co2_emissions_unconv_oil()


def coal_for_elec_co2_emissions():
    """
    Real Name: Coal for Elec CO2 emissions
    Original Eqn:
    Units: GtCO2/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        pe_demand_coal_elec_plants_ej() * mj_per_ej() * gco2_per_mj_coal() / g_per_gt()
        + ped_coal_for_chp_plants_ej() * mj_per_ej() * gco2_per_mj_coal() / g_per_gt()
    )


def coal_for_heat_co2_emissions():
    """
    Real Name: Coal for Heat CO2 emissions
    Original Eqn:
    Units: GtCO2/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


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
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return share_ped_nre_liquids() * real_fe_consumption_liquids_ej()


def fes_coal():
    """
    Real Name: FES coal
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return pec_coal() - ped_coal_total_primary_uses()


def gas_for_elec_co2_emissions():
    """
    Real Name: Gas for Elec CO2 emissions
    Original Eqn:
    Units: GtCO2/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


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
    Original Eqn:
    Units: GtCO2/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


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
    Original Eqn:
    Units: GtCO2/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


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
    Original Eqn:
    Units: GtCO2/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


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
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"])


def oil_for_elec_co2_emissions():
    """
    Real Name: Oil for Elec CO2 emissions
    Original Eqn:
    Units: GtCO2/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


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
    Original Eqn:
    Units: GtCO2/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


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
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


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
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return float(pes_res_for_heat_by_techn().loc["solid bioE heat"])


def ratio_elec_co2_emissions():
    """
    Real Name: ratio Elec CO2 emissions
    Original Eqn:
    Units: GtCO2/EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(total_elec_co2_emissions(), total_fe_elec_consumption_ej())


def ratio_gases_co2_emissions():
    """
    Real Name: ratio Gases CO2 emissions
    Original Eqn:
    Units: GtCO2/EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(gases_fe_co2_emission(), real_fe_consumption_gases_ej())


def ratio_heat_co2_emissions():
    """
    Real Name: ratio Heat CO2 emissions
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(total_heat_co2_emissions(), total_fed_heat_ej())


def ratio_liquids_co2_emissions():
    """
    Real Name: ratio Liquids CO2 emissions
    Original Eqn:
    Units: GtCO2/EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(liquids_fe_co2_emissions(), total_fec_liquids_aut())


def ratio_solids_co2_emissions():
    """
    Real Name: ratio Solids CO2 emissions
    Original Eqn:
    Units: GtCO2/EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(solids_fe_co2_emissions(), required_fed_solids())


def share_coal_for_elec_co2_emissions():
    """
    Real Name: share coal for Elec CO2 emissions
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(coal_for_elec_co2_emissions(), total_elec_nres_co2_emisions())


def share_gas_for_elec_co2_emissions():
    """
    Real Name: share gas for Elec CO2 emissions
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(gas_for_elec_co2_emissions(), total_elec_nres_co2_emisions())


def share_oil_for_elec_co2_emissions():
    """
    Real Name: share oil for Elec CO2 emissions
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(oil_for_elec_co2_emissions(), total_elec_nres_co2_emisions())


def share_ped_nre_liquids():
    """
    Real Name: share PED NRE liquids
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return 1 - zidz(fes_total_biofuels_production_ej(), ped_liquids_ej())


def share_res():
    """
    Real Name: share RES
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return 1 - total_ped_elec() / total_fe_elec_generation_ej()


def solids_fe_co2_emissions():
    """
    Real Name: Solids FE CO2 emissions
    Original Eqn:
    Units: GtCO2/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


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
    Original Eqn:
    Units: GtCO2/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


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
    Original Eqn:
    Units: GtCO2/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return co2_emissions_conv_gas_without_gtl() + co2_emissions_unconv_gas()


def total_co2_gases_emissoin_test():
    """
    Real Name: TOTAL CO2 gases emissoin test
    Original Eqn:
    Units: GtCO2/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        gas_for_elec_co2_emissions()
        + gas_for_heat_co2_emissions()
        + gases_fe_co2_emission()
    )


def total_elec_co2_emissions():
    """
    Real Name: Total Elec CO2 emissions
    Original Eqn:
    Units: GtCO2/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        total_elec_nres_co2_emisions()
        + float(pe_real_generation_res_elec().loc["solid bioE elec"])
        * mj_per_ej()
        * gco2_per_mj_conv_gas()
        / g_per_gt()
    )


def total_elec_nres_co2_emisions():
    """
    Real Name: Total Elec NRES CO2 emisions
    Original Eqn:
    Units: GtCO2/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        coal_for_elec_co2_emissions()
        + gas_for_elec_co2_emissions()
        + oil_for_elec_co2_emissions()
    )


def total_fe_co2_emissions():
    """
    Real Name: Total FE CO2 emissions
    Original Eqn:
    Units: GtCO2/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return sum(
        total_per_fe_co2_emissions().rename({"final sources": "final sources!"}),
        dim=["final sources!"],
    )


def total_fe_elec_generation_ej():
    """
    Real Name: Total FE Elec generation EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return total_fe_elec_generation_twh_aut() * ej_per_twh()


def total_fec_liquids_aut():
    """
    Real Name: Total FEC liquids AUT
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return real_fe_consumption_liquids_ej() + gtl_production() + ctl_production()


def total_fed_solids_ej():
    """
    Real Name: Total FED solids EJ
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return fes_coal() + modern_solids_bioe_demand_households()


def total_heat_co2_emissions():
    """
    Real Name: Total Heat CO2 emissions
    Original Eqn:
    Units: GtCO2/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


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
    Original Eqn:
    Units: EJ/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


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
    Units: GtCO2/Year
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['final sources']


    """
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[{"final sources": ["heat"]}] = total_heat_co2_emissions()
    value.loc[{"final sources": ["liquids"]}] = liquids_fe_co2_emissions()
    value.loc[{"final sources": ["gases"]}] = gases_fe_co2_emission()
    value.loc[{"final sources": ["solids"]}] = solids_fe_co2_emissions()
    value.loc[{"final sources": ["electricity"]}] = total_elec_co2_emissions()
    return value
