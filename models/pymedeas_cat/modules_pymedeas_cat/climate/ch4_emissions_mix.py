"""
Module ch4_emissions_mix
Translated using PySD version 3.0.0
"""


@component.add(
    name="CH4 emissions COAL test",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ch4_emissions_coal_test():
    return ch4_emissions_coal_without_ctl() + ch4_emissions_ctl()


@component.add(
    name="CH4 emissions extraction coal",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ch4_emissions_extraction_coal():
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


@component.add(
    name="CH4 emissions extraction gas",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ch4_emissions_extraction_gas():
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


@component.add(
    name="CH4 emissions extraction OIL",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ch4_emissions_extraction_oil():
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


@component.add(
    name="CH4 emissions GAS test",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ch4_emissions_gas_test():
    return (
        ch4_emissions_conv_gas_without_gtl()
        + ch4_emissions_gtl()
        + ch4_emissions_unconv_gas()
    )


@component.add(
    name="CH4 emissions OIL test",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ch4_emissions_oil_test():
    return ch4_emissions_oil()


@component.add(
    name="check hist CH4 emissions", comp_type="Auxiliary", comp_subtype="Normal"
)
def check_hist_ch4_emissions():
    return if_then_else(
        time() < 2012,
        lambda: (total_fe_ch4_emissions() - total_ch4_emissions_fossil_fuels())
        * 100
        / total_ch4_emissions_fossil_fuels(),
        lambda: 0,
    )


@component.add(
    name="Coal for Elec CH4 emissions",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def coal_for_elec_ch4_emissions():
    return (
        (pe_demand_coal_elec_plants_ej() + ped_coal_for_chp_plants_ej())
        * mj_per_ej()
        * gch4_per_mj_coal()
        / g_per_mt()
    )


@component.add(
    name="Coal for Heat CH4 emissions",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def coal_for_heat_ch4_emissions():
    return (
        (ped_coal_heatnc() + ped_coal_for_heat_plants_ej())
        * mj_per_ej()
        * gch4_per_mj_coal()
        / g_per_mt()
    )


@component.add(
    name="FE nat gas consumption",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def fe_nat_gas_consumption():
    return (1 - share_biogas_total_pes_gases_aut()) * real_fe_consumption_gases_ej()


@component.add(
    name="FEC oil 2", units="EJ/Year", comp_type="Auxiliary", comp_subtype="Normal"
)
def fec_oil_2():
    return real_fe_consumption_liquids_ej() - fes_total_biofuels_production_ej()


@component.add(
    name="FED oil", units="EJ/Year", comp_type="Auxiliary", comp_subtype="Normal"
)
def fed_oil():
    return pec_total_oil() - total_demand_oil_other_fed()


@component.add(
    name="Gas for Elec CH4 emissions",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def gas_for_elec_ch4_emissions():
    return (
        (pe_demand_gas_elec_plants_ej() + ped_gas_for_chp_plants_ej())
        * mj_per_ej()
        * gch4_per_mj_conv_gas()
        / g_per_mt()
    )


@component.add(
    name="Gas for Heat CH4 emissions",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def gas_for_heat_ch4_emissions():
    return (
        (ped_gases_for_heat_plants_ej() + ped_gas_heatnc())
        * mj_per_ej()
        * gch4_per_mj_conv_gas()
        / g_per_mt()
    )


@component.add(
    name="Gases FE CH4 emission",
    units="GtCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def gases_fe_ch4_emission():
    return fe_nat_gas_consumption() * mj_per_ej() * gch4_per_mj_conv_gas() / g_per_mt()


@component.add(
    name="Liquids FE CH4 emissions",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def liquids_fe_ch4_emissions():
    return (
        fed_oil() * mj_per_ej() * gch4_per_mj_oil() / g_per_mt()
        + ped_coal_for_ctl_ej() * mj_per_ej() * gch4_per_mj_ctl() / g_per_mt()
        + ped_nat_gas_for_gtl_ej() * mj_per_ej() * gch4_per_mj_gtl() / g_per_mt()
    )


@component.add(
    name="Oil for Elec CH4 emissions",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def oil_for_elec_ch4_emissions():
    return (
        (pe_demand_oil_elec_plants_ej() + ped_oil_for_chp_plants_ej())
        * mj_per_ej()
        * gch4_per_mj_oil()
        / g_per_mt()
    )


@component.add(
    name="Oil for Heat CH4 emissions",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def oil_for_heat_ch4_emissions():
    return (
        (ped_oil_for_heat_plants_ej() + ped_liquids_heatnc())
        * mj_per_ej()
        * gch4_per_mj_oil()
        / g_per_mt()
    )


@component.add(
    name="PES oil 2", units="EJ/Year", comp_type="Auxiliary", comp_subtype="Normal"
)
def pes_oil_2():
    return (
        ped_nre_liquids()
        - other_liquids_required_ej()
        - pe_demand_oil_elec_plants_ej()
        - ped_liquids_heatnc()
        - ped_oil_for_chp_plants_ej()
        - ped_oil_for_heat_plants_ej()
    )


@component.add(
    name="ratio Elec CH4 emissions",
    units="MtCH4/EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ratio_elec_ch4_emissions():
    return zidz(total_elec_nres_ch4_emissions(), total_fe_elec_consumption_ej())


@component.add(
    name="ratio Gases CH4 emissions",
    units="MtCH4/EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ratio_gases_ch4_emissions():
    return zidz(gases_fe_ch4_emission(), real_fe_consumption_gases_ej())


@component.add(
    name="ratio Heat CH4 emissions",
    units="MtCH4/EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ratio_heat_ch4_emissions():
    return zidz(total_heat_ch4_emissions(), total_fed_heat_ej())


@component.add(
    name="ratio Liquids CH4 emissions",
    units="MtCH4/EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ratio_liquids_ch4_emissions():
    return zidz(liquids_fe_ch4_emissions(), total_fec_liquids())


@component.add(
    name="ratio Solids CH4 emissions",
    units="MtCH4/EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ratio_solids_ch4_emissions():
    return zidz(solids_fe_ch4_emissions(), required_fed_solids())


@component.add(
    name="share coal for Elec CH4 emissions",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_coal_for_elec_ch4_emissions():
    return zidz(coal_for_elec_ch4_emissions(), total_elec_nres_ch4_emissions())


@component.add(
    name="share gas for Elec CH4 emissions",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_gas_for_elec_ch4_emissions():
    return zidz(gas_for_elec_ch4_emissions(), total_elec_nres_ch4_emissions())


@component.add(
    name="share oil for Elec CH4 emissions",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_oil_for_elec_ch4_emissions():
    return zidz(oil_for_elec_ch4_emissions(), total_elec_nres_ch4_emissions())


@component.add(
    name="Solids FE CH4 emissions",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def solids_fe_ch4_emissions():
    return coal_in_fec_aut() * mj_per_ej() * gch4_per_mj_coal() / g_per_mt()


@component.add(
    name="Total CH4 emission sper sector",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_ch4_emission_sper_sector():
    return (
        ch4_emissions_extraction_coal()
        + ch4_emissions_extraction_gas()
        + ch4_emissions_extraction_oil()
    )


@component.add(
    name="Total CH4 emissions",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_ch4_emissions():
    return (
        ch4_emissions_coal_test() + ch4_emissions_gas_test() + ch4_emissions_oil_test()
    )


@component.add(
    name="total demand oil other FED",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_demand_oil_other_fed():
    return (
        pe_demand_oil_elec_plants_ej()
        + ped_oil_for_chp_plants_ej()
        + ped_oil_for_heat_plants_ej()
        + ped_liquids_heatnc()
    )


@component.add(
    name="Total Elec NRES CH4 emissions",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_elec_nres_ch4_emissions():
    return (
        coal_for_elec_ch4_emissions()
        + gas_for_elec_ch4_emissions()
        + oil_for_elec_ch4_emissions()
    )


@component.add(
    name="Total FE CH4 emissions",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_fe_ch4_emissions():
    return sum(
        total_per_fe_ch4_emissions().rename({"final sources": "final sources!"}),
        dim=["final sources!"],
    )


@component.add(
    name="Total FEC liquids", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def total_fec_liquids():
    return real_fe_consumption_liquids_ej() + ctl_production() + gtl_production()


@component.add(
    name="Total Heat CH4 emissions",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_heat_ch4_emissions():
    return (
        coal_for_heat_ch4_emissions()
        + gas_for_heat_ch4_emissions()
        + oil_for_heat_ch4_emissions()
    )


@component.add(
    name="Total per FE CH4 emissions",
    units="MtCH4",
    subscripts=["final sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_per_fe_ch4_emissions():
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[{"final sources": ["electricity"]}] = total_elec_nres_ch4_emissions()
    value.loc[{"final sources": ["heat"]}] = total_heat_ch4_emissions()
    value.loc[{"final sources": ["liquids"]}] = liquids_fe_ch4_emissions()
    value.loc[{"final sources": ["gases"]}] = gases_fe_ch4_emission()
    value.loc[{"final sources": ["solids"]}] = solids_fe_ch4_emissions()
    return value
