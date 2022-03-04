"""
Module res_heat_potential
Translated using PySD version 2.2.1
"""


def geot_pe_potential_for_heat_ej():
    """
    Real Name: Geot PE potential for heat EJ
    Original Eqn:
    Units: EJ/Year
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
    "../energy.xlsx",
    "Austria",
    "geot_PE_potential_heat",
    {},
    _root,
    "_ext_constant_geot_pe_potential_for_heat_twth",
)


def max_fe_potential_biogas_for_heat():
    """
    Real Name: max FE potential biogas for heat
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Potential (final energy) of biogas for heat.
    """
    return (
        max_pe_biogas_ej() * share_pes_biogas_for_heat() * efficiency_biogas_for_heat()
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


    """
    value = xr.DataArray(
        np.nan, {"RES heat": _subscript_dict["RES heat"]}, ["RES heat"]
    )
    value.loc[{"RES heat": ["solar heat"]}] = float(
        max_fe_res_for_heat().loc["solar heat"]
    )
    value.loc[{"RES heat": ["geot heat"]}] = float(
        max_fe_res_for_heat().loc["geot heat"]
    )
    value.loc[
        {"RES heat": ["solid bioE heat"]}
    ] = max_pe_potential_solid_bioe_for_heat_ej() * float(
        efficiency_res_heat().loc["solid bioE heat"]
    )
    return value


@subs(["RES heat"], _subscript_dict)
def max_fe_res_for_heat():
    """
    Real Name: Max FE RES for heat
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

    Maximum level of final energy for producing heat from renewables by technology. For technologies solar heat and geot heat this variable corresponds with the maximum potential, but not for solids bioenergy due to the competing use for heat and electricity.
    """
    value = xr.DataArray(
        np.nan, {"RES heat": _subscript_dict["RES heat"]}, ["RES heat"]
    )
    value.loc[{"RES heat": ["solar heat"]}] = (
        max_fe_solar_thermal_urban_twth() * ej_per_twh() / twe_per_twh()
    )
    value.loc[{"RES heat": ["geot heat"]}] = float(
        max_pe_res_for_heat().loc["geot heat"]
    ) * float(efficiency_res_heat().loc["geot heat"])
    value.loc[{"RES heat": ["solid bioE heat"]}] = float(
        max_pe_res_for_heat().loc["solid bioE heat"]
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
    return max_pe_biogas_ej() * share_pes_biogas_for_heat()


@subs(["RES heat"], _subscript_dict)
def max_pe_potential_res_for_heat():
    """
    Real Name: Max PE potential RES for heat
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']


    """
    value = xr.DataArray(
        np.nan, {"RES heat": _subscript_dict["RES heat"]}, ["RES heat"]
    )
    value.loc[{"RES heat": ["solar heat"]}] = float(
        max_pe_res_for_heat().loc["solar heat"]
    )
    value.loc[{"RES heat": ["geot heat"]}] = float(
        max_pe_res_for_heat().loc["geot heat"]
    )
    value.loc[
        {"RES heat": ["solid bioE heat"]}
    ] = max_pe_potential_solid_bioe_for_heat_ej()
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


@subs(["RES heat"], _subscript_dict)
def max_pe_res_for_heat():
    """
    Real Name: Max PE RES for heat
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES heat']

    Maximum level of primary energy for producing heat from renewables by technology.
    """
    value = xr.DataArray(
        np.nan, {"RES heat": _subscript_dict["RES heat"]}, ["RES heat"]
    )
    value.loc[{"RES heat": ["solar heat"]}] = max_fe_solar_thermal_urban_twth() / float(
        efficiency_res_heat().loc["solar heat"]
    )
    value.loc[{"RES heat": ["geot heat"]}] = geot_pe_potential_for_heat_ej()
    value.loc[
        {"RES heat": ["solid bioE heat"]}
    ] = available_max_pe_solid_bioe_for_heat_ej()
    return value


def max_tot_fe_potential_res_for_heat():
    """
    Real Name: Max tot FE potential RES for heat
    Original Eqn:
    Units: EJ
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Potential (final energy) for producing heat from renewables.
    """
    return (
        sum(
            max_fe_potential_res_for_heat().rename({"RES heat": "RES heat!"}),
            dim=["RES heat!"],
        )
        + max_fe_potential_biogas_for_heat()
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
