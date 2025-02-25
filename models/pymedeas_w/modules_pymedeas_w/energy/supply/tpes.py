"""
Module energy.supply.tpes
Translated using PySD version 3.14.2
"""

@component.add(
    name="abundance_TPE",
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
    name="Dynamic_quality_of_electricity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_tfec": 1,
        "total_real_nonenergy_use_consumption_ej": 1,
        "tpes_ej": 1,
    },
)
def dynamic_quality_of_electricity():
    """
    Dynamic quality of electricity (TFES/TPES, the latter without taking into account the non-energy uses).
    """
    return real_tfec() / (tpes_ej() - total_real_nonenergy_use_consumption_ej())


@component.add(
    name="quality_of_electricity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "staticdynamic_quality_of_electricity": 1,
        "quality_of_electricity_2015": 1,
        "dynamic_quality_of_electricity": 1,
    },
)
def quality_of_electricity():
    """
    Quality of electricity (TFES/TPES, the latter without taking into account the non-energy uses).
    """
    return if_then_else(
        staticdynamic_quality_of_electricity() == 1,
        lambda: quality_of_electricity_2015(),
        lambda: dynamic_quality_of_electricity(),
    )


@component.add(
    name="quality_of_electricity_2015",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_quality_of_electricity_2015": 1},
    other_deps={
        "_sampleiftrue_quality_of_electricity_2015": {
            "initial": {"dynamic_quality_of_electricity": 1},
            "step": {"time": 1, "dynamic_quality_of_electricity": 1},
        }
    },
)
def quality_of_electricity_2015():
    """
    Quality of electricity until the year 2015.
    """
    return _sampleiftrue_quality_of_electricity_2015()


_sampleiftrue_quality_of_electricity_2015 = SampleIfTrue(
    lambda: time() < 2015,
    lambda: dynamic_quality_of_electricity(),
    lambda: dynamic_quality_of_electricity(),
    "_sampleiftrue_quality_of_electricity_2015",
)


@component.add(
    name='"static/dynamic_quality_of_electricity?"',
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
    name="Total_extraction_NRE_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_coal_ej": 1,
        "real_extraction_conv_gas": 1,
        "real_extraction_conv_oil": 1,
        "real_extraction_unconv_gas": 1,
        "real_extraction_unconv_oil_ej": 1,
        "extraction_uranium_ej": 1,
    },
)
def total_extraction_nre_ej():
    """
    Annual total extraction of non-renewable energy resources.
    """
    return (
        extraction_coal_ej()
        + real_extraction_conv_gas()
        + real_extraction_conv_oil()
        + real_extraction_unconv_gas()
        + real_extraction_unconv_oil_ej()
        + extraction_uranium_ej()
    )


@component.add(
    name="TPE_from_RES_EJ",
    units="EJ/year",
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
    name="TPED_by_fuel",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extraction_uranium_ej": 1,
        "pe_supply_res_nonelec_ej": 1,
        "pe_elec_generation_from_res_ej": 1,
        "ped_total_oil_ej": 1,
        "ped_coal_ej": 1,
        "ped_nat_gas_ej": 1,
        "pes_waste": 1,
    },
)
def tped_by_fuel():
    """
    Total primary energy demand by fuel.
    """
    return (
        extraction_uranium_ej()
        + pe_supply_res_nonelec_ej()
        + pe_elec_generation_from_res_ej()
        + ped_total_oil_ej()
        + ped_coal_ej()
        + ped_nat_gas_ej()
        + pes_waste()
    )


@component.add(
    name="TPES_EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_extraction_nre_ej": 1, "tpe_from_res_ej": 1, "pes_waste": 1},
)
def tpes_ej():
    """
    Total Primary Energy Supply.
    """
    return total_extraction_nre_ej() + tpe_from_res_ej() + pes_waste()


@component.add(
    name="tpes_intensity_ej_tdollar",
    units="EJ/(year*T$)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tpes_ej": 1, "gdp": 1},
)
def tpes_intensity_ej_tdollar():
    return tpes_ej() / gdp()


@component.add(
    name="Year_scarcity_TPE",
    units="year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"abundance_tpe": 1, "time": 1},
)
def year_scarcity_tpe():
    """
    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_tpe() > 0.95, lambda: 0, lambda: time())
