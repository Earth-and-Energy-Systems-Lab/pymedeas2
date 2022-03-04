"""
Module eroi_system
Translated using PySD version 2.2.1
"""


def eroist_system():
    """
    Real Name: EROIst system
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    EROI standard of the system.
    """
    return np.maximum(0, real_tfec() / feist_system())


def fe_tot_generation_all_res_elec_ej():
    """
    Real Name: FE tot generation all RES elec EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total (dynamic) final energy investment of the whole energy system (standard EROI approach)..
    """
    return (
        share_e_industry_ownuse_vs_tfec_in_2015()
        * (real_tfec() - fe_tot_generation_all_res_elec_ej())
        + total_dyn_fei_res()
    )


def historic_energy_industry_ownuse(x):
    """
    Real Name: "Historic energy industry own-use"
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Lookup
    Subs: []

    Energy industry own-use.
    """
    return _ext_lookup_historic_energy_industry_ownuse(x)


_ext_lookup_historic_energy_industry_ownuse = ExtLookup(
    "../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_energy_industry_own_use",
    {},
    _root,
    "_ext_lookup_historic_energy_industry_ownuse",
)


def historic_share_e_industry_ownuse_vs_tfec():
    """
    Real Name: "Historic share E industry own-use vs TFEC"
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

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
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Stateful
    Subs: []


    """
    return _sampleiftrue_share_e_industry_ownuse_vs_tfec_in_2015()


_sampleiftrue_share_e_industry_ownuse_vs_tfec_in_2015 = SampleIfTrue(
    lambda: time() < 2015,
    lambda: historic_share_e_industry_ownuse_vs_tfec(),
    lambda: historic_share_e_industry_ownuse_vs_tfec(),
    "_sampleiftrue_share_e_industry_ownuse_vs_tfec_in_2015",
)


def total_dyn_fei_res():
    """
    Real Name: Total dyn FEI RES
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total (dynamic) final energy investment for RES.
    """
    return (
        sum(fei_res_elec_var().rename({"RES elec": "RES elec!"}), dim=["RES elec!"])
        + sum(
            fei_over_lifetime_res_elec_dispatch().rename({"RES elec": "RES elec!"}),
            dim=["RES elec!"],
        )
        + fei_ev_batteries()
        + final_energy_invested_phs()
    )
