"""
Module ch4_emissions_mix
Translated using PySD version 3.0.1
"""


@component.add(
    name="CH4 emissions extraction coal",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "coal_in_fec_aut": 1,
        "pe_demand_coal_elec_plants_ej": 1,
        "ped_coal_for_chp_plants_ej": 1,
        "ped_coal_for_ctl_ej": 1,
        "ped_coal_for_heat_plants_ej": 1,
        "ped_coal_heatnc": 1,
        "mj_per_ej": 1,
        "gch4_per_mj_coal": 1,
        "g_per_mt": 1,
    },
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
    depends_on={
        "fe_nat_gas_consumption": 2,
        "pe_demand_gas_elec_plants_ej": 2,
        "ped_gas_for_chp_plants_ej": 2,
        "ped_gas_heatnc": 2,
        "ped_gases_for_heat_plants_ej": 2,
        "ped_nat_gas_for_gtl_ej": 2,
        "share_unconv_tot_gas": 2,
        "mj_per_ej": 2,
        "gch4_per_mj_conv_gas": 1,
        "g_per_mt": 2,
        "gch4_per_mj_unconv_gas": 1,
    },
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
    depends_on={
        "fed_oil": 1,
        "pe_demand_oil_elec_plants_ej": 1,
        "ped_liquids_heatnc": 1,
        "ped_oil_for_chp_plants_ej": 1,
        "ped_oil_for_heat_plants_ej": 1,
        "mj_per_ej": 1,
        "gch4_per_mj_oil": 1,
        "g_per_mt": 1,
    },
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
    depends_on={
        "ch4_emissions_conv_gas_without_gtl": 1,
        "ch4_emissions_gtl": 1,
        "ch4_emissions_unconv_gas": 1,
    },
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
    depends_on={"ch4_emissions_oil": 1},
)
def ch4_emissions_oil_test():
    return ch4_emissions_oil()


@component.add(
    name="CH4 emissions COAL test",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ch4_emissions_coal_without_ctl": 1, "ch4_emissions_ctl": 1},
)
def ch4_emissions_coal_test():
    return ch4_emissions_coal_without_ctl() + ch4_emissions_ctl()


@component.add(
    name="check hist CH4 emissions",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "total_ch4_emissions_fossil_fuels": 2,
        "total_fe_ch4_emissions": 1,
    },
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
    depends_on={
        "pe_demand_coal_elec_plants_ej": 1,
        "ped_coal_for_chp_plants_ej": 1,
        "mj_per_ej": 1,
        "gch4_per_mj_coal": 1,
        "g_per_mt": 1,
    },
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
    depends_on={
        "ped_coal_heatnc": 1,
        "ped_coal_for_heat_plants_ej": 1,
        "mj_per_ej": 1,
        "gch4_per_mj_coal": 1,
        "g_per_mt": 1,
    },
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
    depends_on={
        "share_biogas_total_pes_gases_aut": 1,
        "real_fe_consumption_gases_ej": 1,
    },
)
def fe_nat_gas_consumption():
    return (1 - share_biogas_total_pes_gases_aut()) * real_fe_consumption_gases_ej()


@component.add(
    name="FEC oil 2",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_fe_consumption_liquids_ej": 1,
        "fes_total_biofuels_production_ej": 1,
    },
)
def fec_oil_2():
    return real_fe_consumption_liquids_ej() - fes_total_biofuels_production_ej()


@component.add(
    name="FED oil",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pec_total_oil": 1, "total_demand_oil_other_fed": 1},
)
def fed_oil():
    return pec_total_oil() - total_demand_oil_other_fed()


@component.add(
    name="Gas for Elec CH4 emissions",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pe_demand_gas_elec_plants_ej": 1,
        "ped_gas_for_chp_plants_ej": 1,
        "mj_per_ej": 1,
        "gch4_per_mj_conv_gas": 1,
        "g_per_mt": 1,
    },
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
    depends_on={
        "ped_gases_for_heat_plants_ej": 1,
        "ped_gas_heatnc": 1,
        "mj_per_ej": 1,
        "gch4_per_mj_conv_gas": 1,
        "g_per_mt": 1,
    },
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
    depends_on={
        "fe_nat_gas_consumption": 1,
        "mj_per_ej": 1,
        "gch4_per_mj_conv_gas": 1,
        "g_per_mt": 1,
    },
)
def gases_fe_ch4_emission():
    return fe_nat_gas_consumption() * mj_per_ej() * gch4_per_mj_conv_gas() / g_per_mt()


@component.add(
    name="Liquids FE CH4 emissions",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fed_oil": 1,
        "mj_per_ej": 3,
        "gch4_per_mj_oil": 1,
        "g_per_mt": 3,
        "gch4_per_mj_ctl": 1,
        "ped_coal_for_ctl_ej": 1,
        "ped_nat_gas_for_gtl_ej": 1,
        "gch4_per_mj_gtl": 1,
    },
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
    depends_on={
        "pe_demand_oil_elec_plants_ej": 1,
        "ped_oil_for_chp_plants_ej": 1,
        "mj_per_ej": 1,
        "gch4_per_mj_oil": 1,
        "g_per_mt": 1,
    },
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
    depends_on={
        "ped_oil_for_heat_plants_ej": 1,
        "ped_liquids_heatnc": 1,
        "mj_per_ej": 1,
        "gch4_per_mj_oil": 1,
        "g_per_mt": 1,
    },
)
def oil_for_heat_ch4_emissions():
    return (
        (ped_oil_for_heat_plants_ej() + ped_liquids_heatnc())
        * mj_per_ej()
        * gch4_per_mj_oil()
        / g_per_mt()
    )


@component.add(
    name="PES oil 2",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ped_nre_liquids": 1,
        "other_liquids_required_ej": 1,
        "pe_demand_oil_elec_plants_ej": 1,
        "ped_liquids_heatnc": 1,
        "ped_oil_for_chp_plants_ej": 1,
        "ped_oil_for_heat_plants_ej": 1,
    },
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
    depends_on={"total_elec_nres_ch4_emissions": 1, "total_fe_elec_consumption_ej": 1},
)
def ratio_elec_ch4_emissions():
    return zidz(total_elec_nres_ch4_emissions(), total_fe_elec_consumption_ej())


@component.add(
    name="ratio Gases CH4 emissions",
    units="MtCH4/EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gases_fe_ch4_emission": 1, "real_fe_consumption_gases_ej": 1},
)
def ratio_gases_ch4_emissions():
    return zidz(gases_fe_ch4_emission(), real_fe_consumption_gases_ej())


@component.add(
    name="ratio Heat CH4 emissions",
    units="MtCH4/EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_heat_ch4_emissions": 1, "total_fed_heat_ej": 1},
)
def ratio_heat_ch4_emissions():
    return zidz(total_heat_ch4_emissions(), total_fed_heat_ej())


@component.add(
    name="ratio Liquids CH4 emissions",
    units="MtCH4/EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"liquids_fe_ch4_emissions": 1, "total_fec_liquids": 1},
)
def ratio_liquids_ch4_emissions():
    return zidz(liquids_fe_ch4_emissions(), total_fec_liquids())


@component.add(
    name="ratio Solids CH4 emissions",
    units="MtCH4/EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"solids_fe_ch4_emissions": 1, "required_fed_solids": 1},
)
def ratio_solids_ch4_emissions():
    return zidz(solids_fe_ch4_emissions(), required_fed_solids())


@component.add(
    name="share coal for Elec CH4 emissions",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"coal_for_elec_ch4_emissions": 1, "total_elec_nres_ch4_emissions": 1},
)
def share_coal_for_elec_ch4_emissions():
    return zidz(coal_for_elec_ch4_emissions(), total_elec_nres_ch4_emissions())


@component.add(
    name="share gas for Elec CH4 emissions",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gas_for_elec_ch4_emissions": 1, "total_elec_nres_ch4_emissions": 1},
)
def share_gas_for_elec_ch4_emissions():
    return zidz(gas_for_elec_ch4_emissions(), total_elec_nres_ch4_emissions())


@component.add(
    name="share oil for Elec CH4 emissions",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oil_for_elec_ch4_emissions": 1, "total_elec_nres_ch4_emissions": 1},
)
def share_oil_for_elec_ch4_emissions():
    return zidz(oil_for_elec_ch4_emissions(), total_elec_nres_ch4_emissions())


@component.add(
    name="Solids FE CH4 emissions",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "coal_in_fec_aut": 1,
        "mj_per_ej": 1,
        "gch4_per_mj_coal": 1,
        "g_per_mt": 1,
    },
)
def solids_fe_ch4_emissions():
    return coal_in_fec_aut() * mj_per_ej() * gch4_per_mj_coal() / g_per_mt()


@component.add(
    name="Total CH4 emission sper sector",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ch4_emissions_extraction_coal": 1,
        "ch4_emissions_extraction_gas": 1,
        "ch4_emissions_extraction_oil": 1,
    },
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
    depends_on={
        "ch4_emissions_coal_test": 1,
        "ch4_emissions_gas_test": 1,
        "ch4_emissions_oil_test": 1,
    },
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
    depends_on={
        "pe_demand_oil_elec_plants_ej": 1,
        "ped_oil_for_chp_plants_ej": 1,
        "ped_oil_for_heat_plants_ej": 1,
        "ped_liquids_heatnc": 1,
    },
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
    depends_on={
        "coal_for_elec_ch4_emissions": 1,
        "gas_for_elec_ch4_emissions": 1,
        "oil_for_elec_ch4_emissions": 1,
    },
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
    depends_on={"total_per_fe_ch4_emissions": 1},
)
def total_fe_ch4_emissions():
    return sum(
        total_per_fe_ch4_emissions().rename({"final sources": "final sources!"}),
        dim=["final sources!"],
    )


@component.add(
    name="Total FEC liquids",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_fe_consumption_liquids_ej": 1,
        "ctl_production": 1,
        "gtl_production": 1,
    },
)
def total_fec_liquids():
    return real_fe_consumption_liquids_ej() + ctl_production() + gtl_production()


@component.add(
    name="Total Heat CH4 emissions",
    units="MtCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "coal_for_heat_ch4_emissions": 1,
        "gas_for_heat_ch4_emissions": 1,
        "oil_for_heat_ch4_emissions": 1,
    },
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
    depends_on={
        "total_elec_nres_ch4_emissions": 1,
        "total_heat_ch4_emissions": 1,
        "liquids_fe_ch4_emissions": 1,
        "gases_fe_ch4_emission": 1,
        "solids_fe_ch4_emissions": 1,
    },
)
def total_per_fe_ch4_emissions():
    value = xr.DataArray(
        np.nan, {"final sources": _subscript_dict["final sources"]}, ["final sources"]
    )
    value.loc[["electricity"]] = total_elec_nres_ch4_emissions()
    value.loc[["heat"]] = total_heat_ch4_emissions()
    value.loc[["liquids"]] = liquids_fe_ch4_emissions()
    value.loc[["gases"]] = gases_fe_ch4_emission()
    value.loc[["solids"]] = solids_fe_ch4_emissions()
    return value
