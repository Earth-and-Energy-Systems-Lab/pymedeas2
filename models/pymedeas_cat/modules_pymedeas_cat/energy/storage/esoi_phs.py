"""
Module esoi_phs
Translated using PySD version 3.0.0
"""


@component.add(name="a lineal regr", comp_type="Auxiliary", comp_subtype="Normal")
def a_lineal_regr():
    return (esoi_phs_full_potential() - esoi_phs_depleted_potential()) / (
        0 - max_capacity_potential_phs()
    )


@component.add(name="b lineal regr", comp_type="Auxiliary", comp_subtype="Normal")
def b_lineal_regr():
    return (
        esoi_phs_depleted_potential() - a_lineal_regr() * max_capacity_potential_phs()
    )


@component.add(
    name="CED per TW over lifetime PHS",
    units="EJ/TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def ced_per_tw_over_lifetime_phs():
    return zidz(
        cp_phs()
        * float(lifetime_res_elec().loc["hydro"])
        * ej_per_twh()
        / twe_per_twh(),
        esoi_static_phs() * quality_of_electricity_2015(),
    )


@component.add(
    name="CEDtot over lifetime PHS",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def cedtot_over_lifetime_phs():
    return phs_capacity_under_construction() * ced_per_tw_over_lifetime_phs()


@component.add(
    name="ESOI PHS", units="Dmnl", comp_type="Auxiliary", comp_subtype="Normal"
)
def esoi_phs():
    """
    ESOI of pumped hydro storage. *lifetime RES elec[hydro]
    """
    return zidz(
        output_phs_over_lifetime(),
        cedtot_over_lifetime_phs() * gquality_of_electricity(),
    )


@component.add(
    name="ESOI PHS depleted potential",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
)
def esoi_phs_depleted_potential():
    """
    ESOI PHS of the depleted potential of the resource. We assume the ESOI of PHS linearly decreases with the PHS cumulated installed capacity.
    """
    return _ext_constant_esoi_phs_depleted_potential()


_ext_constant_esoi_phs_depleted_potential = ExtConstant(
    "../energy.xlsx",
    "Global",
    "esoi_phs_depleted_potential",
    {},
    _root,
    {},
    "_ext_constant_esoi_phs_depleted_potential",
)


@component.add(
    name="ESOI PHS full potential",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def esoi_phs_full_potential():
    """
    ESOI of PHS when the full potential is available.
    """
    return float(eroiini_res_elec_dispatch().loc["hydro"]) * (
        cp_phs() / float(cpini_res_elec().loc["hydro"])
    )


@component.add(
    name="ESOI static PHS", units="Dmnl", comp_type="Auxiliary", comp_subtype="Normal"
)
def esoi_static_phs():
    """
    ESOI of the PHS without accounting for endogenous dynamic variations.
    """
    return np.maximum(
        5, a_lineal_regr() * installed_capacity_phs_tw() + b_lineal_regr()
    )


@component.add(
    name="Final energy invested PHS",
    units="EJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
)
def final_energy_invested_phs():
    """
    Final energy invested is equivalent to the denominator of the EROI (=CED*g).
    """
    return zidz(real_fe_elec_stored_phs_twh() * ej_per_twh(), esoi_phs())
