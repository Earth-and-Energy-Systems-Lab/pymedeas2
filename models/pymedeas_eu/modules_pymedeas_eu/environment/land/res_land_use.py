"""
Module res_land_use
Translated using PySD version 3.0.1
"""


@component.add(
    name="Agricultural land 2015",
    units="MHa",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_agricultural_land_2015"},
)
def agricultural_land_2015():
    return _ext_constant_agricultural_land_2015()


_ext_constant_agricultural_land_2015 = ExtConstant(
    "../land.xlsx",
    "Europe",
    "agricultural_land_2015",
    {},
    _root,
    {},
    "_ext_constant_agricultural_land_2015",
)


@component.add(
    name="Land requirements RES elec compet uses",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "surface_hydro_mha": 1,
        "surface_csp_mha": 1,
        "surface_solar_pv_on_land_mha": 1,
    },
)
def land_requirements_res_elec_compet_uses():
    """
    Land requirements for renewable technologies to generate electricity (PV on land, CSP and hydro) requiring land and not easily compatible with double uses.
    """
    return surface_hydro_mha() + surface_csp_mha() + surface_solar_pv_on_land_mha()


@component.add(
    name="Land saved by urban PV",
    units="MHa*Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_generation_res_elec_twh": 1,
        "real_share_pv_urban_vs_total_pv": 1,
        "power_density_res_elec_twemha": 1,
        "twe_per_twh": 1,
    },
)
def land_saved_by_urban_pv():
    """
    Land saved by urban PV.
    """
    return zidz(
        float(potential_generation_res_elec_twh().loc["solar PV"])
        * real_share_pv_urban_vs_total_pv(),
        float(power_density_res_elec_twemha().loc["solar PV"]) / twe_per_twh(),
    )


@component.add(
    name="Share land compet biofuels",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "land_compet_required_dedicated_crops_for_biofuels": 1,
        "agricultural_land_2015": 1,
    },
)
def share_land_compet_biofuels():
    """
    Share of global arable land required by dedicated crops for biofuels (in land competition).
    """
    return (
        land_compet_required_dedicated_crops_for_biofuels() / agricultural_land_2015()
    )


@component.add(
    name="share land RES land compet vs arable",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "land_compet_required_dedicated_crops_for_biofuels": 1,
        "surface_solar_pv_on_land_mha": 1,
        "surface_csp_mha": 1,
        "surface_hydro_mha": 1,
        "agricultural_land_2015": 1,
    },
)
def share_land_res_land_compet_vs_arable():
    """
    Land requirements for RES that compete with other land-uses (solar on land and biofuels on land competition) as a share of the global arable land.
    """
    return (
        land_compet_required_dedicated_crops_for_biofuels()
        + surface_solar_pv_on_land_mha()
        + surface_csp_mha()
        + surface_hydro_mha()
    ) / agricultural_land_2015()


@component.add(
    name="share land total RES vs arable",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_land_requirements_renew_mha": 1, "agricultural_land_2015": 1},
)
def share_land_total_res_vs_arable():
    """
    Land requirements for all RES as a share of the global arable land.
    """
    return total_land_requirements_renew_mha() / agricultural_land_2015()


@component.add(
    name="share land total RES vs urban surface",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_land_requirements_renew_mha": 1, "urban_surface_2015": 1},
)
def share_land_total_res_vs_urban_surface():
    """
    Land requirements for all RES as a share of the global urban land.
    """
    return total_land_requirements_renew_mha() / urban_surface_2015()


@component.add(
    name="surface CSP Mha",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"surface_res_elec": 1},
)
def surface_csp_mha():
    """
    Area required for CSP.
    """
    return float(surface_res_elec().loc["CSP"])


@component.add(
    name="surface hydro Mha",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"surface_res_elec": 1},
)
def surface_hydro_mha():
    """
    Surface required by hydropower plants.
    """
    return float(surface_res_elec().loc["hydro"])


@component.add(
    name="surface onshore wind Mha",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"surface_res_elec": 1},
)
def surface_onshore_wind_mha():
    """
    Surface required to produce "onshore wind TWe".
    """
    return float(surface_res_elec().loc["wind onshore"])


@component.add(
    name="surface RES elec",
    units="MHa",
    subscripts=["RES elec"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_generation_res_elec_twh": 8,
        "power_density_res_elec_twemha": 8,
        "twe_per_twh": 8,
        "real_share_pv_urban_vs_total_pv": 1,
    },
)
def surface_res_elec():
    """
    Land requirements by renewable technologies for electricity generation.
    """
    value = xr.DataArray(
        np.nan, {"RES elec": _subscript_dict["RES elec"]}, ["RES elec"]
    )
    value.loc[["hydro"]] = zidz(
        float(potential_generation_res_elec_twh().loc["hydro"]),
        float(power_density_res_elec_twemha().loc["hydro"]) / twe_per_twh(),
    )
    value.loc[["geot elec"]] = zidz(
        float(potential_generation_res_elec_twh().loc["geot elec"]),
        float(power_density_res_elec_twemha().loc["geot elec"]) / twe_per_twh(),
    )
    value.loc[["solid bioE elec"]] = zidz(
        float(potential_generation_res_elec_twh().loc["solid bioE elec"]),
        float(power_density_res_elec_twemha().loc["solid bioE elec"]) / twe_per_twh(),
    )
    value.loc[["oceanic"]] = zidz(
        float(potential_generation_res_elec_twh().loc["oceanic"]),
        float(power_density_res_elec_twemha().loc["oceanic"]) / twe_per_twh(),
    )
    value.loc[["wind onshore"]] = zidz(
        float(potential_generation_res_elec_twh().loc["wind onshore"]),
        float(power_density_res_elec_twemha().loc["wind onshore"]) / twe_per_twh(),
    )
    value.loc[["wind offshore"]] = zidz(
        float(potential_generation_res_elec_twh().loc["wind offshore"]),
        float(power_density_res_elec_twemha().loc["wind offshore"]) / twe_per_twh(),
    )
    value.loc[["solar PV"]] = zidz(
        float(potential_generation_res_elec_twh().loc["solar PV"])
        * (1 - real_share_pv_urban_vs_total_pv()),
        float(power_density_res_elec_twemha().loc["solar PV"]) / twe_per_twh(),
    )
    value.loc[["CSP"]] = zidz(
        float(potential_generation_res_elec_twh().loc["CSP"]),
        float(power_density_res_elec_twemha().loc["CSP"]) / twe_per_twh(),
    )
    return value


@component.add(
    name="surface solar PV on land Mha",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"surface_res_elec": 1},
)
def surface_solar_pv_on_land_mha():
    """
    Area required for solar PV plants on land.
    """
    return float(surface_res_elec().loc["solar PV"])


@component.add(
    name="Total land requirements renew Mha",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "land_requirements_res_elec_compet_uses": 1,
        "land_compet_required_dedicated_crops_for_biofuels": 1,
        "land_required_biofuels_land_marg": 1,
        "surface_onshore_wind_mha": 1,
    },
)
def total_land_requirements_renew_mha():
    """
    Land required for RES power plants and total bioenergy (land competition + marginal lands).
    """
    return (
        land_requirements_res_elec_compet_uses()
        + land_compet_required_dedicated_crops_for_biofuels()
        + land_required_biofuels_land_marg()
        + surface_onshore_wind_mha()
    )


@component.add(
    name="urban surface 2015",
    units="MHa",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_urban_surface_2015"},
)
def urban_surface_2015():
    """
    Area currently occupied by human settlement and infraestructures.
    """
    return _ext_constant_urban_surface_2015()


_ext_constant_urban_surface_2015 = ExtConstant(
    "../land.xlsx",
    "Europe",
    "urban_surface_2015",
    {},
    _root,
    {},
    "_ext_constant_urban_surface_2015",
)
