"""
Module tpes
Translated using PySD version 2.1.0
"""


def abundance_tpe():
    """
    Real Name: abundance TPE
    Original Eqn: IF THEN ELSE(TPES EJ>TPED by fuel, 1, 1-((TPED by fuel -TPES EJ)/TPED by fuel))
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    The parameter abundance varies between (1;0). Abundance=1 while the supply
        covers the demand; the closest to 0 indicates a higher divergence between
        supply and demand.
    """
    return if_then_else(
        tpes_ej() > tped_by_fuel(),
        lambda: 1,
        lambda: 1 - ((tped_by_fuel() - tpes_ej()) / tped_by_fuel()),
    )


def dynamic_quality_of_electricity():
    """
    Real Name: Dynamic quality of electricity
    Original Eqn: Real TFEC/(TPES EJ-Total real nonenergy use consumption EJ )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Dynamic quality of electricity (TFES/TPES, the latter without taking into
        account the non-energy uses).
    """
    return real_tfec() / (tpes_ej() - total_real_nonenergy_use_consumption_ej())


def percent_res_vs_tpes():
    """
    Real Name: Percent RES vs TPES
    Original Eqn: share RES vs TPES*100
    Units: percent
    Limits: (None, None)
    Type: component
    Subs: None

    Percent of primary energy from RES in the TPES.
    """
    return share_res_vs_tpes() * 100


def quality_of_electricity():
    """
    Real Name: quality of electricity
    Original Eqn: IF THEN ELSE("static/dynamic quality of electricity?"=1,quality of electricity 2015 ,Dynamic quality of electricity)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Quality of electricity (TFES/TPES, the latter without taking into account
        the non-energy uses).
    """
    return if_then_else(
        staticdynamic_quality_of_electricity() == 1,
        lambda: quality_of_electricity_2015(),
        lambda: dynamic_quality_of_electricity(),
    )


def quality_of_electricity_2015():
    """
    Real Name: quality of electricity 2015
    Original Eqn: SAMPLE IF TRUE(Time<2015, Dynamic quality of electricity, Dynamic quality of electricity)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Quality of electricity until the year 2015.
    """
    return _sample_if_true_quality_of_electricity_2015()


def share_res_vs_tpes():
    """
    Real Name: share RES vs TPES
    Original Eqn: TPE from RES EJ/TPES EJ
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of primary energy from RES in the TPES.
    """
    return tpe_from_res_ej() / tpes_ej()


def staticdynamic_quality_of_electricity():
    """
    Real Name: "static/dynamic quality of electricity?"
    Original Eqn: 0
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    This variable controls the method of calculation of the parameter "quality of
        electricity" from static (2015 value) or dynamic (MEDEAS endogenous
        calculation:        1. Static EROI calculation (2015 value)        0. Dynamic EROI calculation (endogenous MEDEAS)
    """
    return 0


def total_extraction_nre_ej():
    """
    Real Name: Total extraction NRE EJ
    Original Eqn: extraction coal EJ+real extraction conv gas EJ+real extraction conv oil EJ +real extraction unconv gas EJ+real extraction unconv oil EJ+extraction uranium EJ
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

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


def tpes_ej():
    """
    Real Name: TPES EJ
    Original Eqn: Total extraction NRE EJ+TPE from RES EJ+PES waste EJ
    Units: EJ/year
    Limits: (None, None)
    Type: component
    Subs: None

    Total Primary Energy Supply.
    """
    return total_extraction_nre_ej() + tpe_from_res_ej() + pes_waste_ej()


def tpes_mtoe():
    """
    Real Name: TPES Mtoe
    Original Eqn: TPES EJ*MToe per EJ
    Units: MToe/year
    Limits: (None, None)
    Type: component
    Subs: None

    Total Primary Energy Supply.
    """
    return tpes_ej() * mtoe_per_ej()


def year_scarcity_tpe():
    """
    Real Name: Year scarcity TPE
    Original Eqn: IF THEN ELSE(abundance TPE>0.95, 0, Time)
    Units: year
    Limits: (None, None)
    Type: component
    Subs: None

    Year when the parameter abundance falls below 0.95, i.e. year when
        scarcity starts.
    """
    return if_then_else(abundance_tpe() > 0.95, lambda: 0, lambda: time())


_sample_if_true_quality_of_electricity_2015 = SampleIfTrue(
    lambda: time() < 2015,
    lambda: dynamic_quality_of_electricity(),
    lambda: dynamic_quality_of_electricity(),
    "_sample_if_true_quality_of_electricity_2015",
)
