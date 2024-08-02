"""
Module energy.eroi.eroi_system
Translated using PySD version 3.14.1
"""

@component.add(
    name="EROIst system",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"real_tfec": 1, "feist_system": 1},
)
def eroist_system():
    """
    EROI standard of the system.
    """
    return np.maximum(0, real_tfec() / feist_system())


@component.add(
    name="FE tot generation all RES elec EJ",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fe_tot_generation_all_res_elec_twh": 1,
        "ej_per_twh": 1,
        "share_transmdistr_elec_losses": 1,
    },
)
def fe_tot_generation_all_res_elec_ej():
    """
    Electricity generation from all RES technologies.
    """
    return (
        fe_tot_generation_all_res_elec_twh()
        * ej_per_twh()
        * (1 - share_transmdistr_elec_losses())
    )


@component.add(
    name="FEIst system",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "share_e_industry_ownuse_vs_tfec_in_2015": 1,
        "fe_tot_generation_all_res_elec_ej": 1,
        "real_tfec": 1,
        "total_dyn_fei_res": 1,
    },
)
def feist_system():
    """
    Total (dynamic) final energy investment of the whole energy system (standard EROI approach)..
    """
    return (
        share_e_industry_ownuse_vs_tfec_in_2015()
        * (real_tfec() - fe_tot_generation_all_res_elec_ej())
        + total_dyn_fei_res()
    )


@component.add(
    name='"Historic energy industry own-use"',
    units="EJ/year",
    comp_type="Lookup",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_lookup_historic_energy_industry_ownuse",
        "__lookup__": "_ext_lookup_historic_energy_industry_ownuse",
    },
)
def historic_energy_industry_ownuse(x, final_subs=None):
    """
    Energy industry own-use.
    """
    return _ext_lookup_historic_energy_industry_ownuse(x, final_subs)


_ext_lookup_historic_energy_industry_ownuse = ExtLookup(
    r"../energy.xlsx",
    "World",
    "time_historic_data",
    "historic_energy_industry_own_use",
    {},
    _root,
    {},
    "_ext_lookup_historic_energy_industry_ownuse",
)


@component.add(
    name='"Historic share E industry own-use vs TFEC"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 2,
        "fe_tot_generation_all_res_elec_ej": 1,
        "real_tfec": 1,
        "historic_energy_industry_ownuse": 1,
    },
)
def historic_share_e_industry_ownuse_vs_tfec():
    """
    Historic share of the energy industry own-energy use vs TFEC.
    """
    return if_then_else(
        time() < 2016,
        lambda: historic_energy_industry_ownuse(time())
        / (real_tfec() - fe_tot_generation_all_res_elec_ej()),
        lambda: 0,
    )


@component.add(
    name='"Share E industry own-use vs TFEC in 2015"',
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_share_e_industry_ownuse_vs_tfec_in_2015": 1},
    other_deps={
        "_sampleiftrue_share_e_industry_ownuse_vs_tfec_in_2015": {
            "initial": {"historic_share_e_industry_ownuse_vs_tfec": 1},
            "step": {"time": 1, "historic_share_e_industry_ownuse_vs_tfec": 1},
        }
    },
)
def share_e_industry_ownuse_vs_tfec_in_2015():
    return _sampleiftrue_share_e_industry_ownuse_vs_tfec_in_2015()


_sampleiftrue_share_e_industry_ownuse_vs_tfec_in_2015 = SampleIfTrue(
    lambda: time() < 2015,
    lambda: historic_share_e_industry_ownuse_vs_tfec(),
    lambda: historic_share_e_industry_ownuse_vs_tfec(),
    "_sampleiftrue_share_e_industry_ownuse_vs_tfec_in_2015",
)


@component.add(
    name="Total dyn FEI RES",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fei_res_elec_var": 1,
        "fei_over_lifetime_res_elec_dispatch": 1,
        "fei_ev_batteries": 1,
        "final_energy_invested_phs": 1,
    },
)
def total_dyn_fei_res():
    """
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
