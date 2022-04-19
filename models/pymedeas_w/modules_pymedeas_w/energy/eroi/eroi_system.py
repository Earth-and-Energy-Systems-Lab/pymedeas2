"""
Module eroi_system
Translated using PySD version 3.0.0
"""


@component.add(
    name="EROIst system", units="Dmnl", comp_type="Auxiliary", comp_subtype="Normal"
)
def eroist_system():
    """
    EROI standard of the system.
    """
    return np.maximum(0, real_tfec() / feist_system())


@component.add(
    name="FE tot generation all RES elec EJ",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
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
    name="FEIst system", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
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
    units="EJ",
    comp_type="Lookup",
    comp_subtype="External",
)
def historic_energy_industry_ownuse(x, final_subs=None):
    """
    Energy industry own-use.
    """
    return _ext_lookup_historic_energy_industry_ownuse(x, final_subs)


_ext_lookup_historic_energy_industry_ownuse = ExtLookup(
    "../energy.xlsx",
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
    name="Total dyn FEI RES", units="EJ", comp_type="Auxiliary", comp_subtype="Normal"
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
