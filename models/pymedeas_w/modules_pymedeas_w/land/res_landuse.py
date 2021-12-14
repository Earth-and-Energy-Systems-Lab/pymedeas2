"""
Module res_landuse
Translated using PySD version 2.1.0
"""


def global_arable_land():
    """
    Real Name: Global arable land
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'World', 'global_arable_land')
    Units: MHa
    Limits: (None, None)
    Type: constant
    Subs: None

    Current global arable land: 1526 MHa (FAOSTAT).
    """
    return _ext_constant_global_arable_land()


@subs(["RES elec"], _subscript_dict)
def power_density_res_elec_twmha():
    """
    Real Name: "power density RES elec TW/Mha"
    Original Eqn: "power density RES elec TWe/Mha"[RES elec]/"Cp-ini RES elec"[RES elec]
    Units: TW/MHa
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']


    """
    return power_density_res_elec_twemha() / cpini_res_elec()


@subs(["RES elec"], _subscript_dict)
def power_density_res_elec_twemha():
    """
    Real Name: "power density RES elec TWe/Mha"
    Original Eqn: GET DIRECT CONSTANTS('../energy.xlsx', 'Global', 'power_density_res_elec*')
    Units: TWe/MHa
    Limits: (None, None)
    Type: constant
    Subs: ['RES elec']

    Input parameter: power density per RES technology for delivering
        electricity.
    """
    return _ext_constant_power_density_res_elec_twemha()


def share_land_compet_biofuels():
    """
    Real Name: Share land compet biofuels
    Original Eqn: Land compet required dedicated crops for biofuels/Global arable land
    Units:
    Limits: (None, None)
    Type: component
    Subs: None

    Share of global arable land required by dedicated crops for biofuels (in
        land competition).
    """
    return land_compet_required_dedicated_crops_for_biofuels() / global_arable_land()


def share_land_res_land_compet_vs_arable():
    """
    Real Name: share land RES land compet vs arable
    Original Eqn: (Land compet required dedicated crops for biofuels+surface solar PV Mha )/Global arable land
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Land requirements for RES that compete with other land-uses (solar on land
        and biofuels on land competition) as a share of the global arable land.
    """
    return (
        land_compet_required_dedicated_crops_for_biofuels() + surface_solar_pv_mha()
    ) / global_arable_land()


def share_land_total_res_vs_arable():
    """
    Real Name: share land total RES vs arable
    Original Eqn: Total land requirements renew Mha/Global arable land
    Units: MHa
    Limits: (None, None)
    Type: component
    Subs: None

    Land requirements for all RES as a share of the global arable land.
    """
    return total_land_requirements_renew_mha() / global_arable_land()


def share_land_total_res_vs_urban_surface():
    """
    Real Name: share land total RES vs urban surface
    Original Eqn: Total land requirements renew Mha/urban surface 2008
    Units:
    Limits: (None, None)
    Type: component
    Subs: None

    Land requirements for all RES as a share of the global urban land.
    """
    return total_land_requirements_renew_mha() / urban_surface_2008()


def surface_csp_mha():
    """
    Real Name: surface CSP Mha
    Original Eqn: surface RES elec[CSP]
    Units: MHa
    Limits: (None, None)
    Type: component
    Subs: None

    Area required for CSP.
    """
    return float(surface_res_elec().loc["CSP"])


def surface_hydro_mha():
    """
    Real Name: surface hydro Mha
    Original Eqn: surface RES elec[hydro]
    Units: MHa
    Limits: (None, None)
    Type: component
    Subs: None

    Surface required by hydropower plants.
    """
    return float(surface_res_elec().loc["hydro"])


def surface_onshore_wind_mha():
    """
    Real Name: surface onshore wind Mha
    Original Eqn: surface RES elec[wind onshore]
    Units: MHa
    Limits: (None, None)
    Type: component
    Subs: None

    Surface required to produce "onshore wind TWe".
    """
    return float(surface_res_elec().loc["wind onshore"])


@subs(["RES elec"], _subscript_dict)
def surface_res_elec():
    """
    Real Name: surface RES elec
    Original Eqn: IF THEN ELSE("power density RES elec TW/Mha"[RES elec]=0, 0, installed capacity RES elec TW[RES elec]/"power density RES elec TW/Mha"[RES elec])
    Units: MHa
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']


    """
    return if_then_else(
        power_density_res_elec_twmha() == 0,
        lambda: 0,
        lambda: installed_capacity_res_elec_tw() / power_density_res_elec_twmha(),
    )


def surface_solar_pv_mha():
    """
    Real Name: surface solar PV Mha
    Original Eqn: surface RES elec[solar PV]
    Units: MHa
    Limits: (None, None)
    Type: component
    Subs: None

    Area required for solar PV plants on land.
    """
    return float(surface_res_elec().loc["solar PV"])


def total_land_requirements_renew_mha():
    """
    Real Name: Total land requirements renew Mha
    Original Eqn: surface solar PV Mha+surface CSP Mha+surface hydro Mha +Land compet required dedicated crops for biofuels +Land required biofuels land marg+surface onshore wind Mha *0
    Units: MHa
    Limits: (None, None)
    Type: component
    Subs: None

    Land required for RES power plants and total bioenergy (land competition +
        marginal lands).
    """
    return (
        surface_solar_pv_mha()
        + surface_csp_mha()
        + surface_hydro_mha()
        + land_compet_required_dedicated_crops_for_biofuels()
        + land_required_biofuels_land_marg()
        + surface_onshore_wind_mha() * 0
    )


def urban_surface_2008():
    """
    Real Name: urban surface 2008
    Original Eqn: GET DIRECT CONSTANTS('../parameters.xlsx', 'World', 'urban_surface_2008')
    Units: MHa
    Limits: (None, None)
    Type: constant
    Subs: None

    Area occupied by human settlement and infraestructures. This area is
        roughly 200-400MHa (Wackernagel et al., 2002; WWF, 2008; Young, 1999).
    """
    return _ext_constant_urban_surface_2008()


_ext_constant_global_arable_land = ExtConstant(
    "../parameters.xlsx",
    "World",
    "global_arable_land",
    {},
    _root,
    "_ext_constant_global_arable_land",
)


_ext_constant_power_density_res_elec_twemha = ExtConstant(
    "../energy.xlsx",
    "Global",
    "power_density_res_elec*",
    {"RES elec": _subscript_dict["RES elec"]},
    _root,
    "_ext_constant_power_density_res_elec_twemha",
)


_ext_constant_urban_surface_2008 = ExtConstant(
    "../parameters.xlsx",
    "World",
    "urban_surface_2008",
    {},
    _root,
    "_ext_constant_urban_surface_2008",
)
