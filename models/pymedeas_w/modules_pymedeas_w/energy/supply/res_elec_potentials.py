"""
Module res_elec_potentials
Translated using PySD version 2.2.3
"""


def efficiency_conversion_geot_pe_to_elec():
    """
    Real Name: Efficiency conversion geot PE to Elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Constant
    Subs: []

    Efficiency of the transformation from geothermal (primary energy) to electricity.
    """
    return _ext_constant_efficiency_conversion_geot_pe_to_elec()


_ext_constant_efficiency_conversion_geot_pe_to_elec = ExtConstant(
    "../energy.xlsx",
    "Global",
    "efficiency_conversion_geot_pe_to_elec",
    {},
    _root,
    "_ext_constant_efficiency_conversion_geot_pe_to_elec",
)


def max_csp_on_land_mha():
    """
    Real Name: max CSP on land MHa
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Available land for solar CSP taking into account the total land availability for solar and the actual occupation from solar PV on land.
    """
    return max_solar_on_land_mha() - surface_solar_pv_mha()


def max_pe_geotelec_twth():
    """
    Real Name: "max PE geot-elec TWth"
    Original Eqn:
    Units: TWe
    Limits: (None, None)
    Type: Constant
    Subs: []

    Primary energy of geothermal for electricity.
    """
    return _ext_constant_max_pe_geotelec_twth()


_ext_constant_max_pe_geotelec_twth = ExtConstant(
    "../energy.xlsx",
    "World",
    "max_PE_geot_elect_potential",
    {},
    _root,
    "_ext_constant_max_pe_geotelec_twth",
)


@subs(["RES elec"], _subscript_dict)
def max_potential_res_elec_twe():
    """
    Real Name: max potential RES elec TWe
    Original Eqn:
    Units: TWe
    Limits: (None, None)
    Type: Constant, Auxiliary
    Subs: ['RES elec']

    Maximum potential of RES for electricity per technology considering an optimal Cp.
    """
    value = xr.DataArray(
        np.nan, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
    )
    value.loc[["hydro", "oceanic", "wind onshore", "wind offshore"]
    ] = _ext_constant_max_potential_res_elec_twe().loc[
        ["hydro", "oceanic", "wind onshore", "wind offshore"]].values
    value.loc[{"RES elec": ["geot elec"]}] = (
        max_pe_geotelec_twth() * efficiency_conversion_geot_pe_to_elec()
    )
    value.loc[{"RES elec": ["solid bioE elec"]}] = (
        available_potential_fe_solid_bioe_for_elec_ej() * twe_per_twh() / ej_per_twh()
    )
    value.loc[{"RES elec": ["solar PV"]}] = max_solar_pv_on_land_mha() * float(
        power_density_res_elec_twemha().loc["solar PV"]
    )
    value.loc[{"RES elec": ["CSP"]}] = max_csp_on_land_mha() * float(
        power_density_res_elec_twemha().loc["CSP"]
    )
    return value


_ext_constant_max_potential_res_elec_twe = ExtConstant(
    "../energy.xlsx",
    "World",
    "max_hydro_potential",
    {"RES elec": ["hydro"]},
    _root,
    "_ext_constant_max_potential_res_elec_twe",
)

_ext_constant_max_potential_res_elec_twe.add(
    "../energy.xlsx", "World", "max_oceanic_potential", {"RES elec": ["oceanic"]}
)

_ext_constant_max_potential_res_elec_twe.add(
    "../energy.xlsx",
    "World",
    "max_onshore_wind_potential",
    {"RES elec": ["wind onshore"]},
)

_ext_constant_max_potential_res_elec_twe.add(
    "../energy.xlsx",
    "World",
    "max_offshore_wind_potential",
    {"RES elec": ["wind offshore"]},
)


@subs(["RES elec"], _subscript_dict)
def max_potential_res_elec_twh():
    """
    Real Name: max potential RES elec TWh
    Original Eqn:
    Units: TWh
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES elec']

    Maximum potential of RES for electricity per technology considering an optimal Cp.
    """
    return max_potential_res_elec_twe() / twe_per_twh()


def max_potential_tot_res_elec_twh():
    """
    Real Name: max potential tot RES elec TWh
    Original Eqn:
    Units: TWh
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Maximum total potential of RES for electricity considering an optimal Cp.
    """
    return (
        sum(
            max_potential_res_elec_twh().rename({"RES elec": "RES elec!"}),
            dim=["RES elec!"],
        )
        + max_potential_phs_twe() / twe_per_twh()
        + max_biogas_ej() * share_pes_biogas_for_elec() / ej_per_twh()
    )


def max_solar_on_land_mha():
    """
    Real Name: max solar on land Mha
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Constant
    Subs: []

    Assumed land availability for solar power plants on land (PV and CSP).
    """
    return _ext_constant_max_solar_on_land_mha()


_ext_constant_max_solar_on_land_mha = ExtConstant(
    "../energy.xlsx",
    "World",
    "max_solar_on_land_potential",
    {},
    _root,
    "_ext_constant_max_solar_on_land_mha",
)


def max_solar_pv_on_land_mha():
    """
    Real Name: max solar PV on land MHa
    Original Eqn:
    Units: MHa
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Available land for solar PV taking into account the total land availability for solar and the actual occupation from CSP.
    """
    return max_solar_on_land_mha() - surface_csp_mha()


def percent_remaining_potential_tot_res_elec():
    """
    Real Name: Percent remaining potential tot RES elec
    Original Eqn:
    Units: percent
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Remaining potential available as a percentage.
    """
    return remaining_potential_tot_res_elec() * 100


@subs(["RES elec"], _subscript_dict)
def remaining_potential():
    """
    Real Name: remaining potential
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: ['RES elec']


    """
    return if_then_else(
        max_potential_res_elec_twh() > real_generation_res_elec_twh(),
        lambda: (max_potential_res_elec_twh() - real_generation_res_elec_twh())
        / max_potential_res_elec_twh(),
        lambda: xr.DataArray(
            0, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
        ),
    )


def remaining_potential_tot_res_elec():
    """
    Real Name: remaining potential tot RES elec
    Original Eqn:
    Units: Dmnl
    Limits: (None, None)
    Type: Auxiliary
    Subs: []

    Remaining potential available as a fraction of unity.
    """
    return if_then_else(
        max_potential_tot_res_elec_twh() > fe_tot_generation_all_res_elec_twh(),
        lambda: (
            max_potential_tot_res_elec_twh() - fe_tot_generation_all_res_elec_twh()
        )
        / max_potential_tot_res_elec_twh(),
        lambda: 0,
    )
