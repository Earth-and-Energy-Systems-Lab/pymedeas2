"""
Module energy.supply.tpes
Translated using PySD version 3.10.0
"""


@component.add(
    name="abundance TPE",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tpes_ej": 2, "tped_by_fuel": 3},
)
def abundance_tpe():
    """
    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        tpes_ej() > tped_by_fuel(),
        lambda: 1,
        lambda: 1 - (tped_by_fuel() - tpes_ej()) / tped_by_fuel(),
    )


@component.add(
    name='"g=quality of electricity"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "staticdynamic_quality_of_electricity": 1,
        "quality_of_electricity_2015": 1,
        "share_total_final_energy_vs_tpes": 1,
    },
)
def gquality_of_electricity():
    """
    Quality of electricity (TFES/TPES, the latter without taking into account the non-energy uses), also know as factor "g" in EROI studies.
    """
    return if_then_else(
        staticdynamic_quality_of_electricity() == 1,
        lambda: quality_of_electricity_2015(),
        lambda: share_total_final_energy_vs_tpes(),
    )


@component.add(
    name="quality of electricity 2015",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "share_total_final_energy_vs_tpes": 2},
)
def quality_of_electricity_2015():
    """
    Quality of electricity until the year 2015.
    """
    return if_then_else(
        time() < 2015,
        lambda: share_total_final_energy_vs_tpes(),
        lambda: share_total_final_energy_vs_tpes(),
    )


@component.add(
    name="share imports EU NRE from RoW vs world extraction",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_imports_eu_nre_from_row": 1, "total_extraction_nre_ej_world": 1},
)
def share_imports_eu_nre_from_row_vs_world_extraction():
    return total_imports_eu_nre_from_row() / total_extraction_nre_ej_world()


@component.add(
    name="share imports EU NRE vs TPEC",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_imports_eu_nre_from_row": 1, "tpes_ej": 1},
)
def share_imports_eu_nre_vs_tpec():
    return total_imports_eu_nre_from_row() / tpes_ej()


@component.add(
    name="share total final energy vs TPES",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_tfec": 1,
        "total_real_nonenergy_use_consumption_ej": 1,
        "tpes_ej": 1,
    },
)
def share_total_final_energy_vs_tpes():
    """
    Total final energy vs TPES, the latter without taking into account the non-energy uses. We consider this ratio for the dynamic quality of electricity.
    """
    return real_tfec() / (tpes_ej() - total_real_nonenergy_use_consumption_ej())


@component.add(
    name='"static/dynamic quality of electricity?"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def staticdynamic_quality_of_electricity():
    """
    This variable controls the method of calculation of the parameter "quality of electricity" from static (2015 value) or dynamic (MEDEAS endogenous calculation: 1. Static EROI calculation (2015 value) 0. Dynamic EROI calculation (endogenous MEDEAS)
    """
    return 0


@component.add(
    name="Total consumption NRE EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_coal_eu": 1,
        "imports_eu_coal_from_row_ej": 1,
        "real_extraction_conv_gas_ej": 1,
        "real_extraction_conv_oil_ej": 1,
        "real_extraction_unconv_gas_ej": 1,
        "real_extraction_unconv_oil_ej": 1,
        "extraction_uranium": 1,
        "imports_eu_nat_gas_from_row_ej": 1,
        "imports_eu_total_oil_from_row_ej": 1,
        "extraction_uranium_row": 1,
    },
)
def total_consumption_nre_ej():
    """
    Annual total consumption of non-renewable energy resources.
    """
    return (
        extraction_coal_eu()
        + imports_eu_coal_from_row_ej()
        + real_extraction_conv_gas_ej()
        + real_extraction_conv_oil_ej()
        + real_extraction_unconv_gas_ej()
        + real_extraction_unconv_oil_ej()
        + extraction_uranium()
        + imports_eu_nat_gas_from_row_ej()
        + imports_eu_total_oil_from_row_ej()
        + extraction_uranium_row()
    )


@component.add(
    name="Total imports EU NRE from Row",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_uranium_row": 1,
        "imports_eu_coal_from_row_ej": 1,
        "imports_eu_nat_gas_from_row_ej": 1,
        "imports_eu_total_oil_from_row_ej": 1,
    },
)
def total_imports_eu_nre_from_row():
    return (
        extraction_uranium_row()
        + imports_eu_coal_from_row_ej()
        + imports_eu_nat_gas_from_row_ej()
        + imports_eu_total_oil_from_row_ej()
    )


@component.add(
    name="TPE from RES EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pe_elec_generation_from_res_ej": 1, "pe_supply_res_nonelec_ej": 1},
)
def tpe_from_res_ej():
    """
    Total primary energy supply from all RES.
    """
    return pe_elec_generation_from_res_ej() + pe_supply_res_nonelec_ej()


@component.add(
    name="TPED by fuel",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_uranium": 1,
        "pe_supply_res_nonelec_ej": 1,
        "pe_elec_generation_from_res_ej": 1,
        "ped_total_oil_ej": 1,
        "ped_coal_ej": 1,
        "ped_nat_gas_ej": 1,
        "pes_waste_ej": 1,
    },
)
def tped_by_fuel():
    """
    Total primary energy demand by fuel.
    """
    return (
        extraction_uranium()
        + pe_supply_res_nonelec_ej()
        + pe_elec_generation_from_res_ej()
        + ped_total_oil_ej()
        + ped_coal_ej()
        + ped_nat_gas_ej()
        + pes_waste_ej()
    )


@component.add(
    name="TPES EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_consumption_nre_ej": 1, "tpe_from_res_ej": 1, "pes_waste_ej": 1},
)
def tpes_ej():
    """
    Total Primary Energy Supply.
    """
    return total_consumption_nre_ej() + tpe_from_res_ej() + pes_waste_ej()


@component.add(
    name="Year scarcity TPE",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_tpe": 1, "time": 1},
)
def year_scarcity_tpe():
    """
    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_tpe() > 0.95, lambda: 0, lambda: time())
