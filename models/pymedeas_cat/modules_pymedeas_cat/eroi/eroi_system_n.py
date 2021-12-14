"""
Module eroi_system_n
Translated using PySD version 2.1.0
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
    Original Eqn: GET DIRECT LOOKUPS('../energy.xlsx', 'Austria', 'time_historic_data', 'historic_energy_industry_own_use')
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


_ext_lookup_historic_energy_industry_ownuse = ExtLookup(
    "../energy.xlsx",
    "Austria",
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
