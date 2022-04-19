"""
Module co2_emissions_mix
Translated using PySD version 3.0.0
"""


@component.add(
    name="check historic CO2 emissions", comp_type="Auxiliary", comp_subtype="Normal"
)
def check_historic_co2_emissions():
    return if_then_else(
        time() < 2015,
        lambda: (total_fe_co2_emissions() - total_co2_emissions_all_fuels())
        * 100
        / co2_fossil_fuel_emissions(),
        lambda: 0,
    )


@component.add(
    name="CO2 emissions COAL",
    units="GtCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def co2_emissions_coal():
    return (
        modern_solids_bioe_demand_households()
        * gco2_per_mj_conv_gas()
        * mj_per_ej()
        / g_per_gt()
        + coal_for_elec_co2_emissions()
        + coal_for_heat_co2_emissions()
    )


@component.add(
    name="CO2 emissions liquids",
    units="GtCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def co2_emissions_liquids():
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


@component.add(
    name="CO2 emissions OIL test",
    units="GtCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def co2_emissions_oil_test():
    return co2_emissions_conv_oil() + co2_emissions_unconv_oil()


@component.add(
    name="Coal for Elec CO2 emissions",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def coal_for_elec_co2_emissions():
    return (
        pe_demand_coal_elec_plants_ej() * mj_per_ej() * gco2_per_mj_coal() / g_per_gt()
        + ped_coal_for_chp_plants_ej() * mj_per_ej() * gco2_per_mj_coal() / g_per_gt()
    )


@component.add(
    name="Coal for Heat CO2 emissions",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def coal_for_heat_co2_emissions():
    return (
        (ped_coal_heatnc() + ped_coal_for_heat_plants_ej())
        * mj_per_ej()
        * gco2_per_mj_coal()
        / g_per_gt()
    )


@component.add(
    name="FEC oil EJ", units="EJ/Year", comp_type="Auxiliary", comp_subtype="Normal"
)
def fec_oil_ej():
    return share_ped_nre_liquids() * real_fe_consumption_liquids_ej()


@component.add(
    name="FES coal", units="EJ/Year", comp_type="Auxiliary", comp_subtype="Normal"
)
def fes_coal():
    return pec_coal() - ped_coal_total_primary_uses()


@component.add(
    name="Gas for Elec CO2 emissions",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def gas_for_elec_co2_emissions():
    return (
        pe_demand_gas_elec_plants_ej() + ped_gas_for_chp_plants_ej()
    ) * gco2_per_mj_conv_gas() * mj_per_ej() / g_per_gt() + (
        pe_demand_gas_elec_plants_ej() + ped_gas_for_chp_plants_ej()
    ) * (
        1 - share_conv_vs_total_gas_extraction_eu()
    ) * gco2_per_mj_unconv_gas() * mj_per_ej() / g_per_gt()


@component.add(
    name="Gas for Heat CO2 emissions",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def gas_for_heat_co2_emissions():
    return (
        (ped_gases_for_heat_plants_ej() + ped_gas_heatnc())
        * mj_per_ej()
        * gco2_per_mj_conv_gas()
        / g_per_gt()
    )


@component.add(
    name="Gases FE CO2 emission",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def gases_fe_co2_emission():
    return (
        (real_fe_consumption_gases_ej() - non_energy_use_gas_demand())
        * mj_per_ej()
        * gco2_per_mj_conv_gas()
        / g_per_gt()
    )


@component.add(
    name="Liquids FE CO2 emissions",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def liquids_fe_co2_emissions():
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


@component.add(
    name="non energy use gas demand",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def non_energy_use_gas_demand():
    return float(nonenergy_use_demand_by_final_fuel_ej().loc["gases"])


@component.add(
    name="Oil for Elec CO2 emissions",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def oil_for_elec_co2_emissions():
    return (
        pe_demand_oil_elec_plants_ej() + ped_oil_for_chp_plants_ej()
    ) * share_conv_vs_total_oil_extraction_eu() * mj_per_ej() * gco2_per_mj_conv_oil() / g_per_gt() + (
        pe_demand_oil_elec_plants_ej() + ped_oil_for_chp_plants_ej()
    ) * (
        1 - share_conv_vs_total_oil_extraction_eu()
    ) * mj_per_ej() * gco2_per_mj_unconv_oil() / g_per_gt()


@component.add(
    name="Oil for Heat CO2 emissions",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def oil_for_heat_co2_emissions():
    return (
        ped_oil_for_heat_plants_ej() + ped_liquids_heatnc()
    ) * share_conv_vs_total_oil_extraction_eu() * mj_per_ej() * gco2_per_mj_conv_oil() / g_per_gt() + (
        ped_oil_for_heat_plants_ej() + ped_liquids_heatnc()
    ) * (
        1 - share_conv_vs_total_oil_extraction_eu()
    ) * mj_per_ej() * gco2_per_mj_unconv_oil() / g_per_gt()


@component.add(
    name="PED coal total primary uses",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ped_coal_total_primary_uses():
    return (
        pe_demand_coal_elec_plants_ej()
        + ped_coal_for_chp_plants_ej()
        + ped_coal_for_ctl_ej()
        + ped_coal_for_heat_plants_ej()
        + ped_coal_heatnc()
    )


@component.add(
    name="PES solids BioE for heat",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def pes_solids_bioe_for_heat():
    return float(pes_res_for_heat_by_techn().loc["solid bioE heat"])


@component.add(
    name="ratio Elec CO2 emissions",
    units="GtCO2/EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ratio_elec_co2_emissions():
    return zidz(total_elec_co2_emissions(), total_fe_elec_consumption_ej())


@component.add(
    name="ratio Gases CO2 emissions",
    units="GtCO2/EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ratio_gases_co2_emissions():
    return zidz(gases_fe_co2_emission(), real_fe_consumption_gases_ej())


@component.add(
    name="ratio Heat CO2 emissions",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ratio_heat_co2_emissions():
    return zidz(total_heat_co2_emissions(), total_fed_heat_ej())


@component.add(
    name="ratio Liquids CO2 emissions",
    units="GtCO2/EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ratio_liquids_co2_emissions():
    return zidz(liquids_fe_co2_emissions(), total_fec_liquids_aut())


@component.add(
    name="ratio Solids CO2 emissions",
    units="GtCO2/EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ratio_solids_co2_emissions():
    return zidz(solids_fe_co2_emissions(), required_fed_solids())


@component.add(
    name="share coal for Elec CO2 emissions",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_coal_for_elec_co2_emissions():
    return zidz(coal_for_elec_co2_emissions(), total_elec_nres_co2_emisions())


@component.add(
    name="share gas for Elec CO2 emissions",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_gas_for_elec_co2_emissions():
    return zidz(gas_for_elec_co2_emissions(), total_elec_nres_co2_emisions())


@component.add(
    name="share oil for Elec CO2 emissions",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_oil_for_elec_co2_emissions():
    return zidz(oil_for_elec_co2_emissions(), total_elec_nres_co2_emisions())


@component.add(
    name="share PED NRE liquids",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_ped_nre_liquids():
    return 1 - zidz(fes_total_biofuels_production_ej(), ped_liquids_ej())


@component.add(name="share RES", comp_type="Auxiliary", comp_subtype="Normal")
def share_res():
    return 1 - total_ped_elec() / total_fe_elec_generation_ej()


@component.add(
    name="Solids FE CO2 emissions",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def solids_fe_co2_emissions():
    return (
        coal_in_fec_aut() * mj_per_ej() * gco2_per_mj_coal() / g_per_gt()
        + co2_emissions_peat()
        + modern_solids_bioe_demand_households()
        * gco2_per_mj_conv_gas()
        * mj_per_ej()
        / g_per_gt()
    )


@component.add(
    name="Total CO2 emissions all fuels",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_co2_emissions_all_fuels():
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


@component.add(
    name="TOTAL CO2 emissions nat gas",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_co2_emissions_nat_gas():
    return co2_emissions_conv_gas_without_gtl() + co2_emissions_unconv_gas()


@component.add(
    name="TOTAL CO2 gases emissoin test",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_co2_gases_emissoin_test():
    return (
        gas_for_elec_co2_emissions()
        + gas_for_heat_co2_emissions()
        + gases_fe_co2_emission()
    )


@component.add(
    name="Total Elec CO2 emissions",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_elec_co2_emissions():
    return (
        total_elec_nres_co2_emisions()
        + float(pe_real_generation_res_elec().loc["solid bioE elec"])
        * mj_per_ej()
        * gco2_per_mj_conv_gas()
        / g_per_gt()
    )


@component.add(
    name="Total Elec NRES CO2 emisions",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_elec_nres_co2_emisions():
    return (
        coal_for_elec_co2_emissions()
        + gas_for_elec_co2_emissions()
        + oil_for_elec_co2_emissions()
    )


@component.add(
    name="Total FE CO2 emissions",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_fe_co2_emissions():
    return sum(
        total_per_fe_co2_emissions().rename({"final sources": "final sources!"}),
        dim=["final sources!"],
    )


@component.add(
    name="Total FE Elec generation EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_fe_elec_generation_ej():
    return total_fe_elec_generation_twh_aut() * ej_per_twh()


@component.add(
    name="Total FEC liquids AUT",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_fec_liquids_aut():
    return real_fe_consumption_liquids_ej() + gtl_production() + ctl_production()


@component.add(
    name="Total FED solids EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_fed_solids_ej():
    return fes_coal() + modern_solids_bioe_demand_households()


@component.add(
    name="Total Heat CO2 emissions",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_heat_co2_emissions():
    return (
        coal_for_heat_co2_emissions()
        + gas_for_heat_co2_emissions()
        + oil_for_heat_co2_emissions()
        + pes_solids_bioe_for_heat() * mj_per_ej() * gco2_per_mj_conv_gas() / g_per_gt()
    )


@component.add(
    name="Total PED Elec", units="EJ/Year", comp_type="Auxiliary", comp_subtype="Normal"
)
def total_ped_elec():
    return (
        pe_demand_coal_elec_plants_ej()
        + pe_demand_gas_elec_plants_ej()
        + pe_demand_oil_elec_plants_ej()
        + ped_coal_for_chp_plants_ej()
        + ped_gas_for_chp_plants_ej()
        + ped_oil_for_chp_plants_ej()
    )


@component.add(
    name="Total per FE CO2 emissions",
    units="GtCO2/Year",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_per_fe_co2_emissions():
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[{"final sources": ["heat"]}] = total_heat_co2_emissions()
    value.loc[{"final sources": ["liquids"]}] = liquids_fe_co2_emissions()
    value.loc[{"final sources": ["gases"]}] = gases_fe_co2_emission()
    value.loc[{"final sources": ["solids"]}] = solids_fe_co2_emissions()
    value.loc[{"final sources": ["electricity"]}] = total_elec_co2_emissions()
    return value
