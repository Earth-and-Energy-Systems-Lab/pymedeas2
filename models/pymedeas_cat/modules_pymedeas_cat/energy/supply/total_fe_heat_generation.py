"""
Module total_fe_heat_generation
Translated using PySD version 3.0.0
"""


@component.add(
    name="Abundance heat", units="Dmnl", comp_type="Auxiliary", comp_subtype="Normal"
)
def abundance_heat():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        total_fe_heat_generation_ej() > total_fed_heat_ej(),
        lambda: 1,
        lambda: 1
        - zidz(
            total_fed_heat_ej() - total_fe_heat_generation_ej(), total_fed_heat_ej()
        ),
    )


@component.add(
    name="Annual growth rate RES for heat",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def annual_growth_rate_res_for_heat():
    """
    Annual growth rate of heat generation from RES.
    """
    return -1 + fes_res_for_heat_ej() / fes_res_for_heat_delayed_1yr()


@component.add(
    name="FES Heat from coal", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def fes_heat_from_coal():
    """
    Heat from Heat plants that burn coal (both commercial and non-commercial).
    """
    return (
        pes_coal_for_heatcom_plants() + pes_coal_for_heatnc_plants()
    ) * efficiency_coal_for_heat_plants()


@component.add(
    name="FES Heat from oil", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def fes_heat_from_oil():
    """
    Heat from Heat plants that burn oil (both commercial and non-commercial).
    """
    return (
        pes_oil_for_heatcom_plants() + pes_oil_for_heatnc_plants()
    ) * efficiency_liquids_for_heat_plants()


@component.add(
    name="FES NRE for heat", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def fes_nre_for_heat():
    """
    Heat from non-renewable energy resources.
    """
    return (
        fes_heatcom_fossil_fuels_chp_plants_ej()
        + fes_heat_from_coal()
        + fes_heat_from_nat_gas()
        + fes_heat_from_oil()
        + fes_heatcom_nuclear_chp_plants_ej()
    )


@component.add(
    name="FES RES for heat delayed 1yr",
    units="Tdollars/Year",
    comp_type="Stateful",
    comp_subtype="DelayFixed",
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
    name="FES RES for heat EJ", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def fes_res_for_heat_ej():
    """
    Heat from renewable energy sources.
    """
    return (
        fe_real_supply_res_for_heatcom_tot_ej()
        + fe_real_supply_res_for_heatnc_tot_ej()
        + fes_heatcom_from_biogas_ej()
    )


@component.add(
    name="FES heat from BioW", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
)
def fes_heat_from_biow():
    """
    Heat generation of total bioenergy and waste (to compare with more common statistics).
    """
    return (
        fe_real_supply_res_for_heatcom_tot_ej()
        + fe_real_supply_res_for_heatnc_tot_ej()
        + fes_heatcom_from_biogas_ej()
        + fes_heatcom_from_waste_ej()
    )


@component.add(
    name='"FES Heat from nat. gas"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def fes_heat_from_nat_gas():
    """
    Heat from Heat plants that burn fossil natural gas (both commercial and non-commercial).
    """
    return (
        pes_nat_gas_for_heatcom_plants() + pes_nat_gas_for_heatnc_plants()
    ) * efficiency_gases_for_heat_plants()


@component.add(
    name='"PES coal for Heat-com plants"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def pes_coal_for_heatcom_plants():
    """
    Primary energy supply of coal for commercial Heat plants.
    """
    return (
        extraction_coal_aut() + imports_aut_coal_from_row_ej()
    ) * share_coal_dem_for_heatcom()


@component.add(
    name='"PES coal for Heat-nc plants"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def pes_coal_for_heatnc_plants():
    """
    Primary energy supply of coal for non-commercial Heat plants.
    """
    return (
        extraction_coal_aut() + imports_aut_coal_from_row_ej()
    ) * share_coal_dem_for_heatnc()


@component.add(
    name='"PES nat. gas for Heat-com plants"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def pes_nat_gas_for_heatcom_plants():
    """
    Primary energy supply of fossil natural gas for commercial Heat plants.
    """
    return (
        pes_nat_gas_aut_1() + imports_aut_nat_gas_from_row_ej()
    ) * share_nat_gas_dem_for_heatcom()


@component.add(
    name='"PES nat. gas for Heat-nc plants"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def pes_nat_gas_for_heatnc_plants():
    """
    Primary energy supply of natural gas for non-commercial Heat plants.
    """
    return (pes_gases() - ped_nat_gas_for_gtl_ej()) * share_gases_dem_for_heatnc()


@component.add(
    name='"PES oil for Heat-com plants"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def pes_oil_for_heatcom_plants():
    """
    Primary energy supply of oil for commercial Heat plants.
    """
    return (
        pes_total_oil_ej_aut() + imports_aut_total_oil_from_row_ej()
    ) * share_oil_dem_for_heatcom()


@component.add(
    name='"PES oil for Heat-nc plants"',
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def pes_oil_for_heatnc_plants():
    """
    Primary energy supply of natural oil for non-commercial Heat plants.
    """
    return pes_liquids_ej() * share_liquids_dem_for_heatnc()


@component.add(
    name="share RES heat generation",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def share_res_heat_generation():
    """
    Share of RES in the total heat generation.
    """
    return fes_res_for_heat_ej() / total_fe_heat_generation_ej()


@component.add(
    name="Total FE Heat consumption EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_fe_heat_consumption_ej():
    """
    Total final heat consumption (fossil fuels, nuclear, waste & renewables) (EJ).
    """
    return total_fe_heat_generation_ej() / (1 + share_heat_distribution_losses())


@component.add(
    name="Total FE Heat generation EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def total_fe_heat_generation_ej():
    """
    Total final heat generation (fossil fuels, nuclear, waste & renewables) (EJ).
    """
    return fes_res_for_heat_ej() + fes_heatcom_from_waste_ej() + fes_nre_for_heat()


@component.add(
    name="Year scarcity Heat",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def year_scarcity_heat():
    """
    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_heat() > 0.95, lambda: 0, lambda: time())
