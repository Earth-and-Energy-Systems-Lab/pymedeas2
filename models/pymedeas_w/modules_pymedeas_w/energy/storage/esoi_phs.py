"""
Module energy.storage.esoi_phs
Translated using PySD version 3.14.0
"""

@component.add(
    name="a_lineal_regr",
    units="1/TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "esoi_phs_full_potential": 1,
        "esoi_phs_depleted_potential": 1,
        "max_capacity_potential_phs": 1,
    },
)
def a_lineal_regr():
    return (esoi_phs_full_potential() - esoi_phs_depleted_potential()) / (
        0 - max_capacity_potential_phs()
    )


@component.add(
    name="b_lineal_regr",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "esoi_phs_depleted_potential": 1,
        "a_lineal_regr": 1,
        "max_capacity_potential_phs": 1,
    },
)
def b_lineal_regr():
    return (
        esoi_phs_depleted_potential() - a_lineal_regr() * max_capacity_potential_phs()
    )


@component.add(
    name="CED_per_TW_over_lifetime_PHS",
    units="EJ/TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "cp_phs": 1,
        "lifetime_res_elec": 1,
        "ej_per_twh": 1,
        "twe_per_twh": 1,
        "esoi_static_phs": 1,
        "quality_of_electricity_2015": 1,
    },
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
    name="CEDtot_over_lifetime_PHS",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "phs_capacity_under_construction": 1,
        "ced_per_tw_over_lifetime_phs": 1,
    },
)
def cedtot_over_lifetime_phs():
    return phs_capacity_under_construction() * ced_per_tw_over_lifetime_phs()


@component.add(
    name="ESOI_PHS",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "output_phs_over_lifetime": 1,
        "cedtot_over_lifetime_phs": 1,
        "quality_of_electricity": 1,
    },
)
def esoi_phs():
    """
    ESOI of pumped hydro storage. *lifetime RES elec[hydro]
    """
    return zidz(
        output_phs_over_lifetime(),
        cedtot_over_lifetime_phs() * quality_of_electricity(),
    )


@component.add(
    name="ESOI_PHS_depleted_potential",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_esoi_phs_depleted_potential"},
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
    name="ESOI_PHS_full_potential",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"eroiini_res_elec_dispatch": 1, "cp_phs": 1, "cpini_res_elec": 1},
)
def esoi_phs_full_potential():
    """
    ESOI of PHS when the full potential is available.
    """
    return float(eroiini_res_elec_dispatch().loc["hydro"]) * (
        cp_phs() / float(cpini_res_elec().loc["hydro"])
    )


@component.add(
    name="ESOI_static_PHS",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"a_lineal_regr": 1, "installed_capacity_phs": 1, "b_lineal_regr": 1},
)
def esoi_static_phs():
    """
    ESOI of the PHS without accounting for endogenous dynamic variations.
    """
    return np.maximum(5, a_lineal_regr() * installed_capacity_phs() + b_lineal_regr())


@component.add(
    name="Final_energy_invested_PHS",
    units="EJ/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_fe_elec_stored_phs_twh": 1, "ej_per_twh": 1, "esoi_phs": 1},
)
def final_energy_invested_phs():
    """
    Final energy invested is equivalent to the denominator of the EROI (=CED*g).
    """
    return potential_fe_elec_stored_phs_twh() * ej_per_twh() / esoi_phs()
