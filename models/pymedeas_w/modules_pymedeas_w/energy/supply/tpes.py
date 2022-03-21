"""
Module tpes
Translated using PySD version 2.2.3
"""


def abundance_tpe():
    """
    Real Name: abundance TPE
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    The parameter abundance varies between (1;0). Abundance=1 while the supply covers the demand; the closest to 0 indicates a higher divergence between supply and demand.
    """
    return if_then_else(
        tpes_ej() > tped_by_fuel(),
        lambda: 1,
        lambda: 1 - (tped_by_fuel() - tpes_ej()) / tped_by_fuel(),
    )


def dynamic_quality_of_electricity():
    """
    Real Name: Dynamic quality of electricity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Dynamic quality of electricity (TFES/TPES, the latter without taking into account the non-energy uses).
    """
    return real_tfec() / (tpes_ej() - total_real_nonenergy_use_consumption_ej())


def quality_of_electricity():
    """
    Real Name: quality of electricity
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Quality of electricity (TFES/TPES, the latter without taking into account the non-energy uses).
    """
    return if_then_else(
        staticdynamic_quality_of_electricity() == 1,
        lambda: quality_of_electricity_2015(),
        lambda: dynamic_quality_of_electricity(),
    )


def quality_of_electricity_2015():
    """
    Real Name: quality of electricity 2015
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: []

    Quality of electricity until the year 2015.
    """
    return _sampleiftrue_quality_of_electricity_2015()


_sampleiftrue_quality_of_electricity_2015 = SampleIfTrue(
    lambda: time() < 2015,
    lambda: dynamic_quality_of_electricity(),
    lambda: dynamic_quality_of_electricity(),
    "_sampleiftrue_quality_of_electricity_2015",
)


def staticdynamic_quality_of_electricity():
    """
    Real Name: "static/dynamic quality of electricity?"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    This variable controls the method of calculation of the parameter "quality of electricity" from static (2015 value) or dynamic (MEDEAS endogenous calculation: 1. Static EROI calculation (2015 value) 0. Dynamic EROI calculation (endogenous MEDEAS)
    """
    return 0


def total_extraction_nre_ej():
    """
    Real Name: Total extraction NRE EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Annual total extraction of non-renewable energy resources.
    """
    return (
        extraction_coal_ej()
        + real_extraction_conv_gas_ej()
        + real_extraction_conv_oil_ej()
        + real_extraction_unconv_gas_ej()
        + real_extraction_unconv_oil_ej()
        + extraction_uranium_ej()
    )


def tpe_from_res_ej():
    """
    Real Name: TPE from RES EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total primary energy supply from all RES.
    """
    return pe_elec_generation_from_res_ej() + pe_supply_res_nonelec_ej()


def tped_by_fuel():
    """
    Real Name: TPED by fuel
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total primary energy demand by fuel.
    """
    return (
        extraction_uranium_ej()
        + pe_supply_res_nonelec_ej()
        + pe_elec_generation_from_res_ej()
        + ped_total_oil_ej()
        + ped_coal_ej()
        + ped_nat_gas_ej()
        + pes_waste_ej()
    )


def tpes_ej():
    """
    Real Name: TPES EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total Primary Energy Supply.
    """
    return total_extraction_nre_ej() + tpe_from_res_ej() + pes_waste_ej()


def year_scarcity_tpe():
    """
    Real Name: Year scarcity TPE
    Original Eqn:
    Units: year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Year when the parameter abundance falls below 0.95, i.e. year when scarcity starts.
    """
    return if_then_else(abundance_tpe() > 0.95, lambda: 0, lambda: time())
