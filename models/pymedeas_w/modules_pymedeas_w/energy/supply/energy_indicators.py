"""
Module energy_indicators
Translated using PySD version 2.2.3
"""


def average_elec_consumption_per_capita():
    """
    Real Name: Average elec consumption per capita
    Original Eqn:
    Units: kWh/people
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Electricity consumption per capita (kWh per capita).
    """
    return total_fe_elec_consumption_twh() * kwh_per_twh() / population()


def average_tpes_per_capita():
    """
    Real Name: Average TPES per capita
    Original Eqn:
    Units: GJ/(year*people)
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Average Total Primary Energy Supply per capita (GJ per capita).
    """
    return tpes_ej() * gj_per_ej() / population()


def average_tpespc_without_trad_biomass():
    """
    Real Name: "Average TPESpc (without trad biomass)"
    Original Eqn:
    Units: GJ/people
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Average per capita TPES without accounting for the energy supplied by traditional biomass. The population considered for estimating the average is not the global population, but the share of the population not relying on traditional biomass for covering their energy uses.
    """
    return (
        tpes_without_trad_biomass() * gj_per_ej() / pop_not_dependent_on_trad_biomass()
    )


def gj_per_ej():
    """
    Real Name: GJ per EJ
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Conversion from GJ to EJ (1 EJ = 1e9 GJ).
    """
    return 1000000000.0


def kwh_per_twh():
    """
    Real Name: kWh per TWh
    Original Eqn:
    Units: kWh/TWh
    Limits: (None, None)
    Type: Constant
    Subs: []

    Conversion between kWh and TWh (1 TWh=1e9 kWh).
    """
    return 1000000000.0


def net_tfec_per_capita():
    """
    Real Name: Net TFEC per capita
    Original Eqn:
    Units: GJ/person
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(real_tfec() * gj_per_ej(), population())


def pop_not_dependent_on_trad_biomass():
    """
    Real Name: Pop not dependent on trad biomass
    Original Eqn:
    Units: people
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Global population not dependent on traditional biomass.
    """
    return population() - population_dependent_on_trad_biomass()


def tfec_from_res_per_capita():
    """
    Real Name: TFEC from RES per capita
    Original Eqn:
    Units: GJ/person
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(tfec_res_ej() * gj_per_ej(), population())


def tfec_per_capita():
    """
    Real Name: TFEC per capita
    Original Eqn:
    Units: GJ/person
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(real_tfec() * gj_per_ej(), population())


def tfec_res_ej():
    """
    Real Name: TFEC RES EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total final energy consumption from RES.
    """
    return (
        fe_tot_generation_all_res_elec_ej()
        + fes_res_for_heat_ej()
        + pe_traditional_biomass_consum_ej()
        + fes_total_biofuels()
        + fes_total_biogas()
    )


def tpes_without_trad_biomass():
    """
    Real Name: "TPES (without trad biomass)"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    TPES without accounting for traditional biomass.
    """
    return tpes_ej() - pe_traditional_biomass_ej_delayed_1yr()
