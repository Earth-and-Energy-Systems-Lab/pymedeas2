"""
Module required_final_energy_invested_res
Translated using PySD version 2.1.0
"""


def share_dyn_fei_for_res_vs_tfec():
    """
    Real Name: share dyn FEI for RES vs TFEC
    Original Eqn: Total dyn FEI RES/Real TFEC
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Share of dynamic final energy investments for RES technologies vs TFES.
    """
    return total_dyn_fei_res() / real_tfec()


def share_tot_fei_res_elec_var():
    """
    Real Name: share tot FEI RES elec var
    Original Eqn: Total final energy invested RES elec var/Total dyn FEI RES
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return total_final_energy_invested_res_elec_var() / total_dyn_fei_res()


def total_dyn_fei_res():
    """
    Real Name: Total dyn FEI RES
    Original Eqn: Total final energy invested RES elec var+FEI EV batteries+Total FEI over lifetime RES elec dispatch+Final energy invested PHS
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Total (dynamic) final energy investment for RES.
    """
    return (
        total_final_energy_invested_res_elec_var()
        + fei_ev_batteries()
        + total_fei_over_lifetime_res_elec_dispatch()
        + final_energy_invested_phs()
    )


def total_fei_over_lifetime_res_elec_dispatch():
    """
    Real Name: Total FEI over lifetime RES elec dispatch
    Original Eqn: SUM(FEI over lifetime RES elec dispatch[RES elec!])
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return sum(fei_over_lifetime_res_elec_dispatch(), dim=("RES elec",))
