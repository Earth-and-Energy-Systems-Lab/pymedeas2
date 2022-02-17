"""
Module eroi_system
Translated using PySD version 2.2.1
"""


def eroist_system():
    """
    Real Name: EROIst system
    Original Eqn: MAX(0, (Real TFEC)/FEIst system)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    EROI standard of the system.
    """
    return np.maximum(0, (real_tfec()) / feist_system())


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


def feist_system():
    """
    Real Name: FEIst system
    Original Eqn: "Share E industry own-use vs TFEC in 2015"*(Real TFEC-FE tot generation all RES elec EJ)+Total dyn FEI RES
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total (dynamic) final energy investment of the whole energy system
        (standard EROI approach)..
    """
    return (
        share_e_industry_ownuse_vs_tfec_in_2015()
        * (real_tfec() - fe_tot_generation_all_res_elec_ej())
        + total_dyn_fei_res()
    )


def historic_energy_industry_ownuse(x):
    """
    Real Name: "Historic energy industry own-use"
    Original Eqn: GET DIRECT LOOKUPS('../energy.xlsx', 'World', 'time_historic_data', 'historic_energy_industry_own_use')
    Units: EJ
    Limits: (None, None)
    Type: lookup
    Subs: None

    Energy industry own-use.
    """
    return _ext_lookup_historic_energy_industry_ownuse(x)


def historic_share_e_industry_ownuse_vs_tfec():
    """
    Real Name: "Historic share E industry own-use vs TFEC"
    Original Eqn: IF THEN ELSE(Time<2016, "Historic energy industry own-use"(Time)/(Real TFEC -FE tot generation all RES elec EJ), 0)
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Historic share of the energy industry own-energy use vs TFEC.
    """
    return if_then_else(
        time() < 2016,
        lambda: historic_energy_industry_ownuse(time())
        / (real_tfec() - fe_tot_generation_all_res_elec_ej()),
        lambda: 0,
    )


def share_e_industry_ownuse_vs_tfec_in_2015():
    """
    Real Name: "Share E industry own-use vs TFEC in 2015"
    Original Eqn: SAMPLE IF TRUE(Time<2015, "Historic share E industry own-use vs TFEC", "Historic share E industry own-use vs TFEC")
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _sample_if_true_share_e_industry_ownuse_vs_tfec_in_2015()


def total_dyn_fei_res():
    """
    Real Name: Total dyn FEI RES
    Original Eqn: SUM(FEI RES elec var[RES elec!])+SUM(FEI over lifetime RES elec dispatch[RES elec!])+FEI EV batteries+Final energy invested PHS
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total (dynamic) final energy investment for RES.
    """
    return (
        sum(fei_res_elec_var(), dim=("RES elec",))
        + sum(fei_over_lifetime_res_elec_dispatch(), dim=("RES elec",))
        + fei_ev_batteries()
        + final_energy_invested_phs()
    )


_ext_lookup_historic_energy_industry_ownuse = ExtLookup(
    "../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_energy_industry_own_use",
    {},
    _root,
    "_ext_lookup_historic_energy_industry_ownuse",
)


_sample_if_true_share_e_industry_ownuse_vs_tfec_in_2015 = SampleIfTrue(
    lambda: time() < 2015,
    lambda: historic_share_e_industry_ownuse_vs_tfec(),
    lambda: historic_share_e_industry_ownuse_vs_tfec(),
    "_sample_if_true_share_e_industry_ownuse_vs_tfec_in_2015",
)
