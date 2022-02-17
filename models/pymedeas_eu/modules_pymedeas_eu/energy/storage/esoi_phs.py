"""
Module esoi_phs
Translated using PySD version 2.2.1
"""


def a_lineal_regr():
    """
    Real Name: a lineal regr
    Original Eqn: (ESOI PHS full potential-ESOI PHS depleted potential)/(0-max capacity potential PHS )
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (esoi_phs_full_potential() - esoi_phs_depleted_potential()) / (
        0 - max_capacity_potential_phs()
    )


def b_lineal_regr():
    """
    Real Name: b lineal regr
    Original Eqn: ESOI PHS depleted potential-a lineal regr*max capacity potential PHS
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        esoi_phs_depleted_potential() - a_lineal_regr() * max_capacity_potential_phs()
    )


def ced_per_tw_over_lifetime_phs():
    """
    Real Name: CED per TW over lifetime PHS
    Original Eqn: ZIDZ( (Cp PHS*lifetime RES elec[hydro]*EJ per TWh/TWe per TWh), ESOI static PHS *quality of electricity 2015 )
    Units: EJ/TW
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return zidz(
        (
            cp_phs()
            * float(lifetime_res_elec().loc["hydro"])
            * ej_per_twh()
            / twe_per_twh()
        ),
        esoi_static_phs() * quality_of_electricity_2015(),
    )


def cedtot_over_lifetime_phs():
    """
    Real Name: CEDtot over lifetime PHS
    Original Eqn: PHS capacity under construction*CED per TW over lifetime PHS
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return phs_capacity_under_construction() * ced_per_tw_over_lifetime_phs()


def esoi_phs_depleted_potential():
    """
    Real Name: ESOI PHS depleted potential
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'esoi_phs_depleted_potential')
    Units: Dmnl
    Limits: (None, None)
    Type: constant
    Subs: None

    ESOI PHS of the depleted potential of the resource. We assume the ESOI of
        PHS linearly decreases with the PHS cumulated installed capacity.
    """
    return _ext_constant_esoi_phs_depleted_potential()


def esoi_phs_full_potential():
    """
    Real Name: ESOI PHS full potential
    Original Eqn: "EROI-ini RES elec dispatch"[hydro]*(Cp PHS/"Cp-ini RES elec"[hydro])
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    ESOI of PHS when the full potential is available.
    """
    return float(eroiini_res_elec_dispatch().loc["hydro"]) * (
        cp_phs() / float(cpini_res_elec().loc["hydro"])
    )


def esoi_static_phs():
    """
    Real Name: ESOI static PHS
    Original Eqn: MAX(5,a lineal regr*installed capacity PHS TW+b lineal regr )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    ESOI of the PHS without accounting for endogenous dynamic variations.
    """
    return np.maximum(
        5, a_lineal_regr() * installed_capacity_phs_tw() + b_lineal_regr()
    )


def final_energy_invested_phs():
    """
    Real Name: Final energy invested PHS
    Original Eqn: real FE elec stored PHS TWh*EJ per TWh/ESOI PHS
    Units: EJ
    Limits: (None, None)
    Type: component
    Subs: None

    Final energy invested is equivalent to the denominator of the EROI
        (=CED*g).
    """
    return real_fe_elec_stored_phs_twh() * ej_per_twh() / esoi_phs()


def esoi_phs():
    """
    Real Name: ESOI PHS
    Original Eqn: ZIDZ( output PHS over lifetime, CEDtot over lifetime PHS*"g=quality of electricity" )
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    ESOI of pumped hydro storage.        *lifetime RES elec[hydro]
    """
    return zidz(
        output_phs_over_lifetime(),
        cedtot_over_lifetime_phs() * gquality_of_electricity(),
    )


_ext_constant_esoi_phs_depleted_potential = ExtConstant(
    "../energy.xlsx",
    "Global",
    "esoi_phs_depleted_potential",
    {},
    _root,
    "_ext_constant_esoi_phs_depleted_potential",
)
