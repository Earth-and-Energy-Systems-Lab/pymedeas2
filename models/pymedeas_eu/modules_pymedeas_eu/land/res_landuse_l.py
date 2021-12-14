"""
Module res_landuse_l
Translated using PySD version 2.1.0
"""


def agricultural_land_2015():
    """
    Real Name: Agricultural land 2015
    Original Eqn: GET DIRECT CONSTANTS('../land.xlsx', 'Europe', 'agricultural_land_2015')
    Units: MHa
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return _ext_constant_agricultural_land_2015()


def land_requirements_res_elec_compet_uses():
    """
    Real Name: Land requirements RES elec compet uses
    Original Eqn: surface hydro Mha+surface CSP Mha+surface solar PV on land Mha
    Units: MHa
    Limits: (None, None)
    Type: component
    Subs: None

    Land requirements for renewable technologies to generate electricity (PV
        on land, CSP and hydro) requiring land and not easily compatible with
        double uses.
    """
    return surface_hydro_mha() + surface_csp_mha() + surface_solar_pv_on_land_mha()


def land_saved_by_urban_pv():
    """
    Real Name: Land saved by urban PV
    Original Eqn: ZIDZ( potential generation RES elec TWh[solar PV]*real share PV urban vs total PV, ("power density RES elec TWe/Mha"[solar PV]/TWe per TWh) )
    Units: MHa*Year
    Limits: (None, None)
    Type: component
    Subs: None

    Land saved by urban PV.
    """
    return zidz(
        float(potential_generation_res_elec_twh().loc["solar PV"])
        * real_share_pv_urban_vs_total_pv(),
        (float(power_density_res_elec_twemha().loc["solar PV"]) / twe_per_twh()),
    )


def share_land_compet_biofuels():
    """
    Real Name: Share land compet biofuels
    Original Eqn: Land compet required dedicated crops for biofuels/Agricultural land 2015
    Units:
    Limits: (None, None)
    Type: component
    Subs: None

    Share of global arable land required by dedicated crops for biofuels (in
        land competition).
    """
    return (
        land_compet_required_dedicated_crops_for_biofuels() / agricultural_land_2015()
    )


def share_land_res_land_compet_vs_arable():
    """
    Real Name: share land RES land compet vs arable
    Original Eqn: (Land compet required dedicated crops for biofuels+surface solar PV on land Mha+surface CSP Mha+surface hydro Mha)/Agricultural land 2015
    Units: Dmnl
    Limits: (None, None)
    Type: component
    Subs: None

    Land requirements for RES that compete with other land-uses (solar on land
        and biofuels on land competition) as a share of the global arable land.
    """
    return (
        land_compet_required_dedicated_crops_for_biofuels()
        + surface_solar_pv_on_land_mha()
        + surface_csp_mha()
        + surface_hydro_mha()
    ) / agricultural_land_2015()


def share_land_total_res_vs_arable():
    """
    Real Name: share land total RES vs arable
    Original Eqn: Total land requirements renew Mha/Agricultural land 2015
    Units: MHa
    Limits: (None, None)
    Type: component
    Subs: None

    Land requirements for all RES as a share of the global arable land.
    """
    return total_land_requirements_renew_mha() / agricultural_land_2015()


def share_land_total_res_vs_urban_surface():
    """
    Real Name: share land total RES vs urban surface
    Original Eqn: Total land requirements renew Mha/urban surface 2015
    Units:
    Limits: (None, None)
    Type: component
    Subs: None

    Land requirements for all RES as a share of the global urban land.
    """
    return total_land_requirements_renew_mha() / urban_surface_2015()


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
    Original Eqn:
      ZIDZ( potential generation RES elec TWh[hydro], ("power density RES elec TWe/Mha"[hydro]/TWe per TWh) )
        .
        .
        .
      ZIDZ( potential generation RES elec TWh[CSP], ("power density RES elec TWe/Mha"[CSP]/TWe per TWh) )
    Units: MHa
    Limits: (None, None)
    Type: component
    Subs: ['RES elec']

    Land requirements by renewable technologies for electricity generation.
    """
    return xrmerge(
        rearrange(
            zidz(
                float(potential_generation_res_elec_twh().loc["hydro"]),
                (float(power_density_res_elec_twemha().loc["hydro"]) / twe_per_twh()),
            ),
            ["RES elec"],
            {"RES elec": ["hydro"]},
        ),
        rearrange(
            zidz(
                float(potential_generation_res_elec_twh().loc["geot elec"]),
                (
                    float(power_density_res_elec_twemha().loc["geot elec"])
                    / twe_per_twh()
                ),
            ),
            ["RES elec"],
            {"RES elec": ["geot elec"]},
        ),
        rearrange(
            zidz(
                float(potential_generation_res_elec_twh().loc["solid bioE elec"]),
                (
                    float(power_density_res_elec_twemha().loc["solid bioE elec"])
                    / twe_per_twh()
                ),
            ),
            ["RES elec"],
            {"RES elec": ["solid bioE elec"]},
        ),
        rearrange(
            zidz(
                float(potential_generation_res_elec_twh().loc["oceanic"]),
                (float(power_density_res_elec_twemha().loc["oceanic"]) / twe_per_twh()),
            ),
            ["RES elec"],
            {"RES elec": ["oceanic"]},
        ),
        rearrange(
            zidz(
                float(potential_generation_res_elec_twh().loc["wind onshore"]),
                (
                    float(power_density_res_elec_twemha().loc["wind onshore"])
                    / twe_per_twh()
                ),
            ),
            ["RES elec"],
            {"RES elec": ["wind onshore"]},
        ),
        rearrange(
            zidz(
                float(potential_generation_res_elec_twh().loc["wind offshore"]),
                (
                    float(power_density_res_elec_twemha().loc["wind offshore"])
                    / twe_per_twh()
                ),
            ),
            ["RES elec"],
            {"RES elec": ["wind offshore"]},
        ),
        rearrange(
            zidz(
                float(potential_generation_res_elec_twh().loc["solar PV"])
                * (1 - real_share_pv_urban_vs_total_pv()),
                (
                    float(power_density_res_elec_twemha().loc["solar PV"])
                    / twe_per_twh()
                ),
            ),
            ["RES elec"],
            {"RES elec": ["solar PV"]},
        ),
        rearrange(
            zidz(
                float(potential_generation_res_elec_twh().loc["CSP"]),
                (float(power_density_res_elec_twemha().loc["CSP"]) / twe_per_twh()),
            ),
            ["RES elec"],
            {"RES elec": ["CSP"]},
        ),
    )


def surface_solar_pv_on_land_mha():
    """
    Real Name: surface solar PV on land Mha
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
    Original Eqn: Land requirements RES elec compet uses+Land compet required dedicated crops for biofuels+Land required biofuels land marg+surface onshore wind Mha
    Units: MHa
    Limits: (None, None)
    Type: component
    Subs: None

    Land required for RES power plants and total bioenergy (land competition +
        marginal lands).
    """
    return (
        land_requirements_res_elec_compet_uses()
        + land_compet_required_dedicated_crops_for_biofuels()
        + land_required_biofuels_land_marg()
        + surface_onshore_wind_mha()
    )


def urban_surface_2015():
    """
    Real Name: urban surface 2015
    Original Eqn: GET DIRECT CONSTANTS('../land.xlsx', 'Europe', 'urban_surface_2015')
    Units: MHa
    Limits: (None, None)
    Type: constant
    Subs: None

    Area currently occupied by human settlement and infraestructures.
    """
    return _ext_constant_urban_surface_2015()


_ext_constant_agricultural_land_2015 = ExtConstant(
    "../land.xlsx",
    "Europe",
    "agricultural_land_2015",
    {},
    _root,
    "_ext_constant_agricultural_land_2015",
)


_ext_constant_urban_surface_2015 = ExtConstant(
    "../land.xlsx",
    "Europe",
    "urban_surface_2015",
    {},
    _root,
    "_ext_constant_urban_surface_2015",
)
