"""
Module energy_indicators
Translated using PySD version 2.2.1
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
    Units: GJ/(Year*people)
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


def net_tfec():
    """
    Real Name: Net TFEC
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Net total final energy consumption (final energy minus energy invested to produce energy).
    """
    return real_tfec() - feist_system()


def net_tfec_per_capita():
    """
    Real Name: Net TFEC per capita
    Original Eqn:
    Units: GJ/person
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Net total final energy consumption per capita.
    """
    return zidz(net_tfec() * gj_per_ej(), population())


def physical_energy_intensity_tpes_vs_final():
    """
    Real Name: Physical energy intensity TPES vs final
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Physical energy intensity
    """
    return 1 / share_total_final_energy_vs_tpes()


def physical_energy_intensity_tpes_vs_net():
    """
    Real Name: Physical energy intensity TPES vs net
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Physical energy intensity
    """
    return 1 / share_total_net_energy_vs_tpes()


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


def share_total_net_energy_vs_tpes():
    """
    Real Name: share total net energy vs TPES
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Share of total net energy vs total primary energy supply (without accounting for non-energy uses).
    """
    return zidz(net_tfec(), tpes_ej() - total_real_nonenergy_use_consumption_ej())


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


def tfec_per_capita_before_heat_dem_corr():
    """
    Real Name: TFEC per capita before heat dem corr
    Original Eqn:
    Units: GJ/person
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(real_tfec_before_heat_dem_corr() * gj_per_ej(), population())


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
