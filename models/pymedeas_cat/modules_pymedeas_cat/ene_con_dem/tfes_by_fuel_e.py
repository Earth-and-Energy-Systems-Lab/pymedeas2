"""
Module tfes_by_fuel_e
Translated using PySD version 2.2.0
"""


def fe_tot_generation_all_res_elec_ej():
    """
    Real Name: FE tot generation all RES elec EJ
    Original Eqn: FE tot generation all RES elec TWh*EJ per TWh*(1-"share transm&distr elec losses")
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Electricity generation from all RES technologies.
    """
    return (
        fe_tot_generation_all_res_elec_twh()
        * ej_per_twh()
        * (1 - share_transmdistr_elec_losses())
    )


def share_res_vs_tfec():
    """
    Real Name: share RES vs TFEC
    Original Eqn: ZIDZ( TFEC RES EJ, Real TFEC )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of total final energy consumption from RES over the total.
    """
    return zidz(tfec_res_ej(), real_tfec())


def tfec_res_ej():
    """
    Real Name: TFEC RES EJ
    Original Eqn: FE tot generation all RES elec EJ+FES RES for heat EJ+PE traditional biomass consum EJ+FES total biofuels+FES total biogas
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total final energy consumption from RES.
    """
    return (
        fe_tot_generation_all_res_elec_ej()
        + fes_res_for_heat_ej()
        + pe_traditional_biomass_consum_ej()
        + fes_total_biofuels()
        + fes_total_biogas()
    )
