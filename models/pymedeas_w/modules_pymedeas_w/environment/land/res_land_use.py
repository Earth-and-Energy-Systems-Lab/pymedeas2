"""
Module environment.land.res_land_use
Translated using PySD version 3.14.0
"""

@component.add(
    name="Global_arable_land",
    units="MHa",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_global_arable_land"},
)
def global_arable_land():
    """
    Current global arable land: 1526 MHa (FAOSTAT).
    """
    return _ext_constant_global_arable_land()


_ext_constant_global_arable_land = ExtConstant(
    "../parameters.xlsx",
    "World",
    "global_arable_land",
    {},
    _root,
    {},
    "_ext_constant_global_arable_land",
)


@component.add(
    name='"power_density_RES_elec_TWe/Mha"',
    units="TWe/MHa",
    subscripts=[np.str_("RES_elec")],
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_power_density_res_elec_twemha"},
)
def power_density_res_elec_twemha():
    """
    Input parameter: power density per RES technology for delivering electricity.
    """
    return _ext_constant_power_density_res_elec_twemha()


_ext_constant_power_density_res_elec_twemha = ExtConstant(
    "../energy.xlsx",
    "Global",
    "power_density_res_elec*",
    {"RES_elec": _subscript_dict["RES_elec"]},
    _root,
    {"RES_elec": _subscript_dict["RES_elec"]},
    "_ext_constant_power_density_res_elec_twemha",
)


@component.add(
    name='"power_density_RES_elec_TW/Mha"',
    units="TW/MHa",
    subscripts=[np.str_("RES_elec")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"power_density_res_elec_twemha": 1, "cpini_res_elec": 1},
)
def power_density_res_elec_twmha():
    return power_density_res_elec_twemha() / cpini_res_elec()


@component.add(
    name="Share_land_compet_biofuels",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "land_compet_required_dedicated_crops_for_biofuels": 1,
        "global_arable_land": 1,
    },
)
def share_land_compet_biofuels():
    """
    Share of global arable land required by dedicated crops for biofuels (in land competition).
    """
    return land_compet_required_dedicated_crops_for_biofuels() / global_arable_land()


@component.add(
    name="share_land_RES_land_compet_vs_arable",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "land_compet_required_dedicated_crops_for_biofuels": 1,
        "surface_solar_pv_mha": 1,
        "global_arable_land": 1,
    },
)
def share_land_res_land_compet_vs_arable():
    """
    Land requirements for RES that compete with other land-uses (solar on land and biofuels on land competition) as a share of the global arable land.
    """
    return (
        land_compet_required_dedicated_crops_for_biofuels() + surface_solar_pv_mha()
    ) / global_arable_land()


@component.add(
    name="share_land_total_RES_vs_arable",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_land_requirements_renew_mha": 1, "global_arable_land": 1},
)
def share_land_total_res_vs_arable():
    """
    Land requirements for all RES as a share of the global arable land.
    """
    return total_land_requirements_renew_mha() / global_arable_land()


@component.add(
    name="share_land_total_RES_vs_urban_surface",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_land_requirements_renew_mha": 1, "urban_surface_2008": 1},
)
def share_land_total_res_vs_urban_surface():
    """
    Land requirements for all RES as a share of the global urban land.
    """
    return total_land_requirements_renew_mha() / urban_surface_2008()


@component.add(
    name="surface_CSP_Mha",
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
    name="surface_hydro_Mha",
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
    name="surface_onshore_wind_Mha",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"surface_res_elec": 1},
)
def surface_onshore_wind_mha():
    """
    Surface required to produce "onshore wind TWe".
    """
    return float(surface_res_elec().loc["wind_onshore"])


@component.add(
    name="surface_RES_elec",
    units="MHa",
    subscripts=[np.str_("RES_elec")],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"power_density_res_elec_twmha": 2, "res_installed_capacity_delayed": 1},
)
def surface_res_elec():
    return if_then_else(
        power_density_res_elec_twmha() == 0,
        lambda: xr.DataArray(
            0, {"RES_elec": _subscript_dict["RES_elec"]}, ["RES_elec"]
        ),
        lambda: res_installed_capacity_delayed() / power_density_res_elec_twmha(),
    )


@component.add(
    name="surface_solar_PV_Mha",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"surface_res_elec": 1},
)
def surface_solar_pv_mha():
    """
    Area required for solar PV plants on land.
    """
    return float(surface_res_elec().loc["solar_PV"])


@component.add(
    name="Total_land_requirements_renew_Mha",
    units="MHa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "surface_solar_pv_mha": 1,
        "surface_csp_mha": 1,
        "surface_hydro_mha": 1,
        "land_compet_required_dedicated_crops_for_biofuels": 1,
        "land_required_biofuels_land_marg": 1,
        "nvs_1_year": 1,
        "surface_onshore_wind_mha": 1,
    },
)
def total_land_requirements_renew_mha():
    """
    Land required for RES power plants and total bioenergy (land competition + marginal lands).
    """
    return (
        surface_solar_pv_mha()
        + surface_csp_mha()
        + surface_hydro_mha()
        + land_compet_required_dedicated_crops_for_biofuels()
        + land_required_biofuels_land_marg() * nvs_1_year()
        + surface_onshore_wind_mha() * 0
    )


@component.add(
    name="urban_surface_2008",
    units="MHa",
    comp_type="Constant",
    comp_subtype="External",
    depends_on={"__external__": "_ext_constant_urban_surface_2008"},
)
def urban_surface_2008():
    """
    Area occupied by human settlement and infraestructures. This area is roughly 200-400MHa (Wackernagel et al., 2002; WWF, 2008; Young, 1999).
    """
    return _ext_constant_urban_surface_2008()


_ext_constant_urban_surface_2008 = ExtConstant(
    "../parameters.xlsx",
    "World",
    "urban_surface_2008",
    {},
    _root,
    {},
    "_ext_constant_urban_surface_2008",
)
