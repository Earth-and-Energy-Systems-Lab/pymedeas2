"""
Module res_heat_potential
Translated using PySD version 2.2.3
"""


def fe_solar_potential_for_heat():
    """
    Real Name: FE solar potential for heat
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Constant
    Subs: []

    Global solar thermal potential. We assume that the primary energy coincides with the final energy. See Technical Report Appendix D.
    """
    return _ext_constant_fe_solar_potential_for_heat()


_ext_constant_fe_solar_potential_for_heat = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "solar_thermal_pot_FE",
    {},
    _root,
    "_ext_constant_fe_solar_potential_for_heat",
)


def geot_pe_potential_for_heat_ej():
    """
    Real Name: Geot PE potential for heat EJ
    Original Eqn:
    Units: EJ/year
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Geothermal potential (primary energy) for producing heat.
    """
    return geot_pe_potential_for_heat_twth() * ej_per_twh() / twe_per_twh()


def geot_pe_potential_for_heat_twth():
    """
    Real Name: Geot PE potential for heat TWth
    Original Eqn:
    Units: TWth
    Limits: (None, None)
    Type: Constant
    Subs: []

    Geothermal primary energy potential for heat.
    """
    return _ext_constant_geot_pe_potential_for_heat_twth()


_ext_constant_geot_pe_potential_for_heat_twth = ExtConstant(
    "../../scenarios/scen_w.xlsx",
    "BAU",
    "geothermal_PE_pot_heat",
    {},
    _root,
    "_ext_constant_geot_pe_potential_for_heat_twth",
)


@subs(["RES heat"], _subscript_dict)
def max_fe_potential_res_for_heat():
    """
    Real Name: Max FE potential RES for heat
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

    Potential (final energy) for producing heat from renewables.
    """
    value = xr.DataArray(
        np.nan, {"RES heat": _subscript_dict["RES heat"]}, ["RES heat"]
    )
    value.loc[{"RES heat": ["solar heat"]}] = (
        float(max_pe_potential_res_for_heat().loc["solar heat"])
        + float(efficiency_res_heat().loc["solar heat"]) * 0
    )
    value.loc[{"RES heat": ["geot heat"]}] = float(
        max_pe_potential_res_for_heat().loc["geot heat"]
    ) * float(efficiency_res_heat().loc["geot heat"])
    value.loc[{"RES heat": ["solid bioE heat"]}] = float(
        max_pe_potential_res_for_heat().loc["solid bioE heat"]
    ) * float(efficiency_res_heat().loc["solid bioE heat"])
    return value


def max_pe_potential_biogas_for_heat():
    """
    Real Name: max PE potential biogas for heat
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Primary energy potential of biogas for heat taking into account the current share.
    """
    return max_biogas_ej() * share_pes_biogas_for_heat()


@subs(["RES heat"], _subscript_dict)
def max_pe_potential_res_for_heat():
    """
    Real Name: Max PE potential RES for heat
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

    Potential (primary energy) for producing heat from renewables.
    """
    value = xr.DataArray(
        np.nan, {"RES heat": _subscript_dict["RES heat"]}, ["RES heat"]
    )
    value.loc[{"RES heat": ["solar heat"]}] = fe_solar_potential_for_heat()
    value.loc[{"RES heat": ["geot heat"]}] = geot_pe_potential_for_heat_ej()
    value.loc[
        {"RES heat": ["solid bioE heat"]}
    ] = available_pe_potential_solid_bioe_for_heat_ej()
    return value


def max_pe_potential_tot_res_heat_ej():
    """
    Real Name: max PE potential tot RES heat EJ
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Maximum total primary energy potential of RES for heat.
    """
    return max_pe_potential_biogas_for_heat() + sum(
        max_pe_potential_res_for_heat().rename({"RES heat": "RES heat!"}),
        dim=["RES heat!"],
    )


def percent_remaining_potential_tot_res_heat():
    """
    Real Name: Percent remaining potential tot RES heat
    Original Eqn:
    Units: percent
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Remaining potential available as a percentage.
    """
    return remaining_potential_tot_res_heat() * 100


def pes_tot_res_for_heat():
    """
    Real Name: PES tot RES for heat
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Total primary energy supply for generating commercial and non-commercial heat from renewables.
    """
    return (
        sum(
            pes_res_for_heatcom_by_techn().rename({"RES heat": "RES heat!"}),
            dim=["RES heat!"],
        )
        + sum(
            pes_res_for_heatnc_by_techn().rename({"RES heat": "RES heat!"}),
            dim=["RES heat!"],
        )
        + pes_tot_biogas_for_heatcom()
    )


def remaining_potential_tot_res_heat():
    """
    Real Name: remaining potential tot RES heat
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Remaining potential available as a fraction of unity.
    """
    return if_then_else(
        max_pe_potential_tot_res_heat_ej() > pes_tot_res_for_heat(),
        lambda: zidz(
            max_pe_potential_tot_res_heat_ej() - pes_tot_res_for_heat(),
            max_pe_potential_tot_res_heat_ej(),
        ),
        lambda: 0,
    )
