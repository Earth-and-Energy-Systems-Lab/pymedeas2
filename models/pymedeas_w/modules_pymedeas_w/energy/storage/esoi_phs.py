"""
Module esoi_phs
Translated using PySD version 2.2.3
"""


def a_lineal_regr():
    """
    Real Name: a lineal regr
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (esoi_phs_full_potential() - esoi_phs_depleted_potential()) / (
        0 - max_capacity_potential_phs()
    )


def b_lineal_regr():
    """
    Real Name: b lineal regr
    Original Eqn:
    Units:
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return (
        esoi_phs_depleted_potential() - a_lineal_regr() * max_capacity_potential_phs()
    )


def ced_per_tw_over_lifetime_phs():
    """
    Real Name: CED per TW over lifetime PHS
    Original Eqn:
    Units: EJ/TW
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return zidz(
        cp_phs()
        * float(lifetime_res_elec().loc["hydro"])
        * ej_per_twh()
        / twe_per_twh(),
        esoi_static_phs() * quality_of_electricity_2015(),
    )


def cedtot_over_lifetime_phs():
    """
    Real Name: CEDtot over lifetime PHS
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []


    """
    return phs_capacity_under_construction() * ced_per_tw_over_lifetime_phs()


def esoi_phs():
    """
    Real Name: ESOI PHS
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    ESOI of pumped hydro storage. *lifetime RES elec[hydro]
    """
    return zidz(
        output_phs_over_lifetime(),
        cedtot_over_lifetime_phs() * quality_of_electricity(),
    )


def esoi_phs_depleted_potential():
    """
    Real Name: ESOI PHS depleted potential
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    ESOI PHS of the depleted potential of the resource. We assume the ESOI of PHS linearly decreases with the PHS cumulated installed capacity.
    """
    return _ext_constant_esoi_phs_depleted_potential()


_ext_constant_esoi_phs_depleted_potential = ExtConstant(
    "../energy.xlsx",
    "Global",
    "esoi_phs_depleted_potential",
    {},
    _root,
    "_ext_constant_esoi_phs_depleted_potential",
)


def esoi_phs_full_potential():
    """
    Real Name: ESOI PHS full potential
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    ESOI of PHS when the full potential is available.
    """
    return float(eroiini_res_elec_dispatch().loc["hydro"]) * (
        cp_phs() / float(cpini_res_elec().loc["hydro"])
    )


def esoi_static_phs():
    """
    Real Name: ESOI static PHS
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    ESOI of the PHS without accounting for endogenous dynamic variations.
    """
    return np.maximum(
        5, a_lineal_regr() * installed_capacity_phs_tw() + b_lineal_regr()
    )


def final_energy_invested_phs():
    """
    Real Name: Final energy invested PHS
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Final energy invested is equivalent to the denominator of the EROI (=CED*g).
    """
    return potential_fe_elec_stored_phs_twh() * ej_per_twh() / esoi_phs()
