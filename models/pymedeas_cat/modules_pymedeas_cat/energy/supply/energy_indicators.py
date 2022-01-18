"""
Module energy_indicators
Translated using PySD version 2.2.0
"""


def annual_share_res_vs_tfec_growth_rate():
    """
    Real Name: Annual share RES vs TFEC growth rate
    Original Eqn: -1+share RES vs TFEC/share RES vs TFEC delayed 1yr
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return -1 + share_res_vs_tfec() / share_res_vs_tfec_delayed_1yr()


def annual_share_res_vs_tpes_growth_rate():
    """
    Real Name: Annual share RES vs TPES growth rate
    Original Eqn: -1+share RES vs TPES/share RES vs TPES delayed 1yr
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return -1 + share_res_vs_tpes() / share_res_vs_tpes_delayed_1yr()


def annual_tfec_res_growth_rate():
    """
    Real Name: Annual TFEC RES growth rate
    Original Eqn: -1+TFEC RES EJ/TFEC RES delayed 1yr
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return -1 + tfec_res_ej() / tfec_res_delayed_1yr()


def annual_tpes_res_growth_rate():
    """
    Real Name: Annual TPES RES growth rate
    Original Eqn: -1+TPE from RES EJ/TPES RES delayed 1yr
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return -1 + tpe_from_res_ej() / tpes_res_delayed_1yr()


def average_elec_consumption_per_capita():
    """
    Real Name: Average elec consumption per capita
    Original Eqn: Total FE Elec consumption TWh*kWh per TWh/Population
    Units: kWh/people
    Limits: (None, None)
    Type: component
    Subs: None

    Electricity consumption per capita (kWh per capita).
    """
    return total_fe_elec_consumption_twh() * kwh_per_twh() / population()


def average_tpes_per_capita():
    """
    Real Name: Average TPES per capita
    Original Eqn: TPES EJ*GJ per EJ/Population
    Units: GJ/(Year*people)
    Limits: (None, None)
    Type: component
    Subs: None

    Average Total Primary Energy Supply per capita (GJ per capita).
    """
    return tpes_ej() * gj_per_ej() / population()


def average_tpespc_without_trad_biomass():
    """
    Real Name: "Average TPESpc (without trad biomass)"
    Original Eqn: "TPES (without trad biomass)"*GJ per EJ/Pop not dependent on trad biomass
    Units: GJ/people
    Limits: (None, None)
    Type: component
    Subs: None

    Average per capita TPES without accounting for the energy supplied by
        traditional biomass. The population considered for estimating the average
        is not the global population, but the share of the population not relying
        on traditional biomass for covering their energy uses.
    """
    return (
        tpes_without_trad_biomass() * gj_per_ej() / pop_not_dependent_on_trad_biomass()
    )


def gj_per_ej():
    """
    Real Name: GJ per EJ
    Original Eqn: 1e+09
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    Conversion from GJ to EJ (1 EJ = 1e9 GJ).
    """
    return 1e09


def kwh_per_twh():
    """
    Real Name: kWh per TWh
    Original Eqn: 1e+09
    Units: kWh/TWh
    Limits: (None, None)
    Type: constant
    Subs: None

    Conversion between kWh and TWh (1 TWh=1e9 kWh).
    """
    return 1e09


def net_tfec():
    """
    Real Name: Net TFEC
    Original Eqn: Real TFEC-FEIst system
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Net total final energy consumption (final energy minus energy invested to
        produce energy).
    """
    return real_tfec() - feist_system()


def net_tfec_per_capita():
    """
    Real Name: Net TFEC per capita
    Original Eqn: ZIDZ( Net TFEC*GJ per EJ, Population )
    Units: GJ/person
    Limits: (None, None)
    Type: component
    Subs: None

    Net total final energy consumption per capita.
    """
    return zidz(net_tfec() * gj_per_ej(), population())


def physical_energy_intensity_tpes_vs_final():
    """
    Real Name: Physical energy intensity TPES vs final
    Original Eqn: 1/share total final energy vs TPES
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Physical energy intensity
    """
    return 1 / share_total_final_energy_vs_tpes()


def physical_energy_intensity_tpes_vs_net():
    """
    Real Name: Physical energy intensity TPES vs net
    Original Eqn: 1/share total net energy vs TPES
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Physical energy intensity
    """
    return 1 / share_total_net_energy_vs_tpes()


def pop_not_dependent_on_trad_biomass():
    """
    Real Name: Pop not dependent on trad biomass
    Original Eqn: Population-Population dependent on trad biomass
    Units: people
    Limits: (None, None)
    Type: component
    Subs: None

    Global population not dependent on traditional biomass.
    """
    return population() - population_dependent_on_trad_biomass()


def share_res_vs_tfec_delayed_1yr():
    """
    Real Name: share RES vs TFEC delayed 1yr
    Original Eqn: DELAY FIXED ( share RES vs TFEC, 1, 0.2786)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _delayfixed_share_res_vs_tfec_delayed_1yr()


def share_res_vs_tpes_delayed_1yr():
    """
    Real Name: share RES vs TPES delayed 1yr
    Original Eqn: DELAY FIXED ( share RES vs TPES, 1, 0.2137)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _delayfixed_share_res_vs_tpes_delayed_1yr()


def share_tfec_before_heat_dem_corr_vs_real_tfec():
    """
    Real Name: share TFEC before heat dem corr vs real TFEC
    Original Eqn: Real TFEC/Real TFEC before heat dem corr
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of total final energy consumption before heat demand correction vs.
        real TFEC as estimated in MEDEAS correcting for heat demand for
        non-commercial sectors.
    """
    return real_tfec() / real_tfec_before_heat_dem_corr()


def share_total_net_energy_vs_tpes():
    """
    Real Name: share total net energy vs TPES
    Original Eqn: ZIDZ( Net TFEC, (TPES EJ-"Total real non-energy use consumption EJ") )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of total net energy vs total primary energy supply (without
        accounting for non-energy uses).
    """
    return zidz(net_tfec(), (tpes_ej() - total_real_nonenergy_use_consumption_ej()))


def tfec_from_res_per_capita():
    """
    Real Name: TFEC from RES per capita
    Original Eqn: ZIDZ( TFEC RES EJ*GJ per EJ, Population )
    Units: GJ/person
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(tfec_res_ej() * gj_per_ej(), population())


def tfec_per_capita():
    """
    Real Name: TFEC per capita
    Original Eqn: ZIDZ( Real TFEC*GJ per EJ, Population )
    Units: GJ/person
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(real_tfec() * gj_per_ej(), population())


def tfec_per_capita_before_heat_dem_corr():
    """
    Real Name: TFEC per capita before heat dem corr
    Original Eqn: ZIDZ( Real TFEC before heat dem corr*GJ per EJ, Population )
    Units: GJ/person
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(real_tfec_before_heat_dem_corr() * gj_per_ej(), population())


def tfec_res_delayed_1yr():
    """
    Real Name: TFEC RES delayed 1yr
    Original Eqn: DELAY FIXED ( TFEC RES EJ, 1, 0.2458)
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _delayfixed_tfec_res_delayed_1yr()


def tpes_without_trad_biomass():
    """
    Real Name: "TPES (without trad biomass)"
    Original Eqn: TPES EJ-PE traditional biomass EJ delayed 1yr
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    TPES without accounting for traditional biomass.
    """
    return tpes_ej() - pe_traditional_biomass_ej_delayed_1yr()


def tpes_res_delayed_1yr():
    """
    Real Name: TPES RES delayed 1yr
    Original Eqn: DELAY FIXED ( TPE from RES EJ, 1, 0.262)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _delayfixed_tpes_res_delayed_1yr()


_delayfixed_share_res_vs_tfec_delayed_1yr = DelayFixed(
    lambda: share_res_vs_tfec(),
    lambda: 1,
    lambda: 0.2786,
    time_step,
    "_delayfixed_share_res_vs_tfec_delayed_1yr",
)


_delayfixed_share_res_vs_tpes_delayed_1yr = DelayFixed(
    lambda: share_res_vs_tpes(),
    lambda: 1,
    lambda: 0.2137,
    time_step,
    "_delayfixed_share_res_vs_tpes_delayed_1yr",
)


_delayfixed_tfec_res_delayed_1yr = DelayFixed(
    lambda: tfec_res_ej(),
    lambda: 1,
    lambda: 0.2458,
    time_step,
    "_delayfixed_tfec_res_delayed_1yr",
)


_delayfixed_tpes_res_delayed_1yr = DelayFixed(
    lambda: tpe_from_res_ej(),
    lambda: 1,
    lambda: 0.262,
    time_step,
    "_delayfixed_tpes_res_delayed_1yr",
)
