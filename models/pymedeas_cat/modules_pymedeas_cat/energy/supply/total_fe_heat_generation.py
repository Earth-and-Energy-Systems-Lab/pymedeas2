"""
Module energy.supply.total_fe_heat_generation
Translated using PySD version 3.14.0
"""

@component.add(
    name="Abundance_heat",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fe_heat_generation": 2, "total_fed_heat_ej": 3},
)
def abundance_heat():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        total_fe_heat_generation() > total_fed_heat_ej(),
        lambda: 1,
        lambda: 1
        - zidz(total_fed_heat_ej() - total_fe_heat_generation(), total_fed_heat_ej()),
    )


@component.add(
    name="Annual_growth_rate_RES_for_heat",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fes_res_for_heat_ej": 1, "fes_res_for_heat_delayed_1yr": 1},
)
def annual_growth_rate_res_for_heat():
    """
    Annual growth rate of heat generation from RES.
    """
    return -1 + zidz(fes_res_for_heat_ej(), fes_res_for_heat_delayed_1yr())


@component.add(
    name="FES_heat_from_BioW",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_real_supply_res_for_heatcom_tot": 1,
        "fe_real_supply_res_for_heatnc_tot_ej": 1,
        "fes_heatcom_from_biogas_ej": 1,
        "fes_heatcom_from_waste_ej": 1,
    },
)
def fes_heat_from_biow():
    """
    Heat generation of total bioenergy and waste (to compare with more common statistics).
    """
    return (
        fe_real_supply_res_for_heatcom_tot()
        + fe_real_supply_res_for_heatnc_tot_ej()
        + fes_heatcom_from_biogas_ej()
        + fes_heatcom_from_waste_ej()
    )


@component.add(
    name="FES_Heat_from_coal",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_coal_for_heatcom_plants": 1,
        "pes_coal_for_heatnc_plants": 1,
        "efficiency_coal_for_heat_plants": 1,
    },
)
def fes_heat_from_coal():
    """
    Heat from Heat plants that burn coal (both commercial and non-commercial).
    """
    return (
        pes_coal_for_heatcom_plants() + pes_coal_for_heatnc_plants()
    ) * efficiency_coal_for_heat_plants()


@component.add(
    name='"FES_Heat_from_nat._gas"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_nat_gas_for_heatcom_plants": 1,
        "pes_nat_gas_for_heatnc_plants": 1,
        "efficiency_gases_for_heat_plants": 1,
    },
)
def fes_heat_from_nat_gas():
    """
    Heat from Heat plants that burn fossil natural gas (both commercial and non-commercial).
    """
    return (
        pes_nat_gas_for_heatcom_plants() + pes_nat_gas_for_heatnc_plants()
    ) * efficiency_gases_for_heat_plants()


@component.add(
    name="FES_Heat_from_oil",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_oil_for_heatcom_plants": 1,
        "pes_oil_for_heatnc_plants": 1,
        "efficiency_liquids_for_heat_plants": 1,
    },
)
def fes_heat_from_oil():
    """
    Heat from Heat plants that burn oil (both commercial and non-commercial).
    """
    return (
        pes_oil_for_heatcom_plants() + pes_oil_for_heatnc_plants()
    ) * efficiency_liquids_for_heat_plants()


@component.add(
    name="FES_NRE_for_heat",
    units="EJ/year",
    subscripts=["primary_sources"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fes_heatcom_fossil_fuels_chp_plants_ej": 3,
        "fes_heat_from_coal": 1,
        "fes_heat_from_nat_gas": 1,
        "fes_heat_from_oil": 1,
        "fes_heatcom_nuclear_chp_plants_ej": 1,
    },
)
def fes_nre_for_heat():
    """
    Heat from non-renewable energy resources.
    """
    value = xr.DataArray(
        np.nan,
        {"primary_sources": _subscript_dict["primary_sources"]},
        ["primary_sources"],
    )
    value.loc[["coal"]] = (
        float(fes_heatcom_fossil_fuels_chp_plants_ej().loc["coal"])
        + fes_heat_from_coal()
    )
    value.loc[["natural_gas"]] = (
        float(fes_heatcom_fossil_fuels_chp_plants_ej().loc["natural_gas"])
        + fes_heat_from_nat_gas()
    )
    value.loc[["oil"]] = (
        float(fes_heatcom_fossil_fuels_chp_plants_ej().loc["oil"]) + fes_heat_from_oil()
    )
    value.loc[["others"]] = fes_heatcom_nuclear_chp_plants_ej()
    return value


@component.add(
    name="FES_RES_for_heat_delayed_1yr",
    units="EJ/year",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_fes_res_for_heat_delayed_1yr": 1},
    other_deps={
        "_delayfixed_fes_res_for_heat_delayed_1yr": {
            "initial": {},
            "step": {"fes_res_for_heat_ej": 1},
        }
    },
)
def fes_res_for_heat_delayed_1yr():
    """
    Heat from renewable energy sources delayed 1 year.
    """
    return _delayfixed_fes_res_for_heat_delayed_1yr()


_delayfixed_fes_res_for_heat_delayed_1yr = DelayFixed(
    lambda: fes_res_for_heat_ej(),
    lambda: 1,
    lambda: 0.04,
    time_step,
    "_delayfixed_fes_res_for_heat_delayed_1yr",
)


@component.add(
    name="FES_RES_for_heat_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_real_supply_res_for_heatcom_tot": 1,
        "fe_real_supply_res_for_heatnc_tot_ej": 1,
        "fes_heatcom_from_biogas_ej": 1,
    },
)
def fes_res_for_heat_ej():
    """
    Heat from renewable energy sources.
    """
    return (
        fe_real_supply_res_for_heatcom_tot()
        + fe_real_supply_res_for_heatnc_tot_ej()
        + fes_heatcom_from_biogas_ej()
    )


@component.add(
    name='"PES_coal_for_Heat-com_plants"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_coal_cat": 1,
        "imports_cat_coal_from_row_ej": 1,
        "share_coal_dem_for_heatcom": 1,
    },
)
def pes_coal_for_heatcom_plants():
    """
    Primary energy supply of coal for commercial Heat plants.
    """
    return (
        extraction_coal_cat() + imports_cat_coal_from_row_ej()
    ) * share_coal_dem_for_heatcom()


@component.add(
    name='"PES_coal_for_Heat-nc_plants"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_coal_cat": 1,
        "imports_cat_coal_from_row_ej": 1,
        "share_coal_dem_for_heatnc": 1,
    },
)
def pes_coal_for_heatnc_plants():
    """
    Primary energy supply of coal for non-commercial Heat plants.
    """
    return (
        extraction_coal_cat() + imports_cat_coal_from_row_ej()
    ) * share_coal_dem_for_heatnc()


@component.add(
    name='"PES_nat._gas_for_Heat-com_plants"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_nat_gas_cat_": 1,
        "imports_cat_nat_gas_from_row_ej": 1,
        "share_nat_gas_dem_for_heatcom": 1,
    },
)
def pes_nat_gas_for_heatcom_plants():
    """
    Primary energy supply of fossil natural gas for commercial Heat plants.
    """
    return (
        pes_nat_gas_cat_() + imports_cat_nat_gas_from_row_ej()
    ) * share_nat_gas_dem_for_heatcom()


@component.add(
    name='"PES_nat._gas_for_Heat-nc_plants"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "imports_cat_nat_gas_from_row_ej": 1,
        "pes_gases": 1,
        "ped_nat_gas_for_gtl_ej": 1,
        "share_gases_dem_for_heatnc": 1,
    },
)
def pes_nat_gas_for_heatnc_plants():
    """
    Primary energy supply of natural gas for non-commercial Heat plants.
    """
    return (
        imports_cat_nat_gas_from_row_ej() + pes_gases() - ped_nat_gas_for_gtl_ej()
    ) * share_gases_dem_for_heatnc()


@component.add(
    name='"PES_oil_for_Heat-com_plants"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pes_total_oil_ej_cat": 1,
        "imports_cat_total_oil_from_row_ej": 1,
        "share_oil_dem_for_heatcom": 1,
    },
)
def pes_oil_for_heatcom_plants():
    """
    Primary energy supply of oil for commercial Heat plants.
    """
    return (
        pes_total_oil_ej_cat() + imports_cat_total_oil_from_row_ej()
    ) * share_oil_dem_for_heatcom()


@component.add(
    name='"PES_oil_for_Heat-nc_plants"',
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "imports_cat_total_oil_from_row_ej": 1,
        "pes_liquids": 1,
        "share_liquids_dem_for_heatnc": 1,
    },
)
def pes_oil_for_heatnc_plants():
    """
    Primary energy supply of natural oil for non-commercial Heat plants.
    """
    return (
        imports_cat_total_oil_from_row_ej() + pes_liquids()
    ) * share_liquids_dem_for_heatnc()


@component.add(
    name="share_RES_heat_generation",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fes_res_for_heat_ej": 1, "total_fe_heat_generation": 1},
)
def share_res_heat_generation():
    """
    Share of RES in the total heat generation.
    """
    return fes_res_for_heat_ej() / total_fe_heat_generation()


@component.add(
    name="Total_FE_Heat_consumption_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_fe_heat_generation": 1,
        "share_heat_distribution_losses": 1,
        "total_fed_heat_ej": 1,
    },
)
def total_fe_heat_consumption_ej():
    """
    Total final heat consumption (fossil fuels, nuclear, waste & renewables) (EJ).
    """
    return np.minimum(
        total_fe_heat_generation() / (1 + share_heat_distribution_losses()),
        total_fed_heat_ej(),
    )


@component.add(
    name="Total_FE_Heat_generation",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fes_res_for_heat_ej": 1,
        "fes_heatcom_from_waste_ej": 1,
        "fes_nre_for_heat": 1,
    },
)
def total_fe_heat_generation():
    """
    Total final heat generation (fossil fuels, nuclear, waste & renewables) (EJ).
    """
    return (
        fes_res_for_heat_ej()
        + fes_heatcom_from_waste_ej()
        + sum(
            fes_nre_for_heat().rename({"primary_sources": "primary_sources!"}),
            dim=["primary_sources!"],
        )
    )


@component.add(
    name="Year_scarcity_Heat",
    units="year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_heat": 1, "time": 1},
)
def year_scarcity_heat():
    """
    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_heat() > 0.95, lambda: 0, lambda: time())
